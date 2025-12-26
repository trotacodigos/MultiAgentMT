def gen_postedit_message(*, src_lang, tgt_lang, src_text, target, ref_text=None):
    """
    Generates message prompts for post-editing task.
    """
    messages = [
        {"role": "system", "content": "You are a professional evaluator of machine translation quality."}
    ]

    shots = icl_examples()
    messages.extend(shots)

    prompt = create_template(
        src_lang=src_lang,
        tgt_lang=tgt_lang,
        src_text=src_text,
        target=target,
        ref_text=ref_text
    )
    messages.append({"role": "user", "content": prompt})

    return messages



def icl_examples() -> list:
    """Returns ICL examples as message pairs (user/assistant format)."""

    examples = {
        'ende': {
            "src_lang": "English",
            "tgt_lang": "German",
            "src_text": (
                "I do apologise about this, we must gain permission from the "
                "account holder to discuss an order with another person, I "
                "apologise if this was done previously, however, I would not be able "
                "to discuss this with yourself without the account holder’s permission."
            ),
            "target": (
                "Ich entschuldige mich dafür, wir müssen die Erlaubnis einholen, um "
                "eine Bestellung mit einer anderen Person zu besprechen. Ich entschuldige "
                "mich, falls dies zuvor geschehen wäre<, aber ohne die Erlaubnis "
                "des Kontoinhabers wäre ich nicht in der Lage, dies mit dir "
                "zu besprechen."
            ),
            "answer": (
"""{
  "<,": {
    "category": "punctuation",
    "severity": 1,
    "suggestion": ""
  },
  "wäre": {
    "category": "grammar",
    "severity": 2,
    "suggestion": "bin"
  },
  "einholen,": {
    "category": "omission",
    "severity": 3,
    "suggestion": "einholen vom Kontoinhaber,"
  }
}"""
            )
        },

        'encz': {
            "src_lang": "English",
            "tgt_lang": "Czech",
            "src_text": (
                "Talks have resumed in Vienna to try to revive the nuclear pact, "
                "with both sides trying to gauge the prospects of success after the "
                "latest exchanges in the stop-start negotiations."
            ),
            "target": (
                "Ve Vídni se ve Vídni obnovily rozhovory o oživení jaderného "
                "paktu, přičemž obě partaje se snaží posoudit vyhlídky na úspěch "
                "po posledních výměnách v jednáních."
            ),
            "answer": (
"""{
  "ve Vídni": {
    "category": "addition",
    "severity": 3,
    "suggestion": ""
  },
  "partaje": {
    "category": "terminology",
    "severity": 1,
    "suggestion": "strany"
  }
}"""
            )
        },

        'zhen': {
            "src_lang": "Chinese",
            "tgt_lang": "English",
            "src_text": (
                "大众点评乌鲁木齐家居卖场频道为您提供高铁居然之家地址，"
                "电话，营业时间等最新商户信息， 找装修公司，就上大众点评"
            ),
            "target": (
                "Urumqi Home Furnishing Store Channel provides you with the latest "
                "business information such as the address, telephone number, business "
                "hours, etc., of high-speed rail, and find a decoration "
                "company, and go to the reviews."
            ),
            "answer": (
"""{
  "of high-speed rail": {
    "category": "addition",
    "severity": 4,
    "suggestion": ""
  },
  "go to the reviews": {
    "category": "mistranslation",
    "severity": 3,
    "suggestion": "check out Dazhong Dianping"
  }
}"""
            )
        },

    'jako': {
        "src_lang": "Japanese",
        "tgt_lang": "Korean",
        "src_text": (
            "ご注文の商品が本日発送されたことをお知らせいたします。"
        ),
        "target": (
            "우리는 당신의 주문이 오늘 배송되었음을 알려드립니다."
        ),
        "answer": (
"""{
  "주문이": {
    "category": "style",
    "severity": 2,
    "suggestion": "상품이"
  }
}"""),
    }
    }

    messages = []

    for data in examples.values():
        from_user = create_template(
            src_lang=data["src_lang"],
            tgt_lang=data["tgt_lang"],
            src_text=data["src_text"],
            target=data["target"],
        )

        user_message = {"role": "user", "content": from_user}
        assistant_message = {"role": "assistant", "content": data["answer"]}
        messages.extend([user_message, assistant_message])

    return messages



def create_template(*, src_lang, tgt_lang, src_text, target, ref_text=None):
    """
    Generates an MQM-style prompt to identify and classify translation errors.
    Efficiently builds the prompt string using list-based construction.
    """

    parts = [
        f"{src_lang} source: ```{src_text}```",
        f"{tgt_lang} translation: ```{target}```"
    ]

    if ref_text is not None:
        parts.append(f"{tgt_lang} reference: ```{ref_text}```")
        intro = "Based on the source, reference, and translation enclosed in triple backticks, "
    else:
        intro = "Based on the source and translation enclosed in triple backticks, "

    instruction_lines = [
        intro + "identify only errors in the translation and classify each by category.",
        "Categories: addition, mistranslation, omission, untranslated text, grammar, "
        "inconsistency, punctuation, word order, terminology, and style.",
        "You must find at least one issue, even minor, stylistic, or subjective.",
        "Rate severity from 1 (minor) to 4 (severe distortion) according to the rubric.",
        "Scale 1: Slight wording change with no impact on clarity or intent.",
        "Scale 2: Alters wording but message and intent remain mostly clear.",
        "Scale 3: Noticeable impact on comprehension; may slightly distort intent.",
        "Scale 4: Substantial distortion; translation is unfaithful and potentially misleading.",
        "Never select entire sentences or long phrases as an error span.",
        "Select only the exact word or short phrase where the error occurs.",
        "Suggest fixes *only* for the erroneous parts — do not rewrite the full sentence.",
        "Format:",
        "{",
        '  "<error span>": {',
        '    "category": "<category>",',
        '    "severity": <1-4>,',
        '    "suggestion": "<fix>"',
        "  },",
        "  ...",
        "}",
        "No extra text or explanations."
    ]

    return "\n".join(parts) + "\n\n" + "\n".join(instruction_lines)
    
    
    