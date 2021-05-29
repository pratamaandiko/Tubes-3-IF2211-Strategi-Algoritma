import re
from booyer import bmMatch
from Levenshtein import *

def checkTypo(text, match):
    listWord = text.lower().split(" ")#split text berdasarkan spasi
    for word in listWord:
        if(jaro(word, match) > 0.75 and jaro(word, match) != 1):
            print("did you mean " + match)
            return True
    return False

checkTypo("Deddline", "deadline")
checkTypo("Twwubesz", "tubes")
# comparator = r'.*([a|A][p|P][a|A] [s|S][a|A][j|J][a|A]).*'
# comparator1 = 'deadline' or 'Deadline'
# txt = input("Masukkan text: ")
# x = re.match(comparator, txt)
# splt = txt.split(" ")
# if(x):
#     if(bmMatch(txt, comparator1)):
#         print("Match")
# else:
#     print("Not Match")

# isTypo = False
# if(x):
#     for sp in splt:
#         if(jaro(sp, comparator1)>0.75 and jaro(sp, comparator1)!=1):
#             print("ada yang mendekati deadline")
#             print(sp)
#             isTypo = True
#             break
#     if(bmMatch(txt, comparator1) and isTypo == False):
#         print("masuk ke segmen deadline")

#     elif(isTypo == False):
#         print("input invalid")
