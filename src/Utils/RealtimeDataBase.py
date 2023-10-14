import time
try:
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import db
    from PostApi import PostApi
    from BaseByteConverter import BaseByteConverter as Bb

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
        dir_ref = root_ref.child("ShopAccount")

        dir_ref.set(data)
    
    
    def createUsersStructure(self, data:dict):
        # ルートの参照を取得
        root_ref = db.reference(f"/CFMS2024/SHOPS/{self.shopId}/Users")
        
        # "ShopAccount"という名前の新しいネストされたデータ構造を作成
        dir_ref = root_ref.child(data["mac"])

        dir_ref.set(data)

    
    def shopSignup(self, shopData):

        if not self.hasDirectory(self.shopId):
            self.createShopAccountStructure(shopData)

            return True
        
        else:
            return False


if __name__ == "__main__":
    from Authentication import Authentication 
    from DataBase import DataBase
    r = RealtimeDataBase()
    a = Authentication()
    d = DataBase()

    def signUpTest():
    
        a.setDisplayName("よーへーのMac")
        
        print(r.hasDirectory("Admin's Shop"))

        a.setLocation("横浜市南区中里町")
        a.setShopName("実家の味")

        print(a.createShopAccountData())
        print(r.shopSignup("Admin's Shop",a.createShopAccountData()))
        r.setShopPassWord("Admin's Shop", a.createHash("admin"))
        r.createUsersStructure("Admin's Shop",a.getUserData())
    
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
    

    def localLoginTest():

        r.setShopId("Admin's Shop")
        if a.localShopLogin(d.getLocalShopPassword(r.getShopId()),r.getShopPassWord()):
            print("おかえりなさい")
        
        else:
            print("保存されているパスワードが無効です")
        
        
    localLoginTest()


