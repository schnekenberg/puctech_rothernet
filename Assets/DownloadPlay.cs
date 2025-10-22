using UnityEngine;
using NativeWebSocket;
using UnityEngine.Networking;
using System.IO;
using System.Collections;

[RequireComponent(typeof(AudioSource))]
public class DownloadPlay : MonoBehaviour
{
    private WebSocket websocket;
    private AudioSource audioSource;
    private bool conectado = false;

    // Evento para avisar que a IA terminou de falar
    public delegate void InteracaoFinalizada();
    public event InteracaoFinalizada AoFinalizarInteracao;

    [System.Serializable]
    public class AudioMessage
    {
        public string audio;     // Áudio em base64
        public bool finished;    // Flag de encerramento da conversa
    }

    public void IniciarConexao()
    {
        if (conectado) return;
        conectado = true;

        audioSource = GetComponent<AudioSource>();
        websocket = new WebSocket("ws://servidor:porta");

        websocket.OnOpen += () =>
        {
            Debug.Log("Conexão WebSocket aberta.");
        };

        websocket.OnError += (e) =>
        {
            Debug.LogError(" Erro WebSocket: " + e);
        };

        websocket.OnClose += (e) =>
        {
            Debug.Log("Conexão WebSocket encerrada.");
        };

        websocket.OnMessage += (bytes) =>
        {

            string json = System.Text.Encoding.UTF8.GetString(bytes);
            AudioMessage mensagem = JsonUtility.FromJson<AudioMessage>(json);

            byte[] audioBytes = System.Convert.FromBase64String(mensagem.audio);
            string audioPath = Path.Combine(Application.persistentDataPath, "audioRecebido.wav");

            File.WriteAllBytes(audioPath, audioBytes);
            Debug.Log(" Áudio recebido e salvo em: " + audioPath);

            StartCoroutine(TocarAudio(audioPath, mensagem.finished));
        };

        websocket.Connect();
    }

    private IEnumerator TocarAudio(string path, bool finished)
    {
        string uri = "file://" + path;
        using (UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip(uri, AudioType.WAV))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Erro ao carregar áudio: " + www.error);
            }
            else
            {
                AudioClip clip = DownloadHandlerAudioClip.GetContent(www);
                audioSource.clip = clip;
                audioSource.Play();
                Debug.Log("Reproduzindo áudio...");

                // Espera o áudio terminar antes de liberar nova gravação
                yield return new WaitForSeconds(clip.length);

                if (finished)
                {
                    Debug.Log(" Interação encerrada pelo servidor.");
                    AoFinalizarInteracao?.Invoke();
                }
            }
        }
    }

    private void Update()
    {
#if !UNITY_WEBGL || UNITY_EDITOR
        websocket?.DispatchMessageQueue();
#endif
    }

    private async void OnDestroy()
    {
        if (websocket != null)
            await websocket.Close();
    }
}
