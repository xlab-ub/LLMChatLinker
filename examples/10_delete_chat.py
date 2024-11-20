# examples/10_delete_chat.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "CHAT_DELETE",
        "data": {
            "chat_id": "{CHAT_ID}"  # ID of the chat to delete
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()