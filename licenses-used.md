# Open Source Licenses

This document lists all open source dependencies used in IFC Tarkistaja and their respective licenses for legal review.

## Summary

| License Type | Count | Notes |
|--------------|-------|-------|
| MIT | 25+ | Most permissive, no issues |
| Apache 2.0 | 5+ | Permissive, attribution required |
| BSD | 3+ | Permissive variants |
| MPL 2.0 | 2 | File-level copyleft |
| LGPL | 1 | Dynamic linking OK |

## Frontend Dependencies

### Core Framework

| Package | Version | License | URL |
|---------|---------|---------|-----|
| React | 19.2.0 | MIT | https://github.com/facebook/react |
| React DOM | 19.2.0 | MIT | https://github.com/facebook/react |
| TypeScript | 5.9.3 | Apache-2.0 | https://github.com/microsoft/TypeScript |
| Vite | 7.2.4 | MIT | https://github.com/vitejs/vite |

### UI & Styling

| Package | Version | License | URL |
|---------|---------|---------|-----|
| Tailwind CSS | 4.1.18 | MIT | https://github.com/tailwindlabs/tailwindcss |
| Lucide React | 0.562.0 | ISC | https://github.com/lucide-icons/lucide |
| react-resizable-panels | 4.0.15 | MIT | https://github.com/bvaughn/react-resizable-panels |

### State Management & Data

| Package | Version | License | URL |
|---------|---------|---------|-----|
| Zustand | 5.0.9 | MIT | https://github.com/pmndrs/zustand |
| Axios | 1.13.2 | MIT | https://github.com/axios/axios |
| i18next | 25.7.3 | MIT | https://github.com/i18next/i18next |
| react-i18next | 16.5.0 | MIT | https://github.com/i18next/react-i18next |

### File Handling

| Package | Version | License | URL |
|---------|---------|---------|-----|
| react-dropzone | 14.3.8 | MIT | https://github.com/react-dropzone/react-dropzone |

### 3D Visualization

| Package | Version | License | URL |
|---------|---------|---------|-----|
| Three.js | 0.182.0 | MIT | https://github.com/mrdoob/three.js |
| @types/three | 0.182.0 | MIT | https://github.com/DefinitelyTyped/DefinitelyTyped |
| web-ifc | 0.0.74 | MPL-2.0 | https://github.com/IFCjs/web-ifc |
| @thatopen/components | 3.2.6 | MIT | https://github.com/ThatOpen/engine_components |
| @thatopen/fragments | 3.2.13 | MIT | https://github.com/ThatOpen/engine_fragment |

### Tauri (Native App)

| Package | Version | License | URL |
|---------|---------|---------|-----|
| @tauri-apps/api | 2.9.1 | MIT/Apache-2.0 | https://github.com/tauri-apps/tauri |
| @tauri-apps/cli | 2.9.6 | MIT/Apache-2.0 | https://github.com/tauri-apps/tauri |
| @tauri-apps/plugin-dialog | 2.4.2 | MIT/Apache-2.0 | https://github.com/tauri-apps/plugins-workspace |
| @tauri-apps/plugin-fs | 2.4.4 | MIT/Apache-2.0 | https://github.com/tauri-apps/plugins-workspace |
| @tauri-apps/plugin-notification | 2.3.3 | MIT/Apache-2.0 | https://github.com/tauri-apps/plugins-workspace |
| @tauri-apps/plugin-shell | 2.3.3 | MIT/Apache-2.0 | https://github.com/tauri-apps/plugins-workspace |

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
| FastAPI | 0.109.0 | MIT | https://github.com/tiangolo/fastapi |
| Uvicorn | 0.27.0 | BSD-3-Clause | https://github.com/encode/uvicorn |
| Pydantic | 2.5.3 | MIT | https://github.com/pydantic/pydantic |
| IfcOpenShell | 0.8.1 | LGPL-3.0 | https://github.com/IfcOpenShell/IfcOpenShell |
| python-multipart | 0.0.6 | Apache-2.0 | https://github.com/andrew-d/python-multipart |
| python-dotenv | 1.0.0 | BSD-3-Clause | https://github.com/theskumar/python-dotenv |
| PyYAML | 6.0.1 | MIT | https://github.com/yaml/pyyaml |
| ReportLab | 4.0.8 | BSD | https://www.reportlab.com/dev/docs/faq/#1.3 |

## Rust Dependencies (Tauri Native)

| Crate | Version | License | URL |
|-------|---------|---------|-----|
| tauri | 2.x | MIT/Apache-2.0 | https://github.com/tauri-apps/tauri |
| tauri-plugin-shell | 2.x | MIT/Apache-2.0 | https://github.com/tauri-apps/plugins-workspace |
| tauri-plugin-dialog | 2.x | MIT/Apache-2.0 | https://github.com/tauri-apps/plugins-workspace |
| tauri-plugin-notification | 2.x | MIT/Apache-2.0 | https://github.com/tauri-apps/plugins-workspace |
| tauri-plugin-fs | 2.x | MIT/Apache-2.0 | https://github.com/tauri-apps/plugins-workspace |
| serde | 1.x | MIT/Apache-2.0 | https://github.com/serde-rs/serde |
| serde_json | 1.x | MIT/Apache-2.0 | https://github.com/serde-rs/json |
| tokio | 1.x | MIT | https://github.com/tokio-rs/tokio |

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

Example (React):
```
MIT License

Copyright (c) Meta Platforms, Inc. and affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### Apache License 2.0

Used by TypeScript, python-multipart, and Tauri (dual-licensed).

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

Used by **web-ifc**.

Allows:
- Commercial use
- Modification
- Distribution
- Patent use
- Private use

Requirements:
- Disclose source of MPL-licensed files if modified
- Include copyright notice
- Include license text

**Important**: This is a "file-level" copyleft license. Only modified files need to have source disclosed, not the entire application.

For IFC Tarkistaja:
- We use web-ifc as a binary/WASM module
- No modifications made to web-ifc source
- No source disclosure required for our application code

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
- If IfcOpenShell is bundled, users must be able to replace it
- For App Store distribution, provide mechanism to use different IfcOpenShell version

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

### Required in Application

The project is licensed under the MIT License. See the [LICENSE](LICENSE) file for the full license text and third-party attributions.

Include the following in your app's About section:

```
IFC Tarkistaja - Copyright (c) 2024-2026 Jaakko Rastas and IFC Tarkistaja Contributors
Licensed under the MIT License

This software uses the following open source components:

React - Copyright (c) Meta Platforms, Inc. - MIT License
Three.js - Copyright (c) 2010-2024 three.js authors - MIT License
Tauri - Copyright (c) 2017-2024 Tauri Contributors - MIT/Apache-2.0
FastAPI - Copyright (c) 2018 Sebastián Ramírez - MIT License
IfcOpenShell - Copyright (c) IfcOpenShell Contributors - LGPL-3.0
web-ifc - Copyright (c) IFC.js Contributors - MPL-2.0

Full license texts are available in the LICENSE file.
```

### LGPL Compliance Notice

For IfcOpenShell, include:

```
This application uses IfcOpenShell, which is licensed under LGPL-3.0.
The source code for IfcOpenShell is available at:
https://github.com/IfcOpenShell/IfcOpenShell

You may replace the IfcOpenShell library with a compatible version.
```

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

### For Rust crates:

```bash
cd frontend/src-tauri
cargo install cargo-license
cargo license --json > licenses.json
```

---

## Legal Considerations

### App Store Distribution

Apple has specific requirements:
1. All licenses must permit App Store distribution
2. GPL (not LGPL) libraries may be problematic
3. LGPL requires ability to relink (can be complex for native apps)

Current assessment:
- **MIT, Apache-2.0, BSD, ISC**: No issues
- **MPL-2.0 (web-ifc)**: OK, file-level copyleft only
- **LGPL-3.0 (IfcOpenShell)**: Requires compliance measures

### Recommendations

1. **Keep license file updated** when adding dependencies
2. **Review new dependencies** before adding
3. **Avoid GPL-licensed** packages if possible
4. **Document LGPL compliance** for IfcOpenShell
5. **Include attribution** in app's About section

---

## Contact

For licensing questions, contact the project maintainer:

**Jaakko Rastas** - Project Maintainer

Last updated: January 2026
