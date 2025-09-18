import argparse
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# carrega variáveis de ambiente (no .env), ou seja, a chave API da OpenAI
load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]

CHROMA_CAMINHO = "chroma"

TEMPLATE_PROMPT = """
Dê uma resposta baseando-se somente no contexto a seguir:

{contexto}

---

Dê uma resposta baseada no contexto acima: {pergunta}
"""

def main():
    # CLI; receberá os textos da interações com o usuário, convertidos a partir da mensagem por voz
    parser = argparse.ArgumentParser()
    parser.add_argument("texto_query", type = str, nargs = "?", help = "o texto query")
    args = parser.parse_args()
    if args.texto_query:
        texto_query = args.texto_query
    else:
        texto_query = input("Digite sua pergunta: ")

    # preparar a DB
    funcao_embedding = OpenAIEmbeddings()
    db = Chroma(persist_directory = CHROMA_CAMINHO, embedding_function = funcao_embedding)

    # faz a busca por similaridades na database
    resultados_busca = db.similarity_search_with_relevance_scores(texto_query, k = 3)
    if len(resultados_busca) == 0 or resultados_busca[0][1] < 0.7:
        print(f"Não foi possível encontrar resultados.")
        return

    texto_contexto = "\n\n---\n\n".join([doc.page_content for doc, _score in resultados_busca])
    template_prompt = ChatPromptTemplate.from_template(TEMPLATE_PROMPT)
    
    mensagens = template_prompt.format_messages(
        contexto = texto_contexto,
        pergunta = texto_query
    )

    modelo = ChatOpenAI(model = "gpt-4o-mini")
    resposta = modelo.invoke(mensagens)


    print(resposta.content)

if __name__ == "__main__":
    main()



