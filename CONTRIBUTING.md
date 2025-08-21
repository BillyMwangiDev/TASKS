# 🤝 Contributing to TASKY

Thank you for your interest in contributing to TASKY! This document provides guidelines and information for contributors.

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.8+
- Git
- Basic knowledge of Python and PyQt6
- Familiarity with GitHub workflows

### **Fork and Clone**
1. Fork the TASKY repository
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/TASKY.git
   cd TASKY
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/originalusername/TASKY.git
   ```

### **Setup Development Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Run the application
python main.py
```

## 🔧 **Development Workflow**

### **1. Create a Feature Branch**
```bash
# Update your main branch
git checkout main
git pull upstream main

# Create and checkout feature branch
git checkout -b feature/your-feature-name
```

### **2. Make Your Changes**
- Follow the coding standards (see below)
- Write tests for new functionality
- Update documentation as needed
- Test your changes thoroughly

### **3. Commit Your Changes**
```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add new task priority feature

- Add priority levels (High, Medium, Low)
- Update task dialog to include priority selection
- Add priority column to task table
- Update database schema for priority storage"
```

### **4. Push and Create Pull Request**
```bash
# Push your branch
git push origin feature/your-feature-name

# Create pull request on GitHub
```

## 📝 **Coding Standards**

### **Python Style Guide**
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for all function parameters and return values
- Maximum line length: 88 characters (Black formatter)
- Use descriptive variable and function names

### **Code Formatting**
```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check code style with flake8
flake8 .
```

### **Documentation Standards**
- Use Google-style docstrings for all functions and classes
- Include examples in docstrings for complex functions
- Update README.md for user-facing changes
- Update USER_MANUAL.md for feature changes

### **Example Docstring**
```python
def create_task(title: str, description: str, due_date: datetime) -> Task:
    """Create a new task with the specified details.
    
    Args:
        title: The task title (required)
        description: The task description (optional)
        due_date: When the task is due
        
    Returns:
        A new Task instance with the specified details
        
    Raises:
        ValueError: If title is empty or due_date is in the past
        
    Example:
        >>> task = create_task("Buy groceries", "Milk, bread, eggs", 
        ...                    datetime.now() + timedelta(days=1))
        >>> print(task.title)
        Buy groceries
    """
```

## 🧪 **Testing Guidelines**

### **Running Tests**
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_database.py

# Run tests in verbose mode
pytest -v
```

### **Writing Tests**
- Test all new functionality
- Include edge cases and error conditions
- Use descriptive test names
- Mock external dependencies when appropriate

### **Test Structure**
```python
def test_create_task_success():
    """Test successful task creation."""
    # Arrange
    title = "Test Task"
    description = "Test Description"
    due_date = datetime.now() + timedelta(days=1)
    
    # Act
    task = create_task(title, description, due_date)
    
    # Assert
    assert task.title == title
    assert task.description == description
    assert task.due_date == due_date
    assert not task.completed
```

## 📚 **Documentation Updates**

### **When to Update Documentation**
- Adding new features
- Changing existing functionality
- Fixing bugs that affect user experience
- Updating installation or setup instructions

### **Documentation Files to Update**
- `README.md` - Project overview and quick start
- `USER_MANUAL.md` - User guide and features
- `DISTRIBUTION_GUIDE.md` - Build and distribution
- `CONTRIBUTING.md` - This file
- Code docstrings and comments

## 🔨 **Building and Testing**

### **Test Build Process**
```bash
# Clean previous builds
python build.py --clean

# Build executable
python build.py

# Test the built executable
./TASKY-Distribution/TASKY.exe
```

### **Verify Build Artifacts**
- Check that `TASKY.exe` runs without errors
- Verify all features work in the built version
- Test on a clean Windows machine if possible
- Ensure file size is reasonable (50-100MB)

## 🐛 **Bug Reports and Issues**

### **Before Reporting**
- Search existing issues for duplicates
- Test with the latest version
- Try to reproduce the issue consistently
- Check if it's a known limitation

### **Issue Template**
Use the provided issue templates:
- 🐛 Bug Report for problems
- 💡 Feature Request for new ideas
- 📚 Documentation for documentation issues

### **Good Bug Report Example**
```
Title: [BUG] Application crashes when adding task with empty title

Description: The application crashes with a "ValueError: Title cannot be empty" 
when trying to add a task without a title.

Steps to Reproduce:
1. Click "Add Task" button
2. Leave title field empty
3. Fill in description and due date
4. Click "Save"
5. Application crashes

Expected: Show validation error message
Actual: Application crashes

System: Windows 11, TASKY v1.0.0
```

## 💡 **Feature Requests**

### **Good Feature Request Example**
```
Title: [FEATURE] Task categories and tags

Description: Add the ability to organize tasks by categories and add tags 
for better organization.

Problem: Currently all tasks are in one flat list, making it difficult 
to organize work by project or priority.

Proposed Solution: Add a category dropdown and tag input field to the 
task dialog. Display categories in the task table and allow filtering 
by category.

Use Cases:
- Organize work tasks vs personal tasks
- Group tasks by project or client
- Filter tasks by priority or type

Priority: Medium - Important for workflow
```

## 🔄 **Pull Request Process**

### **Before Submitting**
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No new warnings are generated
- [ ] Changes are tested thoroughly

### **Pull Request Template**
Use the provided pull request template and fill in all sections:
- Clear description of changes
- Type of change (bug fix, feature, etc.)
- Testing performed
- Screenshots if UI changes
- Related issues

### **Review Process**
1. Automated checks must pass (CI/CD)
2. Code review by maintainers
3. Address feedback and suggestions
4. Maintainers approve and merge

## 🏷️ **Commit Message Convention**

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): description

[optional body]

[optional footer]
```

### **Types**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### **Examples**
```
feat(ui): add dark mode toggle button

fix(database): resolve SQL injection vulnerability in task search

docs(readme): update installation instructions for Windows 11

style: format code with Black formatter

refactor(notifications): simplify notification manager class

test(database): add tests for task deletion edge cases

chore: update dependencies to latest versions
```

## 🎯 **Areas for Contribution**

### **High Priority**
- Bug fixes and stability improvements
- Performance optimizations
- Security enhancements
- Cross-platform compatibility

### **Medium Priority**
- New features and functionality
- UI/UX improvements
- Documentation updates
- Test coverage improvements

### **Low Priority**
- Code refactoring
- Style improvements
- Additional themes
- Localization support

## 📞 **Getting Help**

### **Communication Channels**
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: [your-email@example.com] for security issues

### **Resources**
- [PyQt6 Documentation](https://doc.qt.io/qtforpython/)
- [Python Documentation](https://docs.python.org/)
- [GitHub Guides](https://guides.github.com/)

## 🙏 **Acknowledgments**

Thank you to all contributors who help make TASKY better! Your contributions are appreciated and help improve the experience for all users.

## 📄 **License**

By contributing to TASKY, you agree that your contributions will be licensed under the MIT License.

---

**Happy Contributing! 🚀**
