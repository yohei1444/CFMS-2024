import time

try:
    import requests
    import datetime

except Exception as e:

    print(e)
    time.sleep(10)


class PostApi:

    def __init__(self) -> None:
        self.firebaseInfoUrl = "https://script.google.com/macros/s/AKfycbwAKHirPJkkoMraDWSuaj37YzlLgd5KNOMb-W7fYyngucRE1H7uyrxd5_kI5U-ADAwM/exec"


    def getFirebaseInfo(self):

        #GET送信
        self.response = requests.get(self.firebaseInfoUrl)
        self.res_data = self.response.json()
        self.res_data["private_key"] = self.res_data["private_key"].replace("\\n", "\n")

        return self.res_data


if __name__ == "__main__":
    api = PostApi()
    print(datetime.datetime.now())
    print(api.getFirebaseInfo())
    print(datetime.datetime.now())