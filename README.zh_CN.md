# Subtitle-It-Yourself
 A simple speech to text program, powered by whisper.

[English](./README.md) [简体中文](./README.zh_CN.md)

# 这是什么？
将音视频文件生成字幕，只能说是能用，界面不友好，但是因为调用了whisper所以识别功能很好用，没有半点收费的地方。大家有兴趣可以复制或者Fork，以这个项目为起点。

# 使用方式
1. 克隆整个项目。
2. 安装缺失的Python包。
3. 运行gui.py

# 已知的问题
- 丑陋的界面
- 本地模型巨大
- 不良好的交互
- 如果电脑不支持Flash-Attention可能会出现错误
- 某些文件格式FFmpeg读取会出现错误（如修改了错误的后缀名，和实际文件类型不匹配）
- 无法翻译为中文，是翻译模型存在问题，最终总是会被翻译为英文等，可以尝试手动翻译srt文件内容。

# 贡献
语音转文字（speech-to-text）部分依赖Whisper模型（whisper-large-v3），
多语种翻译部分依赖facebook/mbart-large-50-many-to-many-mmt。
