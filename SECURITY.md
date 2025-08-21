# 🔒 Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅                 |
| < 1.0   | ❌                 |

## Reporting a Vulnerability

We take the security of TASKY seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to **[your-email@example.com]**.

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the requested information listed below (as much as you can provide) to help us better understand the nature and scope of the possible issue:

- **Type of issue** (buffer overflow, SQL injection, cross-site scripting, etc.)
- **Full paths of source file(s) related to the vulnerability**
- **The location of the affected source code** (tag/branch/commit or direct URL)
- **Any special configuration required to reproduce the issue**
- **Step-by-step instructions to reproduce the issue**
- **Proof-of-concept or exploit code** (if possible)
- **Impact of the issue**, including how an attacker might exploit it

This information will help us triage your report more quickly.

## Preferred Languages

We prefer all communications to be in English.

## Policy

TASKY follows the principle of [Responsible Disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure).

## Security Updates

Security updates will be released as patch versions (e.g., 1.0.1, 1.0.2) and will be clearly marked in the changelog.

## Reporting Security Issues in Dependencies

If you find a security issue in one of our dependencies, please report it to the maintainers of that package first. If the issue affects TASKY specifically, please also report it to us.

## Security Best Practices

When using TASKY:

1. **Keep your system updated** - Ensure Windows and TASKY are running the latest versions
2. **Use strong passwords** - If you implement authentication features
3. **Be cautious with task data** - Don't share sensitive information in task descriptions
4. **Regular backups** - Backup your `tasks.db` file regularly
5. **Monitor for updates** - Check for new releases regularly

## Security Features

TASKY includes several security features:

- **Local data storage** - All data is stored locally on your machine
- **No network communication** - TASKY doesn't send data over the internet
- **Input validation** - All user inputs are validated and sanitized
- **SQL injection protection** - Database queries use parameterized statements
- **File permission checks** - Ensures proper file access permissions

## Contact Information

- **Security Email**: [your-email@example.com]
- **PGP Key**: [Your PGP key if you have one]
- **Response Time**: Within 48 hours

## Acknowledgments

We would like to thank all security researchers and users who responsibly report security issues to us. Your contributions help make TASKY more secure for everyone.
