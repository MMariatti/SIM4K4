print("1 - Metodo congruente Mixto\n2 - Metodo congruente Multiplicativo \n3 - salir \n")

opc = int(input("Ingrese una opción :"))

while opc != 3:

    if opc == 1:

        semilla = int(input("Ingrese la semilla : "))
        print("==================================================================")
        a = int(input("Ingrese el valor de 'a' : "))
        print("==================================================================")
        constante = int(input("Ingrese el valor de la constante : "))
        print("==================================================================")
        m = int(input("Ingrese el valor de m :"))
        print("==================================================================")
        numeros = int(input("Ingrese la cantidad de numeros que desea generar : "))
        print("==================================================================")
        print("Los valores ingresados son: \n Semilla :", semilla, "\n a :", a, "\n Constante : ", constante, "\n m :", m, "\n La cantidad de numeros a generar :", numeros, "\n")

        print("Generando numeros aleatorios por el metodo de congruencia mixta \n")

        for i in range(numeros):
            if i == 0:

                nRandom = semilla / m

                print("Numero :", i + 1, " | Semilla:", semilla, " | número random : ", nRandom)
            else:
                semilla = (a * semilla + constante) % m
                nRandom = semilla / m


                print("Numero :", i + 1, " | X+1 :", semilla, " | Número random : ", nRandom)
        opc = int(input("Ingrese una opción :"))

    elif opc == 2:

        semilla = int(input("Ingrese la semilla : "))
        print("==================================================================")
        a = int(input("Ingrese el valor de 'a' : "))
        print("==================================================================")
        m = int(input("Ingrese el valor de m :"))
        print("==================================================================")
        numeros = int(input("Ingrese la cantidad de numeros que desea generar : "))
        print("==================================================================")
        print("Los valores ingresados son: \n Semilla :", semilla, "\n a :", a, "\n m :", m, "\n La cantidad de numeros a generar :", numeros, "\n")
        print("Generando numeros aleatorios por el Metodo de congruencia multiplicativa\n")
        for i in range(numeros):
            if i == 0:

                nRandom = semilla / m

                print("Numero :", i + 1, " | Semilla:", semilla, " | número random : ", nRandom)
            else:
                semilla = (a * semilla) % m
                nRandom = semilla / m
                print("Numero :", i + 1, " | X+1 :", semilla, " | Número random : ", nRandom)

        opc = int(input("Ingrese una opción :"))
