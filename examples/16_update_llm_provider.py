# examples/13_update_llm_provider.py

from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config

def main():
    client = LLMChatLinkerClient()

    # Load provider_id from config.json
    config = read_config()
    provider_id = config.get('provider_id')

    response = client.update_llm_provider(
        provider_id=provider_id,
        name="Updated Provider Name",
        api_endpoint="http://updated.endpoint/v1/chat/completions"
    )
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()