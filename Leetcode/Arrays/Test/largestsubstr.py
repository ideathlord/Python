def lenOfLargSubStr(s : str) :
    max_len = 0
    map_1 = {}
    start = 0

    # abcabbac
    # bbbbb 
    # {(a,0),(b,1),(c,2)}
    #start, i(next)

    for i, ch in enumerate(s):
        if ch in map_1 and map_1[ch] >= start:
            start = map_1[ch] + 1

        map_1[ch] = i
        max_len = max(max_len, i-start+1)

    return max_len    

s = input("Enter String ")
print("Largest Substr" , lenOfLargSubStr(s))