import tkinter as tk, strings, custom_ui, webbrowser
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from utils import preferences
from dialogs import app_license

strings.load_language(open(preferences.user_preferences + "\\language", "r").read())

def show():
    global arrow, show_os_licenses, show_licenses

    show_os_licenses = False

    window = custom_ui.Toplevel()
    window.title(strings.lang.about_title)
    window.resizable(False, False)
    window.configure(padx = 16, pady = 0)

    icon = tk.PhotoImage(file = f"{preferences.internal}icons\\icon.png")

    def show_hide_licenses():
        global arrow, show_os_licenses
        show_os_licenses = not show_os_licenses

        if show_os_licenses: licenses.pack(pady = 16)
        else: licenses.forget()

        if custom_ui.light_theme: arrow = tk.PhotoImage(file = f"{preferences.internal}icons/dropdown{'_up' if show_os_licenses else ''}_light.png")
        else: arrow = tk.PhotoImage(file = f"{preferences.internal}icons/dropdown{'_up' if show_os_licenses else ''}_dark.png")

        show_licenses.configure(image = arrow)

    app_info = ttk.Frame(window)
    app_info.pack(fill = "x")

    app_icon = tk.Canvas(app_info, width = 63, height = 40, highlightthickness = 0, background = custom_ui.bg)
    app_icon.pack(side = "left", padx = (0, 16), pady = (16, 0))
    app_icon.create_image(0, 0, image = icon, anchor = "nw")

    app_name_and_version = ttk.Frame(app_info)
    app_name_and_version.pack(side = "left")

    ttk.Label(app_name_and_version, text = "Volume Labeler", width = 20, font = ("Segoe UI Semibold", 17)).pack(anchor = "w", pady = (8, 0))
    ttk.Label(app_name_and_version, text = strings.lang.version.replace("%v", "1.0.0 alpha")).pack(anchor = "w")

    if custom_ui.light_theme: arrow = tk.PhotoImage(file = f"{preferences.internal}icons/dropdown_light.png")
    else: arrow = tk.PhotoImage(file = f"{preferences.internal}icons/dropdown_dark.png")

    links = ttk.Frame(window)
    links.pack(fill = "x", pady = (16, 0))

    custom_ui.Toolbutton(links, text = "GitHub", link = True, command = lambda: webbrowser.open("https:\\\\github.com\\Valer100\\Volume-Labeler")).pack(side = "left")
    custom_ui.Toolbutton(links, text = strings.lang.issues, link = True, command = lambda: webbrowser.open("https:\\\\github.com\\Valer100\\Volume-Labeler\\issues")).pack(side = "left", padx = (4, 0))
    custom_ui.Toolbutton(links, text = strings.lang.latest_version, link = True, command = lambda: webbrowser.open("https:\\\\github.com\\Valer100\\Volume-Labeler\\releases\\latest")).pack(side = "left", padx = (4, 0))
    custom_ui.Toolbutton(links, text = strings.lang.license, link = True, command = app_license.show).pack(side = "left", padx = (4, 0))

    buttons = ttk.Frame(window)
    buttons.pack(fill = "x", pady = (16, 16))

    show_licenses = custom_ui.Button(buttons, text = strings.lang.open_source_licenses, command = show_hide_licenses, compound = "left", image = arrow)
    show_licenses.pack(anchor = "w", side = "left")
    show_licenses.configure(width = 0)

    ttk.Button(buttons, text = strings.lang.ok, command = window.destroy, default = "active").pack(side = "right")

    licenses = ScrolledText(window, width = 80, height = 20, wrap = "word", background = custom_ui.entry_bg,
                                 foreground = custom_ui.fg, selectbackground = custom_ui.entry_select,
                                 selectforeground = "#ffffff", highlightthickness = 1, relief = "solid",
                                 highlightbackground = custom_ui.entry_bd, highlightcolor = custom_ui.entry_bd,
                                 border = 0, font = ("Consolas", 10))

    licenses.insert("1.0", open(preferences.internal + "OPEN_SOURCE_LICENSES.txt", "r", encoding = "utf8").read())
    licenses.configure(state = "disabled")

    window.focus_set()
    window.mainloop()