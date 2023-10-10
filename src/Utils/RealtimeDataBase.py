import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from PostApi import PostApi


class RealtimeDataBase:

    def __init__(self) -> None:
        

        # サービスアカウントキーの内容を辞書として直接記述
        self.api = PostApi()
        self.serviceAcountKey = self.api.getFirebaseInfo()

        # 資格情報の作成
        self.cred = credentials.Certificate(self.serviceAcountKey)

        # Firebase Admin SDKの初期化
        firebase_admin.initialize_app(self.cred, {
        'databaseURL': 'https://cfms2023-60251-default-rtdb.firebaseio.com/'
        })

    # データベースの変更をリスンします
    def listener(self,event):
        print(f"Data changed: {event.data}")
    
    def getShopPassWord(self,shopId):
        return db.reference(f'/CFMS2024/SHOPS/{shopId}/ShopAccount/Password').get()
    


if __name__ == "__main__":
    r = RealtimeDataBase()
    print(r.getShopPassWord("Seiken2025"))