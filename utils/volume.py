import strings, os, random, re, shutil, datetime, subprocess, ctypes, win32com.client, win32file, win32api
from utils import preferences

class VolumeNotAccessibleError(Exception): pass
class IconNotFoundError(Exception): pass
class AutorunEncodingError(Exception): pass


def read_autorun_file(volume: str) -> str:
    try: 
        autorun_file = open(f"{volume}autorun.inf", encoding = "utf-16-le")
        autorun_contents = autorun_file.read()
    except:
        try: 
            autorun_file = open(f"{volume}autorun.inf", encoding = "utf-8")
            autorun_contents = autorun_file.read()
        except:
            try:
                autorun_file = open(f"{volume}autorun.inf")
                autorun_contents = autorun_file.read()
            except:
                raise AutorunEncodingError("Invalid `autorun.inf` file encoding.")
            
    autorun_file.close()

    return autorun_contents


def modify_volume_info(
    volume: str, label: str, default_icon: bool = False, 
    icon_path: str = preferences.temp + "\\icon.ico", 
    hide_autorun: bool = True, hide_vl_icon: bool = True, 
    backup_existing_autorun: bool = True
) -> None:
    
    if os.path.exists(volume):
        if not default_icon and not os.path.exists(icon_path):
            raise IconNotFoundError(f"Icon not found. Path: " + icon_path)
        
        if not default_icon:
            id = random.randint(1000000, 9999999)

            if os.path.exists(f"{volume}vl_icon"):
                shutil.rmtree(f"{volume}vl_icon")

            os.mkdir(f"{volume}vl_icon")
            shutil.copyfile(icon_path, f"{volume}vl_icon\\icon{id}.ico")

            readme_file = open(f"{volume}vl_icon\\! {strings.lang.readme}.txt", "w", encoding = "utf-8")
            readme_file.write(strings.lang.icon_folder)
            readme_file.close()

            if hide_vl_icon: 
                add_hidden_attribute(f"{volume}vl_icon")

        if os.path.exists(f"{volume}autorun.inf") and backup_existing_autorun:
            if not os.path.exists(f"{volume}Autorun.inf Backups"): 
                os.mkdir(f"{volume}Autorun.inf Backups")

            remove_hidden_attribute(f"{volume}autorun.inf")
            shutil.copyfile(f"{volume}autorun.inf", f"{volume}Autorun.inf Backups\\autorun_{str(datetime.datetime.now()).replace('-', '_').replace(':', '_')}.inf")

            readme_file = open(f"{volume}Autorun.inf Backups\\! {strings.lang.readme}.txt", "w", encoding = "utf-8")
            readme_file.write(strings.lang.autorun_backup)
            readme_file.close()


        def modify_existing_autorun_file():
            autorun = read_autorun_file(volume)
            autorun_new = ""
            autorun_lines = autorun.split("\n")

            icon_changed = False
            label_changed = False

            for line in autorun_lines:
                entry_and_param = line.split("=", 1)

                if len(entry_and_param) == 2:
                    entry = entry_and_param[0].strip().lower()

                    if entry == "icon": 
                        if not default_icon:
                            autorun_new += f"\nicon=vl_icon\\icon{id}.ico,0"
                            icon_changed = True
                    elif entry == "label": 
                        autorun_new += f"\nlabel=\"{label}\""
                        label_changed = True
                    else: autorun_new += "\n" + line
                else:
                    autorun_new += "\n" + line

            
            if not icon_changed and not default_icon: 
                autorun_new, replacements = re.subn(r"(?i)^\[autorun(?:\.[a-zA-Z0-9_]+)?\]", lambda match: f"{match.group(0)}\nicon=vl_icon\\icon{id}.ico,0", autorun_new, flags = re.MULTILINE)
                if replacements > 0: icon_changed = True
            
            if not label_changed: 
                autorun_new, replacements = re.subn(r"(?i)^\[autorun(?:\.[a-zA-Z0-9_]+)?\]", lambda match: f"{match.group(0)}\nlabel=\"{label}\"", autorun_new, flags = re.MULTILINE)
                if replacements > 0: label_changed = True

            if not (icon_changed or label_changed):
                autorun_new += f"\n\n[autorun]\nlabel=\"{label}\""
                if not default_icon == "default": autorun_new += f"\nicon=vl_icon\\icon{id}.ico,0"

            autorun_new = autorun_new.strip()

            remove_hidden_attribute(f"{volume}autorun.inf")
            autorun_file = open(f"{volume}autorun.inf", "w", encoding = "utf-16-le")
            autorun_file.write(autorun_new)
            autorun_file.close()
            
            if hide_autorun:
                add_hidden_attribute(f"{volume}autorun.inf")
        

        def create_new_autorun_file():
            autorun = f"[autorun]\nlabel=\"{label}\""
            if not default_icon: autorun += f"\nicon=vl_icon\\icon{id}.ico,0"

            remove_hidden_attribute(f"{volume}autorun.inf")

            autorun_file = open(f"{volume}autorun.inf", "w", encoding = "utf-16-le")
            autorun_file.write(autorun)
            autorun_file.close()

            if hide_autorun:
                add_hidden_attribute(f"{volume}autorun.inf")


        if os.path.exists(f"{volume}autorun.inf"):
            autorun = read_autorun_file(volume)

            if re.search("(?i)^\\[[^\\]]+\\]", autorun):
                modify_existing_autorun_file()
            else:
                create_new_autorun_file()
        else:
            create_new_autorun_file()
    else:
        raise VolumeNotAccessibleError(f"The volume {volume} is not accessible.")


def remove_volume_customizations(volume: str, backup_existing_autorun: bool = True) -> None:
    if os.path.exists(volume):
        if os.path.exists(f"{volume}autorun.inf") and backup_existing_autorun:
            if not os.path.exists(f"{volume}Autorun.inf Backups"):
                os.mkdir(f"{volume}Autorun.inf Backups")

            remove_hidden_attribute(f"{volume}autorun.inf")
            shutil.copyfile(f"{volume}autorun.inf", f"{volume}Autorun.inf Backups\\autorun_{str(datetime.datetime.now()).replace('-', '_').replace(':', '_')}.inf")

            readme_file = open(f"{volume}Autorun.inf Backups\\! {strings.lang.readme}.txt", "w", encoding = "utf-8")
            readme_file.write(strings.lang.autorun_backup)
            readme_file.close()

        os.remove(f"{volume}autorun.inf")

        if os.path.exists(f"{volume}vl_icon"):
            shutil.rmtree(f"{volume}vl_icon")
    else:
        raise VolumeNotAccessibleError(f"The volume {volume} is not accessible.")
    

def reassign_volume_letter(volume: str) -> int:
    cmd_path = "C:\\Windows\\System32\\cmd.exe"
    diskpart_path = "C:\\Windows\\System32\\diskpart.exe"

    script_path = preferences.diskpart + "\\script.txt"
    status_path = preferences.diskpart + "\\status.txt"
    log_path = preferences.diskpart + "\\log.txt"

    open(script_path, "w").write(f"select volume {volume[0]}\nassign letter {volume[0]}\nexit")

    subprocess.call(f"\"{cmd_path}\" /c \"\"{diskpart_path}\" /s \"{script_path}\" > \"{log_path}\" && echo 1 > \"{status_path}\" || echo 0 > \"{status_path}\"\"", shell = True)
    
    return int(open(status_path, "r").read())  # 1 - success; 0 - failure


def get_volume_label(volume: str) -> str:
    buffer = ctypes.create_unicode_buffer(261)    
    result = ctypes.windll.kernel32.GetVolumeInformationW(ctypes.c_wchar_p(volume), buffer, ctypes.sizeof(buffer), None, None, None, None, None)
    
    if result: return buffer.value if buffer.value != "" else win32com.client.Dispatch("Shell.Application").Namespace(volume.replace("\\", "")).Self.Name[:-5]
    else: return win32com.client.Dispatch("Shell.Application").Namespace(volume.replace("\\", "")).Self.Name[:-5]


def get_volume_label_and_icon(volume: str) -> dict[str, str, int]:
    if os.path.exists(volume):
        icon_path = None
        icon_index = 0

        volume_label = get_volume_label(volume)

        if os.path.exists(f"{volume}autorun.inf"):
            autorun = read_autorun_file(volume)
            autorun_lines = autorun.split("\n")

            for line in autorun_lines:
                entry_and_param = line.split("=", 1)

                if len(entry_and_param) == 2:
                    entry = entry_and_param[0].strip().lower()
                    param = entry_and_param[1].strip()

                    if entry == "icon":
                        path_and_index = preferences.remove_string_quotes(param).rsplit(",", 1)
                        icon_path = path_and_index[0]

                        if len(path_and_index) == 2: icon_index = int(path_and_index[1].strip())

                        if not icon_path.lower().startswith(volume.lower()):
                            icon_path = volume + icon_path

                        if not os.path.exists(icon_path): icon_path = None 
                    elif entry == "label":
                        volume_label = preferences.remove_string_quotes(param)

        return {"label": volume_label, "icon_path": icon_path, "icon_index": icon_index}
    else:
        raise VolumeNotAccessibleError(f"The volume {volume} is not accessible.")


def is_system_volume(volume: str) -> bool:
    return win32api.GetSystemDirectory().split("\\")[0] + "\\" == volume 


def get_available_volumes() -> list:
    return [f"{chr(65 + i)}:\\" for i in range(26) if (ctypes.windll.kernel32.GetLogicalDrives() >> i) & 1]


def is_network_volume(volume) -> bool:
    return win32file.GetDriveType(volume) == 4


def add_hidden_attribute(file_path: str) -> None:
    ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02)


def remove_hidden_attribute(file_path: str) -> None:
    ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x80)