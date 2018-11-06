# -*- coding: utf-8 -*-

import sys
import os
import json
from watson_developer_cloud import PersonalityInsightsV3
from RadarChart import show_chart


# IBM Watoson personality_insightsのAPIキー
personality_insights = PersonalityInsightsV3(
  version='2017-10-13',
  username='YOUR USERNAME',
  password='YOUR PASSWORD'
)

# ファイルからテキストを取得
def read_document(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


# ファイルpathの取得
filepath = sys.argv[1]


input_text = read_document(filepath)


# ディレクトリ名とファイル名に分割（ディレクトリ名は使わない）
dirname, filename = os.path.split(filepath)

# プロファイリング
profile = personality_insights.profile(
  input_text,
  content_type="text/plain;charset=utf-8", content_language="ja",
  accept="application/json", accept_language="ja",
  raw_scores=True, consumption_preferences=True)


# 結果を表示する
labels = []
datas = []
print("{0} のビッグファイブスコア".format(filename))
for i in range(0, 5):
    percentage = float(profile["personality"][i]["percentile"]) * 100
    percentage = int(percentage)
    print(("{0}: {1}%").format(profile["personality"][i]["name"], percentage))
    labels.append(profile["personality"][i]["name"])
    datas.append(percentage)

print()

# raw_scoresの表示
print("{0} の raw score".format(filename))
for i in range(0, 5):
    raw_score = float(profile["personality"][i]["raw_score"])
    print(("{0}: {1:.5f}").format(profile["personality"][i]["name"], raw_score))


# レーダーチャートに描画
show_chart(filename, labels, datas)
