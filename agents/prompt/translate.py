from agents.prompt.load_instruction import load_instruction


def gen_message(*, 
                src_lang,
                tgt_lang,
                src_text,
                target=None,
                domain=None,
                version="1.0",
                ):
    
    instruction = load_instruction(version=version, role="translate")
    domain = domain or "general"

    content = instruction.format(
        src_lang=src_lang,
        tgt_code=lang2code(tgt_lang),
        tgt_lang=tgt_lang,
        domain=domain
    )

    return [
        {
            "role": "system",
            "content": "You are a professional {src_lang}-to-{tgt_lang} translator, tasked with providing translations suitable for use in {tgt_lang} {tgt_code}.".format(
                src_lang=src_lang,
                tgt_lang=tgt_lang,
                tgt_code=lang2code(tgt_lang),
            )
        },
        {
            "role": "user",
            "content": (
                content +
                f"\n\n{src_lang} source: ```{src_text}```\n"
            )
        }
    ]

def lang2code(lang: str) -> str: #TODO!
    lang_map = {
        "English": "en_US",
        "Chinese": "zh_CN",
        "French": "fr",
        "German": "de_DE",
        "Spanish": "es",
        "Japanese": "ja",
        "Korean": "ko_KR",
        "Russian": "ru",
        "Italian": "it",
        "Portuguese": "pt",
    }
    return "(" + lang_map.get(lang, "") + ")"