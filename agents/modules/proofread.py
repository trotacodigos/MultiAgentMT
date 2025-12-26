def gen_proofread_message(*, 
                          src_lang,
                          tgt_lang,
                          src_text,
                          target,
                          domain=None,
                          ref_text=None,):
    """
    Generates a structured message prompt for translation refinement tasks.

    Parameters:
        domain (str): Domain of the translation (e.g., 'news').
        src_lang (str): Source language name.
        tgt_lang (str): Target language name.
        src_text (str): Source language segment.
        target (str): Existing target language translation.

    Returns:
        list: Message structure for chat-based API usage.
    """
    domain = domain if domain is not None else 'genera'
    
    # Basic input checks for robustness
    if not all([src_lang, tgt_lang, src_text, target]):
        raise ValueError("All parameters (src_lang, tgt_lang, src_text, target) are required.")

    return [
        {
            "role": "system",
            "content":  "You are a professional editor specializing in machine translation quality improvement."
        },
        {
            "role": "user",
            "content": (
                f"Review the given translation for errors. Find errors and correct them first. "
                f"Then, generate five rephrased translations optimized for fluency and adequacy in the {domain} domain. "
                f"Select the most contextually appropriate version based on linguistic fluency in {tgt_lang}, "
                "preservation of source accuracy, and adherence to professional translation standards. "
                "Output only the final best translation. Do not include the other versions, "
                "reasoning, or any additional text. The output must consist of a single sentence only.\n\n"
                f"{src_lang} source: ```{src_text}```\n"
                f"{tgt_lang} translation: ```{target}```"
            )
        }
    ]