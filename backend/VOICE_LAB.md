# Hindi Voice Lab — zero-budget test

All engines receive the exact same Devanagari sample and male voice selection where available.

## Quick CPU-friendly comparison
```bash
cd backend
python -m pip install -r requirements.txt
python -m pip install -r requirements-tiny.txt
python voice_test.py --engines edge,tiny,espeak --output ../output/voice-comparison
```
Indic Tiny TTS is 22.5M parameters, has a male Hindi voice, runs on CPU, and its model card provides an ONNX Runtime path. Its licence requires attribution (CC-BY-4.0 weights; MIT code; vocoder MIT). It is a calm reading voice, not a high-emotion actor voice.

## Optional heavyweight comparisons
- **Maya 2 Native**: use Python 3.10–3.12, Linux and supported NVIDIA CUDA 12.8 GPU. Model is 2.5B parameters, about 5 GB BF16 weights, and reference docs report around 9.2 GB loading peak. Test uses Hindi male persona Abhay. Install using the upstream instructions: https://github.com/MayaResearch/maya2-native
- **Indic Parler-TTS**: see requirements-parler.txt; heavyweight model.
- **IndicF5**: needs a permitted male reference WAV and exact transcript; Hugging Face requires accepting model access conditions. It is not auto-run until a reference clip and access are provided.
- **Indic-Speak**: 3B parameter model; no hosted inference provider is listed on its model card. Treat as a future self-hosted candidate, not a lightweight CI job.

Run heavy engines explicitly when hardware/dependencies are ready:
```bash
python voice_test.py --engines edge,tiny,maya,parler,espeak
```

The default comparison is Edge + Tiny + eSpeak. GitHub Actions uses a CPU runner, so Maya is correctly marked unavailable there rather than silently substituting a different engine. No audio metric can determine which voice sounds most natural: listen to the generated clips before changing production default. Edge Madhur remains production default until a human listening test selects a winner.
