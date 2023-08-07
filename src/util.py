import customtkinter as ctk
import os


class Util():
    @staticmethod
    def center(widget):
        widget.update()
        frame_width = widget.winfo_rootx() - widget.winfo_x()
        window_width = widget.winfo_width() + 2 * frame_width
        titlebar_height = widget.winfo_rooty() - widget.winfo_y()
        window_height = widget.winfo_height() + titlebar_height + frame_width
        x = widget.winfo_screenwidth() // 2 - window_width // 2
        y = widget.winfo_screenheight() // 2 - window_height // 2
        widget.geometry(f'{widget.winfo_width()}x{widget.winfo_height()}+{x}+{y}')
        
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
        
    @staticmethod
    def scroll_into_view(canvas, widget):
        widget_top = widget.winfo_y()
        widget_bot = widget_top + widget.winfo_height()
        canvas_top = int(canvas.canvasy(0))
        canvas_bot = canvas_top + canvas.winfo_height()
        
        if widget_bot > canvas_bot:
            canvas.yview_scroll(widget_bot - canvas_bot, 'units')
        elif widget_top < canvas_top:
            canvas.yview_scroll(widget_top - canvas_top, 'units')
            
    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = os.sys._MEIPASS
        except Exception:
            base_path = os.path.abspath('resources/')

        return os.path.join(base_path, relative_path)
