import json
import os
import getpass

config_path = "/home/ahmad/.gemini/config/mcp_config.json"

if not os.path.exists(config_path):
    print("Error: MCP config file not found at", config_path)
    exit(1)

print("This script will configure the GitHub MCP server in your agent settings.")
print("It requires a GitHub Personal Access Token (PAT) with 'repo' scope permissions.")
print("Your token will be read securely and written directly to your config file without being leaked.\n")

token = getpass.getpass("Enter your GitHub Personal Access Token (PAT): ")
if not token.strip():
    print("Error: Token cannot be empty.")
    exit(1)

try:
    with open(config_path, "r") as f:
        config = json.load(f)
except Exception as e:
    print(f"Error reading config file: {e}")
    exit(1)

if "mcpServers" not in config:
    config["mcpServers"] = {}

config["mcpServers"]["github"] = {
    "command": "npx",
    "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": token.strip()
      }
}

try:
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print("\nSuccess: GitHub MCP server configured in settings!")
except Exception as e:
    print(f"Error writing config file: {e}")
    exit(1)
