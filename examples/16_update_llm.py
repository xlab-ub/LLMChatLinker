# examples/16_update_llm.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_UPDATE",
        "data": {
            "llm_id": 1,
            "llm_name": "Updated LLM Name"
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()