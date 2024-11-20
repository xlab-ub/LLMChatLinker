# examples/5_generate_llm_response.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_RESPONSE_GENERATE",
        "data": {
            "user_id": "{USER_ID}",  # ID of the user to generate response for
            "chat_id": "{CHAT_ID}",  # ID of the chat to generate response for
            "provider_id": "{LLM_PROVIDER_ID}",  # ID of the LLM provider to use
            "llm_id": "{LLM_ID}",  # ID of the LLM to use
            "user_input": "What is the longest river in the world?"
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")
    response = json.loads(response.decode('utf-8'))
    print(f" [x] Message ID: {response['data']['llm_response']['message_id']}")

if __name__ == "__main__":
    main()