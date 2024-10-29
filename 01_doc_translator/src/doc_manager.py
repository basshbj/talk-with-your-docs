from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat, AnalyzeResult

class DocumentManager:
  def __init__(self, endpoint: str, key: str):
    self.doc_client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))


  def analyze_doc_markdown(self, file_path: str) -> str:
    with open(file_path, "rb") as f:
      poller = self.doc_client.begin_analyze_document(
        "prebuilt-layout", 
        AnalyzeDocumentRequest(bytes_source=f.read()), 
        output_content_format=ContentFormat.MARKDOWN
      )
      
      result = poller.result()

    return result.content

  def analyze_doc_markdown_from_bytes(self, bytes_content: bytes) -> str:
    poller = self.doc_client.begin_analyze_document(
      "prebuilt-layout", 
      AnalyzeDocumentRequest(bytes_source=bytes_content), 
      output_content_format=ContentFormat.MARKDOWN
    )
    
    result = poller.result()

    return result.content

  def save_file(self, file_path: str, content: str):
    with open(file_path, "w", encoding="utf-8") as f:
      f.write(content)

  def analyze_doc_and_save(self, file_path: str, output_path: str):
    content = self.__analyze_doc_markdown(file_path)
    self.__save_file(output_path, content)