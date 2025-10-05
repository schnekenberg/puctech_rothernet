using UnityEngine;
using NativeWebSocket;
using System.IO;

public class UploadDoAudio : MonoBehaviour
{
    WebSocket websocket;

    public async void UploadWav(string path)
    {
        websocket = new WebSocket("wss://servidor.com/audio");

        websocket.OnOpen += async () =>
        {
            Debug.Log("Conectado!");

            if (File.Exists(path))
            {
                byte[] wavBytes = File.ReadAllBytes(path);
                await websocket.Send(wavBytes);
                Debug.Log("Áudio enviado com sucesso.");
            }
            else
            {
                Debug.LogError("Arquivo WAV não encontrado: " + path);
            }
        };

        websocket.OnError += (e) => Debug.Log("Erro: " + e);
        websocket.OnClose += (e) => Debug.Log("Desconectado.");

        await websocket.Connect();
    }
}