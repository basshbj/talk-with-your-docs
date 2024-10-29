from typing import Any
from promptflow.tracing import trace
from promptflow.core import Prompty, AzureOpenAIModelConfiguration

class AIManager:
    def __init__(self, config: AzureOpenAIModelConfiguration, temperature: float = 0.5):
      override_prompt_config = {
        "configuration": config,
        "paramenters": {
          "temperature": temperature
        }
      }

      self.prompty = Prompty.load(
        source="01_doc_translator/prompts/translate_doc.prompty",
        override_model=override_prompt_config
      )

    @trace
    def __call__(self, *args: Any, **kwds: Any) -> str:
      """Chat Entry Point"""

      # Extract Arguments
      if not isinstance(args[0], str):
        raise ValueError("The first argument must be a string")
      
      language = args[0]

      # Extract Arguments
      if not isinstance(args[1], str):
        raise ValueError("The first argument must be a string")
      
      text_to_translate = args[1]

      output = self.prompty(
        language=language, 
        text_to_translate=text_to_translate
      )

      return output