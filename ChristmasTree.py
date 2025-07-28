character=input('Enter a charater: ')
number=int(input('Enter a number: '))
for level in range(number):
    startpos= number-level-1
    for i in range (startpos):
        print(' ', end='')
    for i in range(level+1):
            print(character, end=' ')
    print()
print('Merry Christmas!')

