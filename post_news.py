# -*- coding: utf-8 -*-

import configparser
import logging
import json
import xml.etree.ElementTree as ET
from datetime import datetime as dt
import requests
from jinja2 import Environment, FileSystemLoader


class News:
    def __init__(self, api_timeout):
        self.timeout = api_timeout
        self.xml = None

    def get_feed(self, feed):
        """
        RSSフィードの取得
        :param feed:
        :return:
        """

        try:
            req = requests.get(feed, timeout=self.timeout)
            self.xml = ET.fromstring(req.content)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            exit(1)

    def post_slack(self, url=None):
        """
        RSSの中身を解析し、チャンネルへ投稿
        :param url:
        :return:
        """

        build_date = self._formating_datetime(
            self.xml[0].find("lastBuildDate").text
        )

        # 再帰的にitemタグの項目を検索・展開
        items = []
        for item in self.xml.iter("item"):
            tmp = {
                "title": item.find("title").text,
                "link": item.find("link").text,
                "pub_date": self._formating_datetime(
                    item.find("pubDate").text
                ),
                "description": item.find("description").text
            }
            items.append(tmp)

        # メッセージ内容の生成
        env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
        tpl = env.get_template('/template/news.jinja2')
        msg = tpl.render({'build_date': build_date, 'items': items})
        logger.debug("msg="+msg)

        # Slackへメッセージ投稿
        self._send_slack_channel(
            url=url,
            text=msg,
            timeout=self.timeout
        )

    @staticmethod
    def _send_slack_channel(url, text, timeout=60):
        """
        Webhock経由でチャンネルへコメントを投稿
        :param url:
        :param text:
        :param timeout:
        :return:
        """
        try:
            requests.post(
                url=url,
                data=json.dumps({
                    "text": text
                }),
                timeout=timeout
            )
        except requests.exceptions.RequestException as e:
            logger.error(e)
            exit(1)

    @staticmethod
    def _formating_datetime(str_datetime):
        """
        日時文字列の整形
        %Y-%m-%d %H:%M:%S（文字列）の形式に整形する
        :param str_datetime:
        :return:
        """

        data = dt.strptime(
            str_datetime,
            '%a, %d %b %Y %H:%M:%S %z'
        )
        return data.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':

    # 設定ファイルの読み込み
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')

    # ロギング設定
    logger = logging.getLogger('post_news')
    handler = logging.FileHandler(config.get("logging", "filename"), 'a')
    handler.setLevel(logging.getLevelName(config.get("logging", "level")))
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
        )
    )
    logger.setLevel(logging.getLevelName(config.get("logging", "level")))
    logger.addHandler(handler)

    # RSSフィード取得後、Slackへメッセージ投稿
    news = News(api_timeout=config.getint("General", "timeout"))
    news.get_feed(config.get("RSS", "feed"))
    news.post_slack(config.get("Slack", "webhock_url"))
