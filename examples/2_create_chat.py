# examples/2_create_chat.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "CHAT_CREATE",
        "data": {
            "title": "Sample Chat",
            "usernames": ["john_doe"]  # List of usernames to be added to the chat
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()