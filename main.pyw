import ctypes, os, sys
from tkinter import messagebox

if not ctypes.windll.shell32.IsUserAnAdmin():
    if getattr(sys, "frozen", False):
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 0)
    else:
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f"\"{os.path.abspath(sys.argv[0])}\" {' '.join(sys.argv[1:])}", None, 1)
    
    if result == 42: sys.exit(0)

import tkinter as tk, strings, custom_ui, traceback, tktooltip, argparse, pywinstyles
from tkinter import ttk, filedialog, messagebox
from utils import volume, icon, preferences, context_menu_entry
from dialogs import change_language, change_theme, about, error

ctypes.windll.shcore.SetProcessDpiAwareness(1)

os.chdir(os.path.dirname(__file__))
if os.path.exists("icons\\icon.ico"): preferences.internal = ""
else: preferences.internal = "_internal\\"

parser = argparse.ArgumentParser()
parser.add_argument("--volume", default = None, help = "The letter of the volume you want to customize", required = False)
arguments = parser.parse_args()

window = custom_ui.App()
window.title("Volume Labeler " + ("(Admin)" if ctypes.windll.shell32.IsUserAnAdmin() else ""))
window.resizable(False, False)

icon_pack = "C:\\Windows\\System32\\shell32.dll"
show_additional_options = False
icon_type_old = "default"
selected_volume_old = ""
volumes = [""]
app_started = False
changes_made = False
selected_volume = tk.StringVar(value = "")
hide_autorun = tk.BooleanVar(value = int(preferences.additional_prefs[0]))
hide_vl_icon = tk.BooleanVar(value = int(preferences.additional_prefs[1]))
backup_existing_autorun = tk.BooleanVar(value = int(preferences.additional_prefs[2]))
icon_type = tk.StringVar(value = "default")
label_old = ""
icon_current = (None, 0)
icon_old = (None, 0)


def select_first_accessible_volume():
    for vol in volumes:
        if os.path.exists(vol) and not volume.is_network_volume(vol):
            update_volume_info(vol, True)
            break


def refresh_volumes_list():
    custom_ui.set_window_loading_cursor(window)

    global volumes
    volumes = volume.get_available_volumes()

    menu = volume_dropdown["menu"]
    menu.delete(0, "end")

    for string in volumes:
        try: volume_label = volume.get_volume_label_and_icon(string)["label"]
        except: volume_label = volume.get_volume_label(string)

        menu.add_checkbutton(label = f"{volume_label} ({string})", command = lambda value = string: update_volume_info(value), variable = selected_volume, onvalue = string)

    custom_ui.set_window_normal_cursor(window)


def update_volume_info(vol, forced = False):
    global icon_type_old, selected_volume_old, label_old, icon_old, icon_current
    selected_volume.set(selected_volume_old)

    custom_ui.set_window_loading_cursor(window)

    if changes_made and not forced:
        confirmation = messagebox.askyesnocancel("Volume Labeler", strings.lang.apply_changes_change_volume, icon = "warning", default = "yes")
        
        if confirmation: 
            modify_volume_info()
            if changes_made: return
        elif confirmation == None:
            return

    if os.path.exists(vol) and not volume.is_network_volume(vol):
        selected_volume.set(vol)
        icon_type.set("default")

        choose_icon.configure(text = "  " + strings.lang.choose_icon, image = custom_ui.icons.icon, width = 0)
        icon_from_image.configure(text = "  " + strings.lang.create_icon_from_image, image = custom_ui.icons.image, width = 0)

        volume_info = volume.get_volume_label_and_icon(vol)

        if not volume_info["icon_path"] == None:
            icon_type.set("icon")
            process_icon(volume_info["icon_path"], volume_info["icon_index"])

        icon_type_old = icon_type.get()
        icon_current = (volume_info["icon_path"], volume_info["icon_index"])
        icon_old = (volume_info["icon_path"], volume_info["icon_index"])

        label.delete(0, "end")
        label.insert(0, volume_info["label"])
        label_old = volume_info["label"]

        disable_changes_actions()
        enable_disable_autorun_actions()

        selected_volume_old = selected_volume.get()
    elif volume.is_network_volume(vol):
        selected_volume.set(selected_volume_old)
        messagebox.showerror(strings.lang.unsupported_volume, strings.lang.unsupported_volume_network)
    else:
        selected_volume.set(selected_volume_old)
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)

    custom_ui.set_window_normal_cursor(window)


def check_for_changes(label_new):
    if label_new != label_old or icon_current != icon_old:
        enable_changes_actions()
    else:
        disable_changes_actions()

    return True


def disable_changes_actions():
    global changes_made
    changes_made = False

    apply_changes.disable()
    reset_changes.disable()


def enable_changes_actions():
    global changes_made
    changes_made = True

    apply_changes.enable(modify_volume_info, True)
    reset_changes.enable(reset_changes_)


def enable_disable_autorun_actions():
    if os.path.exists(f"{selected_volume.get()}autorun.inf"):
        remove_customizations.enable(remove_volume_customizations)
        open_autorun.enable(open_autorun_file)
    else:
        remove_customizations.disable()
        open_autorun.disable()


def show_ready_status():
    status_bar["text"] = strings.lang.ready
    custom_ui.set_window_normal_cursor(window)


def reset_changes_():
    confirmation = messagebox.askyesno(strings.lang.reset_changes, strings.lang.reset_changes_confirmation, icon = "warning", default = "no")

    if confirmation:
        if os.path.exists(selected_volume.get()):
            update_volume_info(selected_volume.get(), True)
            disable_changes_actions()
        else:
            messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)


def modify_volume_info():
    global label_old, icon_old

    status_bar["text"] = strings.lang.creating_autorun
    custom_ui.set_window_loading_cursor(window)

    try:
        volume.modify_volume_info(
            volume = selected_volume.get(), 
            label = label.get(), 
            default_icon = icon_type.get() == "default",
            icon_path = preferences.temp + "\\icon.ico",
            hide_autorun = hide_autorun.get(),
            hide_vl_icon = hide_vl_icon.get(),
            backup_existing_autorun = backup_existing_autorun.get()
        )

        label_old = label.get()
        icon_old = icon_current

        disable_changes_actions()
        enable_disable_autorun_actions()

        if ctypes.windll.shell32.IsUserAnAdmin():
            status_bar["text"] = strings.lang.reassigning_letter
            window.update_idletasks()

            volume_letter_reassigned = volume.reassign_volume_letter(selected_volume.get())
            show_ready_status()

            if volume_letter_reassigned:
                messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
            else:
                messagebox.showinfo(strings.lang.done, strings.lang.operation_complete_reboot_required)
        else:
            show_ready_status()
            messagebox.showinfo(strings.lang.done, strings.lang.operation_complete_reboot_required)
    except PermissionError:
        messagebox.showerror(strings.lang.permission_denied, strings.lang.permission_denied_message)
    except volume.VolumeNotAccessibleError:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)
    except volume.IconNotFoundError:
        messagebox.showerror(strings.lang.error, strings.lang.missing_icon_file)
    except:
        error.show(traceback.format_exc())

    show_ready_status()


def remove_volume_customizations():
    try:
        confirmed = messagebox.askyesno(strings.lang.remove_customizations, strings.lang.remove_customizations_message, icon = "warning", default = "no")

        if confirmed:
            status_bar["text"] = strings.lang.deleting_autorun
            custom_ui.set_window_loading_cursor(window)

            volume.remove_volume_customizations(volume = selected_volume.get(), backup_existing_autorun = backup_existing_autorun.get())
            update_volume_info(selected_volume.get())

            if ctypes.windll.shell32.IsUserAnAdmin():
                status_bar["text"] = strings.lang.reassigning_letter
                window.update_idletasks()

                volume_letter_reassigned = volume.reassign_volume_letter(selected_volume.get())
                show_ready_status()

                if volume_letter_reassigned:
                    messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
                else:
                    messagebox.showinfo(strings.lang.done, strings.lang.operation_complete_reboot_required)
            else:
                show_ready_status()
                messagebox.showinfo(strings.lang.done, strings.lang.operation_complete_reboot_required)
    except volume.VolumeNotAccessibleError:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)
    except FileNotFoundError:
        messagebox.showerror(strings.lang.file_not_found, strings.lang.autorun_file_missing)
    except PermissionError:
        messagebox.showerror(strings.lang.permission_denied, strings.lang.permission_denied_message)
    except:
        error.show(traceback.format_exc())


def open_autorun_file():
    custom_ui.set_window_loading_cursor(window)

    try:
        os.startfile(f"{selected_volume.get()}autorun.inf")
    except FileNotFoundError:
        messagebox.showerror(strings.lang.file_not_found, strings.lang.autorun_file_missing)
    except PermissionError:
        messagebox.showerror(strings.lang.permission_denied, strings.lang.permission_denied_message)
    except:
        error.show(traceback.format_exc())

    custom_ui.set_window_normal_cursor(window)


def process_icon(path, index):
    global icon_from_image, choose_icon, preview

    icon.extract_icon(path, index)
    preview = tk.PhotoImage(file = preferences.temp + "\\preview.png")

    choose_icon.configure(image = preview, text = f"  {preferences.limit_string(os.path.basename(path))}, {index}")
    icon_from_image.configure(text = "  " + strings.lang.create_icon_from_image, image = custom_ui.icons.image)


def choose_icon_():
    global preview, icon_type_old, icon_pack, icon_old

    status_bar["text"] = strings.lang.preparing_icon
    custom_ui.set_window_loading_cursor(window)

    match icon_type.get():
        case "default":
            choose_icon.configure(text = "  " + strings.lang.choose_icon, image = custom_ui.icons.icon)
            icon_from_image.configure(text = "  " + strings.lang.create_icon_from_image, image = custom_ui.icons.image)
            icon_old = (None, 0)
        case "icon":
            try:
                pywinstyles.change_header_color(window, custom_ui.colors.bg)
                icon_path, icon_index = icon.pick_icon(window, icon_pack)
                window.set_theme()

                process_icon(icon_path, icon_index)
                icon_old = (icon_path, icon_index)
            except Exception as e:
                window.set_theme()
                icon_type.set(icon_type_old)

            icon_pack = "C:\\Windows\\System32\\shell32.dll"
            window.after(200, lambda: window.bind("<Shift_L>", enable_new_icon_pack))
        case "image":
            image = filedialog.askopenfile(title = strings.lang.choose_image, filetypes = [(strings.lang.images, (".png", ".jpg", ".jpeg", ".bmp", ".gif"))])

            if not image is None:
                icon.convert_image_to_icon(image.name)
                preview = tk.PhotoImage(file = preferences.temp + "\\preview.png")
                
                icon_from_image.configure(image = preview, text = "  " + preferences.limit_string(os.path.basename(image.name)))
                choose_icon.configure(text = "  " + strings.lang.choose_icon, image = custom_ui.icons.icon, width = 0)
                icon_old = (image.name, 0)
            else:
                icon_type.set(icon_type_old)
        
    icon_type_old = icon_type.get()
    check_for_changes(label.get())

    status_bar["text"] = strings.lang.ready
    custom_ui.set_window_normal_cursor(window)


def change_app_language():
    def update_strings(widget):
        if not preferences.is_portable:
            context_menu_entry.update_context_menu_entry_string()

        for child in widget.winfo_children():
            if isinstance(child, (custom_ui.App, custom_ui.Toplevel, tk.Frame, ttk.Frame, tktooltip.ToolTip)):
                update_strings(child)
            else:
                for variable in dir(old_language_module):
                    if isinstance(getattr(old_language_module, variable), str):
                        try:
                            if child["text"] == getattr(old_language_module, variable):
                                child["text"] = getattr(strings.lang, variable)
                            elif child["text"] in [" " + getattr(old_language_module, variable), "  " + getattr(old_language_module, variable)]:
                                child["text"] = child["text"].replace(getattr(old_language_module, variable), getattr(strings.lang, variable))
                        except:
                            pass

    old_language = preferences.language
    old_language_module = strings.lang

    change_language.show()
    window.wait_window(change_language.window)

    if old_language != preferences.language:             
        strings.load_language(preferences.language)
        update_strings(window)
        
        buttons.columnconfigure([0, 1], minsize = max(apply_changes.winfo_reqwidth(), reset_changes.winfo_reqwidth(), remove_customizations.winfo_reqwidth(), open_autorun.winfo_reqwidth()))
        
        status_bar["text"] = ""
        window.update()
        status_bar.configure(wraplength = window.winfo_reqwidth() - preferences.get_scaled_value(28))
        status_bar["text"] = strings.lang.ready


def change_app_theme():
    old_theme = preferences.theme

    change_theme.show()
    window.wait_window(change_theme.window)

    if old_theme != preferences.theme:
        custom_ui.sync_colors(window)


def add_remove_context_menu_entry():
    global context_menu_integration, context_menu_integration_tooltip
    context_menu_integration_tooltip.destroy()

    if context_menu_entry.is_context_menu_entry_added():
        context_menu_entry.remove_context_menu_entry()

        context_menu_integration.configure(default = "normal")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_disabled, follow = False, delay = 1)
        
        messagebox.showinfo(strings.lang.context_menu_integration, strings.lang.context_menu_entry_removed)
    else:
        context_menu_entry.add_context_menu_entry()

        context_menu_integration.configure(default = "active")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_enabled, follow = False, delay = 1)
        
        messagebox.showinfo(strings.lang.context_menu_integration, strings.lang.context_menu_entry_added)


def draw_ui():
    global status_bar, choose_icon, icon_from_image, reset_changes, volume_dropdown, label, show_additional_options, context_menu_integration, context_menu_integration_tooltip, refresh_volumes, additional_options, default_icon, choose_icon, icon_from_image, apply_changes, reset_changes, remove_customizations, open_autorun, buttons
    show_additional_options = False
    
    for widget in window.winfo_children(): widget.destroy()
    strings.load_language(preferences.language)

    root = ttk.Frame(window, padding = (preferences.get_scaled_value(14), preferences.get_scaled_value(8), preferences.get_scaled_value(14), 0))
    root.pack(fill = "both")

    ttk.Label(root, text = "Volume Labeler", font = ("Segoe UI Semibold", 17)).pack(anchor = "w")

    volume_section = ttk.Frame(root)
    volume_section.pack(fill = "x", anchor = "w", pady = (preferences.get_scaled_value(16), preferences.get_scaled_value(8)))

    ttk.Label(volume_section, text = strings.lang.volume).pack(side = "left")

    volumes_actions = ttk.Frame(volume_section)
    volumes_actions.pack(side = "right", padx = (preferences.get_scaled_value(8), 0), fill = "both")

    refresh_volumes = custom_ui.Button(volumes_actions, command = refresh_volumes_list, text = "\ue72c", font = ("Segoe MDL2 Assets", 8))
    refresh_volumes.pack(fill = "both", expand = True)
    refresh_volumes.configure(padx = preferences.get_scaled_value(7), width = 0)

    tktooltip.ToolTip(refresh_volumes, strings.lang.refresh_volumes_list, follow = False, delay = 1)
    
    volume_dropdown = custom_ui.OptionMenu(volume_section, selected_volume, *volumes)
    volume_dropdown.pack(side = "right")

    ttk.Label(root, text = strings.lang.label).pack(pady = preferences.get_scaled_value(10), anchor = "w")

    label_frame = tk.Frame(root, highlightbackground = custom_ui.colors.entry_bd, highlightcolor = custom_ui.colors.entry_focus,
                          highlightthickness = 1)
    label_frame.pack(anchor = "w", fill = "x")

    label = tk.Entry(label_frame, width = 40, background = custom_ui.colors.entry_bg, 
                    foreground = custom_ui.colors.fg, border = 0, highlightthickness = preferences.get_scaled_value(2), 
                    highlightcolor = custom_ui.colors.entry_bg, highlightbackground = custom_ui.colors.entry_bg, 
                    insertbackground = custom_ui.colors.fg, insertwidth = 1, selectbackground = custom_ui.colors.entry_select,
                    selectforeground = "#FFFFFF", validate = "key", validatecommand = (root.register(check_for_changes), "%P"))
    label.pack(fill = "x")
    label.bind("<Button-3>", lambda event: custom_ui.show_entry_context_menu(label))

    ttk.Label(root, text = strings.lang.icon).pack(pady = (preferences.get_scaled_value(16), preferences.get_scaled_value(8)), anchor = "w")

    default_icon = custom_ui.Radiobutton2(root, text = "  " + strings.lang.default_icon, variable = icon_type, value = "default", command = choose_icon_, image = custom_ui.icons.volume, compound = "left")
    default_icon.pack(anchor = "w", fill = "x", pady = preferences.get_scaled_value(2))

    choose_icon = custom_ui.Radiobutton2(root, text = "  " + strings.lang.choose_icon, variable = icon_type, value = "icon", command = choose_icon_, image = custom_ui.icons.icon, compound = "left")
    choose_icon.pack(anchor = "w", fill = "x", pady = preferences.get_scaled_value(2))

    icon_from_image = custom_ui.Radiobutton2(root, text = "  " + strings.lang.create_icon_from_image, variable = icon_type, value = "image", image = custom_ui.icons.image, command = choose_icon_, compound = "left")
    icon_from_image.pack(anchor = "w", fill = "x", pady = preferences.get_scaled_value(2))

    additional_options = custom_ui.Toolbutton(root, text = " " + strings.lang.additional_options, command = lambda: show_hide_additional_options(), anchor = "w", compound = "left", image = custom_ui.icons.arrow_down)
    additional_options.pack(pady = (preferences.get_scaled_value(14), 0), anchor = "w")
    additional_options.configure(padx = preferences.get_scaled_value(2))

    additional_options_frame = ttk.Frame(root)
    additional_options_frame.pack(anchor = "w")
    
    def show_hide_additional_options():
        global show_additional_options, arrow
        show_additional_options = not show_additional_options

        for widget in additional_options_frame.winfo_children():
            if show_additional_options: 
                if widget["text"] == strings.lang.hide_autorun:
                    widget.pack(pady = (preferences.get_scaled_value(6), 0), anchor = "w")
                else:
                    widget.pack(anchor = "w")
            else: widget.forget()

        if show_additional_options: 
            additional_options_frame.configure(height = -1)
            additional_options.configure(image = custom_ui.icons.arrow_up)
        else: 
            additional_options_frame.configure(height = 1)
            additional_options.configure(image = custom_ui.icons.arrow_down)

    def save_additional_preferences(): 
        preferences.additional_prefs = f"{int(hide_autorun.get())}{int(hide_vl_icon.get())}{int(backup_existing_autorun.get())}"
        preferences.save_settings()

    custom_ui.Checkbutton(additional_options_frame, text = strings.lang.hide_autorun, command = save_additional_preferences, variable = hide_autorun)
    custom_ui.Checkbutton(additional_options_frame, text = strings.lang.hide_vl_icon, command = save_additional_preferences, variable = hide_vl_icon)
    custom_ui.Checkbutton(additional_options_frame, text = strings.lang.backup_existing_autorun, command = save_additional_preferences, variable = backup_existing_autorun)

    buttons = ttk.Frame(root)
    buttons.pack(fill = "x", pady = (preferences.get_scaled_value(16), 0))
    buttons.columnconfigure([0, 1], weight = 1)

    apply_changes = custom_ui.Button(buttons, width = -1, text = strings.lang.apply_changes, command = modify_volume_info, default = "active")
    apply_changes.grid(row = 0, column = 0, padx = (0, preferences.get_scaled_value(4)), sticky = "ew")
    apply_changes.update()

    reset_changes = custom_ui.Button(buttons, width = -1, text = strings.lang.reset_changes)
    reset_changes.grid(row = 0, column = 1, padx = (preferences.get_scaled_value(4), 0), sticky = "ew")
    reset_changes.update()
    pywinstyles.set_opacity(reset_changes, 0.5)
    
    remove_customizations = custom_ui.Button(buttons, width = -1, text = strings.lang.remove_customizations, command = remove_volume_customizations)
    remove_customizations.grid(row = 1, column = 0, padx = (0, preferences.get_scaled_value(4)), pady = (preferences.get_scaled_value(8), 0), sticky = "ew")
    remove_customizations.update()

    open_autorun = custom_ui.Button(buttons, width = -1, text = strings.lang.open_autorun, command = open_autorun_file)
    open_autorun.grid(row = 1, column = 1, padx = (preferences.get_scaled_value(4), 0), pady = (preferences.get_scaled_value(8), 0), sticky = "ew")
    open_autorun.update()

    buttons.columnconfigure([0, 1], minsize = max(apply_changes.winfo_reqwidth(), reset_changes.winfo_reqwidth(), remove_customizations.winfo_reqwidth(), open_autorun.winfo_reqwidth()))

    settings = ttk.Frame(root)
    settings.pack(anchor = "w", pady = (preferences.get_scaled_value(20), preferences.get_scaled_value(2)), fill = "x")
    settings.pack_propagate(False)
    
    language = custom_ui.Toolbutton(settings, text = "\ue774", link = True, icononly = True, anchor = "n", command = change_app_language, font = ("Segoe UI", 12))
    language.pack(anchor = "nw", side = "left")

    theme = custom_ui.Toolbutton(settings, text = "\ue771", link = True, icononly = True, anchor = "n", command = change_app_theme, font = ("Segoe UI", 12))
    theme.pack(anchor = "nw", side = "left", padx = (preferences.get_scaled_value(4), 0))

    context_menu_integration = custom_ui.Toolbutton(settings, text = "\ue71d", link = True, icononly = True, anchor = "n", command = add_remove_context_menu_entry, font = ("Segoe UI", 12))
    context_menu_integration.pack(anchor = "nw", side = "left", padx = (preferences.get_scaled_value(4), 0))

    if preferences.is_portable: 
        context_menu_integration.configure(state = "disabled", cursor = "")
        context_menu_integration.unbind("<Enter>")
        context_menu_integration.unbind("<Leave>")

    about_app = custom_ui.Toolbutton(settings, text = "\ue946", link = True, icononly = True, anchor = "n", command = about.show, font = ("Segoe UI", 13))
    about_app.pack(anchor = "nw", side = "left", padx = (preferences.get_scaled_value(4), 0))
    
    language.update()
    settings.configure(height = language.winfo_reqwidth())

    ttk.Frame(window, height = 1, style = "StatusBarBd.TFrame").pack(fill = "x", pady = (preferences.get_scaled_value(10), 0))

    status_bar = ttk.Label(
        window, style = "StatusBar.TLabel", 
        padding = (preferences.get_scaled_value(14), preferences.get_scaled_value(7), preferences.get_scaled_value(14), preferences.get_scaled_value(7))
    )
    status_bar.pack(anchor = "w", fill = "x")

    window.update()
    status_bar.configure(wraplength = window.winfo_reqwidth() - preferences.get_scaled_value(28))
    status_bar.configure(text = strings.lang.ready)

    tktooltip.ToolTip(language, strings.lang.change_language, follow = False, delay = 1)
    tktooltip.ToolTip(theme, strings.lang.change_theme, follow = False, delay = 1)
    tktooltip.ToolTip(about_app, strings.lang.about_this_app, follow = False, delay = 1)

    if not preferences.is_portable:
        context_menu_entry.update_context_menu_entry_string()
    
        if context_menu_entry.is_context_menu_entry_added():
            context_menu_integration.configure(default = "active")
            context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_enabled, follow = False, delay = 1)
        else:
            context_menu_integration.configure(default = "normal")
            context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_disabled, follow = False, delay = 1)
    else:
        tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_not_available_portable, follow = False, delay = 1)

    window.update()


def enable_new_icon_pack(event):
    global icon_pack
    icon_pack = os.path.abspath("icons\\storage_types.icl")

    window.unbind("<Shift_L>")
    window.bind("<KeyRelease-Shift_L>", disable_new_icon_pack)


def disable_new_icon_pack(event):
    global icon_pack
    icon_pack = "C:\\Windows\\System32\\shell32.dll"

    window.unbind("<KeyRelease-_L>")
    window.bind("<Shift_L>", enable_new_icon_pack)


def on_app_close():
    if changes_made:
        confirmation = messagebox.askyesnocancel("Volume Labeler", strings.lang.apply_changes_exit, icon = "warning", default = "yes")
        
        if confirmation: 
            modify_volume_info()
            if not changes_made: window.destroy()
        elif confirmation == False:
            window.destroy()
    else:
        window.destroy()


draw_ui()
refresh_volumes_list()

if not app_started and arguments.volume != None:
    if os.path.exists(arguments.volume.upper()) and not volume.is_network_volume(arguments.volume.upper()):
        update_volume_info(arguments.volume.upper())
    elif volume.is_network_volume(arguments.volume.upper()):
        messagebox.showerror(strings.lang.unsupported_volume, strings.lang.unsupported_volume_network)
        window.destroy()
        sys.exit(1)
    else:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)
        window.destroy()
        sys.exit(1)
else:
    select_first_accessible_volume()

app_started = True

custom_ui.sync_colors_with_system(window)

if not ctypes.windll.shell32.IsUserAnAdmin():
    window.deiconify()
    window.focus_set()
    messagebox.showerror(strings.lang.admin_rights_not_granted, strings.lang.admin_rights_not_granted_message)

window.bind("<Shift_L>", enable_new_icon_pack)
window.protocol("WM_DELETE_WINDOW", on_app_close)
window.focus_set()
window.mainloop()