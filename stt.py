import os
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from GToolbox.translate import MBartTranslator

def sec2hmsm(sec):
    h = str(int(sec // 3600))
    m = str(int(sec % 3600) // 60)
    s = str(int(sec % 60))
    ms = str(int((sec - int(sec)) * 1000))

    if len(h) < 2:
        h = '0' + h
    if len(m) < 2:
        m = '0' + m
    if len(s) < 2:
        s = '0' + s
    if len(ms) < 3:
        ms = '0' * (3 - len(ms)) + ms
    
    return f"{h}:{m}:{s},{ms}"

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # 隐藏TensorFlow的提示信息

def transcribe_audio(audio, model_id="./models/whisper-large-v3",output="output.srt", enable_translation=False, src_lang="en_XX", tgt_lang="zh_CN"):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    if torch.cuda.is_available():
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True,
            use_safetensors=True, attn_implementation="flash_attention_2"
        )
        model.to(device)
    else:
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True,
            use_safetensors=True
        )
        model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )
    result = pipe(audio)

    if enable_translation:
        translator = MBartTranslator()  # 初始化翻译器

    with open(output,'w',encoding='utf-8') as f:
        i = 1
        for segment in result['chunks']:
            start = sec2hmsm(segment['timestamp'][0])
            end = sec2hmsm(segment['timestamp'][1])
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            text = segment['text']

            if enable_translation:
                text = translator.translate(text, src_lang, tgt_lang)  # 调用翻译
            f.write(text + '\n')
            f.write('\n')
            i += 1

    return result

if __name__ == "__main__":
    
    audio = input("请输入音频文件路径: ")
    model_id = input("请选择模型: ")
    if not model_id.strip():
        model_id = "./models/whisper-large-v3"
    output = os.path.splitext(audio)[0] + ".srt"
    enable_translation = input("是否启用翻译功能? (y/n): ").strip().lower() == 'y'
    if enable_translation:
        print("可参考的语言代码：\nEnglish: en_XX \n日本語: ja_XX \n中文: zh_CN\n韩语: ko_KR")
        src_lang = input("请输入源语言代码: ")
        if not src_lang.strip():
            src_lang = "en_XX"
        tgt_lang = input("请输入目标语言代码: ")
        if not tgt_lang.strip():
            tgt_lang = "zh_CN"
    else:
        src_lang = tgt_lang = ""

    result = transcribe_audio(audio=audio, model_id=model_id, output=output,src_lang=src_lang, tgt_lang=tgt_lang)
