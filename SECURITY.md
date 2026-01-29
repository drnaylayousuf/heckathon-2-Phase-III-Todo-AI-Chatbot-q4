# Security Policy

## Supported Versions

We release patches for security vulnerabilities. The table below shows which versions are currently supported:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | ✅ Yes             |
| < 1.0   | ❌ No              |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it to us responsibly:

1. **Do not** open a public issue
2. Contact us directly through private channels
3. Provide detailed information about the vulnerability
4. Allow time for us to investigate and address the issue

## Security Measures

### Authentication & Authorization
- JWT-based authentication with secure token handling
- Role-based access control for API endpoints
- Secure password hashing using bcrypt

### Data Protection
- All sensitive data encrypted in transit (HTTPS/TLS)
- Environment variables used for secrets (never hardcoded)
- Input validation and sanitization on all endpoints

### API Security
- Rate limiting to prevent abuse
- CORS configured for specific origins only
- SQL injection prevention through parameterized queries
- Proper error handling that doesn't leak sensitive information

### AI Integration Security
- API keys stored securely in environment variables
- Rate limiting on AI service calls
- Input sanitization for AI prompts

## Best Practices for Deployment

### Environment Variables
- Never commit sensitive data to version control
- Use secure vaults/secrets management for production
- Rotate API keys regularly
- Use strong, randomly generated secret keys

### Database Security
- Use parameterized queries to prevent SQL injection
- Regular database backups
- Secure database connections with SSL
- Least privilege principle for database users

### Network Security
- Enable HTTPS in production
- Configure proper CORS policies
- Use security headers
- Regular security audits