# Hindi Voice Lab

Generate identical Hindi male narration samples for a fair listening comparison.

## Quick ₹0 comparison (lightweight)
```bash
cd backend
python -m pip install -r requirements.txt
python voice_test.py --output ../output/voice-comparison
```

Outputs: Edge Neural Madhur, eSpeak offline baseline, exact shared script, and a JSON report.

## Optional local open-source neural voice
```bash
python -m pip install -r requirements-parler.txt
python voice_test.py --engines edge,parler,espeak --output ../output/voice-comparison
```
Indic Parler-TTS uses the recommended Hindi male speaker Rohit and a natural conversational delivery prompt. It is a roughly 0.9B parameter model, so it may require substantial RAM/VRAM and can be slow on CPU. No hosted inference or paid API is used.

## Default selection
The production default remains Edge Neural Madhur until actual listening confirms an alternative is better. File size, duration, and loudness cannot objectively determine naturalness. A Hindi listener should compare the clips on the same phone/headphones before switching the default. Edge is an online third-party service; free access is not a guarantee of unlimited use.
