# Contributing to Autonomous Tumor Board

Thank you for your interest in contributing! This project was initially built for educational and competition purposes.

## 🚫 Important Notice

**This is a demonstration/research project.** It is NOT approved for clinical use and should NOT be deployed in healthcare settings without proper validation and regulatory approval.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the Issues tab
2. Create a new issue with:
   - Clear title
   - Detailed description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior

### Code Contributions

We welcome contributions that improve:
- Code quality and documentation
- Test coverage
- Educational value
- Research capabilities

**We DO NOT accept contributions that:**
- Claim clinical accuracy or diagnostic capability
- Remove safety disclaimers
- Enable unsupervised clinical deployment

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Run tests: `python test_system.py`
5. Update documentation if needed
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

### Code Standards

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include type hints where appropriate
- Write tests for new features
- Update relevant documentation

### Testing

Before submitting:

```bash
# Run full test suite
python test_system.py

# Check code style
black --check .

# Run type checking (optional)
mypy agents/ models/ orchestrator/
```

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License (see LICENSE file).

## ⚠️ Clinical Deployment

Do NOT submit PRs that:
- Remove safety warnings
- Claim diagnostic accuracy
- Enable autonomous clinical decisions
- Bypass human review requirements

Any clinical deployment requires separate regulatory approval and validation.

## 🔬 Research Contributions

We encourage contributions for:
- Improved multi-agent architectures
- Better uncertainty quantification
- Enhanced transparency mechanisms
- Educational documentation

## 📞 Questions?

Open an issue with the `question` label or refer to existing documentation:
- README.md - Overview
- SETUP_GUIDE.md - Setup instructions
- FEATURES.md - Feature documentation
- IMPROVEMENTS.md - Recent enhancements

---

**Thank you for helping improve this educational project!**
