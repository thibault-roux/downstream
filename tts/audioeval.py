import torchaudio
import torch
from speechbrain.lobes.models.huggingface_wav2vec import HuggingFaceWav2Vec2



def load_wav(path):
    waveform, sample_rate = torchaudio.load(path)
    # Resample if needed
    target_sample_rate = 16000  # Wav2Vec 2.0's expected sample rate
    if sample_rate != target_sample_rate:
        resampler = torchaudio.transforms.Resample(sample_rate, target_sample_rate)
        waveform = resampler(waveform)
    # Ensure mono-channel (1 channel)
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)
    return waveform


def load_model():
    # HuggingFace model hub
    model_hub_w2v2 = "LeBenchmark/wav2vec2-FR-7K-large"
    model_w2v2 = HuggingFaceWav2Vec2(model_hub_w2v2, save_path='./save')
    # infer the features
    features = model_w2v2.forward(waveform)
    return features

if __name__ == "__main__":
    for i in range(10):
        waveform = load_wav("files/bfmtv" + str(i) + ".wav")
        features = load_model()
        print(features.shape)

