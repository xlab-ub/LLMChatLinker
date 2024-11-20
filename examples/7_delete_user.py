# examples/7_delete_user.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "USER_DELETE",
        "data": {
            "user_id": "{USER_ID}"  # ID of the user to delete
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()