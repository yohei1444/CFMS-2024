import time
try:
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import db
    from PostApi import PostApi
    from BaseByteConverter import BaseByteConverter as Bb
    import datetime

except Exception as e:

    print(e)
    time.sleep(10)


class RealtimeDataBase(Bb):

    def __init__(self) -> None:
        super().__init__()

        # サービスアカウントキーの内容を辞書として直接記述
        self.api = PostApi()
        self.serviceAcountKey = self.api.getFirebaseInfo()

        # 資格情報の作成
        self.cred = credentials.Certificate(self.serviceAcountKey)

        # Firebase Admin SDKの初期化
        firebase_admin.initialize_app(self.cred, {
        'databaseURL': 'https://cfms2023-60251-default-rtdb.firebaseio.com/'
        })

        self.hasAllProductsDirectory = False
        self.hasSalesDirectory = False
        self.hasValidProductsDirectory = False
    
    def setShopId(self, shopId):

        self.shopId = shopId.replace("\\", "-")
    
    def getShopId(self):

        return self.shopId
    
    # データベースの変更をリスンします
    def listener(self,event):
        print(f"Data changed: {event.data}")
    
    def hasDirectory(self, path):
        if db.reference(f'/CFMS2024/SHOPS/{path}').get():
            return True
        else:
            return False
    
    #ProductsディレクトリーとSalesディレクトリーがあるかどうかを変数に格納する
    def hasPrSaDirectory(self):

        self.hasAllProductsDirectory = self.hasDirectory(self.shopId+"/Products/All")
        self.hasValidProductsDirectory = self.hasDirectory(self.shopId+"/Products/Valid")
        self.hasSalesDirectory = self.hasDirectory(self.shopId+"/Sales")
    
    # SHOPACCOUNTからパスワードのハッシュ値を取得します
    def getShopPassWord(self) -> str:
        return db.reference(f'/CFMS2024/SHOPS/{self.shopId}/ShopAccount/Password').get()
    
    def getUserData(self, userMac) -> str:
        return db.reference(f'/CFMS2024/SHOPS/{self.shopId}/Users/{userMac}').get()
    
    def getShopName(self) -> str:
        return db.reference(f'/CFMS2024/SHOPS/{self.shopId}/ShopAccount/ShopName').get()
    
    def setShopPassWord(self, password:bytes):
        ref = db.reference(f'/CFMS2024/SHOPS/{self.shopId}/ShopAccount/')
        
        # バイナリデータをBase64エンコード
        ref.update({
            'Password': self.encodeToBase64(password)
        })

    def createShopAccountStructure(self, data:dict):
        # ルートの参照を取得
        root_ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/")
        
        # "ShopAccount"という名前の新しいネストされたデータ構造を作成
        new_ref = root_ref.child("ShopAccount")

        new_ref.set(data)
    
    
    def createUsersStructure(self, data:dict):
        # ルートの参照を取得
        root_ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/Users")
        
        #ユーザーのMacアドレスの新しいネストされたデータ構造を作成
        new_ref = root_ref.child(data["mac"])

        new_ref.set(data)

    
    def shopSignup(self, shopData):

        if not self.hasDirectory(self.shopId):
            self.createShopAccountStructure(shopData)

            return True
        
        else:
            return False
    
    def addNewProduct(self, data, PCInformation):

        if not self.hasAllProductsDirectory:
            # ルートの参照を取得
            root_ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/")
            new_ref = root_ref.child("Products/All")

            #Productの一意のIDを設定・取得
            productKey = new_ref.push({"DefaultHistoryID":"None"}).key
        
        else:
            # ルートの参照を取得
            ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/Products/All")
            
            #Productの一意のIDを設定・取得
            productKey = ref.push({"DefaultHistoryID":"None"}).key
        
        product_ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/Products/All/{productKey}")
        history_ref = product_ref.child("History")

        historyKey = history_ref.push(data).key
        
        #HistoryIDを設定し、非表示フラグを初期化する
        product_ref.update({
            "DefaultHistoryID": historyKey,
            "Hidden" : False
        })

        self.addValidProduct(data["ProductID"], productKey + "|" + historyKey, PCInformation)
    
    #非表示フラグを有効にする
    def hidenProduct(self, productKey):
        
        product_ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/Products/All/{productKey}")
        product_ref.update({
            "Hidden" : True
        })

    #有効化商品番号の追加
    def addValidProduct(self, number, productHistoryKey, PCInformation):

        #Validディレクトリがない場合
        if not self.hasValidProductsDirectory:
            root_ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/Products")
            new_ref = root_ref.child("Valid")

            new_ref.update(
                {
                number : 
                    {
                    "ProductHistoryID":productHistoryKey,
                    }
                })
            
            self.addValidProductHistory(number, productHistoryKey, PCInformation)

            return True
        
        #Validディレクトリがあり、有効化されている商品番号に重複がない場合
        elif not self.hasValidProdct(number):
            ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/Products/Valid")
            ref.update(
                {
                number : 
                    {
                    "ProductHistoryID":productHistoryKey,
                    }
                })
            
            self.addValidProductHistory(number, productHistoryKey, PCInformation)

            return True
        
        #Validディレクトリがあるが、有効化されている商品番号に重複がある場合
        else:
            
            return False
    
    #有効化商品番号の重複検証
    def hasValidProdct(self, number):
        
        return self.hasDirectory(f"{self.shopId}/Products/Valid/{number}")

    #有効化商品番号の無効化
    def deleteValidProduct(self, number, PCInformation):

        ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/Products/Valid/{number}")
        ref.update(
                    {
                    "ProductHistoryID":"None",
                    }
                )
        self.addValidProductHistory(number, "None", PCInformation)

    
    #有効化商品番号の変更
    def changeValidProduct(self, number, productHistoryKey, PCInformation):
        
        ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/Products/Valid/{number}")
        ref.update(
                    {
                    "ProductHistoryID":productHistoryKey,
                    }
                )
        
        self.addValidProductHistory(number, productHistoryKey, PCInformation)

    def addValidProductHistory(self, number, productHistoryKey, PCInformation):
        timeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not self.hasDirectory(f"Products/Valid/{number}/History"):

            ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/Products/Valid/{number}")
            new_ref = ref.child(f"History/{timeStamp}")

        
        else:
            ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/Products/Valid/{number}/History")
            new_ref = ref.child(timeStamp)
        
        print(timeStamp)
        print(new_ref.get())
        new_ref.update({
            "ProductHistoryID": productHistoryKey,
            "PCInformation": PCInformation}
        )

        



if __name__ == "__main__":
    from Authentication import Authentication 
    from DataBase import DataBase
    import datetime
    import time
    r = RealtimeDataBase()
    a = Authentication()
    d = DataBase()

    def signUpTest():

        r.setShopId("Admin's Shop")
    
        a.setDisplayName("よーへーのMac")
        
        print(r.hasDirectory("Admin's Shop"))

        a.setLocation("横浜市南区中里町")
        a.setShopName("実家の味")

        print(a.createShopAccountData())
        print(r.shopSignup(a.createShopAccountData()))
        r.setShopPassWord( a.createHash("admin"))
        r.createUsersStructure(a.getUserData())
    
    def loginTest():

        r.setShopId("Admin's Shop")

        if a.shopLogin("admin",r.getShopPassWord()):

            if r.hasDirectory(f"{r.getShopId()}/Users/{a.macAddress}"):
                d.addShopLoginHistory(r.getShopId(), r.getShopName(), a.createLocalPasswordHash())
                
                print("おかえりなさい")
            
            else:
                a.setDisplayName(input("表示名を決めましょう！"))
                r.createUsersStructure(a.getUserData())
        
        else:
            print("パスワードが違います")
    
    def addProdTest(PCInformation):

        r.addNewProduct({
                    "Date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "PCInfomation":a.getPCInformation(),
                    "ProductID":"0001",
                    "ProductName":"アンパン",
                    "ProductPrice":150
                    },PCInformation)
    

    def localLoginTest():

        r.setShopId("Admin's Shop")
        if a.localShopLogin(d.getLocalShopPassword(r.getShopId()),r.getShopPassWord()):
            print("おかえりなさい")
        
        else:
            print("保存されているパスワードが無効です")
        
        
    localLoginTest()
    r.hasPrSaDirectory()
    addProdTest(a.getPCInformation())
    time.sleep(4)
    r.deleteValidProduct("0001",a.getPCInformation())
    r.changeValidProduct("0001","うまくいった！",a.getPCInformation())
