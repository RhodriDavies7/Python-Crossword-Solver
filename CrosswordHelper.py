import sys, http.client, json
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

with open('/home/rhodri/Desktop/Python/CrosswordHelper/wordlist.txt', 'r') as file:
    wordlist = [line.strip() for line in file]

def crosswordHelper(string, widget):
    widget.clear()
    word = string.upper()

    lengthWords = []
    for items in wordlist:
        if len(items) == len(word):
            lengthWords.append(items)

    letterWord = []
    for letters in word:
        letterWord.append(letters)

    indexes = []
    for i in range(len(letterWord)):
        if letterWord[i] == "*":
            indexes.append(i)

    for q in sorted(indexes, reverse=True):
                del letterWord[q]

    match = []
    for word1 in lengthWords:
        possibleMatches = []
        for letters1 in word1:
            possibleMatches.append(letters1)
        finalWord = ''.join(possibleMatches)
        for z in sorted(indexes, reverse=True):
            del possibleMatches[z]
            if possibleMatches == letterWord:
                match.append(finalWord)

    for matches in match:
        widget.addItem(matches)

def definitionSearch(string, widget):
    widget.clear()
    conn = http.client.HTTPSConnection("wordsapiv1.p.rapidapi.com")

    headers = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        'x-rapidapi-key': "16393d5041mshe5a763039089b68p198f4djsn5ed274ef7d01"
        }

    searchStr = "/words/%s/" % (string)
    conn.request("GET", searchStr, headers=headers)

    res = conn.getresponse()
    data = res.read()
    dataDict = json.loads(data.decode("utf-8"))
    for item in dataDict["results"]:
        widget.addItem(item["definition"] + "\n")

class Handler(QMainWindow):
    def __init__(self):
        super(Handler,self).__init__()
        loadUi('/home/rhodri/Desktop/Python/CrosswordHelper/CrosswordHelperGUI.ui', self)
        self.btn_search.clicked.connect(self.on_btn_search_clicked)
    def on_btn_search_clicked(self):
        listWidget = self.listWidget
        crosswordHelper(self.search_word.text(), listWidget)
    def on_btn_search2_clicked(self):
        listWidget2 = self.listWidget2
        definitionSearch(self.search_definition.text(), listWidget2)
    

app = QApplication(sys.argv)
widget = Handler()
widget.show()
sys.exit(app.exec_())

