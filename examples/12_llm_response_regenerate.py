# examples/12_llm_response_regenerate.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_RESPONSE_REGENERATE",
        "data": {
            "message_id": 2  # ID of the original user message to regenerate response for
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()