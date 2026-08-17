word=input("Enter the string: ")
# print(word[::-1])
ans=""
for i in range(len(word)-1,-1,-1):
    ans+=word[i]
print(ans)