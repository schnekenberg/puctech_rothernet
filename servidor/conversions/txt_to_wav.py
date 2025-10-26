# conversions/txt_to_wav.py
from TTS.api import TTS

tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=False)

def text_to_wav_pt(text: str, output_path: str = "output.wav"):
    tts.tts_to_file(text=text, file_path=output_path, speaker="female", language="pt")
    return output_path
