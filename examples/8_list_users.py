# examples/8_list_users.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "USER_LIST",
        "data": {}
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()