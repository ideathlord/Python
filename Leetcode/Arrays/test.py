Abcadefghbikj

abcadefghbikj

duplicate = False

for i in range(len(s)):
    for j in range(i+1,len(s)):
        start = s[i]
        next = s[j]
        max_value = next - start + 1

        for k in range(i+1,j):
            if s[k] == s[i]:
                duplicate = True
                break   



    next = s[i]
    max_value = next - start + 1
