# Contributing to Daodejing Multi-Version Study Platform

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to:
- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Setup Steps

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/daodejing.git
   cd daodejing
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

6. Verify the setup:
   ```bash
   python app.py
   # Open http://localhost:5000 in your browser
   ```

## Code Quality Standards

We maintain high code quality standards. All contributions must pass the following checks:

### Code Formatting

We use **Black** for code formatting:
```bash
black .
```

### Import Sorting

We use **isort** for import organization:
```bash
isort .
```

### Linting

We use **Flake8** for linting:
```bash
flake8 --config=.flake8 .
```

### Type Checking

We use **MyPy** for type checking:
```bash
mypy --config-file=mypy.ini services/ routes/ utils/
```

### Testing

We use **pytest** for testing:
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=services --cov-report=term-missing

# Run specific test file
pytest tests/test_services.py -v
```

**Target**: Maintain test coverage ≥ 80%

### Running All Checks

You can run all quality checks with:
```bash
python scripts/check_code_quality.py
```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-search-filter`
- `fix/tts-timeout-issue`
- `docs/update-api-docs`
- `refactor/optimize-queries`

### Commit Messages

Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

Examples:
```
feat(search): add full-text search functionality

fix(tts): resolve timeout issue with Fish Audio API
docs(readme): update installation instructions
```

### Pull Request Process

1. **Create a branch** from `main` for your changes
2. **Make your changes** following our code quality standards
3. **Test thoroughly** - ensure all tests pass
4. **Update documentation** if needed
5. **Submit a Pull Request** using our PR template

#### PR Requirements

- [ ] All tests pass
- [ ] Code follows style guidelines (Black, isort, Flake8)
- [ ] Type checking passes (MyPy)
- [ ] Coverage remains ≥ 80%
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md updated (if applicable)

#### PR Review Process

1. Automated checks must pass (CI/CD)
2. At least one maintainer review required
3. Address review comments
4. Squash commits if requested
5. Merge by maintainer

## Testing Guidelines

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names
- Follow Arrange-Act-Assert pattern

Example:
```python
def test_chapter_search_returns_results():
    # Arrange
    query = "道可道"

    # Act
    results = search_chapters(query)

    # Assert
    assert len(results) > 0
    assert all(query in r['content'] for r in results)
```

### Test Coverage

Aim for:
- 100% coverage for critical paths
- ≥80% overall coverage
- Test edge cases and error conditions

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Follow Google-style docstrings
- Include type hints

Example:
```python
def get_chapter(classic_id: str, chapter_id: int) -> Dict[str, Any]:
    """Retrieve a specific chapter by ID.

    Args:
        classic_id: The classic identifier (e.g., 'ddj', 'zzj')
        chapter_id: The chapter number

    Returns:
        Dictionary containing chapter data

    Raises:
        ValueError: If chapter_id is out of range
        KeyError: If classic_id is not found
    """
```

### Project Documentation

Update relevant documentation when:
- Adding new features
- Changing APIs
- Modifying deployment process
- Adding dependencies

Documentation locations:
- `docs/` - Technical documentation
- `README.md` - Project overview
- `docs/user-guide.md` - User documentation
- `docs/architecture.md` - Architecture docs

## Adding New Classics

To add support for a new classic text:

1. Prepare data file in `data/{classic_id}/chapters.json`
2. Add entry to `data/classics.json`
3. Test the integration
4. Update documentation

## Questions?

- Open an issue for questions
- Join our discussions
- Contact maintainers

## Attribution

Contributors will be acknowledged in our README and release notes.

Thank you for contributing! ☯️
