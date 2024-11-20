# examples/14_delete_llm_provider.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_PROVIDER_DELETE",
        "data": {
            "provider_id": "{LLM_PROVIDER_ID}"  # ID of the LLM provider to delete
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()