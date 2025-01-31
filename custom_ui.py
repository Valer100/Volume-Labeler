import tkinter as tk, pywinstyles, winaccent, sys, hPyT, threading
from tkinter import ttk

import winaccent._utils
from utils import preferences, icon

def update_colors():
    global light_theme, bg, bg_hover, bg_press, fg, entry_focus, entry_bd, entry_bg, button_bg, button_hover, button_press, button_bd, button_bd_active, tooltip_bg, tooltip_bd, tooltip_fg, accent, accent_link, option_selected, option_bd, entry_select
    light_theme = winaccent.apps_use_light_theme if preferences.theme == "default" else True if preferences.theme == "light" else False

    entry_select = winaccent.accent_normal
    
    if light_theme:
        bg = "#f0f0f0"
        bg_hover = "#e0e0e0"
        bg_press = "#cecece"
        fg = "#000000"
        entry_focus = winaccent.accent_dark
        entry_bd = "#8d8d8d"
        entry_bg = "#ffffff"
        button_bg = "#ffffff"
        button_hover = "#ebebeb"
        button_press = "#dbdbdb"
        button_bd = "#d0d0d0"
        button_bd_active = winaccent.accent_dark
        tooltip_bg = "#ffffff"
        tooltip_bd = "#8f8f8f"
        tooltip_fg = "#505050"
        option_bd = winaccent._utils.blend_colors(winaccent.accent_dark, bg, 70)
        option_selected = winaccent._utils.blend_colors(winaccent.accent_dark, bg, 20)
        accent = winaccent.accent_dark
        accent_link = winaccent.accent_dark_2
    else:
        bg = "#202020"
        bg_hover = "#333333"
        bg_press = "#292929"
        fg = "#ffffff"
        entry_focus = winaccent.accent_light_3
        entry_bd = "#6e6e6e"
        entry_bg = "#404040"
        button_bg = "#333333"
        button_hover = "#454545"
        button_press = "#676767"
        button_bd = "#9b9b9b"
        button_bd_active = winaccent.accent_light_3
        tooltip_bg = "#2b2b2b"
        tooltip_bd = "#747474"
        tooltip_fg = "#ffffff"
        option_bd = winaccent._utils.blend_colors(winaccent.accent_light, bg, 40)
        option_selected = winaccent._utils.blend_colors(winaccent.accent_light, bg, 10)
        accent = winaccent.accent_light
        accent_link = winaccent.accent_light_3

update_colors()


def update_icons():
    global ic_volume, ic_icon, ic_image, ic_arrow_down, ic_arrow_up, ic_system, ic_light_mode, ic_dark_mode, ic_language
    theme = "light" if light_theme else "dark"

    icon.tint_image(preferences.internal + "icons\\volume.png", preferences.internal + "icons\\volume_tinted.png", accent)
    icon.tint_image(preferences.internal + "icons\\icon_custom.png", preferences.internal + "icons\\icon_custom_tinted.png", accent)
    icon.tint_image(preferences.internal + "icons\\image.png", preferences.internal + "icons\\image_tinted.png", accent)
    icon.tint_image(preferences.internal + "icons\\system.png", preferences.internal + "icons\\system_tinted.png", accent)
    icon.tint_image(preferences.internal + "icons\\light_mode.png", preferences.internal + "icons\\light_mode_tinted.png", accent)
    icon.tint_image(preferences.internal + "icons\\dark_mode.png", preferences.internal + "icons\\dark_mode_tinted.png", accent)
    icon.tint_image(preferences.internal + "icons\\language.png", preferences.internal + "icons\\language_tinted.png", accent)

    ic_volume = tk.PhotoImage(file = preferences.internal + "icons\\volume_tinted.png")
    ic_icon = tk.PhotoImage(file = preferences.internal + "icons\\icon_custom_tinted.png")
    ic_image = tk.PhotoImage(file = preferences.internal + "icons\\image_tinted.png")
    ic_system = tk.PhotoImage(file = preferences.internal + "icons\\system_tinted.png")
    ic_light_mode = tk.PhotoImage(file = preferences.internal + "icons\\light_mode_tinted.png")
    ic_dark_mode = tk.PhotoImage(file = preferences.internal + "icons\\dark_mode_tinted.png")
    ic_language = tk.PhotoImage(file = preferences.internal + "icons\\language_tinted.png")
    ic_arrow_down = tk.PhotoImage(file = f"{preferences.internal}icons/dropdown_{theme}.png")
    ic_arrow_up = tk.PhotoImage(file = f"{preferences.internal}icons/dropdown_up_{theme}.png")


class CommandLink(tk.Frame):
    def __init__(self, master, text: str = "", command: callable = None, *args, **kwargs):
        super().__init__(master, padx = 8, pady = 8, background = bg, *args, **kwargs)

        ver = sys.getwindowsversion()

        if ver.major == 10 and ver.build >= 22000:
            self.arrow = ttk.Label(self, text = "\ue651  ", font = ("Segoe Fluent Icons", 11), padding = (0, 4, 0, 0), foreground = accent_link)
        else:
            self.arrow = ttk.Label(self, text = "\ue0ad  ", font = ("Segoe MDL2 Assets", 11), padding = (0, 4, 0, 0), foreground = accent_link)
        
        self.arrow.pack(side = "left", anchor = "w")

        self.text = ttk.Label(self, text = text, font = ("Segoe UI Semibold", 11), foreground = accent_link)
        self.text.pack(side = "left", anchor = "w")

        is_touched = False

        def on_enter(event):
            global is_touched
            is_touched = True

            self.configure(background = bg_hover)
            self.arrow.configure(background = bg_hover, foreground = accent_link)
            self.text.configure(background = bg_hover, foreground = accent_link)

        def on_leave(event):
            global is_touched
            is_touched = False

            self.configure(background = bg)
            self.arrow.configure(background = bg, foreground = accent_link)
            self.text.configure(background = bg, foreground = accent_link)

        def on_click(event):
            global is_touched
            is_touched = True

            self.configure(background = bg_press)
            self.arrow.configure(background = bg_press, foreground = accent)
            self.text.configure(background = bg_press, foreground = accent)

        def on_click_release(event):
            global is_touched

            self.configure(background = bg_hover)
            self.arrow.configure(background = bg_hover, foreground = accent_link)
            self.text.configure(background = bg_hover, foreground = accent_link)

            if not command is None and is_touched: command(); is_touched = False

        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)
        self.bind("<Button-1>", on_click)
        self.bind("<ButtonRelease-1>", on_click_release)

        self.arrow.bind("<Enter>", on_enter)
        self.arrow.bind("<Leave>", on_leave)
        self.arrow.bind("<Button-1>", on_click)
        self.arrow.bind("<ButtonRelease-1>", on_click_release)

        self.text.bind("<Enter>", on_enter)
        self.text.bind("<Leave>", on_leave)
        self.text.bind("<Button-1>", on_click)
        self.text.bind("<ButtonRelease-1>", on_click_release)

    def update_colors(self):
        self["background"] = bg
        self.arrow["background"] = bg
        self.text["background"] = bg

        self.arrow["foreground"] = accent_link
        self.text["foreground"] = accent_link


class Toolbutton(tk.Button):
    def __init__(self, master, text: str = "", command: callable = None, link: bool = False, icononly: bool = False, *args, **kwargs):
        super().__init__(master, text = text, command = command, padx = 2 if icononly else 4, pady = 2, background = bg, 
                         foreground = accent_link if link else fg, border = 0, relief = "solid", 
                         activebackground = bg_press, activeforeground = accent if link else fg,
                         cursor = "hand2" if link and not icononly else "", highlightbackground = option_bd, 
                         highlightcolor = option_bd, *args, **kwargs)

        self.link = link

        if icononly: self.configure(width = 2)

        if self["default"] == "active" and (self["background"] != option_selected and self["background"] != bg_hover and self["background"] != bg_press):
            self.configure(background = option_selected)

        self.bind("<Enter>", lambda event: self.configure(background = bg_hover))
        self.bind("<Leave>", lambda event: self.configure(background = bg))

    def configure(self, *args, **kwargs):
        super().configure(*args, **kwargs)

        if self["default"] == "active" and (self["background"] != option_selected and self["background"] != bg_hover and self["background"] != bg_press):
            self.configure(background = option_selected)

    def update_colors(self):
        self.configure(background = bg, foreground = accent_link if self.link else fg, activebackground = bg_press, 
                       activeforeground = accent if self.link else fg, highlightbackground = option_bd, 
                       highlightcolor = option_bd)
        
        if self["default"] == "active" and (self["background"] != option_selected and self["background"] != bg_hover and self["background"] != bg_press):
            self.configure(background = option_selected)


class Button(tk.Button):
    def __init__(self, master, text: str = "", command: callable = None, *args, **kwargs):
        super().__init__(master, text = text, command = command, padx = 4, pady = 3, background = button_bg, 
                         foreground = fg, border = 0, relief = "solid", activebackground = button_press, 
                         activeforeground = fg, highlightthickness = 1, highlightbackground = button_bd,
                         highlightcolor = button_bd, *args, **kwargs)

        if self["width"] == 0:
            if len(self["text"]) >= 10: self.configure(width = len(self["text"]))
            else: self.configure(width = 10)

        if self["default"] == "active": 
            self.configure(highlightbackground = button_bd_active, highlightcolor = button_bd_active)
            self.is_active = True
        else: 
            self.configure(default = "active")
            self.is_active = False

        self.bind("<Enter>", lambda event: self.configure(background = button_hover))
        self.bind("<Leave>", lambda event: self.configure(background = button_bg))

    def update_colors(self):
        self.configure(background = button_bg, foreground = fg, activebackground = button_press, 
                       activeforeground = fg, highlightbackground = button_bd_active if self.is_active else button_bd, 
                       highlightcolor = button_bd_active if self.is_active else button_bd)

ttk.Button = Button


class OptionMenu(tk.OptionMenu):
    def __init__(self, master, variable, value, *values):
        super().__init__(master, variable, value, *values)

        self.configure(background = button_bg, foreground = fg, activebackground = button_hover, 
                       activeforeground = fg, highlightbackground = button_bd, highlightcolor = button_bd, 
                       image = ic_arrow_down, compound = "right", indicatoron = False, border = 0, relief = "solid", 
                       highlightthickness = 1, pady = 4, padx = 7)
        
        self["menu"].configure(activebackground = winaccent.accent_normal)

    def update_colors(self):
        self.configure(background = button_bg, foreground = fg, activebackground = button_hover, 
                       activeforeground = fg, highlightbackground = button_bd, highlightcolor = button_bd, 
                       image = ic_arrow_down)

        self["menu"].configure(activebackground = winaccent.accent_normal)


class Radiobutton2(tk.Radiobutton):
    def __init__(self, master, variable: tk.StringVar, value: str, *args, **kwargs):
        self.variable = variable
        self.value = value

        super().__init__(master, variable = variable, value = value, background = bg, foreground = fg, 
                         activebackground = bg_press, activeforeground = fg, indicatoron = False, 
                         border = 0, relief = "solid", selectcolor = option_selected, anchor = "w",
                         *args, **kwargs)

        self.master.configure(highlightthickness = 1)

        self.bind("<Enter>", lambda event: self.configure(background = bg_hover, selectcolor = bg_hover))
        self.bind("<Leave>", lambda event: self.configure(background = bg, selectcolor = option_selected))

        def on_value_change(var = None, index = None, mode = None):
            try:
                if variable.get() == value:
                    self.master.configure(highlightcolor = option_bd, highlightbackground = option_bd)
                else:
                    self.master.configure(highlightcolor = bg, highlightbackground = bg)
            except:
                pass

        variable.trace_add("write", on_value_change)
        on_value_change()

    def update_colors(self):
        self.configure(background = bg, foreground = fg, activebackground = bg_press, activeforeground = fg,
                       relief = "solid", selectcolor = option_selected)
        
        if self.variable.get() == self.value:
            self.master.configure(highlightcolor = option_bd, highlightbackground = option_bd)
        else:
            self.master.configure(highlightcolor = bg, highlightbackground = bg)


class App(tk.Tk):
    def set_theme(self):
        pywinstyles.apply_style(self, "light" if light_theme else "dark")
        pywinstyles.change_header_color(self, bg)

        style = ttk.Style()
        style.configure(".", background = bg, foreground = fg)
        self.configure(background = bg)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.withdraw()

        self.iconbitmap(default = preferences.internal + "icon.ico")
        self.update()
        self.set_theme()
        update_icons()

    def resizable(self, width: bool = None, height: bool = None):
        value = super().resizable(width, height)
        self.set_theme()

        return value
    
    def mainloop(self, n = 0):
        self.deiconify()
        super().mainloop(n)


class Toplevel(tk.Toplevel):
    def set_titlebar_theme(self):
        self.update()
        self.configure(background = bg)

        pywinstyles.apply_style(self, "light" if light_theme else "dark")
        pywinstyles.change_header_color(self, bg)

        hPyT.maximize_minimize_button.hide(self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.withdraw()

        self.grab_set()
        self.focus_set()
        self.bind("<Escape>", lambda event: self.destroy())
        self.set_titlebar_theme()

    def resizable(self, width: bool = None, height: bool = None):
        value = super().resizable(width, height)
        self.set_titlebar_theme()
        self.deiconify()

        return value
    

def sync_colors(window, callback):
    update_colors()

    if not callback is None: 
        update_icons()
        callback()

    if isinstance(window, App): window.set_theme()
    elif isinstance(window, Toplevel): window.set_titlebar_theme()

    for widget in window.winfo_children():
        if isinstance(widget, (CommandLink, Toolbutton, Button, OptionMenu, Radiobutton2)):
            widget.update_colors()
        elif isinstance(widget, tk.Entry):
            widget.configure(background = entry_bg, foreground = fg, highlightcolor = entry_bg, highlightbackground = entry_bg, insertbackground = fg, selectbackground = entry_select)
            widget.master.configure(highlightbackground = entry_bd, highlightcolor = entry_focus)
        elif isinstance(widget, tk.Canvas):
            widget.configure(background = bg)
        elif isinstance(widget, (Toplevel, ttk.Frame, tk.Frame)):
            sync_colors(widget, None)

def sync_colors_with_system(window, callback = None): 
    threading.Thread(target = lambda: winaccent.on_appearance_changed(lambda: sync_colors(window, callback)), daemon = True).start()