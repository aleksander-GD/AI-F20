'''
Find all of the numbers from 1-1000 that are divisible by 7

Find all of the numbers from 1-1000 that have a 3 in them

Count the number of spaces in a string

Remove all of the vowels in a string

Find all of the words in a string that are less than 4 letters

Challenge:

Use a dictionary comprehension to count the length of each word in a sentence.

Use a nested list comprehension to find all of the numbers from 1-1000 that are divisible by any single digit besides 1 (2-9)

For all the numbers 1-1000, use a nested list/dictionary comprehension to find the highest single digit any of the numbers is divisible by
'''


# Find all of the numbers from 1-1000 that are divisible by 7

def createList(f, t):
    return list(range(f, t))


def divisableBy7(n):
    return (n % 7) == 0


def divisableBy7ListCompre(li):
    return [number for number in range(1000) if divisableBy7(number)]


def main():
    print(divisableBy7ListCompre(createList(1, 1000)))


if __name__ == '__main__':
    main()
