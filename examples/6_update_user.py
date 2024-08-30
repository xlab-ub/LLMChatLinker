# examples/6_update_user.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "USER_UPDATE",
        "data": {
            "user_id": 1,
            "username": "john_doe_updated",
            "profile": "Updated profile"
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()