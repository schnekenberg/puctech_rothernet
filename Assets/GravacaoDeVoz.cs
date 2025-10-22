using UnityEngine;
using UnityEngine.InputSystem;
using System.IO;

[RequireComponent(typeof(UploadDoAudio))]
public class GravacaoDeVoz : MonoBehaviour
{
    public InputActionProperty recordButton;
    private AudioClip audioGravado;
    private UploadDoAudio upload;
    private bool gravando = false;
    private string microphoneName;
    private bool aguardandoResposta = false;

    void Start()
    {
        upload = GetComponent<UploadDoAudio>();

        if (Microphone.devices.Length > 0)
        {
            microphoneName = Microphone.devices[0];
            Debug.Log("Usando microfone: " + microphoneName);
        }
        else
        {
            Debug.LogError("Microfone não encontrado");
        }

        // Conecta ao DownloadPlay e escuta o fim da resposta da IA
        DownloadPlay receiver = FindObjectOfType<DownloadPlay>();
        if (receiver != null)
        {
            receiver.AoFinalizarInteracao -= PermitirNovaGravacao; // evitar duplicação
            receiver.AoFinalizarInteracao += PermitirNovaGravacao;
        }
    }

    void OnEnable()
    {
        recordButton.action.Enable();
        recordButton.action.performed += AlternarGravacao;
    }

    void OnDisable()
    {
        recordButton.action.performed -= AlternarGravacao;
        recordButton.action.Disable();
    }

    public void AlternarGravacao(InputAction.CallbackContext ctx)
    {
        if (aguardandoResposta)
        {
            Debug.Log("Aguardando resposta da IA...");
        }
        else
        {
            if (!gravando)
            {
                audioGravado = Microphone.Start(microphoneName, false, 300, 44100);
                Debug.Log("Gravação iniciada...");
                gravando = true;
            }
            else
            {
                Microphone.End(microphoneName);
                SaveWav("Pedido.wav", audioGravado);
                string path = Path.Combine(Application.persistentDataPath, "Pedido.wav");

                upload.UploadWav(path);
                Debug.Log("Gravação finalizada e enviada.");

                gravando = false;
                aguardandoResposta = true;

                DownloadPlay receiver = FindObjectOfType<DownloadPlay>();
                if (receiver != null)
                {
                    receiver.IniciarConexao();
                }
            }
        }
    }

    private void PermitirNovaGravacao()
    {
        Debug.Log("IA terminou de falar. Você pode gravar novamente.");
        aguardandoResposta = false;
    }

    public static void SaveWav(string filename, AudioClip clip)
    {
        if (!filename.ToLower().EndsWith(".wav"))
            filename += ".wav";

        string filepath = Path.Combine(Application.persistentDataPath, filename);
        Directory.CreateDirectory(Path.GetDirectoryName(filepath));

        using (FileStream fileStream = new FileStream(filepath, FileMode.Create))
        {
            int sampleCount = clip.samples * clip.channels;
            float[] samples = new float[sampleCount];
            clip.GetData(samples, 0);

            byte[] wavData = ConvertToWav(samples, clip.channels, clip.frequency);
            fileStream.Write(wavData, 0, wavData.Length);
        }
    }

    private static byte[] ConvertToWav(float[] samples, int channels, int sampleRate)
    {
        MemoryStream stream = new MemoryStream();
        using (BinaryWriter writer = new BinaryWriter(stream))
        {
            int byteRate = sampleRate * channels * 2;
            short blockAlign = (short)(channels * 2);
            int subChunk2Size = samples.Length * 2;
            int chunkSize = 36 + subChunk2Size;

            writer.Write(System.Text.Encoding.UTF8.GetBytes("RIFF"));
            writer.Write(chunkSize);
            writer.Write(System.Text.Encoding.UTF8.GetBytes("WAVE"));
            writer.Write(System.Text.Encoding.UTF8.GetBytes("fmt "));
            writer.Write(16);
            writer.Write((short)1);
            writer.Write((short)channels);
            writer.Write(sampleRate);
            writer.Write(byteRate);
            writer.Write(blockAlign);
            writer.Write((short)16);
            writer.Write(System.Text.Encoding.UTF8.GetBytes("data"));
            writer.Write(subChunk2Size);

            foreach (float s in samples)
            {
                short val = (short)(s * short.MaxValue);
                writer.Write(val);
            }
        }

        return stream.ToArray();
    }
}
