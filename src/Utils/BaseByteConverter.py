import time

try:
    import base64

except Exception as e:

    print(e)
    time.sleep(10)

class BaseByteConverter:

    # Base64文字列をバイナリデータにデコード
    def decodeFromBase64(self,encoded_data: str) -> bytes:
        return base64.b64decode(encoded_data)
    
    # バイナリデータをBase64エンコード
    def encodeToBase64(self,data: bytes) -> str:
        return base64.b64encode(data).decode('utf-8')
