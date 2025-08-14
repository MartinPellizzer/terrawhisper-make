def sluggify(text):
    text = text.strip().lower().replace(' ', '-').replace('.', '')
    text = text.replace('×', 'x')
    return text
    
