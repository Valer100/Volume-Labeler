import tkinter as tk, pywinstyles, winaccent, sys, hPyT, threading, strings, warnings
from tkinter import ttk
from utils import preferences, icon

class Colors(): pass
class Icons(): pass


def update_colors():
    Colors.light_theme = winaccent.apps_use_light_theme if preferences.theme == "default" else True if preferences.theme == "light" else False
    Colors.entry_select = winaccent.accent_normal
    
    if Colors.light_theme:
        Colors.bg = "#f0f0f0"
        Colors.bg_hover = "#e0e0e0"
        Colors.bg_press = "#cecece"
        Colors.fg = "#000000"
        Colors.entry_focus = winaccent.accent_dark
        Colors.entry_bd = "#8d8d8d"
        Colors.entry_bg = "#ffffff"
        Colors.button_bg = "#ffffff"
        Colors.button_hover = "#ebebeb"
        Colors.button_press = "#dbdbdb"
        Colors.button_bd = "#d0d0d0"
        Colors.button_bd_active = winaccent.accent_dark
        Colors.tooltip_bg = "#ffffff"
        Colors.tooltip_bd = "#767676"
        Colors.tooltip_fg = "#575757"
        Colors.selection_bd = winaccent._utils.blend_colors(winaccent.accent_dark, Colors.bg, 70)
        Colors.selection = winaccent._utils.blend_colors(winaccent.accent_dark, Colors.bg, 20)
        Colors.selection_hover = winaccent._utils.blend_colors(winaccent.accent_dark, Colors.bg, 30)
        Colors.selection_press = winaccent._utils.blend_colors(winaccent.accent_dark, Colors.bg, 40)
        Colors.input_unchecked = "#404040"
        Colors.input_hover = "#808080"
        Colors.input_press = "#afafaf"
        Colors.accent = winaccent.accent_dark
        Colors.accent_hover = winaccent._utils.blend_colors(Colors.accent, Colors.bg, 90)
        Colors.accent_press = winaccent._utils.blend_colors(Colors.accent, Colors.bg, 80)
        Colors.accent_link = winaccent.accent_dark_2
    else:
        Colors.bg = "#202020"
        Colors.bg_hover = "#333333"
        Colors.bg_press = "#292929"
        Colors.fg = "#ffffff"
        Colors.entry_focus = winaccent.accent_light_3
        Colors.entry_bd = "#6e6e6e"
        Colors.entry_bg = "#404040"
        Colors.button_bg = "#333333"
        Colors.button_hover = "#454545"
        Colors.button_press = "#676767"
        Colors.button_bd = "#9b9b9b"
        Colors.button_bd_active = winaccent.accent_light_3
        Colors.tooltip_bg = "#2b2b2b"
        Colors.tooltip_bd = "#747474"
        Colors.tooltip_fg = "#ffffff"
        Colors.selection_bd = winaccent._utils.blend_colors(winaccent.accent_light, Colors.bg, 40)
        Colors.selection = winaccent._utils.blend_colors(winaccent.accent_light, Colors.bg, 10)
        Colors.selection_hover = winaccent._utils.blend_colors(winaccent.accent_light, Colors.bg, 15)
        Colors.selection_press = winaccent._utils.blend_colors(winaccent.accent_light, Colors.bg, 20)
        Colors.input_unchecked = "#404040"
        Colors.input_hover = "#4f4f4f"
        Colors.input_press = "#5f5f5f"
        Colors.accent = winaccent.accent_light
        Colors.accent_hover = winaccent._utils.blend_colors(Colors.accent, Colors.bg, 80)
        Colors.accent_press = winaccent._utils.blend_colors(Colors.accent, Colors.bg, 60)
        Colors.accent_link = winaccent.accent_light_3

update_colors()


def update_icons():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message = "Image was not the expected size", category = UserWarning, module = "PIL")
        
        Icons.app_about = icon.extract_and_tint_icon(preferences.internal + "icons\\icon_about.ico", None, 63)
        Icons.volume = icon.extract_and_tint_icon(preferences.internal + "icons\\volume.ico", Colors.accent, 32)
        Icons.icon = icon.extract_and_tint_icon(preferences.internal + "icons\\icon_custom.ico", Colors.accent, 32)
        Icons.image = icon.extract_and_tint_icon(preferences.internal + "icons\\image.ico", Colors.accent, 32)
        Icons.arrow_up = icon.extract_and_tint_icon(preferences.internal + "icons\\arrow_up.ico", Colors.fg, 9)
        Icons.arrow_down = icon.extract_and_tint_icon(preferences.internal + "icons\\arrow_down.ico", Colors.fg, 9)


class CommandLink(tk.Frame):
    def __init__(self, master, text: str = "", command: callable = None, *args, **kwargs):
        super().__init__(master, padx = 8, pady = 8, background = Colors.bg, *args, **kwargs)

        if sys.getwindowsversion().major == 10 and sys.getwindowsversion().build >= 22000:
            self.arrow = ttk.Label(self, text = "\ue651  ", font = ("Segoe Fluent Icons", 11), padding = (0, 4, 0, 0), foreground = Colors.accent_link)
        else:
            self.arrow = ttk.Label(self, text = "\ue0ad  ", font = ("Segoe MDL2 Assets", 11), padding = (0, 4, 0, 0), foreground = Colors.accent_link)
        
        self.arrow.pack(side = "left", anchor = "w")

        self.text = ttk.Label(self, text = text, font = ("Segoe UI Semibold", 11), foreground = Colors.accent_link)
        self.text.pack(side = "left", anchor = "w")

        is_touched = False

        def on_enter(event):
            global is_touched
            is_touched = True

            self.configure(background = Colors.bg_hover)
            self.arrow.configure(background = Colors.bg_hover, foreground = Colors.accent_link)
            self.text.configure(background = Colors.bg_hover, foreground = Colors.accent_link)

        def on_leave(event):
            global is_touched
            is_touched = False

            self.configure(background = Colors.bg)
            self.arrow.configure(background = Colors.bg, foreground = Colors.accent_link)
            self.text.configure(background = Colors.bg, foreground = Colors.accent_link)

        def on_click(event):
            global is_touched
            is_touched = True

            self.configure(background = Colors.bg_press)
            self.arrow.configure(background = Colors.bg_press, foreground = Colors.accent)
            self.text.configure(background = Colors.bg_press, foreground = Colors.accent)

        def on_click_release(event):
            global is_touched

            self.configure(background = Colors.bg_hover)
            self.arrow.configure(background = Colors.bg_hover, foreground = Colors.accent_link)
            self.text.configure(background = Colors.bg_hover, foreground = Colors.accent_link)

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
        self["background"] = Colors.bg
        self.arrow["background"] = Colors.bg
        self.text["background"] = Colors.bg

        self.arrow["foreground"] = Colors.accent_link
        self.text["foreground"] = Colors.accent_link


class Toolbutton(tk.Button):
    color_exceptions = (Colors.selection, Colors.selection_hover, Colors.selection_press, Colors.bg_hover, Colors.bg_press)

    def __init__(self, master, text: str = "", command: callable = None, link: bool = False, icononly: bool = False, *args, **kwargs):
        super().__init__(
            master, text = text, command = command, padx = preferences.get_scaled_value(2) if icononly else 4, pady = 2, background = Colors.bg, 
            foreground = Colors.accent_link if link else Colors.fg, border = 0, relief = "solid", 
            activebackground = Colors.bg_press, activeforeground = Colors.accent if link else Colors.fg,
            cursor = "hand2" if link else "", highlightbackground = Colors.selection_bd, 
            highlightcolor = Colors.selection_bd, *args, **kwargs
        )

        self.link = link

        if icononly: self.configure(width = 2)

        if self["default"] == "active" and self["background"] not in self.color_exceptions:
            self.configure(background = Colors.selection, activebackground = Colors.selection_press)

        self.bind("<Enter>", lambda event: self.configure(background = Colors.selection_hover if self["default"] == "active" else Colors.bg_hover, activebackground = Colors.selection_press if self["default"] == "active" else Colors.bg_press))
        self.bind("<Leave>", lambda event: self.configure(background = Colors.selection if self["default"] == "active" else Colors.bg))

    def configure(self, *args, **kwargs):
        default_old = self["default"]
        super().configure(*args, **kwargs)

        if self["default"] == "active" and self["background"] not in self.color_exceptions:
            self.configure(background = Colors.selection, activebackground = Colors.selection_press)
        
        if self["default"] != default_old and self["default"] == "normal":
            self.configure(background = Colors.bg, activebackground = Colors.bg_press)


    def update_colors(self):
        self.color_exceptions = (Colors.selection, Colors.selection_hover, Colors.selection_press, Colors.bg_hover, Colors.bg_press)
        
        self.configure(
            background = Colors.bg, foreground = Colors.accent_link if self.link else Colors.fg, activebackground = Colors.bg_press, 
            activeforeground = Colors.accent if self.link else Colors.fg, highlightbackground = Colors.selection_bd, 
            highlightcolor = Colors.selection_bd
        )
        
        if self["default"] == "active" and self["background"] not in self.color_exceptions:
            self.configure(background = Colors.selection, activebackground = Colors.selection_press)


class Button(tk.Button):
    def __init__(self, master, text: str = "", command: callable = None, *args, **kwargs):
        super().__init__(
            master, text = text, command = command, padx = 4, pady = 3, background = Colors.button_bg, 
            foreground = Colors.fg, border = 0, relief = "solid", activebackground = Colors.button_press, 
            activeforeground = Colors.fg, highlightthickness = 1, highlightbackground = Colors.button_bd,
            highlightcolor = Colors.button_bd, *args, **kwargs
        )

        if self["width"] == 0:
            if len(self["text"]) >= 10: self.configure(width = len(self["text"]))
            else: self.configure(width = 10)

        if self["default"] == "active": 
            self.configure(highlightbackground = Colors.button_bd_active, highlightcolor = Colors.button_bd_active)
            self.is_active = True
        else: 
            self.configure(default = "active")
            self.is_active = False

        self.bind("<Enter>", lambda event: self.configure(background = Colors.button_hover))
        self.bind("<Leave>", lambda event: self.configure(background = Colors.button_bg))
    
    def update_colors(self):
        self.configure(
            background = Colors.button_bg, foreground = Colors.fg, activebackground = Colors.button_press, 
            activeforeground = Colors.fg, highlightbackground = Colors.button_bd_active if self.is_active else Colors.button_bd,
            highlightcolor = Colors.button_bd_active if self.is_active else Colors.button_bd
        )


class OptionMenu(tk.OptionMenu):
    def __init__(self, master, variable, value, *values):
        super().__init__(master, variable, value, *values)

        self.configure(
            background = Colors.button_bg, foreground = Colors.fg, activebackground = Colors.button_hover, 
            activeforeground = Colors.fg, highlightbackground = Colors.button_bd, highlightcolor = Colors.fg, 
            image = Icons.arrow_down, compound = "right", indicatoron = False, border = 0, relief = "solid", 
            highlightthickness = 1, pady = preferences.get_scaled_value(5), padx = preferences.get_scaled_value(7), 
            takefocus = True
        )

        self["menu"].configure(activebackground = winaccent.accent_normal)

        def open_option_menu(event):
            self["menu"].post(self.winfo_rootx(), self.winfo_rooty() + self.winfo_height())
            return "break"
        
        self.bind("<space>", open_option_menu)

    def update_colors(self):
        self.configure(
            background = Colors.button_bg, foreground = Colors.fg, activebackground = Colors.button_hover, 
            activeforeground = Colors.fg, highlightbackground = Colors.button_bd, highlightcolor = Colors.fg, 
            image = Icons.arrow_down
        )

        self["menu"].configure(activebackground = winaccent.accent_normal)


class Checkbutton(tk.Frame):
    touching = False

    def __init__(self, master, text: str = "", variable: tk.BooleanVar = None, command: callable = None):
        super().__init__(master, takefocus = True, background = Colors.bg, highlightthickness = 1, highlightbackground = Colors.bg, highlightcolor = Colors.fg)

        self.variable = variable
        self.command = command

        self.checkbox = ttk.Frame(self)
        self.checkbox.pack(side = "left", pady = (preferences.get_scaled_value(2), 0))
        self.checkbox.pack_propagate(False)

        self.checkbox_glyph = tk.Label(
            self.checkbox, text = "\ue73d" if variable.get() else "\ue739", font = ("Segoe UI", 10), 
            background = Colors.bg, foreground = Colors.accent if variable.get() else Colors.input_unchecked, 
            padx = 0, pady = 0
        )

        self.checkbox_glyph.pack(side = "left")
        self.checkbox_glyph.update()
        self.checkbox.configure(width = self.checkbox_glyph.winfo_reqwidth(), height = self.checkbox_glyph.winfo_reqwidth())

        self.text = ttk.Label(self, text = text, padding = (preferences.get_scaled_value(2), 0, 0, 0))
        self.text.pack(side = "left")

        self.bind("<Button-1>", lambda event: self.checkbox_glyph.configure(foreground = Colors.accent_press if self.variable.get() else Colors.input_press))
        self.checkbox.bind("<Button-1>", lambda event: self.checkbox_glyph.configure(foreground = Colors.accent_press if self.variable.get() else Colors.input_press))
        self.checkbox_glyph.bind("<Button-1>", lambda event: self.checkbox_glyph.configure(foreground = Colors.accent_press if self.variable.get() else Colors.input_press))
        self.text.bind("<Button-1>", lambda event: self.checkbox_glyph.configure(foreground = Colors.accent_press if self.variable.get() else Colors.input_press))

        self.bind("<ButtonRelease-1>", self.invoke)
        self.checkbox.bind("<ButtonRelease-1>", self.invoke)
        self.checkbox_glyph.bind("<ButtonRelease-1>", self.invoke)
        self.text.bind("<ButtonRelease-1>", self.invoke)

        def on_enter(event): 
            self.touching = True
            self.checkbox_glyph.configure(foreground = Colors.accent_hover if self.variable.get() else Colors.input_hover)

        def on_leave(event): 
            self.touching = False
            self.checkbox_glyph.configure(foreground = Colors.accent if self.variable.get() else Colors.input_unchecked)

        self.bind("<Enter>", on_enter)
        self.checkbox.bind("<Enter>", on_enter)
        self.checkbox_glyph.bind("<Enter>", on_enter)
        self.text.bind("<Enter>", on_enter)

        self.bind("<Leave>", on_leave)
        self.checkbox.bind("<Leave>", on_leave)
        self.checkbox_glyph.bind("<Leave>", on_leave)
        self.text.bind("<Leave>", on_leave)

        def invoke_with_keyboard(event):
            if self.focus_get():
                self.touching = True
                self.invoke(event)
                self.touching = False

        self.bind("<space>", invoke_with_keyboard)
        self.variable.trace_add("write", self.on_value_change)

    def __getitem__(self, key):
        if key == "text": return self.text["text"]
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key == "text": self.text["text"] = value
        else: super().__setitem__(key, value)

    def invoke(self, event: tk.Event = None):
        if (event != None and self.touching) or event == None:
            self.variable.set(not self.variable.get())

        self.checkbox_glyph.configure(
            text = "\ue73d" if self.variable.get() else "\ue739", 
            foreground = Colors.accent if self.variable.get() else Colors.input_unchecked
        )

        if self.command != None: self.command()

    def on_value_change(self, var = None, index = None, mode = None):
        self.checkbox_glyph.configure(
            text = "\ue73d" if self.variable.get() else "\ue739", 
            foreground = Colors.accent if self.variable.get() else Colors.input_unchecked
        )

    def update_colors(self):
        self.configure(background = Colors.bg, highlightbackground = Colors.bg, highlightcolor = Colors.fg)
        self.checkbox_glyph.configure(background = Colors.bg, foreground = Colors.accent if self.variable.get() else Colors.input_unchecked)


class Radiobutton(tk.Frame):
    touching = False

    def __init__(self, master, text: str = "", variable = None, value = "", command: callable = None):
        super().__init__(master, takefocus = True, background = Colors.bg, highlightthickness = 1, highlightbackground = Colors.bg, highlightcolor = Colors.fg)

        self.variable = variable
        self.value = value
        self.command = command

        self.radiobutton = ttk.Frame(self)
        self.radiobutton.pack(side = "left", pady = (preferences.get_scaled_value(2), 0))
        self.radiobutton.pack_propagate(False)

        self.radiobutton_glyph = tk.Label(
            self.radiobutton, text = "\ueccb" if variable.get() == self.value else "\uecca", font = ("Segoe UI", 10), 
            background = Colors.bg, foreground = Colors.accent if variable.get() == self.value else Colors.input_unchecked, 
            padx = 0, pady = 0
        )

        self.radiobutton_glyph.pack(side = "left")
        self.radiobutton_glyph.update()
        self.radiobutton.configure(width = self.radiobutton_glyph.winfo_reqwidth(), height = self.radiobutton_glyph.winfo_reqwidth())

        self.text = ttk.Label(self, text = text, padding = (preferences.get_scaled_value(2), 0, 0, 0))
        self.text.pack(side = "left")

        self.bind("<Button-1>", lambda event: self.radiobutton_glyph.configure(foreground = Colors.accent_press if self.variable.get() == self.value else Colors.input_press))
        self.radiobutton.bind("<Button-1>", lambda event: self.radiobutton_glyph.configure(foreground = Colors.accent_press if self.variable.get() == self.value else Colors.input_press))
        self.radiobutton_glyph.bind("<Button-1>", lambda event: self.radiobutton_glyph.configure(foreground = Colors.accent_press if self.variable.get() == self.value else Colors.input_press))
        self.text.bind("<Button-1>", lambda event: self.radiobutton_glyph.configure(foreground = Colors.accent_press if self.variable.get() == self.value else Colors.input_press))

        self.bind("<ButtonRelease-1>", self.invoke)
        self.radiobutton.bind("<ButtonRelease-1>", self.invoke)
        self.radiobutton_glyph.bind("<ButtonRelease-1>", self.invoke)
        self.text.bind("<ButtonRelease-1>", self.invoke)

        def on_enter(event): 
            self.touching = True
            self.radiobutton_glyph.configure(foreground = Colors.accent_hover if self.variable.get() == self.value else Colors.input_hover)

        def on_leave(event): 
            self.touching = False
            self.radiobutton_glyph.configure(foreground = Colors.accent if self.variable.get() == self.value else Colors.input_unchecked)

        self.bind("<Enter>", on_enter)
        self.radiobutton.bind("<Enter>", on_enter)
        self.radiobutton_glyph.bind("<Enter>", on_enter)
        self.text.bind("<Enter>", on_enter)

        self.bind("<Leave>", on_leave)
        self.radiobutton.bind("<Leave>", on_leave)
        self.radiobutton_glyph.bind("<Leave>", on_leave)
        self.text.bind("<Leave>", on_leave)

        def invoke_with_keyboard(event):
            if self.focus_get():
                self.touching = True
                self.invoke(event)
                self.touching = False

        self.bind("<space>", invoke_with_keyboard)
        self.variable.trace_add("write", self.on_value_change)

    def __getitem__(self, key):
        if key == "text": return self.text["text"]
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key == "text": self.text["text"] = value
        else: super().__setitem__(key, value)

    def invoke(self, event: tk.Event = None):
        if (event != None and self.touching) or event == None:
            self.variable.set(self.value)

        self.radiobutton_glyph.configure(
            text = "\ueccb" if self.variable.get() == self.value else "\uecca", 
            foreground = Colors.accent if self.variable.get() == self.value else Colors.input_unchecked
        )

        if self.command != None: self.command()

    def on_value_change(self, var = None, index = None, mode = None):
        self.radiobutton_glyph.configure(
            text = "\ueccb" if self.variable.get() == self.value else "\uecca", 
            foreground = Colors.accent if self.variable.get() == self.value else Colors.input_unchecked
        )

    def update_colors(self):
        self.configure(background = Colors.bg, highlightbackground = Colors.bg, highlightcolor = Colors.fg)
        self.radiobutton_glyph.configure(background = Colors.bg, foreground = Colors.accent if self.variable.get() == self.value else Colors.input_unchecked)


class Radiobutton2(tk.Frame):
    def __init__(self, master, variable: tk.StringVar, value: str, *args, **kwargs):
        self.variable = variable
        self.value = value

        super().__init__(master, highlightthickness = 1, highlightcolor = Colors.fg, takefocus = True)
        self.bind("<space>", lambda event: self.radio.invoke())

        self.radio = tk.Radiobutton(
            self, variable = variable, value = value, background = Colors.bg, foreground = Colors.fg, 
            activebackground = Colors.bg_press, activeforeground = Colors.fg, indicatoron = False, 
            border = 0, relief = "solid", selectcolor = Colors.selection, anchor = "w",
            takefocus = False, *args, **kwargs
        )

        self.radio.pack(anchor = "w", fill = "x")

        self.radio.bind("<Enter>", lambda event: self.configure(background = Colors.bg_hover, selectcolor = Colors.selection_hover if variable.get() == value else Colors.bg_hover))
        self.radio.bind("<Leave>", lambda event: self.configure(background = Colors.bg, selectcolor = Colors.selection))

        def on_value_change(var = None, index = None, mode = None):
            try: 
                self.configure(background = Colors.bg, selectcolor = Colors.selection)
                self.config(highlightbackground = Colors.selection_bd if self.variable.get() == self.value else Colors.bg)
                self.radio.config(activebackground = Colors.selection_press if self.variable.get() == self.value else Colors.bg_press)
            except: 
                pass

        variable.trace_add("write", on_value_change)
        on_value_change()

    def configure(self, highlightcolor: str = None, highlightbackground: str = None, *args, **kwargs):
        return self.radio.configure(*args, **kwargs)

    def __getitem__(self, key):
        return self.radio.__getitem__(key)

    def __setitem__(self, key, value):
        self.radio.__setitem__(key, value)

    def update_colors(self):
        self.radio.configure(
            background = Colors.bg, foreground = Colors.fg, activeforeground = Colors.fg, relief = "solid", selectcolor = Colors.selection,
            activebackground = Colors.selection_press if self.variable.get() == self.value else Colors.bg_press
        )
        
        self.config(highlightcolor = Colors.fg, highlightbackground = Colors.selection_bd if self.variable.get() == self.value else Colors.bg)
        self.radio.config()


class App(tk.Tk):
    def set_theme(self):
        pywinstyles.apply_style(self, "light" if Colors.light_theme else "dark")
        pywinstyles.change_header_color(self, winaccent.titlebar_active if winaccent.is_titlebar_colored and self.focus_get() else Colors.bg)

        self.bind("<FocusIn>", lambda event: pywinstyles.change_header_color(self, winaccent.titlebar_active if winaccent.is_titlebar_colored else Colors.bg))
        self.bind("<FocusOut>", lambda event: pywinstyles.change_header_color(self, Colors.bg))

        style = ttk.Style()
        style.configure(".", background = Colors.bg, foreground = Colors.fg)
        self.configure(background = Colors.bg)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.withdraw()

        self.iconbitmap(default = preferences.internal + "icons\\icon.ico")
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
        self.configure(background = Colors.bg)

        pywinstyles.apply_style(self, "light" if Colors.light_theme else "dark")
        pywinstyles.change_header_color(self, winaccent.titlebar_active if winaccent.is_titlebar_colored and self.focus_get() else Colors.bg)

        self.bind("<FocusIn>", lambda event: pywinstyles.change_header_color(self, winaccent.titlebar_active if winaccent.is_titlebar_colored else Colors.bg))
        self.bind("<FocusOut>", lambda event: pywinstyles.change_header_color(self, Colors.bg))

        hPyT.maximize_minimize_button.hide(self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.withdraw()
        self.master.unbind("<FocusIn>")

        self.transient(self.master)
        self.focus_set()
        self.geometry(f"+{self.master.winfo_x() + preferences.get_scaled_value(50)}+{self.master.winfo_y()+ preferences.get_scaled_value(50)}")
        
        self.after(100, lambda: self.master.wm_attributes("-disabled", True))
        self.after(100, lambda: self.master.bind("<FocusIn>", lambda event: pywinstyles.change_header_color(self.master, winaccent.titlebar_active if winaccent.is_titlebar_colored else Colors.bg)))

        self.bind("<Escape>", lambda event: self.destroy())
        self.set_titlebar_theme()

    def resizable(self, width: bool = None, height: bool = None):
        value = super().resizable(width, height)
        self.set_titlebar_theme()
        self.deiconify()

        return value
    
    def destroy(self):
        self.master.wm_attributes("-disabled", False)
        super().destroy()


def sync_colors(window, callback):
    update_colors()

    if not callback is None: 
        update_icons()
        callback()

    if isinstance(window, App): window.set_theme()
    elif isinstance(window, Toplevel): window.set_titlebar_theme()

    for widget in window.winfo_children():
        if isinstance(widget, (CommandLink, Toolbutton, Button, OptionMenu, Checkbutton, Radiobutton, Radiobutton2)):
            widget.update_colors()
        elif isinstance(widget, tk.Entry):
            widget.configure(background = Colors.entry_bg, foreground = Colors.fg, highlightcolor = Colors.entry_bg, highlightbackground = Colors.entry_bg, insertbackground = Colors.fg, selectbackground = Colors.entry_select)
            widget.master.configure(highlightbackground = Colors.entry_bd, highlightcolor = Colors.entry_focus)
        elif isinstance(widget, tk.Canvas):
            widget.configure(background = Colors.bg)
        elif isinstance(widget, (Toplevel, ttk.Frame, tk.Frame)):
            sync_colors(widget, None)

def sync_colors_with_system(window, callback = None): 
    threading.Thread(target = lambda: winaccent.on_appearance_changed(lambda: sync_colors(window, callback)), daemon = True).start()


def show_entry_context_menu(entry: tk.Entry):
    entry.focus_set()

    def cut(): entry.event_generate("<<Cut>>")
    def copy(): entry.event_generate("<<Copy>>")
    def paste(): entry.event_generate("<<Paste>>")
    def delete(): entry.delete("sel.first", "sel.last")
    def select_all(): entry.select_range(0, tk.END)

    try: entry.selection_get(); some_text_selected = "active"
    except: some_text_selected = "disabled"

    if entry.get() == "": 
        enable_select_all = "disabled"
    else:
        try:
            enable_select_all = "disabled" if entry.selection_get() == entry.get() else "active"
        except:
            enable_select_all = "active"

    try: entry.clipboard_get(); enable_paste = "active"
    except: enable_paste = "disabled"

    entry_menu = tk.Menu(tearoff = 0, activebackground = winaccent.accent_normal)
    entry_menu.add_command(label = strings.lang.cut, command = cut, state = some_text_selected)
    entry_menu.add_command(label = strings.lang.copy, command = copy, state = some_text_selected)
    entry_menu.add_command(label = strings.lang.paste, command = paste, state = enable_paste)
    entry_menu.add_command(label = strings.lang.delete, command = delete, state = some_text_selected)
    entry_menu.add_separator()
    entry_menu.add_command(label = strings.lang.select_all, command = select_all, state = enable_select_all)

    entry_menu.tk_popup(entry.winfo_pointerx(), entry.winfo_pointery())