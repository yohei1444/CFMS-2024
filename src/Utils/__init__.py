import bcrypt

password = b"so-gaku-2024"
# ソルトを生成してパスワードをハッシュ化
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed)

# パスワードの確認
if bcrypt.checkpw(password, hashed):
    print("It Matches!")
else:
    print("It Does not Match :(")
