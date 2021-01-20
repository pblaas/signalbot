a = int(input("Enter 1st Number: "))
b = int(input("Enter 2nd Number: "))
def xyz(x):
    switcher = {
        'addition':a+b,
        'multiplication':a*b,
        'subtraction':a-b,
        'division':a/b
    }
    return switcher.get(x,"Oops! Invalid Option")

result=xyz('multiplication')
print(result)
