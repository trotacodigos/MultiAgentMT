from agents.prompt.load_instruction import load_instruction


def gen_message(*, 
                src_lang,
                tgt_lang,
                src_text,
                target,
                domain=None,
                version="1.0",
                ):
    
    instruction = load_instruction(version=version, role="translate")
    domain = domain or "general"

    content = instruction.format(
        src_lang=src_lang,
        src_code=source_lang2code(src_lang),
        tgt_lang=tgt_lang,
        domain=domain
    )

    return [
        {
            "role": "system",
            "content": "You are a professional editor specializing in machine translation quality improvement."
        },
        {
            "role": "user",
            "content": (
                content +
                f"\n\n{src_lang} source: ```{src_text}```\n"
                f"{tgt_lang} translation: ```{target}```"
            )
        }
    ]

def source_lang2code(lang: str) -> str: #TODO!
    lang_map = {
        "English": "en",
        "Chinese": "zh",
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