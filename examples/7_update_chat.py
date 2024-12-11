# examples/9_update_chat.py

from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config

def main():
    client = LLMChatLinkerClient()

    # Load chat_id from config.json
    config = read_config()
    chat_id = config.get('chat_id')

    response = client.update_chat(chat_id=chat_id, title="Updated Chat Title")
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()