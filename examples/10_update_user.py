# examples/6_update_user.py

from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config

def main():
    client = LLMChatLinkerClient()

    # Load user_id from config.json
    config = read_config()
    user_id = config.get('user_id')

    response = client.update_user(user_id=user_id, username="john_doe_updated", profile="Updated profile")
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()