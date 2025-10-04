from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader # utilizado para padronizar documentos como .pdf
from langchain.text_splitter import RecursiveCharacterTextSplitter # utilizado para separar os dados dos documentos (texto) em chunks
from langchain.schema import Document # utilizado para criar Document a partir dos dados
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai
import os
import re
import shutil # utilizados para operações com documentos
from dotenv import load_dotenv

# carrega variáveis de ambiente (no .env), ou seja, a chave API da OpenAI
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

DOCUMENTOS_CAMINHO = "documentos"
CHROMA_CAMINHO = "chroma"

def main():
    gerar_data_store()

def gerar_data_store():
    documentos = carregar_documentos()
    chunks = separar_texto(documentos) # separamos em chunks para consultas mais precisas e por escalabilidade
    salvar_no_chroma(chunks)

def carregar_documentos():
    loader = DirectoryLoader(DOCUMENTOS_CAMINHO, glob = "*.pdf", loader_cls = UnstructuredPDFLoader, loader_kwargs = {"language": "pt"})
    documentos = loader.load()

    documentos_finais = [] # vamos caçar o documento do cardápio para dividir seus chunks de modo específico
    for doc in documentos:
        if "manual_cardapio" in doc.metadata["source"].lower(): # é possível acessas fontes e metadata do documentos utilizados
            documentos_finais.extend(carregar_cardapio(doc))
        else:
            documentos_finais.append(doc)

    return documentos_finais

def carregar_cardapio(doc: Document):
    texto = doc.page_content
    chunks = re.split(r"(?=ID:\s*\d{2})", texto) # padrão que divide antes de cada ocorrência de um ID

    documentos = []
    for bloco in chunks:
        bloco = bloco.strip()
        if not bloco:
            continue # ignora blocos vazios
        documentos.append(Document(page_content = bloco, metadata = {"source": "manual_cardapio"}))

    return documentos

def separar_texto(documentos: list[Document]):
    separador = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50,
        length_function = len,
        add_start_index = True
    )

    chunks = []
    for doc in documentos:
        if doc.metadata.get("source") == "manual_cardapio":
            chunks.append(doc) # como já dividimos em chunks, basta adicionar na lista
        else:
            chunks.extend(separador.split_documents([doc]))

    #chunks = separador.split_documents(documentos)
    print(f"Didiviu {len(documentos)} documento(s) em {len(chunks)} chunks.") # teste

    # visualização dos chunks
    documentos = chunks
    for doc in documentos:
        print(doc.page_content)
        print(doc.metadata)

    return chunks

def salvar_no_chroma(chunks: list[Document]):
    # limpa a database caso já tenha alguma coisa armazenada
    if os.path.exists(CHROMA_CAMINHO):
        shutil.rmtree(CHROMA_CAMINHO)

    # criar uma DB a partir dos documentos
    _ = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory = CHROMA_CAMINHO
    )

    print(f"Salvou {len(chunks)} chunks em {CHROMA_CAMINHO}.")

if __name__ == "__main__":
    main()
