# examples/9_update_chat.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "CHAT_UPDATE",
        "data": {
            "chat_id": 1,
            "title": "Updated Chat Title"
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()