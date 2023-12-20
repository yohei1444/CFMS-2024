import time
try:
    import tkinter as tk

except Exception as e:

    print(e)
    time.sleep(10)

class LoginPartsView(tk.Frame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self["bg"] = "#ffffff"

        self.titleLabel = tk.Label(self ,text="場所", font=("BIZ UDゴシック", 15), width=4, height=2, anchor=tk.W, bg="#ffffff", fg="#696969")


    
    def createWidgets(self, resources, slipId, customerCategorys, memo):

        self.resources = resources
        self.slipId = slipId
        self.customerCategorys = customerCategorys
        self.memo = memo

        self.grid(row=0, column=0,sticky=tk.W+tk.E)

        self.resourceLabel.grid(row=0, column=0, padx=3,sticky=tk.W)
        self.resourceValueLabel["text"] = self.resources[0]
        self.resourceValueLabel.grid(row=0, column=1, padx=3, sticky=tk.E)
        

        self.border_frame1.grid(row=1,column=0,columnspan=2,sticky=tk.W+tk.E)

        self.slipIdLabel.grid(row=2, column=0, padx=3,sticky=tk.W)
        self.slipIdValueLabel["text"] = self.slipId
        self.slipIdValueLabel.grid(row=2, column=1, padx=3, sticky=tk.E)
        

        self.border_frame2.grid(row=3,column=0,columnspan=2,sticky=tk.W+tk.E)

        self.cutomerCategoryLabel.grid(row=4, column=0, padx=3,sticky=tk.W)
        self.cutomerCategoryValueLabel["text"] = self.customerCategorys[0]
        self.cutomerCategoryValueLabel.grid(row=4, column=1, padx=3, sticky=tk.E)
        

        self.border_frame3.grid(row=5,column=0,columnspan=2,sticky=tk.W+tk.E)




    def on_click(self,event):
        print(self.slipId)


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPartsView(root,width=500,height=400)
    app.grid(sticky=tk.NSEW)
    app.createWidgets(["食物実習室","C3B"],"10231",["一般","部員","先生"],"hoge")


    root.mainloop()
