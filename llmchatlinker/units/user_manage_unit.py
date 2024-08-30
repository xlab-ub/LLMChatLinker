# llmchatlinker/units/user_manage_unit.py

class UserManageUnit:
    def __init__(self, database_manage_unit):
        self.database_manage_unit = database_manage_unit

    def handle_instruction(self, instruction_type, data):
        if instruction_type == 'USER_CREATE':
            return self.create_user(data)
        elif instruction_type == 'USER_UPDATE':
            return self.update_user(data)
        elif instruction_type == 'USER_DELETE':
            return self.delete_user(data)
        elif instruction_type == 'USER_LIST':
            return self.list_users()
        elif instruction_type == 'USER_INSTRUCTION_RECORDING_ENABLE':
            return self.database_manage_unit.enable_instruction_recording(data['user_id'])
        elif instruction_type == 'USER_INSTRUCTION_RECORDING_DISABLE':
            return self.database_manage_unit.disable_instruction_recording(data['user_id'])
        elif instruction_type == 'USER_INSTRUCTION_RECORDS_DELETE':
            return self.database_manage_unit.delete_instruction_records(data['user_id'])
        elif instruction_type == 'USER_INSTRUCTION_RECORDS_LIST':
            return self.database_manage_unit.list_instruction_records(data['user_id'])
        # Handle other user-related instructions here...

    def create_user(self, data):
        try:
            existing_user = self.database_manage_unit.query_user_by_username(data['username'])
            if existing_user:
                return {"status": "error", "message": f"User {data['username']} already exists."}
            self.database_manage_unit.add_user(data['username'], data.get('profile'))
            return {"status": "success", "message": f"User {data['username']} created successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to create user {data['username']}. {str(e)}"}

    def update_user(self, data):
        try:
            user = self.database_manage_unit.query_user_by_id(data['user_id'])
            if not user:
                return {"status": "error", "message": f"User with id {data['user_id']} does not exist."}
            user.username = data.get('username', user.username)
            user.profile = data.get('profile', user.profile)
            self.database_manage_unit.commit_session()
            return {"status": "success", "message": f"User {data['user_id']} updated successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update user {data['user_id']}. {str(e)}"}

    def delete_user(self, data):
        try:
            user = self.database_manage_unit.query_user_by_id(data['user_id'])
            if not user:
                return {"status": "error", "message": f"User with id {data['user_id']} does not exist."}
            self.database_manage_unit.delete_user(user)
            return {"status": "success", "message": f"User {data['user_id']} deleted successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete user {data['user_id']}. {str(e)}"}

    def list_users(self):
        try:
            users = self.database_manage_unit.query_all_users()
            return {"status": "success", "users": [{"user_id": user.user_id, "username": user.username, "profile": user.profile} for user in users]}
        except Exception as e:
            return {"status": "error", "message": f"Failed to list users. {str(e)}"}