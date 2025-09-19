# conversions/wav_to_txt.py

# so e necessario importar os para os testes
import os
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

# Para testes:
if __name__ == '__main__':
    caminho_teste = "digite_o_nome_do_arquivo.wav" 

    if os.path.exists(caminho_teste):
        print(f"Testando a funcao com o arquivo: {caminho_teste}")
        resultado_teste = transcrever_audio(caminho_teste)
        
        print("\n--- Resultado do Teste ---")
        print(resultado_teste)
        print("--------------------------")
    else:
        print(f"\nAVISO: Arquivo de teste '{caminho_teste}' nao encontrado.  :(")