import netifaces
import requests

response = requests.get("https://httpbin.org/ip")
print(f"Your IP is {response.json()['origin']}")


class Authentication:

    def __init__(self) -> None:
        self.macAddress = self.getMacAddresses()
        self.ipAddress = self.getGlobalIpAddress()
    
    def getMacAddresses(self):
        macs = []
        
        for interface in netifaces.interfaces():
            ifaddrs = netifaces.ifaddresses(interface)
            if netifaces.AF_LINK in ifaddrs:
                link_info = ifaddrs[netifaces.AF_LINK][0]
                mac_address = link_info.get("addr")
                if mac_address:
                    macs.append(mac_address)
        
        return macs[0]
    
    def getGlobalIpAddress(self):

        try:
            response = requests.get("https://httpbin.org/ip")
            return response.json()['origin']
        
        except:

            return None
        

    def getInfo(self):

        return {"ip":self.ipAddress, "mac":self.macAddress}


if __name__ == "__main__":

    auth = Authentication()
    print(auth.getInfo())