# Code Security Review Guide

> Code security review checklists and guidelines

## OWASP Top 10

1. **Injection** - SQL, NoSQL, OS command injection
2. **Broken Authentication** - Authentication vulnerabilities
3. **Sensitive Data Exposure** - Sensitive data exposure
4. **XML External Entities (XXE)** - XML external entities
5. **Broken Access Control** - Access control vulnerabilities
6. **Security Misconfiguration** - Security configuration errors
7. **Cross-Site Scripting (XSS)** - Cross-site scripting
8. **Insecure Deserialization** - Insecure deserialization
9. **Using Components with Known Vulnerabilities** - Known vulnerabilities
10. **Insufficient Logging & Monitoring** - Insufficient logging

## Review Checklist

- [ ] Input validation and sanitization
- [ ] Authentication/authorization checks
- [ ] Sensitive information encryption
- [ ] SQL parameterization
- [ ] XSS prevention (escape/encode)
- [ ] CSRF token usage
- [ ] Minimize error message information exposure
- [ ] Dependency vulnerability scanning
