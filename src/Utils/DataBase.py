import time
try:
    import sqlite3
    from BaseByteConverter import BaseByteConverter as Bb
except Exception as e:

    print(e)
    time.sleep(10)

class DataBase(Bb):

    def __init__(self) -> None:
        super().__init__()

        self.conn = sqlite3.connect('CFMS2024.db')
        self.cursor = self.conn.cursor()
    
    def addShopLoginHistory(self, shopId, shopName, password):
        respones = None

        if self.hasTable("ShopLoginHistory"):
            try:
                respones = "insert"
                self.cursor.execute(f'''
                INSERT INTO ShopLoginHistory (ShopId, ShopName, Password) VALUES (?,?,?)
                ''',(shopId,shopName,self.encodeToBase64(password)))
            
            except sqlite3.IntegrityError:
                respones = "update"
                self.cursor.execute("""
                    UPDATE ShopLoginHistory
                    SET LoginDate = datetime('now', 'localtime'), ShopName = ?, Password = ?
                    WHERE ShopId = ?
                """, (shopName, self.encodeToBase64(password),shopId,))


        else:
            respones = "create"
            # テーブルを作成
            self.cursor.execute('''
            CREATE TABLE ShopLoginHistory (
                ShopId TEXT PRIMARY KEY,
                ShopName TEXT NOT NULL,
                Password TEXT NOT NULL,
                LoginDate TEXT DEFAULT (datetime('now', 'localtime'))
            )
            ''')

            self.cursor.execute('''
            INSERT INTO ShopLoginHistory (ShopId, ShopName, Password) VALUES (?,?,?)
            ''',(shopId,shopName,self.encodeToBase64(password)))
            
        # 変更をコミット
        self.conn.commit()
        return respones

    def getShopLoginHistory(self):
        self.cursor.execute("SELECT * FROM ShopLoginHistory")
        
        # 結果を取得して表示
        return self.cursor.fetchall()
    
    def getLocalShopPassword(self,shopId):

        self.cursor.execute('''SELECT Password FROM ShopLoginHistory WHERE ShopId =?''',(shopId,))
        rows = self.cursor.fetchall()
        # 結果を取得して表示
        return rows[0][0]


    def hasTable(self,tableName):

        self.cursor.execute(f"""
        SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';
        """)

        table_exists = self.cursor.fetchone()

        if table_exists:
            return True
        else:
            return False


if __name__ == "__main__":

    a = DataBase()
    print(a.getLocalShopPassword("Admin's Shop"))



