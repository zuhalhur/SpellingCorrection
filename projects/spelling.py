# coding = utf-8

import MySQLdb
import edit
import sys

connection = MySQLdb.connect (host = "localhost", user = "root", passwd = "161214tz", db = "nlp",charset='utf8')
cursor = connection.cursor ()
previousWord=''
nextWord=''
mostcommon=[]
predicts=[]
predictsPreCount=[]
predictsNextCount=[]
totalCount=[]
errorIndex = 0
print "Enter an input:"
filename = raw_input()
words = filename.split(' ')
for i in range(0,len(words)):
    words[i] = unicode(words[i],"utf-8")
length = words.__len__()
datas=[]
def getMax(total):
    i = 0;
    for index in range(0,len(total)):
        if(total[index]>total[i]):
            i = index
    return i
cursor.execute ("SELECT text,COUNT(text) AS `value_occurrence` FROM `hw2` GROUP BY `text` ORDER BY `value_occurrence` DESC LIMIT 16")
data=cursor.fetchall()
for row in data:
    mostcommon.append(row[0].lower())
for i in range(0,len(words)):
    cursor.execute("Select count(*) from hw2 where text=%s",words[i])
    a=cursor.fetchall()
    if(a[0][0]==0):
        size=len(words[i])
        errorIndex = i
        cursor.execute("select text from hw2 where text like %s and (char_length(text)='%s' or char_length(text)='%s' or char_length(text)='%s' or char_length(text)='%s' or char_length(text)='%s')",
            ((words[i][:1] + '%'),size-1,size,size+1,size-2,size+2))
        results = cursor.fetchall()
        for row in results:
            if (edit.editDistDP(words[i].lower(),row[0].lower())<=2):
                if (row[0].lower() not in predicts):
                    predicts.append(row[0].lower())
        counter = i-1
        while(counter>=0):
            uniWord = words[counter].lower()
            if (uniWord not in mostcommon):
                previousWord = words[counter]
                break;
            counter=counter-1;
        counter = i + 1
        while (counter < len(words)):
            uniWord = words[counter].lower()
            if (uniWord not in mostcommon):
                nextWord = words[counter]
                break;
            counter = counter + 1;
        break;
for i in range(0,len(predicts)):
    cursor.execute(
        "Select COUNT(*) from hw2 as R INNER JOIN (select FName, S_No, IX, TEXT from hw2 where text=%s) AS T where R.FName = T.FName AND R.S_No = T.S_No AND R.IX>T.IX and R.TEXT=%s",
        (previousWord, predicts[i]))
    data = cursor.fetchall()
    for row in data:
        predictsPreCount.append(row[0])
for i in range(0,len(predicts)):
    cursor.execute(
        "Select COUNT(*) from hw2 as R INNER JOIN (select FName, S_No, IX, TEXT from hw2 where text=%s) AS T where R.FName = T.FName AND R.S_No = T.S_No AND R.IX>T.IX and R.TEXT=%s",
        (predicts[i],nextWord))
    data = cursor.fetchall()
    for row in data:
        predictsNextCount.append(row[0])
for i in range(0,len(predicts)):
    totalCount.append(predictsPreCount[i]+predictsNextCount[i])
maximum = getMax(totalCount)
if(len(predicts)!=0):
    words[errorIndex] = predicts[maximum]
else:
    print 'Hata, tahmin bulunamadi !!!'
for i in range(0,len(words)):
    print words[i]
