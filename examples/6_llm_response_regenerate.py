# examples/12_llm_response_regenerate.py

from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config, write_config

def main():
    client = LLMChatLinkerClient()

    # Load message_id from config.json
    config = read_config()
    message_id = config.get('message_id')

    response = client.regenerate_llm_response(message_id=message_id)
    print(f" [x] Received {response}")
    new_message_id = response['data']['llm_response']['message_id']
    print(f" [x] New Message ID: {new_message_id}")

    # Save new_message_id to config.json
    config['message_id'] = new_message_id
    write_config(config)

if __name__ == "__main__":
    main()