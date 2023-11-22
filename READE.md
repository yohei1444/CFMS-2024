# ソフトウェア名：CFMS2024（予定）

このソフトウェアはWindowsPC上で誰でも簡単に、本格的なレジシステムを提供する目的で作成。
使用シーンとして、学園祭などで手動では管理の難しい中規模の出展団体が使用する。
CFMS2022の過去二回の運用を通して得られたフィードバックを活かし、よりピンポイントに特化した改良版がこのソフトウェアである。
2022ではデータなどのすべてがローカル管理だったが、今回からオンライン（Firebase Realtime Database）とローカル(Sqlite)が併用可能になる。
それに伴い、以下のメリットが得られる。
 - PC間でのデータファイルの引継ぎが不要になる
 - だれのPCからでも同じ情報にアクセスできる
 - 二台以上の並列会計が可能になる
 - 一つのソフトウェアで複数店舗の会計が可能になる
 - リアルタイムで遠隔地から売り上げ情報にアクセスできる
etc

## CFMS2022こちら
https://github.com/yohei1444/CFMS2022

インストール方法
未完の為配布方法は無し。完成後はリポジトリから直接exeファイルをダウンロード

## 必要機材
 - Windows10以上のPC
 - バーコードスキャナ（なくても可能な予定）

## 開発環境
 - Python3.9.13
 - windows11
 - VScode Version1.83.0

## 使用ライブラリ
|名前　| バージョン|
| --- | --- |
|argon2-cffi-bindings|21.2.0|
|bcrypt|4.0.1|
|CacheControl|0.13.1|
|cachetools|5.3.1|
|certifi|2023.7.22|
|cffi|1.16.0|
|charset-normalizer|3.3.0|
|cryptography|41.0.4|
|firebase-admin|6.2.0|
|google-api-core|2.12.0|
|google-api-python-client|2.102.0|
|google-auth|2.23.2|
|google-auth-httplib2|0.1.1|
|google-cloud-core|2.3.3|
|google-cloud-firestore|2.12.0|
|google-cloud-storage|2.11.0|
|google-crc32c|1.5.0|
|google-resumable-media|2.6.0|
|googleapis-common-protos|1.60.0|
|grpcio|1.59.0|
|grpcio-status|1.59.0|
|httplib2|0.22.0|
|idna|3.4|
|msgpack|1.0.7|
|netifaces|0.11.0|
|proto-plus|1.22.3|
|protobuf|4.24.4|
|pyasn1|0.5.0|
|pyasn1-modules|0.3.0|
|pycparser|2.21|
|PyJWT|2.8.0|
|pyparsing|3.1.1|
|requests|2.31.0|
|rsa|4.9|
|uritemplate|4.1.1|
|urllib3|2.0.6|

(今後はGUI製作用のライブラリが増える)

## 機能一覧（実装予定も含む）
GUIまで取り掛かれていないため、バックグラウンドで動作可能な部分から解説。
 - Macアドレスを用いてユーザーの判定機能
 - 店舗アカウントごとのログイン機能
 - 店舗アカウントのパスワード変更
 - 過去にそのPCからログインした店舗アカウントへのショートカットログイン
 - パスワードのハッシュ化保存
 - 商品の新規登録
 - 商品の表示非表示を今後可能にするhidenフラグの操作
 - 商品情報を変更した際の履歴をすべて追跡可能
 - 重複した商品番号を登録しても、任意の商品を単体で有効に指定できる
