# Selenium Test

## 準備
1. python3をインストール
2. pip install -r requirements.txt

## エラー検出テスト
### できること
- 500, 404等エラー検出
- consoleエラー検出
- PCページをSPデバイスで開いた時のリダイレクトチェック
- ページを開いた時、勝手にリダイレクトが発生していないかチェック

### 使い方
1. csv/check_url_map.csv にチェックしたいURLを記載。行ごとに、対応する[PCURL,SPURL]という形にする。
2. python pageCheck.py というように実行。
3. csv/result.csv にエラー内容が検出される。

#### tips
pageCheck.py IGNORE_CONSOLE_ERRORS に無視したいconsoleエラーを書くと、それはresult.csvに書き込まれません。

## 自動スクロール
### できること
- 指定したURLのページを自動でスクロールする。

### 使い方
1. csv/scroll_url.csv にスクロールして見たいURLを記載。
2. python pageScroll.py というように実行。
