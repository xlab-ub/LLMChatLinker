# examples/11_list_chats.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "CHAT_LIST",
        "data": {}
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()