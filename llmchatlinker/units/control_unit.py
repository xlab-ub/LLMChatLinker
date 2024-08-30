# llmchatlinker/units/control_unit.py

class ControlUnit:
    def __init__(self, user_manage_unit, chat_manage_unit, llm_manage_unit, database_manage_unit):
        self.user_manage_unit = user_manage_unit
        self.chat_manage_unit = chat_manage_unit
        self.llm_manage_unit = llm_manage_unit
        self.database_manage_unit = database_manage_unit

    def decode_and_execute_instruction(self, instruction):
        instruction_type = instruction['type']
        data = instruction['data']
        
        if instruction_type.startswith('USER_'):
            return self.user_manage_unit.handle_instruction(instruction_type, data)
        elif instruction_type.startswith('CHAT_'):
            return self.chat_manage_unit.handle_instruction(instruction_type, data)
        elif instruction_type.startswith('LLM_'):
            return self.llm_manage_unit.handle_instruction(instruction_type, data)
        elif instruction_type.startswith('INSTRUCTION_'):
            return self.database_manage_unit.handle_instruction(instruction_type, data)
        else:
            return {"error": "Unknown instruction type"}