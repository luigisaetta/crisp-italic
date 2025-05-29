"""
utils.py

Utility functions for text processing and JSON extraction from LLM outputs.
"""

import json
import logging

# this is the prompt used to query the model
prompt_template = """Sei un assistente utile.

Rispondi alla seguente domanda a scelta multipla sull'argomento '{topic}'.
Ragiona brevemente prima di rispondere.
La tua risposta deve essere nel seguente formato: 'Risposta: LETTERA' (senza virgolette) dove LETTERA è una tra: {merged_letters}. 
Rispondi soltanto con la LETTERA che corrisponde alla risposta corretta.
Non aggiungere ulteriori commenti o dettagli sui ragionamenti compiuti.

Esempio:
Risposta: A

{question}

{options}
"""


def get_console_logger(
    name: str = "console_logger", level=logging.INFO
) -> logging.Logger:
    """
    Create a console logger for debugging purposes.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def parse_model_response(response: str) -> str:
    """
    Parse the model response to extract the answer letter.
    Args:
        response (str): The response from the model.
    Returns:
        str: The extracted answer letter or None if not found.
    """
    if response.startswith("Risposta: "):
        return response.split("Risposta: ")[1].strip()
    return None


def read_all_items(file_path: str):
    """
    Read all items from a JSONL file.

    Args:
        file_path (str): Path to the JSONL file.

    Returns:
        list: List of items read from the file.
    """
    items = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():  # Skip empty lines if any
                data = json.loads(line)
                items.append(data)
    return items
