import os
import gradio as gr

from dotenv import load_dotenv
from promptflow.core import AzureOpenAIModelConfiguration
from src.doc_manager import DocumentManager
from src.ai_manager import AIManager


# --- Init Environment ---
load_dotenv()

DOC_MANAGER = None
AI_MANAGER = None

def init_enviroment():
  global DOC_MANAGER, AI_MANAGER  # Declare as global

  model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_key=os.getenv("AOAI_API_KEY"),
    api_version=os.getenv("AOAI_API_VERSION"),
    azure_deployment=os.getenv("AOAI_DEPLOYMENT")
  )

  DOC_MANAGER = DocumentManager(os.getenv("DOC_AI_ENDPOINT"), os.getenv("DOC_AI_API_KEY"))
  AI_MANAGER = AIManager(config=model_config, temperature=0.7)


# --- Gradio Functions ---
def process_file_as_binary(value: bytes) -> str:
  markdown_content = DOC_MANAGER.analyze_doc_markdown_from_bytes(value)

  return markdown_content

def translate_document(lang: str, value: str) -> str:
  translation = AI_MANAGER(lang, value)

  return translation

# --- Gradio UI ---s
with gr.Blocks(theme=gr.themes.Soft()) as demo:
  init_enviroment()

  gr.Markdown("# Document Translator")

  # --- Inputs ---
  with gr.Row():
    with gr.Column(scale=1):
      gr.Markdown("## File Upload")

      file_upload = gr.File(
        label="Allowed File Types: pdf, docx, txt",
        file_count='single',
        file_types=['pdf', 'docx', 'txt'],
        type='binary'
      )

    with gr.Column(scale=1):
      gr.Markdown("## Translation")

      lang_select = gr.Radio(
        label="Select Language",
        choices=["English", "Spanish", "Japanese"],
        value="English"
      )

  with gr.Row():
    btn_file_upload = gr.Button("Upload File", variant="primary")
    btn_translate   = gr.Button("Translate", variant="primary")

  # --- Outputs ---
  with gr.Row():
    with gr.Column(scale=1):
      gr.Markdown("## Content Preview")

      content_preview = gr.Markdown(
        value="", 
        container=True,
        min_height=300,
        max_height=800
      )

    with gr.Column(scale=1):
      gr.Markdown("## Translation Preview")

      translation_preview = gr.Markdown(
        value="", 
        container=True,
        min_height=300,
        max_height=800
      )


  # --- Event Handlers ---
  btn_file_upload.click(
    fn=process_file_as_binary, 
    inputs=file_upload, 
    outputs=content_preview,
    show_progress=True
  )
  
  btn_translate.click(
    fn=translate_document, 
    inputs=[lang_select, content_preview], 
    outputs=translation_preview, 
    show_progress=True
  )

# --- Main Function ---
if __name__ == "__main__":  
  demo.launch()