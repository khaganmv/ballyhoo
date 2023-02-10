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
        
    @staticmethod
    def scroll_into_view(canvas, widget):
        widget_top = widget.winfo_y()
        widget_bot = widget_top + widget.winfo_height()
        canvas_top = canvas.canvasy(0)
        canvas_bot = canvas_top + canvas.winfo_height()

        if widget_bot > canvas_bot:
            canvas.yview_scroll(int(widget_bot - canvas_bot), 'units')
        elif widget_top < canvas_top:
            canvas.yview_scroll(int(widget_top - canvas_top), 'units')
        
    @staticmethod
    def get_yview_offset(frame, widget):
        widget_y = widget.winfo_y() + widget.winfo_height()
        frame_y = int(frame.winfo_height() * frame._parent_canvas.yview()[1])
        return widget_y - frame_y