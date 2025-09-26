import argparse
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from memoria import MemoriaConversa
import os

# carrega variáveis de ambiente (no .env), ou seja, a chave API da OpenAI
load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]

CHROMA_CAMINHO = "chroma"

TEMPLATE_PROMPT = """
Você é um atendente virtual do restaurante Limpinho.
Siga SOMENTE as regras do manual/documentos e cardápio fornecidos, sem inventar nada.

Manual/documentos e cardápio:
{contexto}

Histórico da conversa até agora:
{historico}

Pergunta do cliente:
{pergunta}

Você deve responder a pergunta do cliente utilizando somente e apenas o contexto de conhecimento apresentado e o histórico da conversa, seguindo as regras fornecidas nos documentos e também as a seguir:

1 - Nunca liste, mencione, invente ou dê sugestões de pratos que não estão registrados no cardápio dos documentos fornecidos
1.1 - Não importa se você pode pensar em um prato que atenda a alguma requisição do pedido; você deve se basear somente nos pratos fornecidos nos documentos
2 - Após a confirmação de um pedido, nunca ofereça outra opção para o cliente, e nunca pergunte se ele quer mais alguma coisa, pois cada cliente só pode fazer um pedido por atendimento
3 - Sempre ao confirmar um prato, repetir seu nome e ID, independentemente do modo que o usuário o identificou (somente nome ou somente ID)
4 - A interação deve seguir o formato: (1) Identificação -> (2) Pedido -> (3) Confirmação -> (4) Pagamento -> (5) Encerramento
4.1 - Você nunca deve repetir uma etapa após ser realizada (exemplo: fazer a identificação do usuário mais de uma vez fazer confirmação do pedido após o pagamento)
5 - Sempre que perguntar a forma de pagamento, informar o preço do prato.
5.1 - Após o cliente informar a forma de pagamento, partir para o encerramento do atendimento.
6 - Informar nome, ID, descrição e preço de cada prato baseando-se somente nos seus registros no cardápio fornecido a você
7 - Quando o usuário pedir para listar todos os pratos, responder exatamente com: "Nossos cardápio contém uma Salada Fresca da Casa, Sopa de Legumes, Espaguete ao Molho de Tomate, Risoto de Frango com Queijo, Estrogonofe de Carne, Pizza de Margherita e Feijão tropeiro."
8 - Quando o usuário pedir para listar os pratos veganos, responder exatamente com "Nossos pratos veganos são a Salada Fresca da Casa e a Sopa de Legumes."
9 - Quando o usuário pedir para listar os pratos sem lactose, responder exatamente com "Nossos pratos veganos são a Salada Fresca da Casa, a Sopa de Legumes, o Espaguete ao Molho de Tomate e o Feijão tropeiro."
"""


def main():
    # CLI; receberá os textos da interações com o usuário, convertidos a partir da mensagem por voz
    parser = argparse.ArgumentParser()
    parser.add_argument("texto_query", type = str, nargs = "?", help = "o texto query")

    # preparar a DB
    funcao_embedding = OpenAIEmbeddings()
    db = Chroma(persist_directory = CHROMA_CAMINHO, embedding_function = funcao_embedding)

    memoria = MemoriaConversa()
    modelo = ChatOpenAI(model = "gpt-4o-mini")
    template_prompt = ChatPromptTemplate.from_template(TEMPLATE_PROMPT)

    # testagem do agente em "conversa"
    while True:
        texto_query = input("**Cliente:** ").strip()
        if texto_query.lower() in ["sair"]:
            print("**Agente virtual:** Volte sempre!")
            break

        # faz a busca por similaridades na database
        resultados_busca = db.similarity_search_with_relevance_scores(texto_query, k = 3)
        if len(resultados_busca) == 0 or resultados_busca[0][1] < 0.7:
            resposta_fallback = "Desculpe, não consegui entender. Pode reformular?"
            print("**Agente virtual:** " + resposta_fallback)
            memoria.adicionar(usuario = texto_query, agente = resposta_fallback)
            continue

        texto_contexto = "\n\n---\n\n".join([doc.page_content for doc, _score in resultados_busca])

        mensagens = template_prompt.format_messages(
            contexto = texto_contexto,
            historico = memoria.obter_historico(),
            pergunta = texto_query
        )

        resposta = modelo.invoke(mensagens)

        print("**Agente virtual:** " + resposta.content)

        # atualizar memória
        memoria.adicionar(usuario = texto_query, agente = resposta.content)

if __name__ == "__main__":
    main()


# diminuir/compactar o tamanho do contexto
