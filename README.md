# AI Coach V2

## Security & Setup

### Environment Variables
1. Copy `.env.example` to `.env` in the backend directory
2. Fill in your API keys and configuration
3. Never commit the `.env` file

### Development Setup
1. Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

2. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Configure your environment:
- Create a Notion integration at https://www.notion.so/my-integrations
- Get an OpenAI API key at https://platform.openai.com
- Add both keys to your `.env` file

### Security Best Practices
- Never commit API keys or secrets
- Always use environment variables for sensitive data
- Run tests in an environment with test API keys
- Regularly rotate your API keys
- Use pre-commit hooks to prevent accidental exposure