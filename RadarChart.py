#!/usr/bin/env python
# -*- coding: utf-8 -*-

from radar_chart import *

def show_chart(twitterID, label, data):
    # plt.rcParams['font.family'] = 'TakaoPGothic' # Linux用
    # font = {"family":"Yu Mincho"} # Windows用
    font = {"family":"Spica Neue P"} # Windows用
    plt.rc('font', **font)
    plt.rcParams["font.size"] = 13.5
    N = len(data)
    Title = "{0} のビッグファイブスコア".format(twitterID)

    theta = radar_factory(N, frame='circle')

    plt.rcParams["figure.figsize"] = [8.3, 8.3] # グラフのサイズを指定

    ax = plt.subplot(projection='radar')
    # chartの範囲を0-100
    ax.set_ylim(0, 100)
    # Grid線を位置の指定
    ax.set_rgrids([20, 40, 60, 80])
    # 描画処理
    ax.plot(theta, data, 'c.-')
    ax.fill(theta, data, facecolor='cyan', alpha=0.3)
    ax.set_varlabels(label)
    # タイトル
    ax.set_title(Title, weight='bold', size='x-large', position=(0.5, 1.08))

    filename = "./results/{0}.png".format(twitterID)
    plt.savefig(filename, bbox_inches='tight')
    plt.show()
