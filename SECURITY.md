# Security Report

This document outlines security considerations, known issues, and recommendations for the IFC Compliance Checker application.

## Security Audit Summary

| Severity | Count | Status |
|----------|-------|--------|
| Critical | 0 | - |
| High | 2 | Fixed |
| Medium | 5 | Fixed (3), Accepted (2) |
| Low | 3 | Fixed (2), Accepted (1) |

**Last Updated:** 2026-02-27
**Audit Scope:** Backend (Python), Frontend (TypeScript/Nginx)

---

## High Severity Issues

### 1. Unbounded Upload Buffering in `/api/validate`

**Location:** `backend/app/api/routes.py`
**Status:** ✅ Fixed

The file is now read in 1 MB chunks with a cumulative size check via `read_file_with_limit()`. The size limit is also pre-checked against the `Content-Length` header before streaming begins. Memory exhaustion via large uploads is no longer possible.

---

### 2. CORS Configuration with Credentials

**Location:** `backend/app/main.py`
**Status:** ✅ Fixed

A startup-time guard now rejects wildcard origins when `allow_credentials=True` is set. In production mode this raises a `ValueError` and prevents the server from starting. Allowed methods and headers are also explicitly restricted instead of using wildcards.

---

## Medium Severity Issues

### 3. Unbounded PDF Export Input

**Location:** `backend/app/schemas/validation.py`
**Status:** ✅ Fixed

`ValidationReport.errors` and `ValidationReport.warnings` fields are constrained with `Field(max_length=2000)`. A `field_validator` truncates individual items that exceed length limits rather than raising a 500 error.

---

### 4. Permissive Content Security Policy

**Location:** `frontend/nginx.conf`
**Status:** ⚠️ Accepted — known limitation

The CSP retains `'unsafe-inline'` for styles (required by Tailwind CSS) and `'wasm-unsafe-eval'` (required by web-ifc for IFC geometry parsing). These are known trade-offs with the chosen libraries. The overall CSP is otherwise tightly scoped: `default-src 'self'`, no CDN sources, `frame-ancestors 'self'`, `base-uri 'self'`, and `form-action 'self'`.

---

### 5. Content-Disposition Header Injection

**Location:** `backend/app/api/routes.py`
**Status:** ✅ Fixed

Filenames are now encoded with `urllib.parse.quote` and the header uses RFC 5987 format (`filename*=UTF-8''...`). The file stem is extracted via `pathlib.Path.stem` rather than string replacement.

---

### 6. YAML Mapping Files Structure Validation

**Location:** `backend/app/services/validator.py`
**Status:** ✅ Fixed

Mapping files are validated at startup against Pydantic models (`MappingFile`, `MappingCategory`, `MappingField`). Malformed files cause an error log and fall back to an empty mapping rather than propagating a runtime crash.

---

### 7. Exception Details Exposed in Error Responses

**Location:** `backend/app/api/routes.py`, `backend/app/main.py`
**Status:** ✅ Fixed

Internal exception details are only included in error responses when `ENVIRONMENT=development`. In all other environments a generic message is returned. A global exception handler in `main.py` covers unhandled exceptions as well.

---

## Low Severity Issues

### 8. Temporary File Cleanup

**Location:** `backend/app/api/routes.py`
**Status:** ⚠️ Accepted — low risk

Temporary files are cleaned up in a `finally` block which is reliable in practice. The recommended refactor to a `NamedTemporaryFile(delete=True)` context manager would be marginally more robust but is not a security concern under normal conditions.

---

### 9. DOM Manipulation Cleanup in PDF Export

**Location:** `frontend/src/components/controls/ExportButton.tsx`
**Status:** ✅ Fixed

The temporary anchor element and object URL are cleaned up inside a `try/finally` block, ensuring `revokeObjectURL` is always called even if the click fails.

---

### 10. React Key Props Using Array Index

**Location:** `frontend/src/components/results/IssuesSummary.tsx`
**Status:** ⚠️ Accepted — no real-world impact

Error and warning lists use array index as React key. These lists are read-only and never reordered, so this causes no correctness or security issue in practice.

---

## Security Best Practices Implemented

| Practice | Implementation |
|----------|----------------|
| Chunked upload streaming | 1 MB chunks with cumulative size limit |
| File type validation | `.ifc` extension check + ISO-10303-21 magic bytes |
| Filename sanitization | Regex-based sanitization + `pathlib` for extension handling |
| RFC 5987 Content-Disposition | `urllib.parse.quote` encoding |
| Safe YAML loading | `yaml.safe_load()` + Pydantic schema validation |
| CORS wildcard guard | Startup-time check, hard failure in production |
| Error message sanitization | Internal details hidden outside development mode |
| Rate limiting | Nginx zones: 10 req/s general API, 2 req/s uploads |
| Security headers | X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP, COEP |
| Non-root container | Frontend runs as unprivileged `appuser` in Docker |
| Input validation | Pydantic models for all request/response types |

---

## Dependency Security

### Python Dependencies

```bash
cd backend
pip install pip-audit
pip-audit
```

### JavaScript Dependencies

```bash
cd frontend
npm audit
```

As of 2026-02-27, `npm audit` reports 0 vulnerabilities.

---

## Production Deployment Checklist

- [ ] Set `CORS_ORIGINS` to specific production domains only
- [ ] Set `ENVIRONMENT=production` in backend environment
- [ ] Enable HTTPS with valid certificates
- [ ] Configure rate limiting appropriate for expected traffic
- [ ] Set up log aggregation (avoid logging sensitive data)
- [ ] Regular dependency updates (`pip-audit`, `npm audit`)

---

## Reporting Security Issues

If you discover a security vulnerability, please:

1. **Do not** open a public issue
2. Email the maintainers directly
3. Provide detailed steps to reproduce
4. Allow reasonable time for a fix before disclosure

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [RFC 5987 — Content-Disposition encoding](https://datatracker.ietf.org/doc/html/rfc5987)
