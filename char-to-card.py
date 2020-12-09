import pinyin
import csv
import requests
import json

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
    card = []
    card.append(row[0]) # 0 is 汉子
    card.append(pinyin.get(row[0])) # 1 is pinyin

    # get youdao.com data from their api
    requests_url = "http://dict.youdao.com/jsonapi?q=%s" % row[0]
    print(requests_url)
    resp = requests.get(requests_url, headers=FAKE_HEADER).json()

    # Get the English translation
    english_definition = ""
    trans = resp["web_trans"]["web-translation"][0]["trans"]
    for translation in trans:
      english_definition += translation["value"] + ", "
    card.append(english_definition)

    # Just add an empty element for the audio
    card.append("")

    # Get the first example sentence
    exampleSentence = resp["blng_sents_part"]["sentence-pair"][0]
    card.append(exampleSentence["sentence-eng"]) # add in the Chinese sentence. This should have the word bolded
    card.append(pinyin.get(exampleSentence["sentence"], delimiter=" ")) # next have the pinyin
    card.append(exampleSentence["sentence-translation"]) # lastly, include the translation

    print(card)
    newCompletedCards.append(card)

chineseFile.close()

with open('chinese-new.csv', 'w') as chineseNewFile:
  chineseWriter = csv.writer(chineseNewFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for card in newCompletedCards:
    chineseWriter.writerow(card)
chineseNewFile.close()
