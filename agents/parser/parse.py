from agents.parser.aligner import preserve_paragraph_structure
import logging

logger = logging.getLogger(__name__)

def parse_response(response, tgt_text):
    """
    Parses proofread task response into unified dictionary structure.
    """
    raw = response.get("content", "")
    usage = response.get("usage", 0)
    
    corrected = raw.strip() if raw else tgt_text
    if not corrected:
        logger.warning("Empty response received for proofread task.")
        return tgt_text
    
    corrected = preserve_paragraph_structure(tgt_text, corrected)
    logger.info(f"Proofread parsing completed. Usage: {usage} tokens.") 
    return corrected