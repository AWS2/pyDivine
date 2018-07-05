

from random import randint


def endevina():
    secret = randint(1,100)
    intents = 0
    while True:
        intents += 1
        num = int(input("Endevina el número (entre 1 i 100): "))
        if secret > num:
            print("El número secret és major")
        elif secret < num:
            print("El número secret és menor")
        else:
            print("L'has encertat: el número secret era "+str(secret))
            return intents


if __name__ == "__main__":
    intents = endevina()
    print( "Ho has resolt en {} intents".format(intents) )

