# examples/2_create_chat.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "CHAT_CREATE",
        "data": {
            "title": "Sample Chat",
            "user_ids": ["{USER_ID}"]  # List of user_ids to be added to the chat
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")
    response = json.loads(response.decode('utf-8'))
    print(f" [x] Chat ID: {response['data']['chat']['chat_id']}")

if __name__ == "__main__":
    main()