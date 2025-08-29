from pydantic import BaseModel
from google.adk.models.lite_llm import LiteLlm


class ModelConfig(BaseModel):
    litellm: bool = False
    model_id: str
    litellm_kwargs: dict = {}

    def get_model(self):
        if self.litellm:
            return LiteLlm(model=self.model_id, **self.litellm_kwargs)
        return self.model_id


class Config(BaseModel):
    doctor: ModelConfig = ModelConfig(model_id="gemini-2.5-flash")
    information_retriever: ModelConfig = ModelConfig(model_id="gemini-2.5-flash")
    drug_info: ModelConfig = ModelConfig(model_id="gemini-2.5-flash")
    regulator: ModelConfig = ModelConfig(model_id="gemini-2.5-flash")
    patient: ModelConfig = ModelConfig(model_id="gemini-2.5-flash")
    conversation_init: ModelConfig = ModelConfig(model_id="gemini-2.5-flash")


import yaml

config = Config.model_validate(yaml.safe_load(open("config.yaml")))
