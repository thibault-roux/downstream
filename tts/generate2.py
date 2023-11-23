import torch
from TTS.api import TTS

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Init TTS with the target model name
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
tts.tts_to_file("C'est le clonage de la voix.", speaker_wav="files/bfm.wav", language="fr-fr", file_path="files/techno.wav")