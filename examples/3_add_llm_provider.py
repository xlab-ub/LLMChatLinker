# examples/3_add_llm_provider.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_PROVIDER_ADD",
        "data": {
            "name": "MLModelScope",
            "api_endpoint": "http://localhost:15555/api/chat"
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")
    response = json.loads(response.decode('utf-8'))
    print(f" [x] LLM Provider ID: {response['data']['provider']['provider_id']}")

if __name__ == "__main__":
    main()