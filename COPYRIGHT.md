# Copyright Notice

Copyright (c) 2024-2026 Jaakko Rastas and IFC Tarkistaja Contributors

All rights reserved for original code and content unless otherwise noted.

## Project License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for the full license text and third-party attributions.

---

## Third-Party Assets and Content

The following third-party assets are included in this repository and are subject to their respective licenses and terms of use:

### Finnish Government Documents

#### Regulatory Document
- **File**: `SK suunnitelmamalliasetus.pdf`
- **Source**: Finnish Ministry of the Environment (Ympäristöministeriö)
- **Content**: Building permit information model regulation (Suunnitelmamalli asetus)
- **Usage**: Reference document for Finnish building permit requirements
- **Note**: Finnish government documents are generally public domain for official use, but redistribution may be subject to terms. This document is included for educational and development reference purposes only.

#### Ryhti Data Model Schema
- **File**: `Rakentamisen lupapäätösten tietomalli.schema.json`
- **Source**: Finnish Digital and Population Data Services Agency (Digi- ja väestötietovirasto) via [tietomallit.suomi.fi](https://tietomallit.suomi.fi/model/raklu)
- **Content**: JSON Schema for Finnish building permit data model (raklu v1.1.0)
- **Usage**: Reference for Ryhti integration and field alignment
- **Note**: Public data model published by the Finnish government under CC BY 4.0 or similar open license for interoperability purposes.

---

### Sample IFC Files

#### RAVA Sample Files
- **Files**: 
  - `samples/RAVA3x5_ARK_Kerrostalo_v1_0.ifc`
  - `samples/RAVA3x5_ARK_Toimistotalo_v1_0.ifc`
- **Source**: RAVA (Rakennetun ympäristön valtakunnallinen tietovaranto) test files
- **Usage**: Testing and validation of IFC parsing against Finnish requirements
- **Note**: These are sample/test files provided for interoperability testing.

#### Project-Generated Test Files
- **Files**: 
  - `sample.ifc` - Minimal test IFC file
  - `finnish_example_house.ifc` - Finnish example house with FI property sets
  - `backend/tests/fixtures/sample.ifc` - Test fixture
- **License**: MIT (created for this project)
- **Note**: These files were generated specifically for testing this application.

---

### Framework Default Assets

#### Vite Assets
- **Files**: 
  - `frontend/public/vite.svg`
  - `frontend/dist/vite.svg`
- **Source**: [Vite](https://vitejs.dev/)
- **License**: MIT
- **Note**: Default template assets from Vite. May be replaced with custom branding.

#### React Assets
- **File**: `frontend/src/assets/react.svg`
- **Source**: [React](https://react.dev/)
- **License**: MIT
- **Note**: Default template asset. May be replaced with custom branding.

---

### Application Icons

#### Tauri App Icons
- **Location**: `frontend/src-tauri/icons/`
- **Files**: `32x32.png`, `128x128.png`, `128x128@2x.png`, `icon.icns`, `icon.ico`
- **License**: MIT (created for this project)
- **Note**: Custom application icons created for IFC Tarkistaja.

---

## Code Attribution

### No Third-Party Code Snippets

A review of the source code found no copied code snippets from external sources requiring separate attribution beyond the dependencies listed in [LICENSE](LICENSE) and [licenses-used.md](licenses-used.md).

All application code in `frontend/src/`, `backend/app/`, `python-sidecar/src/`, and `IFCTarkistaja.swiftpm/` is original work licensed under MIT.

---

## Font Usage

This project uses **system fonts** by default. No custom fonts are bundled with the application source code. Fonts found in `node_modules/` belong to their respective packages and are not distributed as part of this project.

---

## Recommendations for Distribution

1. **Finnish Regulatory PDF**: For public distribution, consider linking to the official source rather than bundling the PDF, or verify redistribution terms with the Ministry of the Environment.

2. **RAVA Sample Files**: For production releases, these sample files may be omitted or replaced with properly licensed test files, as they are only needed for development/testing.

3. **Framework Assets**: Replace Vite and React SVGs with custom project branding before public release.

4. **LGPL Compliance**: When distributing binaries, ensure IfcOpenShell LGPL compliance as documented in [licenses-used.md](licenses-used.md).

---

## Contact

For questions about copyright or licensing:

**Jaakko Rastas** - Project Maintainer

---

*Last updated: January 2026*
