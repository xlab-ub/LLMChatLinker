# LLMChatLinker

LLMChatLinker is a Middleware SDK designed to facilitate interaction between clients and Large Language Models (LLMs). The SDK acts as an intermediary between the client and the LLM(s), allowing multiple users to communicate with the LLM(s) simultaneously through the client's front-end.

## Architecture

The interaction flow follows the fetch-decode-execute-store cycle, similar to the architecture of a CPU (CISC/RISC):

1. **Fetch**: The Orchestrator (acting as the CPU) fetches the instructions from the instruction queue.
2. **Decode**: The Control Unit decodes the fetched instructions. Depending on the instruction type, it decodes the instruction to be directly executed later.
3. **Execute**: The decoded instruction is executed by the relevant manage unit (User, Chat, LLM, or Database Manage Unit).
4. **Store**: The result from the execution is stored back in the result queue, ensuring each user request is immediately linked to its corresponding result.

## Components

- **Client**: The front-end that interacts with users.
- **Middleware SDK (LLMChatLinker)**: Facilitates communication between the client and LLM(s). Composed of various units that mimic the functionality of CPU components:
  - **Orchestrator**: Acts as the CPU, fetching, decoding, executing, and storing instructions.
  - **Control Unit**: Decodes instructions fetched by the Orchestrator.
  - **User Manage Unit**: Manages user-related instructions.
  - **Chat Manage Unit**: Manages chat-related instructions.
  - **LLM Manage Unit**: Manages LLM-related instructions.
  - **Database Manage Unit**: Manages database interactions.
- **LLM(s)**: Large Language Models providing responses to user queries.

## Features

- **Fetch-Decode-Execute-Store Cycle**: Adopts the CPU-like mechanism to process instructions efficiently.
- **User Management**: Create, update, delete, and list users.
- **Chat Management**: Create, update, delete, load, and list chats.
- **LLM Management**: Add, update, delete, list LLM providers and LLMs.
- **Instruction Management**: Enable/disable instruction recording, delete and list instruction records.

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- RabbitMQ

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/cjlee7128/LLMChatLinker.git
    cd LLMChatLinker
    ```

2. **Create and activate a virtual environment:**
    ```bash
    conda create -n lclinker python=3.8
    conda activate lclinker
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the database:**
    Update the `DATABASE_URI` in `llmchatlinker/units/database_manage_unit.py` with your PostgreSQL credentials.

5. **Initialize the database:**
    ```bash
    python -m llmchatlinker.main
    ```

6. **Run RabbitMQ:**
    Ensure RabbitMQ is running on `localhost` (default settings).
    ```bash
    conda install conda-forge::rabbitmq-server
    rabbitmq-server
    ```

### Postgres Database

#### Pull Postgres Docker Image

```bash
docker pull postgres:16
```

#### Run Postgres Docker Container

```bash
docker run --name my_postgres \
    -e POSTGRES_USER=myuser \
    -e POSTGRES_PASSWORD=mypassword \
    -e POSTGRES_DB=mydatabase \
    -p 5433:5432 \
    -d postgres:16
```

### RabbitMQ Server

#### Install RabbitMQ Server

```bash
conda install conda-forge::rabbitmq-server
```

#### Start RabbitMQ Server

```bash
rabbitmq-server
```

## Usage

### Instructions

#### User-related Instructions

- **USER_CREATE**: Create a new user.
- **USER_UPDATE**: Update an existing user.
- **USER_DELETE**: Delete an existing user.
- **USER_LIST**: List all users.
- **USER_INSTRUCTION_RECORDING_ENABLE**: Enable instruction recording for a user.
- **USER_INSTRUCTION_RECORDING_DISABLE**: Disable instruction recording for a user.
- **USER_INSTRUCTION_RECORDS_DELETE**: Delete all instruction records for a user.
- **USER_INSTRUCTION_RECORDING_LIST**: List all instruction records for a user.

#### Chat-related Instructions

- **CHAT_CREATE**: Create a new chat.
- **CHAT_UPDATE**: Update an existing chat.
- **CHAT_DELETE**: Delete an existing chat.
- **CHAT_LOAD**: Load an existing chat.
- **CHAT_LIST**: List all chats.

#### LLM-related Instructions

- **LLM_RESPONSE_GENERATE**: Generate a response from the LLM.
- **LLM_RESPONSE_REGENERATE**: Regenerate a response from the LLM.
- **LLM_PROVIDER_ADD**: Add a new LLM provider.
- **LLM_PROVIDER_UPDATE**: Update an existing LLM provider.
- **LLM_PROVIDER_DELETE**: Delete an LLM provider.
- **LLM_PROVIDER_LIST**: List all LLM providers.
- **LLM_ADD**: Add a new LLM.
- **LLM_UPDATE**: Update an existing LLM.
- **LLM_DELETE**: Delete an LLM.
- **LLM_LIST**: List all LLMs.

### Examples

Below are some example usage scripts to interact with LLMChatLinker.

#### 1. Create a User

```python
from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "USER_CREATE",
        "data": {
            "username": "john_doe",
            "profile": "Sample profile"
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()
```

#### 2. Create a Chat

```python
from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "CHAT_CREATE",
        "data": {
            "title": "Sample Chat",
            "usernames": ["john_doe"]
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()
```

#### 3. Add an LLM Provider

```python
from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_PROVIDER_ADD",
        "data": {
            "name": "vLLM",
            "api_endpoint": "http://localhost:12500/v1/chat/completions"
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()
```

#### 4. Add an LLM

```python
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
```

#### 5. Generate an LLM Response

```python
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
```

#### 6. Regenerate an LLM Response

```python
from llmchatlinker.message_queue import publish_message
import json

def main():
    instruction = {
        "type": "LLM_RESPONSE_REGENERATE",
        "data": {
            "message_id": 2  # ID of the original user message to regenerate response for
        }
    }

    response = publish_message(json.dumps(instruction))
    print(f" [x] Received {response}")

if __name__ == "__main__":
    main()
```
