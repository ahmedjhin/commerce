import random
a = 7
b = [1, 2, 4, 5, 6, 7]



def missingnumber(inpok , numberinpok):
    for i in range(1, inpok ):
        if i not in numberinpok:
            print(i)



missingnumber(a,b)