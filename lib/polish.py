def vanilla(text):
    text = text.replace('*', '')
    text = text.replace('’', "'")
    text = text.replace('–', '-')
    return text

def sanitize(text):
    text = text.lower().strip()
    text = text.replace('mentha piperita', 'mentha x piperita')
    return text

def sluggify(text):
    text = text.strip().lower().replace(' ', '-').replace('.', '')
    text = text.replace('×', 'x')
    return text
    
def to_ascii(text):
    text = text.replace('–', '-')
    text = text.replace('’', "'")
    return text

