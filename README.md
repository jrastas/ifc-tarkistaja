# IFC Compliance Checker

A web application that validates IFC 4.3.2.0 files against Finnish building permit requirements (Ympäristöministeriön asetus 1340/2025).

## Features

- **IFC File Validation**: Upload and validate IFC files against Finnish building permit requirements (Liite 1 & Liite 2)
- **Compliance Dashboard**: Visual gauges showing overall and required field compliance percentages
- **Detailed Results**: Expandable categories with field-level validation status (valid / missing / invalid)
- **PDF Export**: Generate downloadable PDF compliance reports
- **Bilingual UI**: Finnish (default) and English interfaces with localized validation messages
- **Ryhti Alignment**: Field mappings aligned with Finland's national Ryhti (raklu v1.1.0) data model

## Warning

This is a very badly programmed software and AI was used to assist in it. Please run at your own risk and not in production. This software is intended for educational purposes only. Please contact the maintainer if there are any issues.

## Quick Start

### Docker (Recommended)

```bash
git clone <repository-url>
cd vibeifc

docker-compose up --build

# Frontend: http://localhost
# Backend API: http://localhost:8000
```

### Manual Setup

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
# Access at http://localhost:5173
```

## Usage

### 1. Upload an IFC file

Drag and drop an IFC file onto the upload area, or click to select one. Supported format: IFC 4.3.x (`.ifc`). Maximum file size: 500 MB.

### 2. View validation results

After upload the application validates automatically and shows:

- **Compliance gauges** — overall compliance and required fields compliance
- **Issues summary** — errors (missing required fields) and warnings (missing optional fields)
- **Category breakdown** — expandable sections per requirement category

### 3. Toggle view mode

Use the toggle to switch between **Pakolliset / Required** (required fields only) and **Kaikki / All** (all fields).

### 4. Change language

Click the language selector in the header to switch between Finnish and English. The page re-validates with messages in the selected language.

### 5. Export PDF report

Click **Vie PDF / Export PDF** to download a compliance report with file info, compliance percentages, and a full category breakdown.

## API

### Health check

```
GET /api/health
```

### Validate IFC file

```
POST /api/validate?language=fi
Content-Type: multipart/form-data

file: <IFC file>
```

`language` accepts `fi` (default) or `en`.

### Export PDF

```
POST /api/export/pdf?language=fi
Content-Type: application/json

<ValidationReport JSON>
```

Returns `application/pdf`.

## Project Structure

```
vibeifc/
├── backend/
│   ├── app/
│   │   ├── api/routes.py          # API endpoints
│   │   ├── services/
│   │   │   ├── ifc_parser.py      # IFC file parsing (ifcopenshell)
│   │   │   ├── validator.py       # Validation logic
│   │   │   └── pdf_generator.py   # PDF report generation
│   │   ├── schemas/validation.py  # Pydantic models
│   │   ├── mappings/              # YAML requirement mappings
│   │   │   ├── liite1.yaml        # Liite 1 requirements (16 categories)
│   │   │   └── liite2.yaml        # Liite 2 requirements (12 categories)
│   │   └── i18n/                  # fi.json, en.json
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── controls/          # LanguageToggle, ExportButton, ViewModeToggle
│   │   │   ├── layout/            # Header, Footer
│   │   │   ├── results/           # SummaryDashboard, CategoryAccordion, IssuesSummary
│   │   │   └── upload/            # DropZone
│   │   ├── services/api.ts        # HTTP API client
│   │   ├── store/appStore.ts      # Zustand state
│   │   ├── i18n/                  # fi.json, en.json
│   │   └── types/validation.ts    # TypeScript interfaces
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docs/phases/
├── SECURITY.md
├── docker-compose.yml
└── Makefile
```

## Requirements Mapping

Validation is driven by YAML mappings aligned with the Ryhti data model:

- **Liite 1**: Building information model requirements (16 categories, 61 fields)
- **Liite 2**: Space and element requirements (12 categories)

Each field specifies the IFC property path (`ifc_entity`, `ifc_property`) and whether it is required or optional.

## Configuration

### Backend (`.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | `development` or `production` | `development` |
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:5173` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Frontend (`.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend URL | `http://localhost:8000` |

## Testing

**Backend:**
```bash
cd backend
pytest -v
pytest --cov=app --cov-report=html
```

**Frontend:**
```bash
cd frontend
npm test
npm run test:coverage
```

## Troubleshooting

**ifcopenshell won't install:**
```bash
conda install -c conda-forge ifcopenshell
# or
pip install ifcopenshell==0.8.1 --no-cache-dir
```

**CORS errors:** Ensure `CORS_ORIGINS` in the backend `.env` includes the frontend URL.

**Finnish characters display wrong:** Ensure all files use UTF-8 encoding.

**Large file upload timeout:** For files > 50 MB, increase nginx timeout settings in production.

## License

Copyright (c) 2024–2026 Jaakko Rastas and IFC Tarkistaja Contributors

Licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

This software incorporates components licensed under LGPL-3.0 (IfcOpenShell) and Apache-2.0 (TypeScript). See [licenses-used.md](licenses-used.md) for a full breakdown.

## Acknowledgments

- [IfcOpenShell](https://ifcopenshell.org/) — IFC parsing library
- [Ryhti](https://ryhti.syke.fi/) — Finland's Built Environment Information System
- [FastAPI](https://fastapi.tiangolo.com/) — Python web framework
- [React](https://react.dev/) — Frontend framework
