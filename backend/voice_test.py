#!/usr/bin/env python3
"""Same-script Hindi male voice comparison. Edge Neural + eSpeak baseline; optional Indic Parler."""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from pathlib import Path

SAMPLE = """नमस्कार दोस्तों। आज की कहानी एक छोटे से गाँव की है, जहाँ आरव नाम का एक लड़का रहता था। एक रात उसे आसमान में नीली रोशनी दिखाई दी। वह धीरे-धीरे जंगल की ओर बढ़ा, लेकिन उसके कदमों में डर नहीं, बल्कि जिज्ञासा थी। अचानक पेड़ों के पीछे से एक आवाज़ आई—आरव, क्या तुम मेरी मदद करोगे? आरव ने गहरी साँस ली और बोला, हाँ, मैं तुम्हारी मदद ज़रूर करूँगा।"""

def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)

def duration(path):
    r=run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(path)])
    return float(r.stdout.strip())

def edge(out):
    exe=shutil.which("edge-tts")
    if not exe: raise RuntimeError("Install edge-tts from backend/requirements.txt")
    run([exe,"--voice","hi-IN-MadhurNeural","--rate","+0%","--text",SAMPLE,"--write-media",str(out)])

def espeak(out):
    exe=shutil.which("espeak-ng") or shutil.which("espeak")
    if not exe: raise RuntimeError("eSpeak not installed")
    wav=out.with_suffix(".wav")
    run([exe,"-v","hi","-s","145","-w",str(wav),SAMPLE])
    run(["ffmpeg","-y","-loglevel","error","-i",str(wav),str(out)])
    wav.unlink(missing_ok=True)

def parler(out):
    try:
        import torch, soundfile as sf
        from parler_tts import ParlerTTSForConditionalGeneration
        from transformers import AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("Optional model: pip install -r requirements-parler.txt") from exc
    model_id="ai4bharat/indic-parler-tts"
    device="cuda:0" if torch.cuda.is_available() else "cpu"
    model=ParlerTTSForConditionalGeneration.from_pretrained(model_id).to(device)
    tokenizer=AutoTokenizer.from_pretrained(model_id)
    desc_tokenizer=AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
    desc=("Rohit, a male Hindi speaker, speaks naturally at a moderate conversational pace, "
          "with a warm, clear, close-mic voice and subtle expression. Very clear audio.")
    prompt=tokenizer(SAMPLE,return_tensors="pt").input_ids.to(device)
    description=desc_tokenizer(desc,return_tensors="pt").input_ids.to(device)
    with torch.inference_mode():
        audio=model.generate(input_ids=description,prompt_input_ids=prompt)
    wav=out.with_suffix(".wav")
    sf.write(str(wav),audio.cpu().numpy().squeeze(),model.config.sampling_rate)
    run(["ffmpeg","-y","-loglevel","error","-i",str(wav),str(out)])
    wav.unlink(missing_ok=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="../output/voice-comparison")
    p.add_argument("--engines",default="edge,espeak",help="edge,espeak,parler (Parler is heavyweight)")
    a=p.parse_args()
    out=Path(a.output).resolve(); out.mkdir(parents=True,exist_ok=True)
    (out/"sample_hi.txt").write_text(SAMPLE+"\n",encoding="utf-8")
    funcs={"edge":edge,"espeak":espeak,"parler":parler}
    report={"language":"Hindi","gender":"male","same_script":True,"samples":[]}
    for name in [v.strip() for v in a.engines.split(",") if v.strip()]:
        if name not in funcs: raise SystemExit("Unknown engine: "+name)
        target=out/(name+"_male_hi.mp3")
        try:
            funcs[name](target)
            if not target.exists() or target.stat().st_size<1000: raise RuntimeError("Audio missing/too small")
            report["samples"].append({"engine":name,"file":target.name,"duration_seconds":round(duration(target),3),"bytes":target.stat().st_size,"status":"generated"})
        except Exception as exc:
            report["samples"].append({"engine":name,"status":"failed","error":str(exc)})
            print(name+" failed: "+str(exc),file=sys.stderr)
    (out/"comparison.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not any(x["status"]=="generated" for x in report["samples"]): raise SystemExit(1)

if __name__=="__main__": main()
