import re


def clean_text(text):
    """
    Limpia un texto, eliminando información entre etiquetas,
    caracteres especiales y espacios repetidos
    :param text: String con el texto
    :return: Devuelve un texto legible
    """
    # Expresiones regulares que se van a emplear
    xml_pattern = r'<[^>]*>(.*?)<\/[^>]*>'
    repeated_special_characters = r'([^\w\s])\1+'
    multiple_blanks = r'\s+'

    text = re.sub(xml_pattern, '', text)
    text = re.sub(repeated_special_characters, '', text)
    text = re.sub(multiple_blanks, ' ', text)
    return text.strip()
