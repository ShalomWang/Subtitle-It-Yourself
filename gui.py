import os
import tkinter as tk
from tkinter import filedialog, messagebox
import stt

# 定义语言
lang_mapping = {
    "英语": "en_XX",
    "日语": "ja_XX",
    "简体中文": "zh_CN",
    "韩语": "ko_KR"
}

def browse_file():
    filename = filedialog.askopenfilename()
    entry_audio.delete(0, tk.END)
    entry_audio.insert(0, filename)

def toggle_translation():
    if translation_var.get():
        src_lang_dropdown.config(state="normal")
        tgt_lang_dropdown.config(state="normal")
    else:
        src_lang_dropdown.config(state="disabled")
        tgt_lang_dropdown.config(state="disabled")

def start_conversion():
    audio = entry_audio.get()
    model_id = "./models/" + model_var.get()
    output = os.path.splitext(audio)[0] + ".srt"
    enable_translation = translation_var.get()
    if enable_translation:
        src_lang = lang_mapping.get(src_lang_var.get(), "en_XX")
        tgt_lang = lang_mapping.get(tgt_lang_var.get(), "zh_CN")
    else:
        src_lang = tgt_lang = ""

    # 转换过程的等待消息
    wait_label.config(text="转换中，请稍候...")
    root.update()

    # 命令
    result = stt.transcribe_audio(audio=audio, model_id=model_id, output=output,src_lang=src_lang, tgt_lang=tgt_lang)

    # 转换完成后弹窗提示
    messagebox.showinfo("提示", "转换完成！")

    # 转换完成后清除等待消息
    wait_label.config(text="")

# Create main window
root = tk.Tk()
root.title("音频转换")

# 音视频文件
label_audio = tk.Label(root, text="文件路径:")
label_audio.grid(row=0, column=0)
entry_audio = tk.Entry(root, width=50)
entry_audio.grid(row=0, column=1)
button_browse = tk.Button(root, text="浏览", command=browse_file)
button_browse.grid(row=0, column=2)

# Model ID
label_model = tk.Label(root, text="STT模型:")
label_model.grid(row=1, column=0)
models = ["whisper-large-v3"]  # 模型选项
model_var = tk.StringVar(root)
model_var.set(models[0])  # 默认模型
model_dropdown = tk.OptionMenu(root, model_var, *models)
model_dropdown.grid(row=1, column=1)

# 是否启用翻译复选框
translation_var = tk.BooleanVar()
translation_var.set(False)
check_translation = tk.Checkbutton(root, text="启用翻译功能?", variable=translation_var, command=toggle_translation)
check_translation.grid(row=2, columnspan=3)

# 原始语种
label_src_lang = tk.Label(root, text="源语言代码:")
label_src_lang.grid(row=3, column=0)
src_langs = ["英语", "日语", "简体中文", "韩语"]  # 源语言
src_lang_var = tk.StringVar(root)
src_lang_var.set(src_langs[3])  # 默认源语言
src_lang_dropdown = tk.OptionMenu(root, src_lang_var, *src_langs)
src_lang_dropdown.grid(row=3, column=1)

# 目标语种
label_tgt_lang = tk.Label(root, text="目标语言代码:")
label_tgt_lang.grid(row=4, column=0)
tgt_langs = ["英语", "日语", "简体中文", "韩语"]  # 目标语言
tgt_lang_var = tk.StringVar(root)
tgt_lang_var.set(tgt_langs[2])  # 默认目标语言
tgt_lang_dropdown = tk.OptionMenu(root, tgt_lang_var, *tgt_langs)
tgt_lang_dropdown.grid(row=4, column=1)

# 启动按钮
button_convert = tk.Button(root, text="开始转换", command=start_conversion)
button_convert.grid(row=5, columnspan=3)

# 等待消息标签
wait_label = tk.Label(root, text="")
wait_label.grid(row=6, columnspan=3)

# 不翻译时禁用语言选择
toggle_translation()

root.mainloop()
