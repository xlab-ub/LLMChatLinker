# examples/4_add_llm.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_ADD",
        "data": {
            "provider_name": "vLLM",
            "llm_name": "meta-llama/Meta-Llama-3-8B-Instruct"
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()