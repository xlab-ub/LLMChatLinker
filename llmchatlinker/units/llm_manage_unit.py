# llmchatlinker/units/llm_manage_unit.py

import requests

class LLMManageUnit:
    def __init__(self, database_manage_unit):
        self.database_manage_unit = database_manage_unit

    def handle_instruction(self, instruction_type, data):
        if instruction_type == 'LLM_PROVIDER_ADD':
            return self.add_llm_provider(data)
        elif instruction_type == 'LLM_PROVIDER_UPDATE':
            return self.update_llm_provider(data)
        elif instruction_type == 'LLM_PROVIDER_DELETE':
            return self.delete_llm_provider(data)
        elif instruction_type == 'LLM_PROVIDER_LIST':
            return self.list_llm_providers()
        elif instruction_type == 'LLM_ADD':
            return self.add_llm(data)
        elif instruction_type == 'LLM_UPDATE':
            return self.update_llm(data)
        elif instruction_type == 'LLM_DELETE':
            return self.delete_llm(data)
        elif instruction_type == 'LLM_LIST':
            return self.list_llms()
        elif instruction_type == 'LLM_RESPONSE_GENERATE':
            return self.generate_llm_response(data)
        elif instruction_type == 'LLM_RESPONSE_REGENERATE':
            return self.regenerate_llm_response(data)
        # Handle other LLM-related instructions here...

    def add_llm_provider(self, data):
        try:
            self.database_manage_unit.add_provider(data['name'], data['api_endpoint'])
            return {"status": "success", "message": f"Provider {data['name']} added successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to add provider {data['name']}. {str(e)}"}

    def update_llm_provider(self, data):
        try:
            provider = self.database_manage_unit.query_provider_by_id(data['provider_id'])
            if not provider:
                return {"status": "error", "message": f"Provider with id {data['provider_id']} does not exist."}
            provider.name = data.get('name', provider.name)
            provider.api_endpoint = data.get('api_endpoint', provider.api_endpoint)
            self.database_manage_unit.commit_session()
            return {"status": "success", "message": f"Provider {data['provider_id']} updated successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update provider {data['provider_id']}. {str(e)}"}

    def delete_llm_provider(self, data):
        try:
            provider = self.database_manage_unit.query_provider_by_id(data['provider_id'])
            if not provider:
                return {"status": "error", "message": f"Provider with id {data['provider_id']} does not exist."}
            self.database_manage_unit.delete_provider(provider)
            return {"status": "success", "message": f"Provider {data['provider_id']} deleted successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete provider {data['provider_id']}. {str(e)}"}
    
    def list_llm_providers(self):
        try:
            providers = self.database_manage_unit.query_all_providers()
            return {"status": "success", "providers": [{"provider_id": provider.provider_id, "name": provider.name, "api_endpoint": provider.api_endpoint} for provider in providers]}
        except Exception as e:
            return {"status": "error", "message": f"Failed to list providers. {str(e)}"}

    def add_llm(self, data):
        try:
            provider = self.database_manage_unit.query_provider_by_name(data['provider_name'])
            if not provider:
                return {"status": "error", "message": "Invalid provider name."}
            self.database_manage_unit.add_llm(data['llm_name'], provider.provider_id)
            return {"status": "success", "message": f"LLM {data['llm_name']} added successfully under provider {data['provider_name']}."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to add LLM {data['llm_name']}. {str(e)}"}

    def update_llm(self, data):
        try:
            llm = self.database_manage_unit.query_llm_by_id(data['llm_id'])
            if not llm:
                return {"status": "error", "message": f"LLM with id {data['llm_id']} does not exist."}
            llm.name = data.get('llm_name', llm.name)
            self.database_manage_unit.commit_session()
            return {"status": "success", "message": f"LLM {data['llm_id']} updated successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update LLM {data['llm_id']}. {str(e)}"}

    def delete_llm(self, data):
        try:
            llm = self.database_manage_unit.query_llm_by_id(data['llm_id'])
            if not llm:
                return {"status": "error", "message": f"LLM with id {data['llm_id']} does not exist."}
            self.database_manage_unit.delete_llm(llm)
            return {"status": "success", "message": f"LLM {data['llm_id']} deleted successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete LLM {data['llm_id']}. {str(e)}"}

    def list_llms(self):
        try:
            llms = self.database_manage_unit.query_all_llms()
            return {"status": "success", "llms": [{"llm_id": llm.llm_id, "name": llm.name, "provider_id": llm.provider_id} for llm in llms]}
        except Exception as e:
            return {"status": "error", "message": f"Failed to list LLMs. {str(e)}"}

    def generate_llm_response(self, data):
        try:
            provider = self.database_manage_unit.query_provider_by_name(data['provider_name'])
            if not provider:
                return {"status": "error", "message": "Invalid provider name."}

            llm = self.database_manage_unit.query_llm_by_name_and_provider(data['llm_name'], provider.provider_id)
            if not llm:
                return {"status": "error", "message": "Invalid LLM name."}

            formatted_messages = [{"role": "user", "content": data['user_input']}]
            response = requests.post(provider.api_endpoint, headers={"Content-Type": "application/json"}, json={"model": llm.name, "messages": formatted_messages})
            response.raise_for_status()
            response_data = response.json()

            user_message_id = self.database_manage_unit.add_message(data['chat_id'], data['user_id'], data['user_input'], 'user')
            llm_response_id = self.database_manage_unit.add_message(data['chat_id'], data['user_id'], response_data['choices'][0]['message']['content'], 'assistant', llm.llm_id)

            return {"status": "success", "message_id": llm_response_id, "message": response_data['choices'][0]['message']['content']}
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}

    def regenerate_llm_response(self, data):
        try:
            # Fetch the original user message
            original_message = self.database_manage_unit.query_message_by_id(data['message_id'])
            if not original_message:
                return {"status": "error", "message": "Original message not found."}

            # Check if the message has an associated LLM
            if not original_message.llm_id:
                return {"status": "error", "message": "Message does not have an associated LLM."}

            # Fetch provider and LLM details
            llm = original_message.llm
            if not llm:
                return {"status": "error", "message": "LLM not found for the message."}

            provider = llm.provider
            if not provider:
                return {"status": "error", "message": "Provider not found for the LLM."}

            # Format the input for the LLM
            formatted_messages = [{"role": "user", "content": original_message.content}]
            response = requests.post(
                provider.api_endpoint,
                headers={"Content-Type": "application/json"},
                json={
                    "model": llm.name,
                    "messages": formatted_messages
                }
            )
            response.raise_for_status()
            response_data = response.json()

            # Store the regenerated response
            regenerated_response = self.database_manage_unit.add_message(
                original_message.chat_id,
                original_message.user_id,
                response_data['choices'][0]['message']['content'],
                'assistant',
                llm.llm_id
            )

            return {
                "status": "success",
                "message_id": regenerated_response,
                "message": response_data['choices'][0]['message']['content']
            }
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}
        except Exception as e:
            return {"status": "error", "message": str(e)}