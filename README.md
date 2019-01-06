# post_news

[NHKオンラインで公開されているRSS](https://www3.nhk.or.jp/toppage/rss/index.html)からSlackのチャネルにニュース項目一覧を投稿するPythonスクリプトです。  
取得したRSSの内容をパースし、テンプレートファイルの記述内容に従ったコメントを投稿します。

# 準備

下記の項目がインストール済みの環境を例に説明を進めます。

* Python 3.x
    * 開発および動作確認は3.7.2で実施
* pip 18.1

## 1. リポジトリの配置

本リポジトリを任意の場所へ配置します。

## 2. パッケージのインストール

リポジトリに含まれるrequirements.txtで定義されたパッケージをインストールします。  

```
# pip install -r requirements.txt
```

## 3. Incoming Webhookの設定

Slackを投稿するためにIncoming Webhookを使用します。
[SlackのIncoming Webhookの設定ページ](https://my.slack.com/services/new/incoming-webhook/)より、投稿用URLを用意します。  

## 4. 設定ファイルの記述

リポジトリに含まれるconfig.iniを編集します。

* General
    * timeout:RSS取得、Slack投稿用のAPIを実行する際のタイムアウト秒
* Slack
    * webhock_url:「3. Incoming Webhookの設定」で用意したIncoming WebhookのURLを指定
* RSS
    * feed:取得するRSSのURL。初期値では主要ニュースのフィードを指定しています。
* logging
    * level:ログレベルを指定
    * filename:ログ出力先およびログファイル名を指定。

# スクリプトの実行方法

定期的にスクリプトを実行する場合、cron等で実行します。

```
# python post_news.py
```

# その他

## RSSの利用について

規約通り、個人利用に限られます。
