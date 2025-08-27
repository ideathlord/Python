def print_age_name(name, age):
    print(f"My Name is {name} and my age is {age}")

def input_age_name():
    name = input("Enter your Name : ")
    age = input("Enter your Age : ")
    print_age_name(name, age)
    return name, age

input_age_name()