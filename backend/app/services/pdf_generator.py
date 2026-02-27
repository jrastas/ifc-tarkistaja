"""PDF report generation service."""

import json
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Dict

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.schemas.validation import ValidationReport, ValidationStatus


class PDFGeneratorService:
    """Service for generating PDF reports from validation results."""

    def __init__(self, language: str = "fi") -> None:
        """Initialize the PDF generator.

        Args:
            language: Language code ('fi' or 'en').
        """
        self.language = language if language in ["fi", "en"] else "fi"
        self.translations = self._load_translations()
        self.styles = self._create_styles()

    def _load_translations(self) -> Dict[str, Any]:
        """Load translation file.

        Returns:
            Dictionary of translations.
        """
        i18n_dir = Path(__file__).parent.parent / "i18n"
        lang_file = i18n_dir / f"{self.language}.json"

        with open(lang_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _t(self, key: str) -> str:
        """Get translation by dot-notation key.

        Args:
            key: Dot-notation key (e.g., 'report.title').

        Returns:
            Translated string or key if not found.
        """
        keys = key.split(".")
        value: Any = self.translations
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, key)
            else:
                return key
        return value if isinstance(value, str) else key

    def _create_styles(self) -> Dict[str, ParagraphStyle]:
        """Create PDF styles.

        Returns:
            Dictionary of paragraph styles.
        """
        styles = getSampleStyleSheet()

        styles.add(
            ParagraphStyle(
                name="ReportTitle",
                fontSize=24,
                leading=28,
                alignment=TA_CENTER,
                spaceAfter=6 * mm,
            )
        )

        styles.add(
            ParagraphStyle(
                name="ReportSubtitle",
                fontSize=12,
                leading=14,
                alignment=TA_CENTER,
                textColor=colors.gray,
                spaceAfter=12 * mm,
            )
        )

        styles.add(
            ParagraphStyle(
                name="SectionHeader",
                fontSize=14,
                leading=18,
                spaceBefore=8 * mm,
                spaceAfter=4 * mm,
                fontName="Helvetica-Bold",
            )
        )

        styles.add(
            ParagraphStyle(
                name="CategoryHeader",
                fontSize=12,
                leading=14,
                spaceBefore=4 * mm,
                spaceAfter=2 * mm,
                fontName="Helvetica-Bold",
            )
        )

        return styles

    def generate(self, report: ValidationReport) -> bytes:
        """Generate PDF report.

        Args:
            report: Validation report to convert to PDF.

        Returns:
            PDF byte content.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )

        elements = []

        # Title
        elements.append(
            Paragraph(self._t("report.title"), self.styles["ReportTitle"])
        )
        elements.append(
            Paragraph(self._t("report.subtitle"), self.styles["ReportSubtitle"])
        )

        # Metadata table
        timestamp = (
            report.timestamp
            if isinstance(report.timestamp, datetime)
            else datetime.fromisoformat(str(report.timestamp).replace("Z", "+00:00"))
        )
        meta_data = [
            [self._t("report.file"), report.filename],
            [self._t("report.schema"), report.ifc_schema],
            [self._t("report.generated"), timestamp.strftime("%Y-%m-%d %H:%M")],
        ]
        meta_table = Table(meta_data, colWidths=[50 * mm, 100 * mm])
        meta_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        elements.append(meta_table)
        elements.append(Spacer(1, 8 * mm))

        # Compliance summary
        elements.append(
            Paragraph(self._t("report.summary"), self.styles["SectionHeader"])
        )

        summary_data = [
            [
                self._t("report.overall_compliance"),
                f"{int(report.overall_compliance * 100)}%",
            ],
            [
                self._t("report.required_compliance"),
                f"{int(report.required_compliance * 100)}%",
            ],
        ]
        summary_table = Table(summary_data, colWidths=[100 * mm, 50 * mm])
        summary_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 12),
                    ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                    (
                        "TEXTCOLOR",
                        (1, 0),
                        (1, 0),
                        self._get_compliance_color(report.overall_compliance),
                    ),
                    (
                        "TEXTCOLOR",
                        (1, 1),
                        (1, 1),
                        self._get_compliance_color(report.required_compliance),
                    ),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        elements.append(summary_table)

        # Errors
        if report.errors:
            elements.append(
                Paragraph(
                    f"{self._t('report.errors')} ({len(report.errors)})",
                    self.styles["SectionHeader"],
                )
            )
            for error in report.errors[:15]:
                elements.append(
                    Paragraph(f"• {error}", self.styles["Normal"])
                )
            if len(report.errors) > 15:
                elements.append(
                    Paragraph(
                        f"... +{len(report.errors) - 15} more",
                        self.styles["Normal"],
                    )
                )

        # Warnings
        if report.warnings:
            elements.append(
                Paragraph(
                    f"{self._t('report.warnings')} ({len(report.warnings)})",
                    self.styles["SectionHeader"],
                )
            )
            for warning in report.warnings[:10]:
                elements.append(
                    Paragraph(f"• {warning}", self.styles["Normal"])
                )
            if len(report.warnings) > 10:
                elements.append(
                    Paragraph(
                        f"... +{len(report.warnings) - 10} more",
                        self.styles["Normal"],
                    )
                )

        # Detailed results
        elements.append(PageBreak())
        elements.append(
            Paragraph(self._t("report.details"), self.styles["SectionHeader"])
        )

        for category in report.categories:
            cat_name = (
                category.name if self.language == "fi" else category.name_en
            )
            elements.append(
                Paragraph(
                    f"{cat_name} ({category.compliance_percentage:.0f}%)",
                    self.styles["CategoryHeader"],
                )
            )

            # Build table data
            table_data = [
                [
                    self._t("report.field"),
                    self._t("report.status"),
                    self._t("report.value"),
                ]
            ]

            for field in category.fields:
                field_name = (
                    field.field_name
                    if self.language == "fi"
                    else field.field_name_en
                )
                status_text = self._t(f"status.{field.status.value}")
                value = str(field.value) if field.value is not None else "-"

                # Add required marker
                if field.is_required:
                    field_name += " *"

                # Truncate long values
                if len(value) > 40:
                    value = value[:37] + "..."

                table_data.append([field_name, status_text, value])

            field_table = Table(
                table_data, colWidths=[70 * mm, 30 * mm, 60 * mm]
            )

            table_style = [
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
            ]

            # Color code status column
            for i, field in enumerate(category.fields, start=1):
                color = self._get_status_color(field.status)
                table_style.append(("TEXTCOLOR", (1, i), (1, i), color))

            field_table.setStyle(TableStyle(table_style))
            elements.append(field_table)
            elements.append(Spacer(1, 4 * mm))

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()

    def _get_compliance_color(self, value: float) -> colors.Color:
        """Get color based on compliance percentage.

        Args:
            value: Compliance value between 0 and 1.

        Returns:
            Color object.
        """
        if value >= 0.9:
            return colors.HexColor("#10B981")  # Green
        elif value >= 0.7:
            return colors.HexColor("#F59E0B")  # Amber
        else:
            return colors.HexColor("#EF4444")  # Red

    def _get_status_color(self, status: ValidationStatus) -> colors.Color:
        """Get color based on validation status.

        Args:
            status: Validation status.

        Returns:
            Color object.
        """
        if status == ValidationStatus.VALID:
            return colors.HexColor("#10B981")
        elif status == ValidationStatus.MISSING:
            return colors.HexColor("#EF4444")
        else:
            return colors.HexColor("#F59E0B")
