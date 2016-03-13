# -*- coding: utf-8 -*-
import sys
import re
import datetime
import urllib.request
import sqlite3

if __name__ == '__main__':
  timestump = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
  #
  # 第1引数 : データベースへのパス
  #
  if len(sys.argv) != 2:
    sys.exit("usage : > python GetMSNTitle.py [DatabaseName]")
  db_path = sys.argv[1]
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  # urlopenはurllib.responseオブジェクトを返す
  # urllib.responseはfileのようなオブジェクトで、infoメソッドとgeturlが追加されたもの
  user_agent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)'
  values = {'safe' : 'off'}
  headers = { 'User-Agent' : user_agent }
  data  = urllib.parse.urlencode(values)
  data = data.encode('utf-8')
  req = urllib.request.Request('http://www.msn.com/ja-jp/', None, headers)

  with urllib.request.urlopen(req) as page:
    # WebページのURLを取得する
    # infoメソッドは取得したページのメタデータを返す
    # readlinesでWebページを取得する
    for line in page.readlines():
      m = re.search('secondary-title\">(.*?)<\/span', line.decode('UTF-8'))
      if m:
        title = m.group(1)
        query = "insert into MSNTitle values (\"" + timestump + "\",\"" + title + "\")"
        try:
          c.execute(query)
          conn.commit()
        except:
          continue
  c.close()