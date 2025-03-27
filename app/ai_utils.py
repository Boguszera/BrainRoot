from transformers import pipeline
import random

# Ładowanie modelu TinyLlama/Gemma-2B
generator = pipeline("text-generation", model="distilgpt2", device=-1)

def generate_ai_sentence(direction='ang-pl'):
    """
    generuje zdanie i jego tłumaczenie.
    """
    prompt = "Generate a simple English sentence for a B1-B2 learner."
    result = generator(prompt, max_length=30, num_return_sequences=1)

    sentence = result[0]['generated_text']

    # Sztuczna lista tłumaczeń (dla testów, można użyć API lub innej metody)
    translations = {
        "I like apples.": "Lubię jabłka.",
        "She is reading a book.": "Ona czyta książkę.",
        "We are going to the park.": "Idziemy do parku.",
    }

    translation = translations.get(sentence, "Brak tłumaczenia")

    if direction == 'pl-ang':
        return translation, sentence  # Zamiana kolejności

    return sentence, translation
