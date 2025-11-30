# Contributing to Kai

Thank you for your interest in contributing to Kai! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and considerate in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/kai/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Relevant logs or screenshots

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with the "enhancement" label
3. Describe the feature and its use case
4. Explain why it would benefit Kai users

### Contributing Code

#### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/kai.git
cd kai

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

#### Development Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow the style guide (PEP 8 for Python)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests
   pytest
   
   # Run linters
   flake8 kai/
   black kai/
   mypy kai/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```
   
   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes
   - `refactor:` Code refactoring
   - `test:` Test additions or changes
   - `chore:` Maintenance tasks

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   
   Then create a PR on GitHub with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots/demos if applicable

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints for function signatures
- Write docstrings for public APIs
- Keep functions focused and small
- Use meaningful variable names

Example:
```python
def process_audio_input(audio_data: bytes, sample_rate: int = 16000) -> str:
    """
    Process raw audio data and convert to text.
    
    Args:
        audio_data: Raw audio bytes
        sample_rate: Audio sample rate in Hz
        
    Returns:
        Transcribed text from audio
        
    Raises:
        AudioProcessingError: If audio processing fails
    """
    # Implementation
    pass
```

### Testing

- Write unit tests for new functionality
- Maintain test coverage above 80%
- Use pytest for testing
- Mock external dependencies

```python
def test_audio_processing():
    audio_data = generate_test_audio()
    result = process_audio_input(audio_data)
    assert isinstance(result, str)
    assert len(result) > 0
```

### Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for architectural changes
- Add docstrings to all public functions/classes
- Create tutorials for complex features

## Plugin Development

### Creating a Plugin

1. Create a new directory in `kai/plugins/`
2. Implement the Plugin interface
3. Add configuration schema
4. Write tests
5. Document usage

Example plugin structure:
```
kai/plugins/my_plugin/
├── __init__.py
├── plugin.py
├── config.yaml
├── README.md
└── tests/
    └── test_plugin.py
```

### Plugin Guidelines

- Keep plugins focused on a single responsibility
- Handle errors gracefully
- Respect user privacy
- Document required permissions
- Provide configuration options

## Review Process

1. **Automated Checks**: CI/CD runs tests and linters
2. **Code Review**: Maintainers review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged

## Community

### Getting Help

- **Discord**: Real-time chat and support
- **Forum**: Long-form discussions
- **GitHub Discussions**: Project-related questions

### Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project website

## License

By contributing to Kai, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to reach out:
- Open a discussion on GitHub
- Ask in Discord
- Email: dev@kai-assistant.org

Thank you for making Kai better!
