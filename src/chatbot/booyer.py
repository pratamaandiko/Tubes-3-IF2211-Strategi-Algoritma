def buildIndex(pattern):
    chars = [-1]*128 #ASCII is 128

    for i in range(len(pattern)):
        chars[ord(pattern[i])] = i

    return chars

def bmMatch(text : str, pattern : str): #mencari apakah pattern terdapat pada text
    n = len(text)
    m = len(pattern)

    if(m>n): 
        return False #pattern yang dicari lebih besar daripada teks
    else:
        chars = buildIndex(pattern) #inisialisasi array untuk funsi L
        i=0 #indeks shifting
        while(i <= n-m):
            j = m-1
            while (j>=0) and (pattern[j] == text[i+j]):
                j-=1 #mirror glass
            if j<0:
                return True #pattern ketemu
            else:
                i += max(1, j-chars[ord(text[i+j])]) #proses shifting
        return False #pattern tidak ketemu

def bmIndex(text : str, pattern : str): #mencari indeks pertama kemunculan pattern pada text
    n = len(text)
    m = len(pattern)

    if(m>n):
        return -1 #pattern yang dicari lebih besar daripada teks
    else:
        chars = buildIndex(pattern) #inisialisasi array untuk funsi L
        i=0 #indeks shifting
        while(i <= n-m):
            j = m-1
            while (j>=0) and (pattern[j] == text[i+j]):
                j-=1 #mirror glass
            if j<0:
                return i #pattern ketemu
            else:
                i += max(1, j-chars[ord(text[i+j])]) #proses shifting
        return -1 #pattern tidak ketemu

'''
result = bmMatch("1111111111111111111111111111111 1111111111111111111asdfasdfasdfsad11111111111111", "fasd")
print(result)
'''
