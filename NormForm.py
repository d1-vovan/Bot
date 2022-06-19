def StrToNormForm(str):
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    return morph.parse(str.lower())[0].normal_form