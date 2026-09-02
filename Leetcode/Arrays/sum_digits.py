#i have a number that is the sum of digits of number. Find the orginal number and start from 1

target = int(input("Enter the sum of digits: "))

curr = 1
while True:
    if sum(int(i) for i in str(curr)) == target:
        print("The original number is:", curr)
        break
    curr += 1
    
