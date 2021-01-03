from pypinyin import pinyin
from itertools import chain
import csv
import requests
import json
import re

FAKE_HEADER = {
  "Host": "dict.youdao.com",
  "Accept": "*/*",
  "User-Agent": "YoudaoDict/139 CFNetwork/901.1 Darwin/17.6.0 (x86_64)",
  "Accept-Language": "en-us",
  "Accept-Encoding": "gzip",
  "Connection": "keep-alive",
}

Base_url = "https://tinydict-translateapi.appspot.com/{}"

newCompletedCards = []
with open('chinese.csv') as chineseFile:
  chineseReader = csv.reader(chineseFile, delimiter=',')

  chineseChars = []
  for row in chineseReader:
    word = ""
    print(row)
    if len(row) == 0:
      continue
    for n in re.findall(r'[\u4e00-\u9fff]+', row[0]):
      print(n)
      word = n
    if word == "":
      continue
    card = []
    card.append(word) # 0 is 汉子
    wordInPinyin = pinyin(word)
    card.append(' ' .join(chain.from_iterable(wordInPinyin))) # 1 is pinyin

    # get youdao.com data from their api
    requests_url = "http://dict.youdao.com/jsonapi?q=%s" % word
    print(requests_url)
    resp = requests.get(requests_url, headers=FAKE_HEADER).json()

    # Get the English translation
    english_definition = ""
    if "web_trans" in resp:
      trans = resp["web_trans"]["web-translation"][0]["trans"]
      for translation in trans:
        english_definition += translation["value"] + ", "
    else:
      print("This word doesn't have a translation:" + word)
    card.append(english_definition) # 2 is english translation

    # Just add an empty element for the audio
    card.append("") # 3 is audio. Just use awesomeTTS for this

    # Get the first example sentence
    if "blng_sents_part" in resp: 
      exampleSentence = resp["blng_sents_part"]["sentence-pair"][0]
      card.append(exampleSentence["sentence-eng"]) # add in the Chinese sentence. This should have the word bolded
      sentence = pinyin(exampleSentence["sentence"])
      card.append(' ' .join(chain.from_iterable(sentence))) # next have the pinyin
      card.append(exampleSentence["sentence-translation"]) # lastly, include the translation

    print(card)
    newCompletedCards.append(card)

chineseFile.close()

with open('chinese-new.csv', 'w') as chineseNewFile:
  chineseWriter = csv.writer(chineseNewFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for card in newCompletedCards:
    chineseWriter.writerow(card)
chineseNewFile.close()
