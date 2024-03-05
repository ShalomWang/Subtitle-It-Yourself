from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

class MBartTranslator:
    def __init__(self, model_name="facebook/mbart-large-50-many-to-many-mmt"):
        self.tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
        self.model = MBartForConditionalGeneration.from_pretrained(model_name)

    def translate(self, text, src_lang, tgt_lang):
        # 设置源语言和目标语言
        self.tokenizer.src_lang = src_lang
        encoded = self.tokenizer(text, return_tensors="pt")
        forced_bos_token_id = self.tokenizer.lang_code_to_id[tgt_lang]

        # 生成翻译结果
        generated_tokens = self.model.generate(
            **encoded,
            forced_bos_token_id=forced_bos_token_id
        )

        # 解码翻译结果
        translation = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return translation[0]

if __name__ == "__main__":
    # 使用示例
    translator = MBartTranslator()

    # 翻译印地语到法语
    article_hi = "संयुक्त राष्ट्र के प्रमुख का कहना है कि सीरिया में कोई सैन्य समाधान नहीं है"
    print(translator.translate(article_hi, "hi_IN", "zh_CN"))

    # 翻译阿拉伯语到英语
    article_ar = "الأمين العام للأمم المتحدة يقول إنه لا يوجد حل عسكري في سوريا."
    print(translator.translate(article_ar, "ar_AR", "zh_CN"))
