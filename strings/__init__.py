import locale, ctypes

def load_language(language: str):
    global lang
    if language == "default": language = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()]
    
    match language:
        case "ro_RO": import strings.ro_RO as lang
        case _: import strings.en_US as lang