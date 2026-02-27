"""API routes for IFC validation."""

import logging
import os
import re
import tempfile
from datetime import datetime
from io import BytesIO

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse

from app.schemas.validation import ValidationReport, ValidationResponse
from app.services.ifc_parser import IFCParserService
from app.services.pdf_generator import PDFGeneratorService
from app.services.validator import ValidatorService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["validation"])

# Security constants
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB (supports large building models)
CHUNK_SIZE = 1024 * 1024  # 1 MB chunks for streaming
IFC_MAGIC_BYTES = [b"ISO-10303-21", b"ISO-10303-21;"]


async def read_file_with_limit(file: UploadFile, max_size: int) -> bytes:
    """Read uploaded file in chunks with cumulative size check.

    Prevents memory exhaustion by checking size during streaming
    rather than after buffering the entire file.

    Args:
        file: The uploaded file.
        max_size: Maximum allowed file size in bytes.

    Returns:
        File content as bytes.

    Raises:
        HTTPException: If file exceeds size limit.
    """
    chunks = []
    total_size = 0

    while True:
        chunk = await file.read(CHUNK_SIZE)
        if not chunk:
            break
        total_size += len(chunk)
        if total_size > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {max_size // (1024 * 1024)} MB",
            )
        chunks.append(chunk)

    return b"".join(chunks)


def validate_ifc_content(content: bytes) -> bool:
    """Validate that file content is a valid IFC file.

    Checks for IFC magic bytes (ISO-10303-21 header).

    Args:
        content: File content as bytes.

    Returns:
        True if content appears to be valid IFC.
    """
    # Check first 1KB for IFC header
    header = content[:1024]
    return any(sig in header for sig in IFC_MAGIC_BYTES)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe usage.

    Args:
        filename: Original filename.

    Returns:
        Sanitized filename with only safe characters.
    """
    # Remove path components and keep only basename
    name = os.path.basename(filename)
    # Replace unsafe characters
    name = re.sub(r"[^\w\-_.]", "_", name)
    # Limit length
    if len(name) > 100:
        name = name[:100]
    return name


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint.

    Returns:
        Status and timestamp.
    """
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@router.post("/validate", response_model=ValidationResponse)
async def validate_ifc(
    file: UploadFile = File(...),
    language: str = Query(default="fi", pattern="^(fi|en)$"),
) -> ValidationResponse:
    """Validate an IFC file against Finnish building permit requirements.

    Args:
        file: The uploaded IFC file.
        language: Language code for error messages ('fi' or 'en').

    Returns:
        Validation response with report or error.

    Raises:
        HTTPException: If file is not an IFC file or exceeds size limit.
    """
    # Validate file extension
    if not file.filename or not file.filename.lower().endswith(".ifc"):
        raise HTTPException(status_code=400, detail="File must be an IFC file (.ifc)")

    # Validate file size header first if possible
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // 1024 // 1024} MB"
        )

    tmp_path: str | None = None
    try:
        # Read file content with streaming size check (prevents memory exhaustion)
        content = await read_file_with_limit(file, MAX_FILE_SIZE)

        # Validate file content (magic bytes)
        if not validate_ifc_content(content):
            raise HTTPException(
                status_code=400,
                detail="File does not appear to be a valid IFC file",
            )

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ifc") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        # Parse IFC file
        parser = IFCParserService()
        parser.open_file(tmp_path)

        # Run validation with specified language
        validator = ValidatorService(language=language)
        safe_filename = sanitize_filename(file.filename)
        report = validator.validate(parser, safe_filename)

        return ValidationResponse(success=True, report=report)

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise

    except ValueError as e:
        # Known validation errors - safe to show
        logger.warning(f"Validation error for file '{file.filename}': {str(e)}")
        return ValidationResponse(success=False, error=str(e))

    except Exception as e:
        # Unexpected errors - log full traceback for debugging
        import traceback
        error_traceback = traceback.format_exc()
        logger.error(f"Unexpected error processing file '{file.filename}':\n{error_traceback}")
        
        # Only expose error details in development mode
        if os.getenv("ENVIRONMENT") == "development":
            error_msg = f"{type(e).__name__}: {str(e)}"
            return ValidationResponse(
                success=False, error=f"Processing error: {error_msg}"
            )
        else:
            # Production: hide internal error details
            return ValidationResponse(
                success=False, error="An error occurred while processing the file. Please try again."
            )

    finally:
        # Clean up temp file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError as e:
                logger.warning(f"Failed to delete temp file {tmp_path}: {e}")


@router.post("/export/pdf")
async def export_pdf_report(
    report: ValidationReport,
    language: str = Query(default="fi", pattern="^(fi|en)$"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> StreamingResponse:
    """Generate PDF report from validation results.

    Args:
        report: Validation report to convert to PDF.
        language: Language code ('fi' or 'en').
        background_tasks: FastAPI background tasks for cleanup.

    Returns:
        PDF file as streaming response.
    """
    pdf_stream = None
    try:
        generator = PDFGeneratorService(language=language)
        pdf_bytes = generator.generate(report)
        pdf_stream = BytesIO(pdf_bytes)

        # Sanitize filename and encode for Content-Disposition (RFC 5987)
        from urllib.parse import quote
        import pathlib
        
        safe_filename = sanitize_filename(report.filename)
        # Use pathlib for safer extension replacement
        base_name = pathlib.Path(safe_filename).stem
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"ifc_report_{base_name}_{timestamp}.pdf"
        encoded_filename = quote(filename)

        # Schedule buffer cleanup after response is sent
        background_tasks.add_task(pdf_stream.close)

        return StreamingResponse(
            pdf_stream,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"},
        )

    except Exception as e:
        # Clean up buffer on error
        if pdf_stream is not None:
            pdf_stream.close()
        logger.error(f"PDF generation error: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to generate PDF report"
        )
