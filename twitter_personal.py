# -*- coding: utf-8 -*-

import sys
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV3
from RadarChart import show_chart


# TwitterのAPIキー
CONSUMER_KEY = 'YOUR CONSUMER KEY'
CONSUMER_SECRET = 'YOUR CONSUMER SECRET'
ACCESS_TOKEN = 'YOUR ACCESS TOKEN'
ACCESS_SECRET = 'YOUR ACCESS SECRET'


# IBM Watoson personality_insightsのAPIキー
personality_insights = PersonalityInsightsV3(
  version='2017-10-13',
  username='YOUR USERNAME',
  password='YOUR PASSWORD'
)


# watosonに渡すためのjsonフォーマット
def convert_status_to_pi_content_item(s):
    # My code here
    return {
        'userid': str(s.user.id),
        'id': str(s.id),
        'sourceid': 'python-twitter',
        'contenttype': 'text/plain',
        'language': s.lang,
        'content': s.text,
        'created': s.created_at_in_seconds,
        'reply': (s.in_reply_to_status_id == None),
        'forward': False
    }


twitter_api = twitter.Api(consumer_key=CONSUMER_KEY,
                          consumer_secret=CONSUMER_SECRET,
                          access_token_key=ACCESS_TOKEN,
                          access_token_secret=ACCESS_SECRET,
                          debugHTTP=False)


# TwitterアカウントID
handle = sys.argv[1]


# ツイートを取得
max_id = None
statuses = []
for x in range(0, 5):  # Pulls max number of tweets from an account (取得ツイート数 = この値 * count)
    if x == 0:
        statuses_portion = twitter_api.GetUserTimeline(screen_name=handle,
                                                       count=200,
                                                       include_rts=False)
        status_count = len(statuses_portion)
        max_id = statuses_portion[status_count - 1].id - 1  # get id of last tweet and bump below for next tweet set
    else:
        statuses_portion = twitter_api.GetUserTimeline(screen_name=handle,
                                                       count=200,
                                                       max_id=max_id,
                                                       include_rts=False)
        status_count = len(statuses_portion)
        max_id = statuses_portion[status_count - 1].id - 1  # get id of last tweet and bump below for next tweet set
    for status in statuses_portion:
        statuses.append(status)


# Watoson APIに渡す為のjson形式に変化
pi_content_items_array = map(convert_status_to_pi_content_item, statuses)
pi_content_items = {'contentItems': list(pi_content_items_array)}

print("{0} ツイートを取得".format(len(statuses)))

# プロファイリング
profile = personality_insights.profile(
  json.dumps(pi_content_items, ensure_ascii=False),
  content_type="application/json", content_language="ja",
  accept="application/json", accept_language="ja",
  raw_scores=True, consumption_preferences=True)


# 結果を表示する
labels = []
datas = []
print("{0} のビッグファイブスコア".format(handle))
for i in range(0, 5):
    percentage = float(profile["personality"][i]["percentile"]) * 100
    percentage = int(percentage)
    print(("{0}: {1}%").format(profile["personality"][i]["name"], percentage))
    labels.append(profile["personality"][i]["name"])
    datas.append(percentage)

print()

# raw_scoresの表示
print("{0} の raw score".format(handle))
for i in range(0, 5):
    raw_score = float(profile["personality"][i]["raw_score"])
    print(("{0}: {1:.5f}").format(profile["personality"][i]["name"], raw_score))


# レーダーチャートに描画
show_chart(handle, labels, datas)
