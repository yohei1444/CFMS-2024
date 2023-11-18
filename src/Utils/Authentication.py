import time
try:

    import netifaces
    import requests
    import bcrypt
    import socket
    from BaseByteConverter import BaseByteConverter as Bb

except Exception as e:

    print(e)
    time.sleep(10)

class Authentication(Bb):

    def __init__(self) -> None:
        super().__init__()
        self.macAddress = self.getMacAddresses()
        self.ipAddress = self.getGlobalIpAddress()
        self.hostName = self.getHostName()
        self.displayName = None
        
        self.password = None
        self.shopId = None

        self.location = None
        self.shopName = None


    #Macアドレスを取得
    def getMacAddresses(self):
        self.macs = []
        
        for interface in netifaces.interfaces():
            ifaddrs = netifaces.ifaddresses(interface)
            if netifaces.AF_LINK in ifaddrs:
                link_info = ifaddrs[netifaces.AF_LINK][0]
                mac_address = link_info.get("addr")
                if mac_address:
                    self.macs.append(mac_address)
        
        return self.macs[0]
    
    #IPアドレスを取得する
    def getGlobalIpAddress(self):

        try:

            response = requests.get("https://httpbin.org/ip")
            return response.json()['origin']
        
        except:

            return "Unknow"
    
    #local名を取得
    def getHostName(self):
        
        return socket.gethostname()


    def getUserData(self):

        return {"ip":self.ipAddress, 
                "mac":self.macAddress, 
                "host":self.hostName, 
                "displayName": self.displayName
                }
    
    def getPCInformation(self):

        return {"IPAddress":self.ipAddress, 
                "UserMacAddress":self.macAddress
                }
    
    
    def setDisplayName(self, displayName ):

        self.displayName = displayName

    def setShopId(self, shopId):

        self.shopId = shopId

    def setShopName(self, shopName):

        self.shopName = shopName

    def setLocation(self, location):

        self.location = location

    def setPassword(self, password):

        self.password = password

    def shopLogin(self,password, hashedPassword):
        basePass = self.decodeFromBase64(hashedPassword) 
        
        if bcrypt.checkpw(password.encode("utf8"), basePass):
            self.password = basePass
            return True
        
        else:
            return False
    
    def createShopAccountData(self):
        
        return {
            "Location": self.location,
            "Password": self.password,
            "ShopName": self.shopName,
            "MasterPC": self.getUserData(),
            "Location": self.location,
        }

    def createHash(self,word):
        
        return bcrypt.hashpw(word.encode("utf8"), bcrypt.gensalt())
    
    #ファイルコピー防止のため、クラウドのパスワードにMACアドレスを足したローカルのパスワードを作成
    def createLocalPasswordHash(self):

        word = self.macAddress + self.encodeToBase64(self.password)

        return  bcrypt.hashpw(word.encode("utf8"), bcrypt.gensalt())
    
    def localShopLogin(self, localPass, cludpass):
        
        basePass = self.decodeFromBase64(localPass)
        password = self.macAddress + cludpass
        print(password)

        if bcrypt.checkpw(password.encode("utf8"), basePass):
            self.password = self.decodeFromBase64(cludpass)
            return True
        
        else:
            return False
    


if __name__ == "__main__":
    from RealtimeDataBase import RealtimeDataBase
    from DataBase import DataBase
    
    r = RealtimeDataBase()
    a = Authentication()
    d = DataBase()    

    r.setShopId("Admin's Shop")
    print(d.getLocalShopPassword(r.getShopId()))
    print(a.localShopLogin(d.getLocalShopPassword(r.getShopId()),r.getShopPassWord()))