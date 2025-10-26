"""
Composio Integration with User Authentication and Gmail Tool Execution
This script demonstrates:
1. Smart user authentication - checks for existing connections first!
   - First run: User authenticates via OAuth
   - Subsequent runs: Automatically reuses existing connection (no re-auth!)
2. Fetching Gmail tools for the authenticated user
3. Executing Gmail send email action using OpenAI Agents
"""

import asyncio
import os
from dotenv import load_dotenv

from composio import Composio
from agents import Agent, Runner
from composio_openai_agents import OpenAIAgentsProvider

# Load environment variables (OPENAI_API_KEY, COMPOSIO_API_KEY, EXTERNAL_USER_ID, AUTH_CONFIG_ID)
load_dotenv()

# Initialize Composio with your API key from environment
composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"), provider=OpenAIAgentsProvider())

# Id of the user in your system (loaded from environment)
externalUserId = os.getenv("EXTERNAL_USER_ID")

print("=" * 80)
print("STEP 1: Check for Existing Connection or Authenticate")
print("=" * 80)

# Check if user already has a connected account
try:
    connected_accounts = composio.connected_accounts.get(user_id=externalUserId)
    
    if connected_accounts:
        # User already authenticated - reuse existing connection
        connected_account = connected_accounts[0]
        print(f"✅ Using existing connection!")
        print(f"   Connected account id: {connected_account.id}\n")
    else:
        raise Exception("No connected accounts found")
        
except Exception as e:
    # No existing connection - start OAuth flow
    print("🔐 No existing connection found. Starting authentication flow...\n")
    
    connection_request = composio.connected_accounts.link(
        user_id=externalUserId,
        auth_config_id=os.getenv("AUTH_CONFIG_ID"),
    )
    
    # Get the redirect URL for OAuth flow
    redirect_url = connection_request.redirect_url
    
    print(f"🔗 Please authorize the app by visiting this URL:\n{redirect_url}\n")
    
    # Wait for the connection to be established
    print("⏳ Waiting for user to complete authentication...")
    connected_account = connection_request.wait_for_connection()
    print(f"✅ Connection established successfully!")
    print(f"   Connected account id: {connected_account.id}\n")

print("=" * 80)
print("STEP 2: Fetch Tools and Execute Gmail Action")
print("=" * 80)

# Get Gmail tools that are pre-configured for this user
tools = composio.tools.get(user_id=externalUserId, tools=["GMAIL_CREATE_EMAIL_DRAFT"])
print(f"✅ Successfully fetched {len(tools)} Gmail tool(s)\n")

# Create an agent with Gmail capabilities
agent = Agent(
    name="Email Manager",
    instructions="You are a helpful assistant that can send emails on behalf of the user.",
    tools=tools
)

# Run the agent to send an email
async def main():
    print("📧 Sending email via AI Agent...\n")
    result = await Runner.run(
        starting_agent=agent,
        input="Send an email to yizucodes@gmail.com with the subject 'Hello from composio 👋🏻' and the body 'Congratulations on sending your first email using AI Agents and Composio!'",
    )
    print("=" * 80)
    print("RESULT:")
    print("=" * 80)
    print(result.final_output)
    print("\n✅ Email sent successfully!")

# Execute the async main function
if __name__ == "__main__":
    asyncio.run(main())

