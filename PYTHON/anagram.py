map={}
word1=input("Enter a word1: ")
word2=input("Enter a word2: ")
if(len(word1)!=len(word2)):
    print("not an anagram")
else:
    for ch in range(0,len(word1)):
        if ch in map:
            map[ch]+=1
        else:
            map[ch]=1
    for ch in range(0,len(word2)):
        if ch in map:
            map[ch]-=1
        else:
            print("Not an anagram")
            break
    if map.values()==0:
        print("Valid Anagram")
    else:
        print("Not an anagram")
    