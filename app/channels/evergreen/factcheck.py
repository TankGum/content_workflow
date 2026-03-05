from app.services.llm import LLMService
import json

class EvergreenFactCheck:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def verify(self, script, source_data):
        prompt = f"""
        Act as a scientist or expert researcher. Verify these claims against the source data.
        Script: {json.dumps(script)}
        Source Data: {source_data}
        
        Return JSON format:
        {{
            "accurate": bool,
            "errors": ["list of errors if any"],
            "corrected_script": "if errors, suggest fix"
        }}
        """
        response = self.llm.generate_json(prompt)
        return json.loads(response)
