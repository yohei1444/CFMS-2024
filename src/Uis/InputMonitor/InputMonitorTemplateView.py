import time
try:
    import tkinter as tk

except Exception as e:

    print(e)
    time.sleep(10)


class InputMonitorTemplateView(tk.Frame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self["bg"] = "#ffffff"
        self.canvas = tk.Canvas(self, bg="#ffffff", **kwargs)
        self.canvas.grid(row=2, column=0,columnspan=2, sticky=tk.NSEW)

        self.frame = tk.Frame(self.canvas, bg="#ffffff")
        self.canvas.create_window((self.canvas.winfo_reqwidth()/2,self.canvas.winfo_reqheight()/2), window=self.frame, anchor=tk.CENTER)

    def createWidgets(self):
        
        self.grid(row=0,column=0,padx=3,sticky=tk.NSEW)


if __name__ == "__main__":
    root = tk.Tk()
    root["bg"] = "#ffffff"
    canvas = InputMonitorTemplateView(master=root, width=400, height=450)
    canvas.createWidgets()
    root.mainloop()