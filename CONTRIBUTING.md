# Contributing to GeoGlim

🙏 **Thank you for your interest in contributing to GeoGlim!**

We welcome contributions from the community to help improve this geological dataset processing package. This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Reporting Issues](#reporting-issues)
- [Community](#community)

## 🤝 Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- **Be respectful** and inclusive in all interactions
- **Be constructive** in feedback and discussions
- **Focus on the issue**, not the person
- **Help create a welcoming environment** for all contributors

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of geospatial data processing
- Familiarity with FastAPI (for backend contributions)
- Understanding of GeoPandas and Shapely (for data processing)

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/GeoGlim.git
   cd GeoGlim
   ```

3. **Set up the development environment**:
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Install in development mode
   pip install -e .
   ```

4. **Set up datasets** (see [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md))

5. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ How to Contribute

### Types of Contributions

We welcome various types of contributions:

#### 🐛 Bug Reports
- Use the GitHub issue tracker
- Include detailed reproduction steps
- Provide system information and error messages
- Include sample data or test cases if possible

#### ✨ Feature Requests
- Describe the feature and its use case
- Explain why it would be valuable
- Consider implementation complexity
- Discuss with maintainers before starting large features

#### 📝 Documentation
- Improve existing documentation
- Add examples and tutorials
- Fix typos and clarify explanations
- Translate documentation (future)

#### 🔧 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Code refactoring
- Test improvements

### Areas for Contribution

#### High Priority
- **Dataset support**: Adding new geological datasets
- **Performance optimization**: Improving clipping speed
- **Error handling**: Better error messages and recovery
- **Testing**: Expanding test coverage
- **Documentation**: More examples and tutorials

#### Medium Priority
- **Visualization**: Better plotting and mapping features
- **Export formats**: Additional output formats
- **Caching**: Dataset caching for better performance
- **Authentication**: User authentication for hosted version

#### Future Features
- **Web interface**: Browser-based interface
- **Cloud deployment**: Production hosting setup
- **API versioning**: Multiple API versions
- **Batch processing**: Multiple area processing

## 🔄 Pull Request Process

### Before Submitting

1. **Check existing issues** and PRs to avoid duplicates
2. **Discuss large changes** with maintainers first
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Follow coding standards** (see below)

### Submission Steps

1. **Ensure your branch is up to date**:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Run tests locally**:
   ```bash
   python -m pytest tests/
   python test_api.py
   python test_glim_only.py
   ```

3. **Create a pull request** with:
   - Clear title and description
   - Reference to related issues
   - List of changes made
   - Screenshots (if UI changes)
   - Testing instructions

### Review Process

- Maintainers will review your PR
- Address feedback and requested changes
- Keep discussions constructive and focused
- Be patient - reviews take time

## 📏 Coding Standards

### Python Code Style

- **Follow PEP 8** for Python code style
- **Use Black** for code formatting:
  ```bash
  black geoglim/ backend/ tests/
  ```
- **Use type hints** where appropriate
- **Write docstrings** for functions and classes

### Code Organization

- **Keep functions focused** and single-purpose
- **Use meaningful variable names**
- **Add comments** for complex logic
- **Follow existing patterns** in the codebase

### Example Code Style

```python
from typing import Optional, Dict, Any
import geopandas as gpd
from shapely.geometry import Polygon

def clip_dataset(
    dataset_path: str, 
    geometry: Polygon, 
    output_format: str = "geojson"
) -> Optional[gpd.GeoDataFrame]:
    """
    Clip a geological dataset to a specified geometry.
    
    Args:
        dataset_path: Path to the dataset file
        geometry: Clipping geometry
        output_format: Output format (geojson, shapefile, gpkg)
        
    Returns:
        Clipped GeoDataFrame or None if error
        
    Raises:
        FileNotFoundError: If dataset file doesn't exist
        ValueError: If geometry is invalid
    """
    # Implementation here
    pass
```

## 🧪 Testing

### Test Requirements

- **Write tests** for new functionality
- **Maintain test coverage** above 80%
- **Test edge cases** and error conditions
- **Use meaningful test names**

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_clip_service.py -v

# Run with coverage
python -m pytest tests/ --cov=geoglim --cov-report=html
```

### Test Structure

```python
import pytest
import geopandas as gpd
from shapely.geometry import box
from geoglim.services import clip_service

class TestClipService:
    def test_clip_valid_geometry(self):
        """Test clipping with valid geometry."""
        # Test implementation
        pass
        
    def test_clip_invalid_geometry(self):
        """Test clipping with invalid geometry."""
        with pytest.raises(ValueError):
            # Test implementation
            pass
```

## 📚 Documentation

### Documentation Standards

- **Use clear, concise language**
- **Include code examples**
- **Update relevant documentation** with changes
- **Follow existing documentation style**

### Documentation Types

- **API documentation**: Function and class docstrings
- **User guides**: How-to guides and tutorials
- **Developer documentation**: Architecture and design decisions
- **Examples**: Jupyter notebooks and scripts

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Clear description** of the issue
- **Steps to reproduce** the problem
- **Expected vs. actual behavior**
- **System information** (OS, Python version, package versions)
- **Error messages** and stack traces
- **Sample data** or test case (if possible)

### Feature Requests

For feature requests, please provide:

- **Clear description** of the proposed feature
- **Use case** and motivation
- **Proposed implementation** (if you have ideas)
- **Potential impact** on existing functionality

## 🌍 Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Email**: mgalib@purdue.edu for direct contact

### Getting Help

- Check existing documentation and examples
- Search existing issues and discussions
- Ask questions in GitHub Discussions
- Contact maintainers directly if needed

## 🏷️ Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release notes
- [ ] Tag release in Git

## 🙏 Recognition

Contributors will be recognized in:
- **CONTRIBUTORS.md** file (to be created)
- **Release notes** for significant contributions
- **Documentation** for major features

## 📞 Contact

**Project Maintainer**: Mohammad Galib
- Email: mgalib@purdue.edu
- GitHub: [@galib9690](https://github.com/galib9690)

---

**Thank you for contributing to GeoGlim!** 🌍✨

Your contributions help make geological data more accessible to researchers worldwide.
