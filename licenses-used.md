# Open Source Licenses

This document lists all open source dependencies used in IFC Tarkistaja and their respective licenses for legal review.

## Summary

| License Type | Count | Notes |
|--------------|-------|-------|
| MIT | 17+ | Most permissive, no issues |
| Apache 2.0 | 2 | Permissive, attribution required |
| BSD | 3 | Permissive variants |
| ISC | 1 | Functionally equivalent to MIT |
| LGPL | 1 | Dynamic linking OK |

## Frontend Dependencies

### Core Framework

| Package | Version | License | URL |
|---------|---------|---------|-----|
| React | 18.3.1 | MIT | https://github.com/facebook/react |
| React DOM | 18.3.1 | MIT | https://github.com/facebook/react |
| TypeScript | 5.9.3 | Apache-2.0 | https://github.com/microsoft/TypeScript |
| Vite | 7.2.4 | MIT | https://github.com/vitejs/vite |

### UI & Styling

| Package | Version | License | URL |
|---------|---------|---------|-----|
| Tailwind CSS | 4.1.18 | MIT | https://github.com/tailwindlabs/tailwindcss |
| Lucide React | 0.562.0 | ISC | https://github.com/lucide-icons/lucide |

### State Management & Data

| Package | Version | License | URL |
|---------|---------|---------|-----|
| Zustand | 5.0.9 | MIT | https://github.com/pmndrs/zustand |
| Axios | 1.13.5 | MIT | https://github.com/axios/axios |
| i18next | 25.7.3 | MIT | https://github.com/i18next/i18next |
| react-i18next | 16.5.0 | MIT | https://github.com/i18next/react-i18next |

### File Handling

| Package | Version | License | URL |
|---------|---------|---------|-----|
| react-dropzone | 14.3.8 | MIT | https://github.com/react-dropzone/react-dropzone |

### Development Dependencies

| Package | Version | License | URL |
|---------|---------|---------|-----|
| ESLint | 9.39.1 | MIT | https://github.com/eslint/eslint |
| Vitest | 4.0.16 | MIT | https://github.com/vitest-dev/vitest |
| @testing-library/react | 16.3.1 | MIT | https://github.com/testing-library/react-testing-library |
| @vitejs/plugin-react | 5.1.1 | MIT | https://github.com/vitejs/vite-plugin-react |
| jsdom | 27.3.0 | MIT | https://github.com/jsdom/jsdom |

## Backend Dependencies (Python)

| Package | Version | License | URL |
|---------|---------|---------|-----|
| FastAPI | 0.133.1 | MIT | https://github.com/tiangolo/fastapi |
| Uvicorn | 0.41.0 | BSD-3-Clause | https://github.com/encode/uvicorn |
| Pydantic | 2.12.5 | MIT | https://github.com/pydantic/pydantic |
| IfcOpenShell | 0.8.4 | LGPL-3.0 | https://github.com/IfcOpenShell/IfcOpenShell |
| python-multipart | 0.0.22 | Apache-2.0 | https://github.com/Kludex/python-multipart |
| python-dotenv | 1.0.0 | BSD-3-Clause | https://github.com/theskumar/python-dotenv |
| PyYAML | 6.0.1 | MIT | https://github.com/yaml/pyyaml |
| ReportLab | 4.4.10 | BSD | https://www.reportlab.com/ |

---

## License Details

### MIT License

The most common license in this project. Allows:
- Commercial use
- Modification
- Distribution
- Private use

Requirements:
- Include copyright notice and license text

---

### Apache License 2.0

Used by TypeScript and python-multipart.

Allows:
- Commercial use
- Modification
- Distribution
- Patent use
- Private use

Requirements:
- Include copyright notice
- Include license text
- State changes made
- Include NOTICE file if present

Key clause: Provides explicit patent grant.

---

### Mozilla Public License 2.0 (MPL-2.0)

Not currently used as a direct dependency.

---

### GNU Lesser General Public License 3.0 (LGPL-3.0)

Used by **IfcOpenShell**.

Allows:
- Commercial use
- Modification
- Distribution
- Private use

Requirements:
- Disclose source of LGPL code if modified
- Include copyright notice
- Include license text
- Allow users to replace LGPL library

**Important for distribution**:
- Dynamic linking is permitted without sharing your code
- Users must be able to replace the IfcOpenShell library

Compliance options:
1. Provide written offer for source code
2. Use dynamic linking (recommended)
3. Document how users can replace the library

---

### BSD Licenses

Used by Uvicorn (BSD-3-Clause), python-dotenv (BSD-3-Clause), ReportLab (BSD).

Very permissive, similar to MIT.

Requirements:
- Include copyright notice
- BSD-3-Clause: Don't use author names for endorsement

---

### ISC License

Used by Lucide React.

Functionally equivalent to MIT. Very permissive.

---

## Attribution Requirements

The project is licensed under the MIT License. See the [LICENSE](LICENSE) file for the full license text and third-party attributions.

---

## Generating Full License Report

### For npm packages:

```bash
cd frontend
npx license-checker --json > licenses.json
npx license-checker --summary
```

### For Python packages:

```bash
cd backend
pip install pip-licenses
pip-licenses --format=markdown > licenses.md
```

---

## Legal Considerations

### License Compatibility

All dependencies use permissive licenses (MIT, Apache-2.0, BSD, ISC) except:

- **LGPL-3.0 (IfcOpenShell)**: Requires ability to replace the library. Satisfied by using it as a standard pip package.

### Recommendations

1. **Keep license files updated** when adding dependencies
2. **Review new dependencies** before adding
3. **Avoid GPL-licensed** packages
4. **Document LGPL compliance** for IfcOpenShell

---

## Contact

For licensing questions, contact the project maintainer:

**Jaakko Rastas** - Project Maintainer

Last updated: February 2026
