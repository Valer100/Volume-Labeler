import winreg, strings, sys, os, subprocess


def is_context_menu_entry_added() -> bool:
    try:
        entry = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\Drive\\shell\\Volume Labeler", 0, winreg.KEY_ALL_ACCESS)
        entry.Close()

        return True
    except:
        return False
    

def add_context_menu_entry() -> None:
    entry = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\Drive\\shell\\Volume Labeler")
    winreg.SetValueEx(entry, "", 0, winreg.REG_SZ, strings.lang.customize_with_volume_labeler)
    
    if getattr(sys, "frozen", False): 
        winreg.SetValueEx(entry, "Icon", 0, winreg.REG_SZ, sys.executable)
    else:
        winreg.SetValueEx(entry, "Icon", 0, winreg.REG_SZ, os.path.abspath("icons\\icon.ico"))
    
    entry.Close()

    entry_command = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\Drive\\shell\\Volume Labeler\\command")
    
    if getattr(sys, "frozen", False):
        winreg.SetValueEx(entry_command, "", 0, winreg.REG_SZ, f"\"{sys.executable}\" --volume %1")
    else:
        winreg.SetValueEx(entry_command, "", 0, winreg.REG_SZ, f"\"{sys.executable}\" \"{sys.argv[0]}\" --volume %1")
    
    entry_command.Close()


def remove_context_menu_entry() -> None:
    subprocess.call("C:\\Windows\\System32\\reg.exe delete \"HKEY_CURRENT_USER\\Software\\Classes\\Drive\\shell\\Volume Labeler\" /f", shell = True)


def update_context_menu_entry_string():
    try:
        entry = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\Drive\\shell\\Volume Labeler", 0, winreg.KEY_ALL_ACCESS)
    
        if not winreg.QueryValueEx(entry, "")[0] == strings.lang.customize_with_volume_labeler:
            winreg.SetValueEx(entry, "", 0, winreg.REG_SZ, strings.lang.customize_with_volume_labeler)
                
        entry.Close()
    except:
        pass