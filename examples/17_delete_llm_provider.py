# examples/14_delete_llm_provider.py

from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config

def main():
    client = LLMChatLinkerClient()

    # Load provider_id from config.json
    config = read_config()
    provider_id = config.get('provider_id')

    response = client.delete_llm_provider(provider_id=provider_id)
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()