# Contributing to IFC Tarkistaja

Thank you for your interest in contributing to IFC Tarkistaja! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

1. Check if the issue already exists in [GitHub Issues](../../issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - IFC file sample if relevant (remove sensitive data)
   - Your environment (OS, browser, version)

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests: `npm test` (frontend) and `pytest` (backend)
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Open a Pull Request

### Code Style

**Python (Backend)**
- Follow PEP 8
- Use type hints
- Run `black` for formatting

**TypeScript/React (Frontend)**
- Use ESLint configuration provided
- Prefer functional components with hooks
- Use TypeScript strict mode

**General**
- Write meaningful commit messages
- Keep PRs focused on single features/fixes
- Add tests for new functionality

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest
```

### Frontend
```bash
cd frontend
npm install
npm run dev
npm test
```

### Docker
```bash
docker-compose up --build
```

## Questions?

Open a [Discussion](../../discussions) for questions or ideas.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
