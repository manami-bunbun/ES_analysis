# !apt-get -q -y install swig 
# !apt-get install mecab
# !apt-get install libmecab-dev
# !apt-get install mecab-ipadic-utf8
# !pip install mecab-python3==0.996.5
# !pip install unidic-lite
# !pip install japanize-matplotlib

import MeCab
import numpy as np
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


import collections
import seaborn as sns
import japanize_matplotlib
import matplotlib.pyplot as plt


def main(filepath):
    text = load_data(filepath)
    sen = []
    for row in range(len(text)):
        for col in range(len(text[row])):
            sen.append(text[row][col])
    c = collections.Counter(sen)
    sns.set(context="notebook",font='IPAexGothic')
    fig = plt.subplots(figsize=(8, 8))
    plt.ylabel("単語")
    sns.countplot(y=sen,order=[i[0] for i in c.most_common(20)])

# read file
def load_data(path):
    """読み込むための関数

    :param path: str, パス
    :return text: list of list of str, 各文がトークナイズされた
    """
    text = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            line = tokenize(line)
            text.append(line)
    return text

#形態素解析(MeCab)

def tokenize(sentence):
    """日本語の文を形態素の列に分割する関数

    :param sentence: str, 日本語の文
    :return tokenized_sentence: list of str, 形態素のリスト
    """
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parse(sentence)
    node = node.split("\n")
    tokenized_sentence = []
    for i in range(len(node)):
        feature = node[i].split("\t")
        if feature[0] == "EOS":
            # 文が終わったら終了
            break
        elif not(feature[0] == "、" or feature[0] == "。" or feature[0] == " ") :
           if  feature[3].startswith(('形容詞', '名詞','副詞')):
        # 分割された形態素を追加
                print(feature)
                tokenized_sentence.append(feature[0])
    return tokenized_sentence


class Vocab(object):
    def __init__(self, word2id={}):
        """
        word2id: 単語(str)をインデックス(int)に変換する辞書
        id2word: インデックス(int)を単語(str)に変換する辞書
        """
        self.word2id = dict(word2id)
        self.id2word = {v: k for k, v in self.word2id.items()}    
        
    def build_vocab(self, sentences, min_count=3):
        # 各単語の出現回数の辞書を作成する
        word_counter = {}
        for sentence in sentences:
            for word in sentence:
                word_counter[word] = word_counter.get(word, 0) + 1

        # min_count回以上出現する単語のみ語彙に加える
        for word, count in sorted(word_counter.items(), key=lambda x: -x[1]):
            if count < min_count:
                break
            _id = len(self.word2id)
            self.word2id.setdefault(word, _id)
            self.id2word[_id] = word 
            
