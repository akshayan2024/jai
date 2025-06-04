# Contributing to JAI API

Thank you for considering contributing to the JAI API project! We appreciate your interest in helping us improve this project.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/your-org/jai-api/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/your-org/jai-api/issues/new). Be sure to include:
  - A clear and descriptive title
  - A description of the expected behavior
  - A description of the actual behavior
  - Steps to reproduce the issue
  - Any relevant logs or screenshots

### Suggesting Enhancements

- Use GitHub Issues to suggest new features or improvements.
- Clearly describe the enhancement and why it would be useful.
- Include any relevant examples or use cases.

### Pull Requests

1. Fork the repository and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code follows the style guide.
5. Update the documentation as needed.
6. Issue a pull request.

## Development Setup

### Prerequisites

- Python 3.8+
- pip
- Git

### Installation

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/your-username/jai-api.git
   cd jai-api
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
make test  # Run all tests
make lint  # Run linters
make check-types  # Run type checking
```

### Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **Flake8** for linting
- **Mypy** for type checking

Run the following to format and check your code:

```bash
make format  # Auto-format code
make check   # Run all checks
```

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, including new environment variables, exposed ports, useful file locations, and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent.
4. The pull request will be reviewed by the maintainers and merged if it meets the project's standards.

## License

By contributing, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE) file.
