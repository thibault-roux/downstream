from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
from scipy.io.wavfile import write

models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
    "facebook/tts_transformer-fr-cv7_css10",
    arg_overrides={"vocoder": "hifigan", "fp16": False}
)
model = models[0]
TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)
generator = task.build_generator(model, cfg)

text = "Bonjour, ceci est un test."

sample = TTSHubInterface.get_model_input(task, text)
wav, rate = TTSHubInterface.get_prediction(task, model, generator, sample)

# Save the audio file using scipy
write("output.wav", rate, wav)
