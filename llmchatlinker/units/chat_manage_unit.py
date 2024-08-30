# llmchatlinker/units/chat_manage_unit.py

class ChatManageUnit:
    def __init__(self, database_manage_unit):
        self.database_manage_unit = database_manage_unit

    def handle_instruction(self, instruction_type, data):
        if instruction_type == 'CHAT_CREATE':
            return self.create_chat(data)
        elif instruction_type == 'CHAT_UPDATE':
            return self.update_chat(data)
        elif instruction_type == 'CHAT_DELETE':
            return self.delete_chat(data)
        elif instruction_type == 'CHAT_LOAD':
            return self.load_chat(data)
        elif instruction_type == 'CHAT_LIST':
            return self.list_chats()
        # Handle other chat-related instructions here...

    def create_chat(self, data):
        try:
            chat_id = self.database_manage_unit.add_chat(data['title'])
            self.database_manage_unit.add_users_to_chat(chat_id, data['usernames'])
            return {"status": "success", "message": f"Chat {data['title']} created successfully with users: {', '.join(data['usernames'])}."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to create chat {data['title']}. {str(e)}"}

    def update_chat(self, data):
        try:
            chat = self.database_manage_unit.query_chat_by_id(data['chat_id'])
            if not chat:
                return {"status": "error", "message": f"Chat with id {data['chat_id']} does not exist."}
            chat.title = data.get('title', chat.title)
            self.database_manage_unit.commit_session()
            return {"status": "success", "message": f"Chat {data['chat_id']} updated successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update chat {data['chat_id']}. {str(e)}"}

    def delete_chat(self, data):
        try:
            chat = self.database_manage_unit.query_chat_by_id(data['chat_id'])
            if not chat:
                return {"status": "error", "message": f"Chat with id {data['chat_id']} does not exist."}
            self.database_manage_unit.delete_chat(chat)
            return {"status": "success", "message": f"Chat {data['chat_id']} deleted successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete chat {data['chat_id']}. {str(e)}"}

    def load_chat(self, data):
        try:
            chat = self.database_manage_unit.query_chat_by_id(data['chat_id'])
            if not chat:
                return {"status": "error", "message": f"Chat with id {data['chat_id']} does not exist."}
            return {"status": "success", "chat": {"chat_id": chat.chat_id, "title": chat.title, "users": [user.username for user in chat.users]}}
        except Exception as e:
            return {"status": "error", "message": f"Failed to load chat {data['chat_id']}. {str(e)}"}

    def list_chats(self):
        try:
            chats = self.database_manage_unit.query_all_chats()
            return {"status": "success", "chats": [{"chat_id": chat.chat_id, "title": chat.title, "users": [user.username for user in chat.users]} for chat in chats]}
        except Exception as e:
            return {"status": "error", "message": f"Failed to list chats. {str(e)}"}