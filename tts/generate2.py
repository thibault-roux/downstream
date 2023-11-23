import torch
from TTS.api import TTS


# Init TTS with the target model name
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False).to(device)

# Run TTS
tts.tts_to_file("C'est le clonage de la voix.", language="fr-fr", file_path="files/techno.wav")