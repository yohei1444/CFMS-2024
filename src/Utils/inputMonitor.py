
from datetime import datetime
import time
import threading


class InputMonitor:

    def __init__(self, judgInterval = 0.003, keyboardInterval = 0.0015, readerInterval = 0.00015) -> None:
        
        self.chars = []
        self.times = []
        self.keyboardFlag = False
        self.functionFlag = False
        self.integerOnlyFlag = False

        self.judgInterval = judgInterval #判定に用いるインターバル
        self.keyboardInterval = keyboardInterval #キーボードを長押ししたときの平均インターバル
        self.readerInterval = readerInterval #リーダー読み込み時の平均インターバル

    def setFunction(self, readerEnterFunction = False, keyboardEnterFunction = False, keyboardEmptyEnterFunction = False, spaceFunction = False):
        
        self.readerEnterFunction = readerEnterFunction #バーコード用エンター処理
        self.keyboardEnterFunction = keyboardEnterFunction #キ－ボード入力時用エンター処理
        self.keyboardEmptyEnterFunction = keyboardEmptyEnterFunction #空文字エンター処理
        self.spaceFunction = spaceFunction #キ－ボード入力時用スペース処理
    
    def setJudgInterval(self):

        if self.keyboardInterval <= self.readerInterval :
            return False
        
        else:
            provisionalInterval = self.readerInterval * 2
            while provisionalInterval >= self.keyboardInterval:
                provisionalInterval *= 0.9
            
            self.judgInterval = provisionalInterval
            
            return self.judgInterval
    
    def onKeyPress(self,event):

        key = self.checkKeysym(event)
        #押されたキーの種別を取得。Enterなどの関数トリガーキー、ファンクションキー等はFalse

        if key:
        #文字列として扱う場合の処理
            self.chars.append(key)
            self.checkKeybord()
    
    def getAvarageTime(self):

        if len(self.times) < 3:
            print("測定不能")
            return False
        
        elif len(self.times) >= 3:

            sumTimes = 0

            for i in range(min(len(self.times)-1,20)): #20文字目までの入力時間を参照
                sumTimes = (self.times[i + 1] - self.times[i]).total_seconds()
            
            else:
                avarageTime = sumTimes / min(len(self.times)-1, 20)

            return avarageTime
    
    def setKeyboardInterval(self):
        
        intervalTime = self.getAvarageTime()
        if intervalTime:
            self.keyboardInterval = intervalTime
    
    def setReaderInterval(self):
        
        intervalTime = self.getAvarageTime()
        if intervalTime:
            self.readerInterval = intervalTime
    
    def createStrings(self):

        strings = ""

        return strings.join(map(str, self.chars))
    
    def checkKeybord(self):

        if not self.keyboardFlag:
            threading.Thread(target=self.intervalTimer).start()
    
    def intervalTimer(self):
        beforChars = len(self.chars)

        time.sleep(self.judgInterval)

        if len(self.chars) == beforChars and not self.functionFlag and not self.keyboardFlag: 
            #計測開始から入力文字数が変わっていないこと、エンター関数等が実行されていないこと、すでにキーボード判定になっていないこと

            print("キーボード入力を検知")
            self.keyboardFlag = True
    
    def nextMonitor(self):

        self.chars.clear()
        self.times.clear()

        self.keyboardFlag = False
        self.functionFlag = False


    def checkKeysym(self,event):

        keysym = event.keysym

        if keysym == "Return":
            
            if self.readerEnterFunction and not self.keyboardFlag and len(self.chars) > 0:
                self.readerEnterFunction()
                self.functionFlag = True
                print("リーダーで文字が入力されました")
                self.nextMonitor()
                return False
            
            elif self.keyboardEnterFunction and len(self.chars) > 0:
                self.keyboardEnterFunction()
                self.functionFlag = True
                print("キーボードで文字が入力されました")
                self.nextMonitor()
                return False
            
            elif self.keyboardEmptyEnterFunction and len(self.chars) == 0:
                self.keyboardEmptyEnterFunction()
                self.functionFlag = True
                print("空エンター")
                self.nextMonitor()
                return False
            
            else:
                return False
        
        elif keysym == "space" and self.spaceFunction:
            self.functionFlag = True
            return False
        
        elif keysym == "BackSpace" and len(self.chars) > 0:
            del self.chars[-1]
            return False
        
        elif keysym == "Escape":
            return False
        
        if self.integerOnlyFlag:

            if keysym == "minus" and len(self.chars) == 0:
                print("マイナス例外")
                self.times.append(datetime.now())
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

if __name__ == "__main__":
    import tkinter as tk

    def hoge():
        pass

    root = tk.Tk()
    root.resizable(False, False)
    root.geometry("1000x1000")
    monitor = InputMonitor()
    monitor.setFunction(readerEnterFunction=monitor.setReaderInterval, keyboardEnterFunction=monitor.setKeyboardInterval, keyboardEmptyEnterFunction=hoge)
    root.bind("<Key>", monitor.onKeyPress)
    root.mainloop()
