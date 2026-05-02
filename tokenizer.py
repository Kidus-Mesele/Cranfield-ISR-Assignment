import re

def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    tokens = []
    position = 1
    
    for token in text.split():
        token = token.strip('.')
        if token and re.match(r'^[a-z0-9]+(\.[a-z0-9]+)*$', token):
            tokens.append((token, position))
            position += 1
    
    return tokens