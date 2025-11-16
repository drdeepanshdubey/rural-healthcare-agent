# Contributing to Rural Healthcare Access Agent

Thank you for your interest in improving rural healthcare access through AI!

## 🤝 How to Contribute

### Reporting Issues
- Use [GitHub Issues](https://github.com/drdeepanshdubey/rural-healthcare-agent/issues)
- Describe the bug or feature request clearly
- Include system details and reproduction steps

### Code Contributions

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/rural-healthcare-agent.git`
3. **Create branch**: `git checkout -b feature/your-feature-name`
4. **Make changes** and test thoroughly
5. **Commit**: `git commit -m "Add: description of your changes"`
6. **Push**: `git push origin feature/your-feature-name`
7. **Open Pull Request** with clear description

### Development Setup

Clone and setup
git clone https://github.com/drdeepanshdubey/rural-healthcare-agent.git
cd rural-healthcare-agent
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

Add your Gemini API key to .env 

## 🎯 Areas for Contribution

### High Priority
- 🌐 **Multilingual Support**: Add Hindi, Marathi, regional languages
- 🏥 **Facility Database Expansion**: Add more districts and states
- 🧪 **Testing**: Unit tests, integration tests, end-to-end tests

### Medium Priority
- 📱 **Mobile App**: Android/iOS applications
- 🔬 **Enhanced Algorithms**: Improve urgency assessment accuracy
- 📊 **Analytics Dashboard**: For health departments and monitoring

### Nice to Have
- 📖 **Documentation**: Tutorials, guides, API documentation
- 🎨 **UI/UX**: Improve web interface design
- ♿ **Accessibility**: Screen reader support, keyboard navigation

## 📝 Code Standards

### Python Code
- Follow [PEP 8](https://pep8.org/) style guide
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Maximum line length: 100 characters

### Git Commits
- Use clear, descriptive commit messages
- Format: `Type: Brief description`
- Types: `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Docs`
- Example: `Add: Hindi language support for patient interface`

### Testing
- Write tests for new features
- Ensure existing tests pass: `pytest tests/`
- Aim for >80% code coverage

## 🌟 Recognition

Contributors will be:
- Listed in project README
- Acknowledged in release notes
- Mentioned in project documentation

## 🤔 Questions?

- Open a [GitHub Discussion](https://github.com/drdeepanshdubey/rural-healthcare-agent/discussions)
- Email: dr.deepanshdubey@gmail.com

## 📜 Code of Conduct

This project follows a code of conduct promoting:
- Respectful communication
- Constructive feedback
- Inclusive environment
- Focus on improving rural healthcare access

## 📄 License

By contributing, you agree that your contributions will be licensed under Apache License 2.0.

---

**Thank you for helping improve healthcare access for rural India! 🙏**
