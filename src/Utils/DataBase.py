import sqlite3

class DataBase:

    def __init__(self) -> None:
        self.conn = sqlite3.connect('CFMS2024.db')
        self.cursor = self.conn.cursor()
    
    def addShopLoginHistory(self, shopId, shopName, password):

        if self.hasTable("ShopLoginHistory"):
            try:
                self.cursor.execute(f'''
                INSERT INTO ShopLoginHistory (ShopId, ShopName, Password) VALUES (?,?,?)
                ''',(shopId,shopName,password))
            
            except sqlite3.IntegrityError:
                self.cursor.execute("""
                    UPDATE ShopLoginHistory
                    SET LoginDate = datetime('now', 'localtime')
                    WHERE ShopId = ?
                """, (shopId,))
            
            finally:
                # 変更をコミット
                self.conn.commit()

        else:
            # テーブルを作成
            self.cursor.execute('''
            CREATE TABLE ShopLoginHistory (
                ShopId TEXT PRIMARY KEY,
                ShopName TEXT NOT NULL,
                Password TEXT NOT NULL,
                LoginDate TEXT DEFAULT (datetime('now', 'localtime'))
            )
            ''')

            self.cursor.execute(f'''
            INSERT INTO ShopLoginHistory (ShopId, ShopName, Password) VALUES (?,?,?)
            ''',(shopId,shopName,password))
            
            # 変更をコミット
            self.conn.commit()

    def getShopLoginHistory(self):
        self.cursor.execute("SELECT * FROM ShopLoginHistory")

        # 結果を取得して表示
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)


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
    a.addShopLoginHistory("Seiken2023","生活研究部","$2b$12$vx9ZCSXZhkzNExjoFPq5je1U.nsT/JiUj7mdmH..R.Ttl.pC1kwka")
    a.getShopLoginHistory()



