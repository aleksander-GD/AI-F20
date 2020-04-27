def multiplyBy2(num):
    return num * 2


# remove all even numbers from list

def checkEven(num):
    return (num % 2) == 0


def listOnlyWithEvenNumbers(l):
    return [(en % 2) == 0 for en in l]


def testComprehensionlists1(list):
    newli = [multiplyBy2(x) for x in list]
    print(newli)

def main():
    testComprehensionlists1([1, 3, 5, 7])
    print(listOnlyWithEvenNumbers([1, 4, 3, 6, 7]))


if __name__ == '__main__':
    main()
