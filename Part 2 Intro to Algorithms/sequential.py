# for unsorted list
def sequentialSearch(theValues, target):
    n = len(theValues)

    for i in range(n):
        #  If the target is in the ith element, return True
        if theValues[i] == target:
            return True
    return False  # If not found, return False

# for sorted list
def sortedSequentialSearch(theValues, target):
    n = len(theValues)
    for i in range(n):
        # if the target is in the ith element, return True
        if theValues[i] == target:
            return True
        # if target is larger than the ith element,
        # it is not in the sequence
        elif theValues[i] > target:
            return False
    return False


# Test Codes
print("UNSORTED LIST:")
unsortedList = [11, 4, 5, 9, 2, 17, 24]
print(sequentialSearch(unsortedList, 9))
print(sequentialSearch(unsortedList, 30))

print()
print("SORTED LIST:")
sortedList = [-4, 1, 2, 3, 7, 10, 20]
print(sequentialSearch(sortedList, 10))
print(sequentialSearch(sortedList, 5))

