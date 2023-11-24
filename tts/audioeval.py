import torchaudio
import torch
# Load audio file
audio_file = "files/bfmtv0.wav"
waveform, sample_rate = torchaudio.load(audio_file)
# Resample if needed
target_sample_rate = 16000  # Wav2Vec 2.0's expected sample rate
if sample_rate != target_sample_rate:
    resampler = torchaudio.transforms.Resample(sample_rate, target_sample_rate)
    waveform = resampler(waveform)
# Ensure mono-channel (1 channel)
if waveform.shape[0] > 1:
    waveform = torch.mean(waveform, dim=0, keepdim=True)

# from transformers import Wav2Vec2Processor, Wav2Vec2Model

# model_name = "LeBenchmark/wav2vec2-FR-7K-large"
# processor = Wav2Vec2Processor.from_pretrained(model_name)
# model = Wav2Vec2Model.from_pretrained(model_name)
# inputs = processor(waveform.squeeze().numpy(), return_tensors="pt", padding="longest")
# with torch.no_grad():
#     embeddings = model(**inputs).last_hidden_state
# print(embeddings)
# print(embeddings.shape)




from speechbrain.lobes.models.huggingface_wav2vec import HuggingFaceWav2Vec2

# HuggingFace model hub
model_hub_w2v2 = "LeBenchmark/wav2vec2-FR-7K-large"

model_w2v2 = HuggingFaceWav2Vec2(model_hub_w2v2, save_path='./save')

# infer the features
features = model_w2v2.forward(waveform)
print(features)
print(features.shape)


