from agents.prompt.load_instruction import load_instruction


def gen_message(*, 
                src_lang,
                tgt_lang,
                src_text,
                target,
                domain,
                version="1.0",
                ):
    
    instruction = load_instruction(version=version, role="proofread")
    domain = domain or "general"

    content = instruction.format(
        src_lang=src_lang,
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