import tkinter as tk, strings, custom_ui, os, traceback, tktooltip, argparse, pywinstyles, sys
from tkinter import ttk, filedialog, messagebox
from utils import volume, icon, preferences, context_menu_entry
from dialogs import change_language, change_theme, about, error
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

os.chdir(os.path.dirname(__file__))
if os.path.exists("icons\\icon.ico"): preferences.internal = ""
else: preferences.internal = "_internal\\"

parser = argparse.ArgumentParser()
parser.add_argument("--volume", default = None, help = "The letter of the volume you want to customize", required = False)
arguments = parser.parse_args()

window = custom_ui.App()
window.title("Volume Labeler")
window.resizable(False, False)
window.configure(padx = preferences.get_scaled_value(14), pady = preferences.get_scaled_value(8))

icon_pack = "C:\\Windows\\System32\\shell32.dll"
show_additional_options = False
icon_old = "default"
selected_volume_old = ""
volumes = [""]
app_started = False
reset_button_enabled = False
selected_volume = tk.StringVar(value = "")
hide_autorun = tk.BooleanVar(value = int(preferences.additional_prefs[0]))
hide_vl_icon = tk.BooleanVar(value = int(preferences.additional_prefs[1]))
backup_existing_autorun = tk.BooleanVar(value = int(preferences.additional_prefs[2]))
icon_type = tk.StringVar(value = "default")


def select_first_accessible_volume():
    for volume in volumes:
        if os.path.exists(volume):
            update_volume_info(volume, True)
            break


def refresh_volumes_list():
    global volumes

    volumes = volume.get_available_drives()

    menu = volume_dropdown["menu"]
    menu.delete(0, "end")

    for string in volumes:
        try: volume_label = volume.get_volume_label_and_icon(string)["label"]
        except: volume_label = volume.get_volume_label(string)

        menu.add_checkbutton(label = f"{volume_label} ({string})", command = lambda value = string: update_volume_info(value), variable = selected_volume, onvalue = string)


def update_volume_info(vol, forced = False):
    global icon_old, selected_volume_old
    selected_volume.set(selected_volume_old)

    if reset_button_enabled and not forced:
        confirmation = messagebox.askyesnocancel("Volume Labeler", strings.lang.apply_changes_change_volume, icon = "warning", default = "yes")
        
        if confirmation: 
            modify_volume_info()
            if reset_button_enabled: return
        elif confirmation == None:
            return

    if os.path.exists(vol):
        selected_volume.set(vol)
        icon_type.set("default")

        choose_icon.configure(text = "  " + strings.lang.choose_icon, image = custom_ui.Icons.icon, width = 0)
        icon_from_image.configure(text = "  " + strings.lang.create_icon_from_image, image = custom_ui.Icons.image, width = 0)

        volume_info = volume.get_volume_label_and_icon(vol)

        if not volume_info["icon_path"] == None:
            icon_type.set("icon")
            process_icon(volume_info["icon_path"], volume_info["icon_index"])

        icon_old = icon_type.get()

        label.delete(0, "end")
        label.insert(0, volume_info["label"])
        disable_undo_button()

        selected_volume_old = selected_volume.get()
    else:
        selected_volume.set(selected_volume_old)
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)


def disable_undo_button():
    global reset_button_enabled
    reset_button_enabled = False

    reset_changes.unbind("<Enter>")
    reset_changes.unbind("<Leave>")
    reset_changes.configure(command = lambda: None, background = custom_ui.Colors.button_bg, activebackground = custom_ui.Colors.button_bg)
    pywinstyles.set_opacity(reset_changes, 0.5)


def enable_undo_button():
    global reset_button_enabled
    reset_button_enabled = True

    reset_changes.bind("<Enter>", lambda event: reset_changes.configure(background = custom_ui.Colors.button_hover))
    reset_changes.bind("<Leave>", lambda event: reset_changes.configure(background = custom_ui.Colors.button_bg))
    reset_changes.configure(command = reset_changes_, background = custom_ui.Colors.button_bg, activebackground = custom_ui.Colors.button_press)
    pywinstyles.set_opacity(reset_changes, 1)


def reset_changes_():
    confirmation = messagebox.askyesno(strings.lang.reset_changes, strings.lang.reset_changes_confirmation, icon = "warning", default = "no")

    if confirmation:
        if os.path.exists(selected_volume.get()):
            update_volume_info(selected_volume.get(), True)
            disable_undo_button()
        else:
            messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)


def modify_volume_info():
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

        disable_undo_button()
        messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
    except PermissionError:
        messagebox.showerror(strings.lang.permission_denied, strings.lang.permission_denied_message)
    except volume.VolumeNotAccessibleError:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)
    except volume.IconNotFoundError:
        messagebox.showerror(strings.lang.error, strings.lang.missing_icon_file)
    except:
        error.show(traceback.format_exc())


def remove_volume_customizations():
    try:
        confirmed = messagebox.askyesno(strings.lang.remove_customizations, strings.lang.remove_customizations_message, icon = "warning", default = "no")

        if confirmed:
            volume.remove_volume_customizations(volume = selected_volume.get(), backup_existing_autorun = backup_existing_autorun.get())
            update_volume_info(selected_volume.get())
            messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
    except volume.VolumeNotAccessibleError:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)
    except PermissionError:
        messagebox.showerror(strings.lang.permission_denied, strings.lang.permission_denied_message)
    except:
        error.show(traceback.format_exc())


def process_icon(path, index):
    global icon_from_image, choose_icon, preview

    icon.extract_icon(path, index)
    preview = tk.PhotoImage(file = preferences.temp + "\\preview.png")

    choose_icon.configure(image = preview, text = f"  {preferences.limit_string(os.path.basename(path))}, {index}")
    icon_from_image.configure(text = "  " + strings.lang.create_icon_from_image, image = custom_ui.Icons.image)


def choose_icon_():
    global preview, icon_old, icon_pack

    match icon_type.get():
        case "default":
            choose_icon.configure(text = "  " + strings.lang.choose_icon, image = custom_ui.Icons.icon)
            icon_from_image.configure(text = "  " + strings.lang.create_icon_from_image, image = custom_ui.Icons.image)

            if not icon_old == icon_type.get() == "default": enable_undo_button()
        case "icon":
            try:
                pywinstyles.change_header_color(window, custom_ui.Colors.bg)
                icon_path, icon_index = icon.pick_icon(window, icon_pack)
                window.set_theme()
                process_icon(icon_path, icon_index)
                enable_undo_button()
            except:
                window.set_theme()
                icon_type.set(icon_old)

            icon_pack = "C:\\Windows\\System32\\shell32.dll"
            window.after(200, lambda: window.bind("<Shift_L>", enable_new_icon_pack))
        case "image":
            image = filedialog.askopenfile(title = strings.lang.choose_image, filetypes = [(strings.lang.images, (".png", ".jpg", ".jpeg", ".bmp", ".gif"))])

            if not image is None:
                icon.convert_image_to_icon(image.name)
                preview = tk.PhotoImage(file = preferences.temp + "\\preview.png")
                
                icon_from_image.configure(image = preview, text = "  " + preferences.limit_string(os.path.basename(image.name)))
                choose_icon.configure(text = "  " + strings.lang.choose_icon, image = custom_ui.Icons.icon, width = 0)
                enable_undo_button()
            else:
                icon_type.set(icon_old)
        
    icon_old = icon_type.get()


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
        
        button_width = apply_changes.winfo_reqwidth() if apply_changes.winfo_reqwidth() >= reset_changes.winfo_reqwidth() else reset_changes.winfo_reqwidth()
        buttons.columnconfigure([0, 1], minsize = button_width)


def change_app_theme():
    old_theme = preferences.theme

    change_theme.show()
    window.wait_window(change_theme.window)

    if old_theme != preferences.theme:
        custom_ui.update_colors()
        window.set_theme()
        custom_ui.update_icons()
        custom_ui.sync_colors(window, update_icons)


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
    global choose_icon, icon_from_image, reset_changes, volume_dropdown, label, show_additional_options, context_menu_integration, context_menu_integration_tooltip, refresh_volumes, additional_options, default_icon, choose_icon, icon_from_image, apply_changes, buttons
    show_additional_options = False
    
    for widget in window.winfo_children(): widget.destroy()
    strings.load_language(preferences.language)

    ttk.Label(window, text = "Volume Labeler", font = ("Segoe UI Semibold", 17)).pack(anchor = "w")

    volume_section = ttk.Frame(window)
    volume_section.pack(fill = "x", anchor = "w", pady = (preferences.get_scaled_value(16), preferences.get_scaled_value(8)))

    ttk.Label(volume_section, text = strings.lang.volume).pack(side = "left")

    refresh_volumes_frame = ttk.Frame(volume_section)
    refresh_volumes_frame.pack(side = "right", padx = (preferences.get_scaled_value(8), 0), fill = "both")

    refresh_volumes = custom_ui.Button(refresh_volumes_frame, command = refresh_volumes_list, text = "\ue72c", font = ("Segoe MDL2 Assets", 8))
    refresh_volumes.pack(fill = "both", expand = True)
    refresh_volumes.configure(padx = preferences.get_scaled_value(7), width = 0)

    tktooltip.ToolTip(refresh_volumes, strings.lang.refresh_volumes_list, follow = False, delay = 1)
    
    volume_dropdown = custom_ui.OptionMenu(volume_section, selected_volume, *volumes)
    volume_dropdown.pack(side = "right")

    ttk.Label(window, text = strings.lang.label).pack(pady = preferences.get_scaled_value(10), anchor = "w")

    def on_label_change():
        enable_undo_button()
        return True

    label_frame = tk.Frame(window, highlightbackground = custom_ui.Colors.entry_bd, highlightcolor = custom_ui.Colors.entry_focus,
                          highlightthickness = 1)
    label_frame.pack(anchor = "w", fill = "x")

    label = tk.Entry(label_frame, width = 40, background = custom_ui.Colors.entry_bg, 
                    foreground = custom_ui.Colors.fg, border = 0, highlightthickness = preferences.get_scaled_value(2), 
                    highlightcolor = custom_ui.Colors.entry_bg, highlightbackground = custom_ui.Colors.entry_bg, 
                    insertbackground = custom_ui.Colors.fg, insertwidth = 1, selectbackground = custom_ui.Colors.entry_select,
                    selectforeground = "#FFFFFF", validate = "key", validatecommand = on_label_change)
    label.pack(fill = "x")
    label.bind("<Button-3>", lambda event: custom_ui.show_entry_context_menu(label))

    ttk.Label(window, text = strings.lang.icon).pack(pady = (preferences.get_scaled_value(16), preferences.get_scaled_value(8)), anchor = "w")

    default_icon = custom_ui.Radiobutton2(window, text = "  " + strings.lang.default_icon, variable = icon_type, value = "default", command = choose_icon_, image = custom_ui.Icons.volume, compound = "left")
    default_icon.pack(anchor = "w", fill = "x", pady = preferences.get_scaled_value(2))

    choose_icon = custom_ui.Radiobutton2(window, text = "  " + strings.lang.choose_icon, variable = icon_type, value = "icon", command = choose_icon_, image = custom_ui.Icons.icon, compound = "left")
    choose_icon.pack(anchor = "w", fill = "x", pady = preferences.get_scaled_value(2))

    icon_from_image = custom_ui.Radiobutton2(window, text = "  " + strings.lang.create_icon_from_image, variable = icon_type, value = "image", image = custom_ui.Icons.image, command = choose_icon_, compound = "left")
    icon_from_image.pack(anchor = "w", fill = "x", pady = preferences.get_scaled_value(2))

    additional_options = custom_ui.Toolbutton(window, text = " " + strings.lang.additional_options, command = lambda: show_hide_additional_options(), anchor = "w", compound = "left", image = custom_ui.Icons.arrow_down)
    additional_options.pack(pady = (preferences.get_scaled_value(14), 0), anchor = "w")
    additional_options.configure(padx = preferences.get_scaled_value(2))

    additional_options_frame = ttk.Frame(window)
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
            additional_options.configure(image = custom_ui.Icons.arrow_up)
        else: 
            additional_options_frame.configure(height = 1)
            additional_options.configure(image = custom_ui.Icons.arrow_down)

    def save_additional_preferences(): 
        preferences.additional_prefs = f"{int(hide_autorun.get())}{int(hide_vl_icon.get())}{int(backup_existing_autorun.get())}"
        preferences.save_settings()

    custom_ui.Checkbutton(additional_options_frame, text = strings.lang.hide_autorun, command = save_additional_preferences, variable = hide_autorun)
    custom_ui.Checkbutton(additional_options_frame, text = strings.lang.hide_vl_icon, command = save_additional_preferences, variable = hide_vl_icon)
    custom_ui.Checkbutton(additional_options_frame, text = strings.lang.backup_existing_autorun, command = save_additional_preferences, variable = backup_existing_autorun)

    buttons = ttk.Frame(window)
    buttons.pack(fill = "x", pady = (preferences.get_scaled_value(16), 0))
    buttons.columnconfigure([0, 1], weight = 1)

    apply_changes = custom_ui.Button(buttons, width = -1, text = strings.lang.apply_changes, command = modify_volume_info, default = "active")
    apply_changes.grid(row = 0, column = 0, padx = (0, preferences.get_scaled_value(4)), sticky = "ew")
    apply_changes.update()

    reset_changes = custom_ui.Button(buttons, width = -1, text = strings.lang.reset_changes)
    reset_changes.grid(row = 0, column = 1, padx = (preferences.get_scaled_value(4), 0), sticky = "ew")
    reset_changes.update()
    pywinstyles.set_opacity(reset_changes, 0.5)
    
    button_width = apply_changes.winfo_reqwidth() if apply_changes.winfo_reqwidth() >= reset_changes.winfo_reqwidth() else reset_changes.winfo_reqwidth()
    buttons.columnconfigure([0, 1], minsize = button_width)

    remove_customizations = custom_ui.Button(window, text = strings.lang.remove_customizations, command = remove_volume_customizations)
    remove_customizations.pack(pady = (preferences.get_scaled_value(8), 0), fill = "x")

    settings = ttk.Frame(window)
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


def update_icons():
    if show_additional_options: additional_options.configure(image = custom_ui.Icons.arrow_up)
    else: additional_options.configure(image = custom_ui.Icons.arrow_down)

    default_icon.configure(image = custom_ui.Icons.volume)

    if choose_icon["text"] == "  " + strings.lang.choose_icon:
        choose_icon.configure(image = custom_ui.Icons.icon)

    if icon_from_image["text"] == "  " + strings.lang.create_icon_from_image:
        icon_from_image.configure(image = custom_ui.Icons.image)


    # A hacky way to force the title bar to redraw on Windows 10
    if sys.getwindowsversion().major == 10 and sys.getwindowsversion().build < 22000:
        dummy_widget = tk.Frame(window)
        dummy_widget.pack()
        window.update_idletasks()
        dummy_widget.destroy()


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
    if reset_button_enabled:
        confirmation = messagebox.askyesnocancel("Volume Labeler", strings.lang.apply_changes_exit, icon = "warning", default = "yes")
        
        if confirmation: 
            modify_volume_info()
            if not reset_button_enabled: window.destroy()
        elif confirmation == False:
            window.destroy()
    else:
        window.destroy()


draw_ui()
refresh_volumes_list()

if not app_started and arguments.volume != None:
    if os.path.exists(arguments.volume.upper()):
        update_volume_info(arguments.volume.upper())
    else:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)
        window.destroy()
        sys.exit(1)
else:
    select_first_accessible_volume()

app_started = True

custom_ui.sync_colors_with_system(window, update_icons)

window.bind("<Shift_L>", enable_new_icon_pack)
window.protocol("WM_DELETE_WINDOW", on_app_close)
window.mainloop()