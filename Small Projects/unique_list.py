list_1 = [2,3,4,5,6,2,3,4,12,43,45,24]
list_2 = []
list_3 = [2,2,3,4,5,6,1,2,3,2,4,2,4,5,6]


def find_unique(list_1):
    unique = []
    # if list_1.empty():
    #     print("empty")
    #     exit
    for i in list_1:
        if i not in unique:
            unique.append(i)
    unique.sort(reverse=False)
    print(unique)   

find_unique(list_1)    
find_unique(list_2) 
find_unique(list_3)    