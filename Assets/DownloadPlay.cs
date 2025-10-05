using UnityEngine;
using NativeWebSocket;
using UnityEngine.Networking;
using System.IO;
using System.Collections;

[RequireComponent(typeof(AudioSource))]
public class DownloadPlay : MonoBehaviour
{
    private WebSocket websocket;
    private string audioPath;
    private AudioSource audioSource;
    private bool conectado = false;

    public void IniciarConexao()
    {
        if (conectado) return;
        conectado = true;

        audioPath = Path.Combine(Application.persistentDataPath, "audioRecebido.wav");
        audioSource = GetComponent<AudioSource>();

        websocket = new WebSocket("ws://SEU_SERVIDOR:PORTA");

        websocket.OnOpen += () =>
        {
            Debug.Log("Conexão WebSocket aberta.");
        };

        websocket.OnError += (e) =>
        {
            Debug.LogError("Erro WebSocket: " + e);
        };

        websocket.OnClose += (e) =>
        {
            Debug.Log("Conexão WebSocket encerrada.");
        };

        websocket.OnMessage += (bytes) =>
        {
            File.WriteAllBytes(audioPath, bytes);
            Debug.Log("Áudio recebido e salvo em: " + audioPath);
            StartCoroutine(TocarAudio());
        };

        websocket.Connect();
    }

    private IEnumerator TocarAudio()
    {
        string uri = "file://" + audioPath;
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
