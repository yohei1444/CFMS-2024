import tkinter as tk

class ErrorTmplate:

    def __init__(self, root, errorCode, errorMessage, reStartFunc) -> None:
        
        self.errorCode = errorCode #エラーコード E1xx 
        self.reStartFunc = reStartFunc #再実行ボタンを押した時に実行される関数
    
        self.tmpErrorMessages = {
            "tmp1": ["デバイスがインターネットに接続されていますか？",
                     "通信環境が不安定ではありませんか？"],

        }

        self.errorMessage = errorMessage #エラーコードの下に表示されるメインの文言

        self.frame = tk.Frame(root)

        self.canvas = tk.Canvas(self.frame, width=170, height=170, bg="white")

        self.radius = 80

        self.errorMessageLabel = tk.Label(self.frame, text= self.errorMessage, font=("Helvetica", 30))

        self.reStartButton = tk.Button(self.frame, text="再実行", font=("Helvetica", 20), height=2, width=10, bg= "#008000", fg="#ffffff")
    
    def createErrorText(self, tmps, texts):
        
        self.errorTexts = []
        
        for i in tmps:
            for j in self.tmpErrorMessages[i]:
                self.errorTexts.append(tk.Label(self.frame,text="・" + j, font=("Helvetica", 20)))
        
        for k in texts:
            self.errorTexts.append(tk.Label(self.frame,text="・" + k, font=("Helvetica", 20)))
    

    def draw_circle_with_text(self):
        # 中心座標
        center_x = self.canvas.winfo_reqwidth() // 2
        center_y = self.canvas.winfo_reqheight() // 2

        # 円を描画
        self.canvas.create_oval(center_x - self.radius, center_y - self.radius, center_x + self.radius, center_y + self.radius, fill="#008000")

        # テキストを中央に配置
        self.canvas.create_text(center_x, center_y, text="E101", font=("Helvetica", 30), fill="#ffffff")

        
        
    def createWidget(self):

        self.frame.pack()

        self.canvas.pack()

        self.draw_circle_with_text()

        self.errorMessageLabel.pack(pady=50)

        for i in self.errorTexts:
            i.pack(pady=20)
        
        self.reStartButton.pack(pady=50)




if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Circle with Text")

    root["bg"] = "#ffffff"

    error = ErrorTmplate(root,"E101","インターネットに接続できません",None)
    error.createErrorText(["tmp1"],[])
    error.createWidget()


    root.mainloop()
