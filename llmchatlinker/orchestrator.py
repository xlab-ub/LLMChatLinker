# llmchatlinker/orchestrator.py

import json
from .message_queue import publish_response, consume_messages, init_message_queue
from .units.control_unit import ControlUnit
from .units.user_manage_unit import UserManageUnit
from .units.chat_manage_unit import ChatManageUnit
from .units.llm_manage_unit import LLMManageUnit
from .units.database_manage_unit import DatabaseManageUnit

class Orchestrator:
    def __init__(self):
        self.instruction_channel, self.instruction_queue = init_message_queue(queue_name='instruction_queue')
        self.result_channel, self.result_queue = init_message_queue(queue_name='result_queue')
        self.database_manage_unit = DatabaseManageUnit()
        self.control_unit = ControlUnit(
            UserManageUnit(self.database_manage_unit),
            ChatManageUnit(self.database_manage_unit),
            LLMManageUnit(self.database_manage_unit),
            self.database_manage_unit
        )
        self.database_manage_unit.reset_db()

    def fetch_instruction(self, body, properties):
        instruction = json.loads(body)
        correlation_id = properties.correlation_id
        reply_to = properties.reply_to

        user_id = instruction['data'].get('user_id')
        if user_id:
            user = self.database_manage_unit.query_user_by_id(user_id)
            if user and user.record_instructions:
                self.database_manage_unit.record_instruction(user_id, instruction['data'].get('chat_id'), instruction['type'])

        result = self.control_unit.decode_and_execute_instruction(instruction)
        response_message = json.dumps(result)
        publish_response(self.result_channel, response_message, correlation_id, reply_to)

    def start(self):
        consume_messages(self.instruction_channel, self.instruction_queue, self.fetch_instruction)