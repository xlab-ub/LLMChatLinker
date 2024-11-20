# examples/4_add_llm.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_ADD",
        "data": {
            "provider_id": "{LLM_PROVIDER_ID}",  # ID of the LLM provider to use
            "llm_name": "llama_3_2_1b_instruct"
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")
    response = json.loads(response.decode('utf-8'))
    print(f" [x] LLM ID: {response['data']['llm']['llm_id']}")

if __name__ == "__main__":
    main()