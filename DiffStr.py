from difflib import SequenceMatcher

def similar(a, b):
    a.lower()
    b.lower()
    return SequenceMatcher(None, a, b).ratio()