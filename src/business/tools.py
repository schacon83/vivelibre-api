import re


def clean_text(text):
    # Expresiones regulares que se van a emplear
    xml_pattern = r'<[^>]*>(.*?)<\/[^>]*>'
    repeated_special_characters = r'([^\w\s])\1+'
    multiple_blanks = r'\s+'

    text = re.sub(xml_pattern, '', text)
    text = re.sub(repeated_special_characters, '', text)
    text = re.sub(multiple_blanks, ' ', text)
    return text.strip()
