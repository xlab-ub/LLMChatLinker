# examples/3_add_llm_provider.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_PROVIDER_ADD",
        "data": {
            "name": "vLLM",
            "api_endpoint": "http://localhost:12500/v1/chat/completions"
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()