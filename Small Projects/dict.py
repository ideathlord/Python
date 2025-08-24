customer = {
    "name" : "abhishek",
    "age" : 25,
    "is_verified" : True,
    "gender" : "male"
}

def dict_key_value(dict):

    list_dict = list(dict.keys())
    for i in list_dict:
        print(i," : ",dict.get(i))

dict_key_value(customer)