# examples/15_list_llm_providers.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_PROVIDER_LIST",
        "data": {}
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()