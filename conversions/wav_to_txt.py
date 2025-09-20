# conversions/wav_to_txt.py

#imports importantes para o funcionamente
from openai import OpenAI
from dotenv import load_dotenv

# funcao principal a ser usada:
def transcrever_audio(caminho_arquivo_wav):
    load_dotenv()
    try:
        client = OpenAI()
        with open(caminho_arquivo_wav, "rb") as audio_file:
            transcricao = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="pt"
            )
        return transcricao.text
    except FileNotFoundError:
        return "Erro: o arquivo de audio nao foi encontrado."
    except Exception as e:
        return f"Ocorreu um erro durante a transcricao: {e}"


# para testes:
if __name__ == '__main__':
    import os

    ARQUIVO_PADRAO = "teste.wav"

    print("Teste do modulo 'wav_to_txt.py'")

    prompt = f"Digite o nome do arquivo (ou pressione Enter para usar '{ARQUIVO_PADRAO}'): "
    nome_do_arquivo_de_audio = input(prompt)

    # Se o usuario apenas pressionou Enter, a string sera vazia.
    if not nome_do_arquivo_de_audio:
        nome_do_arquivo_de_audio = ARQUIVO_PADRAO
        print(f"Nenhum arquivo inserido. Usando o padrao: {ARQUIVO_PADRAO}")


    diretorio_atual = os.path.dirname(__file__)
    pasta_raiz_do_projeto = os.path.dirname(diretorio_atual)
    caminho_do_audio_teste = os.path.join(pasta_raiz_do_projeto, "test_data", nome_do_arquivo_de_audio)


    # Verifica se o arquivo realmente existe
    if os.path.exists(caminho_do_audio_teste):
        print("\nArquivo de teste encontrado! Iniciando a transcricao...")
        
        resultado_teste = transcrever_audio(caminho_do_audio_teste)

        print("\n--- Resultado do Teste ---")
        print(resultado_teste)
        print("--------------------------")
    else:
        print("\nERRO: Arquivo de teste nao encontrado!")
        print("Por favor, verifique se:")
        print(f" O arquivo '{nome_do_arquivo_de_audio}' esta dentro desta pasta.")