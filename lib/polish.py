def sluggify(text):
    text = text.strip().lower().replace(' ', '-').replace('.', '')
    text = text.replace('×', 'x')
    return text
    
def to_ascii(text):
    text = text.replace('–', '-')
    text = text.replace('’', "'")
    return text

