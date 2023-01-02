import json
import os

from path import Path

class I18n:
    langs = {}
    
    _lang = "en"
    
    def set_lang(lang):
        if lang in I18n.langs:
            I18n._lang = lang
    
    def get(txt):
        if txt.startswith("r:"):
            return txt[2:]
        
        d = I18n.langs[I18n._lang]
        if txt in d:
            return d[txt]

        return f"[{txt}]"

for f in os.listdir(Path("assets", "i18n")):
    with open(Path("assets", "i18n", f), "r", encoding="utf-8") as file_:
        lang = f.split(".", 1)[0]
        I18n.langs[lang] = json.load(file_)