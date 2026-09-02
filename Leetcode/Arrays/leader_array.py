# array = [10, 15, 5, 8, 37, 23, 28, 17]

# leader in array is an element which is greater than all the elements to its right side.

# input_array = [10, 15, 5, 8, 37, 23, 28, 17]

# input array from user
# input_array = list(map(int, input("Enter the elements of the array separated by space: ").split()))

#input array using for loop

input_array = []
n = int(input("Enter the number of elements in the array: "))
for i in range(n):
    element = int(input(f"Enter element {i+1}:"))
    input_array.append(element)

leaders = []

for i in range(len(input_array)):
    is_lead = True
    for j in range(i + 1, len(input_array)):
        if input_array[i] <= input_array[j]:
            is_lead = False
            break
    if is_lead:
        leaders.append(input_array[i])

print("Leaders in the array are:", leaders)