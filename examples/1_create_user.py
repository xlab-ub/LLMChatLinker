# examples/1_create_user.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "USER_CREATE",
        "data": {
            "username": "john_doe",
            "profile": "Sample profile"
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()