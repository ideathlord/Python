dict_mapping = {
    "1" : "One",
    "2" : "Two",
    "3" : "Three",
    "4" : "Four",
    "5" : "Five",
    "6" : "Six",
    "7" : "Seven",
    "8" : "Eight",
    "9" : "Nine",
    "0" : "Zero"
}
def print_phone_no():

    global dict_mapping
    list_inp = input("Phone : " )
    output = ""
    for ch in list_inp:
        output += dict_mapping.get(ch , "!") + " "
    print(output)    

print_phone_no()