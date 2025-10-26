# Twinly

Twinly is an AI-powered networking follow-up automation system that uses iPhone voice recording, Claude for conversation analysis, and Toolhouse for intelligent multi-API orchestration. The agent extracts key context (contacts, companies, action items) from transcribed conversations and automatically generates personalized follow-up emails via Gmail API and tracking cards via Trello API. Built with a true agentic architecture using Model Context Protocol, Twinly reduces follow-up time from 30 minutes per person to 90 seconds—turning networking conversations into tracked opportunities automatically.

# Composio Integration Demo

This project demonstrates how to use Composio to connect users via auth config and execute tools (Gmail send email) using OpenAI Agents.

## Features

- 🔐 User authentication via Composio auth links
- 📧 Gmail integration for sending emails
- 🤖 OpenAI Agents for intelligent email composition
- 🔄 Async/await support for better performance

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   - Create a `.env` file and add your configuration:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     COMPOSIO_API_KEY=ak_mw8tmutaMn2U4D3191LQ
     EXTERNAL_USER_ID=pg-test-38ed8732-0fd8-4d01-aeb4-2f74953cd427
     AUTH_CONFIG_ID=ac_e7Sn-lQvFZ-Z
     ```

## Usage

Run the script:
```bash
python main.py
```

### Draft-only usage

Create a Gmail draft from `conversation.json` without sending:

```bash
python draft_email.py
```

This uses the Gmail toolkit action `GMAIL_CREATE_EMAIL_DRAFT` per the docs:
`https://docs.composio.dev/toolkits/gmail`

### What happens:

1. **Smart Authentication:**
   - Checks if user already has a connected account
   - **If connected**: Reuses existing connection (no re-auth needed! ✨)
   - **If not connected**: Generates OAuth URL and waits for user to authorize
   - Returns connected account ID

2. **Tool Execution:**
   - Fetches Gmail tools for the authenticated user
   - Creates an AI agent with Gmail capabilities
   - Agent sends an email to `yizucodes@gmail.com`
   - Returns execution result

## How It Works

### Smart User Authentication
```python
# Check for existing connection first
try:
    connected_accounts = composio.connected_accounts.get(user_id=externalUserId)
    if connected_accounts:
        connected_account = connected_accounts[0]  # Reuse existing!
except:
    # No existing connection - create new auth link
    connection_request = composio.connected_accounts.link(
        user_id=externalUserId,
        auth_config_id=os.getenv("AUTH_CONFIG_ID"),
    )
    connected_account = connection_request.wait_for_connection()
```

### Tool Execution
```python
tools = composio.tools.get(user_id=externalUserId, tools=["GMAIL_SEND_EMAIL"])
agent = Agent(name="Email Manager", instructions="...", tools=tools)
result = await Runner.run(starting_agent=agent, input="Send an email...")
```

## Dependencies

- `composio-core` - Core Composio SDK
- `composio-openai-agents` - OpenAI Agents provider for Composio
- `python-dotenv` - Environment variable management
- `openai` - OpenAI API client

## Documentation

For more information, visit:
- [Composio Documentation](https://docs.composio.dev)
- [Authenticating Tools](https://docs.composio.dev/docs/authenticating-tools.mdx)
- [Executing Tools](https://docs.composio.dev/docs/executing-tools.mdx)
- [OpenAI Agents Provider](https://docs.composio.dev/providers/openai-agents.mdx)

## ⚙️ Configuration

All configuration is now managed via environment variables in `.env`:
- **COMPOSIO_API_KEY**: Your Composio API key
- **AUTH_CONFIG_ID**: Your Composio auth configuration ID
- **EXTERNAL_USER_ID**: The ID of the user in your system
- **OPENAI_API_KEY**: Your OpenAI API key

No hardcoded values in the code!

## Notes

- **One-time authentication**: After the first successful auth, subsequent runs will automatically reuse the existing connection - no re-authentication needed! 🎉
- Make sure your Composio API key has the necessary permissions
- The auth config ID should be properly configured in your Composio dashboard
- Email sending requires proper Gmail API permissions
- Composio stores connected accounts server-side, so they persist across script runs

