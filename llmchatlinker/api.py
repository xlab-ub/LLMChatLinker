# llmchatlinker/api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .message_queue import publish_message
import json

app = FastAPI(
    title="LLMChatLinker API",
    description="API for managing chat interactions with LLMs",
    version="1.0.0"
)

class BaseResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

class DataResponse(BaseResponse):
    data: Dict[str, Any]

# User Management Models
class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, pattern=r'^[a-zA-Z][a-zA-Z0-9_]{2,29}$')
    display_name: Optional[str] = Field(None, max_length=50)
    profile: Optional[str] = None

class UserUpdateRequest(BaseModel):
    user_id: str
    username: Optional[str] = Field(None, min_length=3, max_length=30, pattern=r'^[a-zA-Z][a-zA-Z0-9_]{2,29}$')
    display_name: Optional[str] = Field(None, max_length=50)
    profile: Optional[str] = None

class UserResponse(DataResponse):
    data: Dict[str, Any]

# Chat Management Models
class ChatCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    user_ids: List[str] = Field(..., min_items=1)

class ChatUpdateRequest(BaseModel):
    chat_id: str
    title: str = Field(..., min_length=1, max_length=100)

class ChatResponse(DataResponse):
    data: Dict[str, Any]

# LLM Provider Management Models
class LLMProviderAddRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    api_endpoint: str = Field(..., max_length=255)
    api_key: Optional[str] = Field(None, max_length=255)

class LLMProviderUpdateRequest(BaseModel):
    provider_id: str
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    api_endpoint: Optional[str] = Field(None, max_length=255)

# LLM Management Models
class LLMAddRequest(BaseModel):
    provider_id: str
    llm_name: str = Field(..., min_length=1, max_length=100)

class LLMUpdateRequest(BaseModel):
    llm_id: str
    llm_name: str = Field(..., min_length=1, max_length=100)

class LLMResponseGenerateRequest(BaseModel):
    user_id: str
    chat_id: str
    provider_id: str
    llm_id: str
    user_input: str = Field(..., min_length=1)

class LLMResponseRegenerateRequest(BaseModel):
    message_id: str

def process_instruction(instruction_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Process instruction through message queue"""
    instruction = {"type": instruction_type, "data": data}
    response = publish_message(json.dumps(instruction))
    return json.loads(response)

# User Management Endpoints
@app.post("/user/create", response_model=UserResponse, tags=["User Management"])
async def create_user(request: UserCreateRequest):
    """Create a new user with a username and profile."""
    data = request.model_dump(exclude_none=True)
    return process_instruction("USER_CREATE", data)

@app.put("/user/update", response_model=UserResponse, tags=["User Management"])
async def update_user(request: UserUpdateRequest):
    """Update an existing user's username and profile."""
    data = request.model_dump(exclude_none=True)
    return process_instruction("USER_UPDATE", data)

@app.delete("/user/delete", response_model=BaseResponse, tags=["User Management"])
async def delete_user(request: UserUpdateRequest):
    """Delete a user by user ID."""
    return process_instruction("USER_DELETE", {"user_id": request.user_id})

@app.get("/user/list", response_model=DataResponse, tags=["User Management"])
async def list_users():
    """List all users."""
    return process_instruction("USER_LIST", {})

@app.get("/user/{username}", response_model=UserResponse, tags=["User Management"])
async def get_user(username: str):
    """Get user details by username."""
    return process_instruction("USER_GET", {"username": username})

@app.get("/user/id/{user_id}", response_model=UserResponse, tags=["User Management"])
async def get_user_by_id(user_id: str):
    """Get user details by user ID."""
    return process_instruction("USER_GET", {"user_id": user_id})

@app.post("/user/{user_id}/instruction-recording/enable", response_model=BaseResponse, tags=["User Management"])
async def enable_instruction_recording(user_id: str):
    """Enable instruction recording for a user."""
    return process_instruction("USER_INSTRUCTION_RECORDING_ENABLE", {"user_id": user_id})

@app.post("/user/{user_id}/instruction-recording/disable", response_model=BaseResponse, tags=["User Management"])
async def disable_instruction_recording(user_id: str):
    """Disable instruction recording for a user."""
    return process_instruction("USER_INSTRUCTION_RECORDING_DISABLE", {"user_id": user_id})

@app.get("/user/{user_id}/instructions", response_model=DataResponse, tags=["User Management"])
async def list_user_instructions(user_id: str):
    """List instruction records for a user."""
    return process_instruction("USER_INSTRUCTION_RECORDS_LIST", {"user_id": user_id})

@app.delete("/user/{user_id}/instructions", response_model=BaseResponse, tags=["User Management"])
async def delete_user_instructions(user_id: str):
    """Delete all instruction records for a user."""
    return process_instruction("USER_INSTRUCTION_RECORDS_DELETE", {"user_id": user_id})

# Chat Management Endpoints
@app.post("/chat/create", response_model=ChatResponse, tags=["Chat Management"])
async def create_chat(request: ChatCreateRequest):
    """Create a new chat with a title and list of user_ids."""
    data = request.model_dump(exclude_none=True)
    return process_instruction("CHAT_CREATE", data)

@app.put("/chat/update", response_model=ChatResponse, tags=["Chat Management"])
async def update_chat(request: ChatUpdateRequest):
    """Update an existing chat's title."""
    data = request.model_dump(exclude_none=True)
    return process_instruction("CHAT_UPDATE", data)

@app.delete("/chat/delete", response_model=BaseResponse, tags=["Chat Management"])
async def delete_chat(request: ChatUpdateRequest):
    """Delete a chat by chat ID."""
    return process_instruction("CHAT_DELETE", {"chat_id": request.chat_id})

@app.get("/chat/list", response_model=DataResponse, tags=["Chat Management"])
async def list_chats():
    """List all chats."""
    return process_instruction("CHAT_LIST", {})

@app.get("/chat/id/{chat_id}", response_model=DataResponse, tags=["Chat Management"])
async def get_chat(chat_id: str):
    """Get chat details by chat ID."""
    return process_instruction("CHAT_LOAD", {"chat_id": chat_id})

@app.get("/chat/user/{user_id}", response_model=DataResponse, tags=["Chat Management"])
async def list_user_chats(user_id: str):
    """List all chats for a user by user ID."""
    return process_instruction("CHAT_LIST_BY_USER", {"user_id": user_id})

# LLM Provider Management Endpoints
@app.post("/llm_provider/add", response_model=DataResponse, tags=["LLM Provider Management"])
async def add_llm_provider(request: LLMProviderAddRequest):
    """Add a new LLM provider with a name and API endpoint."""
    data = request.model_dump(exclude_none=True)
    return process_instruction("LLM_PROVIDER_ADD", data)

@app.put("/llm_provider/update", response_model=DataResponse, tags=["LLM Provider Management"])
async def update_llm_provider(request: LLMProviderUpdateRequest):
    """Update an existing LLM provider's name and API endpoint."""
    data = request.model_dump(exclude_none=True)
    return process_instruction("LLM_PROVIDER_UPDATE", data)

@app.delete("/llm_provider/delete", response_model=BaseResponse, tags=["LLM Provider Management"])
async def delete_llm_provider(request: LLMProviderUpdateRequest):
    """Delete an LLM provider by provider ID."""
    return process_instruction("LLM_PROVIDER_DELETE", {"provider_id": request.provider_id})

@app.get("/llm_provider/list", response_model=DataResponse, tags=["LLM Provider Management"])
async def list_llm_providers():
    """List all LLM providers."""
    return process_instruction("LLM_PROVIDER_LIST", {})

# LLM Management Endpoints
@app.post("/llm/add", response_model=DataResponse, tags=["LLM Management"])
async def add_llm(request: LLMAddRequest):
    """Add a new LLM with a provider name and LLM name."""
    data = request.model_dump(exclude_none=True)
    return process_instruction("LLM_ADD", data)

@app.put("/llm/update", response_model=DataResponse, tags=["LLM Management"])
async def update_llm(request: LLMUpdateRequest):
    """Update an existing LLM's name."""
    data = request.model_dump(exclude_none=True)
    return process_instruction("LLM_UPDATE", data)

@app.delete("/llm/delete", response_model=BaseResponse, tags=["LLM Management"])
async def delete_llm(request: LLMUpdateRequest):
    """Delete an LLM by LLM ID."""
    return process_instruction("LLM_DELETE", {"llm_id": request.llm_id})

@app.get("/llm/list", response_model=DataResponse, tags=["LLM Management"])
async def list_llms():
    """List all LLMs."""
    return process_instruction("LLM_LIST", {})

@app.get("/llm/llm_provider/{provider_id}", response_model=DataResponse, tags=["LLM Management"])
async def list_llms_by_provider(provider_id: str):
    """List all LLMs for a provider by provider ID."""
    return process_instruction("LLM_LIST_BY_PROVIDER", {"provider_id": provider_id})

# LLM Response Management Endpoints
@app.post("/llm/response_generate", response_model=DataResponse, tags=["LLM Response Management"])
async def generate_llm_response(request: LLMResponseGenerateRequest):
    """Generate a response from an LLM based on user input."""
    data = request.model_dump(exclude_none=True)
    return process_instruction("LLM_RESPONSE_GENERATE", data)

@app.post("/llm/response_regenerate", response_model=DataResponse, tags=["LLM Response Management"])
async def regenerate_llm_response(request: LLMResponseRegenerateRequest):
    """Regenerate a response from an LLM based on a previous message."""
    data = request.model_dump(exclude_none=True)
    return process_instruction("LLM_RESPONSE_REGENERATE", data)