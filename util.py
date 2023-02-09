import customtkinter as ctk


class Util():
    @staticmethod
    def select_all(widget):
        widget.select_range(0, ctk.END)
        widget.icursor(ctk.END)
        return 'break'
        
    @staticmethod
    def shift_focus_from(src, dst):
        src.selection_clear()
        dst.focus()
        dst.icursor(ctk.END)