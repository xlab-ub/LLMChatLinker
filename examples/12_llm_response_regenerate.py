# examples/12_llm_response_regenerate.py

from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_RESPONSE_REGENERATE",
        "data": {
            "message_id": "{MESSAGE_ID}"  # ID of the original user message to regenerate response for
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")
    response = json.loads(response.decode('utf-8'))
    print(f" [x] Message ID: {response['data']['llm_response']['message_id']}")

if __name__ == "__main__":
    main()