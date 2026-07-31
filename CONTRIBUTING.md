# Contributing to GitHub Profile 2.0

Thank you for contributing to GitHub Profile 2.0!

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vaibhavsolanki1/vaibhavsolanki1.git
   cd vaibhavsolanki1
   ```

2. **Set up virtual environment & install dependencies**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

3. **Run Code Quality Checks**:
   ```bash
   python -m black --check .
   python -m isort --check-only .
   python -m ruff check .
   python -m mypy scripts tests
   python -m pytest
   ```

4. **Run Build Pipeline Locally**:
   ```bash
   python scripts/build.py
   # Or alternatively:
   python -m scripts.build
   ```

## Pull Request Guidelines
- All PRs must pass `pytest`, `ruff`, and `mypy` checks.
- Keep SVG file size under 200KB per asset.
- Do not introduce third-party badge or widget dependencies.
