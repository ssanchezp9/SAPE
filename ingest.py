from src.utils.rag.document_ingestor import DocumentIngestor
# Ingestar documentos
ingestor = DocumentIngestor()
metadata =  {"asignatura": "Filosofía", "tema": "Sócrates y los sofistas", "nivel": "Bachillerato", "curso": "1", "source": "tema15_filo_socrates_bach1.docx"}
# Realizar la ingesta del documento
ingestor.ingest(r"C:\Users\ssanc\Documents\SAPE\DOCUMENTOS_RAG\tema15_filo_socrates_bach1.docx", metadata)
