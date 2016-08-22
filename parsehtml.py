# -*- coding: utf-8 -*-
from html.parser import HTMLParser
import os.path
import re
import chardet

from bs4 import BeautifulSoup

class MyHTMLParser(HTMLParser):
    bodyFlg = False
    pFlg = False
    line = ''
    lines = []
        
    def handle_starttag(self, tag, attrs):
        #tagがdivか確認
        if(tag=='div'):
            #属性がなければ戻す
            if(len(attrs)==0):
                return
            #本文でなければもどす
            if(attrs[0][1]!='EntryText' and attrs[0][1]!='ps_text'):
                return
            #print("Encountered a start tag:", tag, attrs[0][1])
            self.bodyFlg = True
##        #tagがpか確認
##        elif(tag=='p'):
##            self.pFlg = True
            
    def handle_endtag(self, tag):
        #本文でなければ無視
        if not self.bodyFlg:
            return
        #タグがdivなら本文終了
        if(tag=='div'):
            #print("Encountered an end tag :", tag)
            self.bodyFlg = False
        #タグがpならその範囲を一文とみなす
        #pでないパターンがある
        #elif(tag=='p'):
        #一文を書き込み初期化
        #文字数0の場合は無視
        if(len(self.line) > 0):
            #空白を削除し、改行コードで分割
            self.lines.append(self.line.strip().splitlines())
        self.line = ''
        self.pFlg = False
            
    def handle_data(self, data):
        #本文でなく、かつpの中でもなければ無視
        #pでないパターンがある
        #if not self.bodyFlg or not self.pFlg:
        #    return
        if not self.bodyFlg:
            return
        self.line += data
##        print("Encountered some data  :", data, self.bodyFlg, self.pFlg)
##        print("linelele",self.line)

#ファイルへ書き込み
def writeToFile(texts,fileName):
    dataDirPath = "./data"
    fileName = os.path.basename(os.path.dirname(fileName))+'.txt'
    # データ用ディレクトリが存在しない場合
    if not os.path.exists(dataDirPath):
        os.mkdir(dataDirPath)

    #ファイルの作成
    try:
        f = open(os.path.join(dataDirPath,fileName),'w')
        for text in texts:
            f.write(text+"\n")
    finally:
        f.close()   
    

#配列に変換した文字列を返す
def makeSplitedText(text):
    #前後の空白を削除
    text = text.strip()
    #行頭の改行を削除
    prog = re.compile(r'^\n',re.MULTILINE)
    result = prog.sub('',text)
    #一行一文の配列に変換
    return result.splitlines()

#ファイルから本文要素のみを抽出
def getText(fileName):
    html = ''
    try:
        f = open(fileName, 'r')
        for line in f:
            html+=line
        soup = BeautifulSoup(html, "html.parser")
        texts = makeSplitedText(soup.find('div', attrs={"class": "EntryText"}).text)
        texts.extend(makeSplitedText(soup.find('div', attrs={"id": "ps_text"}).text))
        writeToFile(texts,fileName)
        
    except:
        f.close()

#ディレクトリの取得
def getDirs(rootDirName):
    dirs = []
    for temp in os.listdir(rootDirName):
        tempPath = os.path.join(rootDirName,temp)
        if os.path.isdir(tempPath):
            dirs.append(tempPath)
    return dirs

def main():
    print("start")
    for dirPath in getDirs('G:/(・∀・)ｱﾋｬ！！/shinobi/20160118/Entry'):
        fileName = os.path.join(dirPath,'index.html')
        if os.path.exists(fileName):
            getText(fileName)
    print("finished")

##print(getText('G:/(・∀・)ｱﾋｬ！！/shinobi/20160118/Entry/1/index.html'))
main()
