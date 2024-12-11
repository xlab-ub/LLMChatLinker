# examples/16_update_llm.py

from llmchatlinker.client import LLMChatLinkerClient
from config_utils import read_config

def main():
    client = LLMChatLinkerClient()

    # Load llm_id from config.json
    config = read_config()
    llm_id = config.get('llm_id')

    response = client.update_llm(llm_id=llm_id, llm_name="Updated LLM Name")
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()