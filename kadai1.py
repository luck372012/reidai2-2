### 検索ツールサンプル
### これをベースに課題の内容を追記してください

# 検索ソース
source=["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]

### 検索ツール
def search():
    word = "ねずこ"
  
    if word in source:
        print("{}が見つかりした".format(word))
        return
    print("{}が見つかりません".format(word))

        
if __name__ == "__main__":
    search()