# examples/5_generate_llm_response.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_RESPONSE_GENERATE",
        "data": {
            "user_id": 1,
            "chat_id": 1,
            "provider_name": "vLLM",
            "llm_name": "meta-llama/Meta-Llama-3-8B-Instruct",
            "user_input": "Who won the world series in 2020?"
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()