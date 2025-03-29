import os, appdirs, ctypes, yaml


if os.path.exists("preferences") and os.path.isdir("preferences"):
    user_preferences = os.path.abspath("preferences")
    is_portable = True
else:
    user_preferences = appdirs.user_config_dir(appname = "Volume Labeler", appauthor = False, roaming = True)
    is_portable = False

temp = user_preferences + "\\temp"
diskpart = user_preferences + "\\temp\\diskpart"

if not os.path.exists(user_preferences): os.mkdir(user_preferences)
if not os.path.exists(temp): os.mkdir(temp)
if not os.path.exists(diskpart): os.mkdir(diskpart)


theme, language, additional_prefs = "default", "default", "1110"

def save_settings():
    settings = {
        "theme": theme,
        "language": language,

        "additional_options": {
            "hide_autorun.inf": bool(int(additional_prefs[0])),
            "hide_vl_icon": bool(int(additional_prefs[1])),
            "backup_autorun.inf": bool(int(additional_prefs[2])),
            "refresh_volume_info_without_asking": bool(int(additional_prefs[3]))
        }
    }

    settings_file = open(user_preferences + "\\settings.yaml", "w", encoding = "utf8")
    settings_file.write(yaml.safe_dump(data = settings, allow_unicode = True, sort_keys = False))
    settings_file.close()

def load_settings():
    global theme, language, additional_prefs

    settings_file = open(user_preferences + "\\settings.yaml", "r", encoding = "utf8")
    settings_yaml = settings_file.read()
    settings_file.close()
    settings = yaml.safe_load(settings_yaml)

    language = settings["language"]
    theme = settings["theme"]

    additional_prefs = ""
    additional_prefs_list = ["hide_autorun.inf", "hide_vl_icon", "backup_autorun.inf", "refresh_volume_info_without_asking"]

    for preference in additional_prefs_list:
        try: additional_prefs += str(int(settings["additional_options"][preference]))
        except: additional_prefs += "0"

try:
    load_settings()
except:
    save_settings()


def limit_string(string: str) -> str:
    if len(string) > 24:
        return "..." + string[-21:]
    
    return string


ctypes.windll.shcore.SetProcessDpiAwareness(1)

dpi = ctypes.c_uint()
monitor_handle = ctypes.windll.user32.MonitorFromPoint(0, 0, 2)
ctypes.windll.shcore.GetDpiForMonitor(monitor_handle, 0, ctypes.byref(dpi), ctypes.byref(dpi))

scale_factor = dpi.value / 96

def get_scaled_value(value: int) -> int:
    return int(value * scale_factor + 0.5)