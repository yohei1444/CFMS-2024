import tkinter as tk
from datetime import datetime, timedelta
import time
import threading


class InputMonitor:

    def __init__(self, enterFunction, spaceFunction) -> None:
        
        self.chars = []
        self.times = []
        self.monitorFlag = False
        self.keyboardFlag = False
        self.functionFlag = False
        self.integerOnlyFlag = False

        self.enterFunction = enterFunction
        self.spaceFunction = spaceFunction
        #バーコード用エンター処理
        #キ－ボード入力時用エンター処理
        #空文字エンター処理

    
    def onKeyPress(self,event):

        key = self.checkKeysym(event)

        if key:
            self.chars.append(key)
            self.checkKeybord()
            print(self.createStrings())
        
        
    
    def createStrings(self):

        strings = ""

        return strings.join(map(str, self.chars))
    
    def checkKeybord(self):

        if not self.keyboardFlag:
            threading.Thread(target=self.intervalTimer).start()
    
    def intervalTimer(self):
        beforChars = len(self.chars)

        time.sleep(0.02)

        if len(self.chars) == beforChars and not self.functionFlag and not self.keyboardFlag:

            print("キーボード入力を検知")
            self.keyboardFlag = True
        


    def checkKeysym(self,event):

        keysym = event.keysym

        if keysym == "Return":
            self.functionFlag = True
            
            print("商品処理")
            return False
        
        elif keysym == "space":
            self.functionFlag = True
            print("会計処理")
            return False
        
        elif keysym == "BackSpace" and len(self.chars) > 0:
            del self.chars[-1]
            return False
        
        elif keysym == "Escape":
            return False
        
        if self.integerOnlyFlag:

            if keysym == "minus" and len(self.chars) == 0:
                print("マイナス例外")
                return "-"

            elif keysym not in [str(i) for i in range(10)]:

                print("文字列は受け付けません")
                return False
        
            else:
                self.times.append(datetime.now())
                return event.char
        
        else:
            self.times.append(datetime.now())
            return event.char


root = tk.Tk()
monitor = InputMonitor(None,None)
root.bind("<Key>", monitor.onKeyPress)
root.mainloop()
