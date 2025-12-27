from agents.prompt.load_instruction import load_instruction


def gen_message(*, 
                src_lang,
                tgt_lang,
                src_text,
                target=None,
                domain,
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
        "Chinese (Taiwan)": "zh_TW",
        "French": "fr_FR",
        "French (Canada)": "fr_CA",
        "German": "de_DE",
        "Spanish (Mexico)": "es_MX",
        "Spanish": "es_ES",
        "Japanese": "ja_JP",
        "Korean": "ko_KR",
        "Russian": "ru_RU",
        "Italian": "it_IT",
        "Portuguese": "pt_PT",
        "Portuguese (Brazil)": "pt_BR",
        "Dutch": "nl_NL",
        "Turkish": "tr_TR",
        "Arabic": "ar_SA",
        "Arabic (Egypt)": "ar_EG",
        "Hindi": "hi_IN",
        "Bengali": "bn_IN",
        "Tamil": "ta_IN",
        "Gujarati": "gu_IN",
        "Malayalam": "ml_IN",
        "Punjabi": "pa_IN",
        "Telugu": "te_IN",
        "Indonesian": "id_ID",
        "Hungarian": "hu_HU",
        "Swahili": "sw_TZ",
        "Swahili (Kenya)": "sw_KE",
        "Vietnamese": "vi_VN",
        "Filipino": "fil_PH",
        "Slovene": "sl_SI",
        "Croatian": "hr_HR",
        "Serbian": "sr_RS",
        "Icelandic": "is_IS",
        "Polish": "pl_PL",
        "Catalan": "ca_ES",
        "Afrikaans": "af_ZA",
        "Zulu": "zu_ZA",
        "Hungarian": "hu_HU",
        "Filipino": "fil_PH",
        "Norwegian": "no_NO",
        "Swedish": "sv_SE",
        "Urdu": "ur_PK",
        "Bulgarian": "bg_BG",
        "Czech": "cs_CZ",
        "Danish": "da_DK",
        "Finnish": "fi_FI",
        "Greek": "el_GR",
        "Hebrew": "he_IL",
        "Lithuanian": "lt_LT",
        "Romanian": "ro_RO",
        "Slovak": "sk_SK",
        "Ukrainian": "uk_UA",
        "Latvian": "lv_LV",
        "Estonian": "et_EE",
        "Thai": "th_TH",
        "Kannada (India)": "kn_IN",
        "Persian": "fa_IR",
    }
    return "(" + lang_map.get(lang, "") + ")"