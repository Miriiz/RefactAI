def getMaxFromArr(arr):
    return max(arr)


def getDiscountAmount(products):
    sum = sum(products)
    if sum > 75:
        for i in range(len(products)):
            if products[i] == max(products):
                products[i] = products[i] * 0.6
    sum = sum(products)
    return sum


def getDoublon(arr):
    for i in range(len(arr) - 1):
        for j in range(1, len(arr)):
            if i == j:
                return True
    return False


def endString(string, ending):
    return string.endswith(ending)
