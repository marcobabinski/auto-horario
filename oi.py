import time
import random
import os

def run():
    f = open("oi.txt", "r+")

    status = f.read()

    if (status == "0" or status == "2"):
        # Po rodar

        # Determina estado como rodando
        f.seek(0)
        f.write("1")
        f.truncate()


    elif (status == "1"):
        # Ta rodando

        print("To rodano man carma")
        pass
    elif (status == "2"):
        # rodo

        f.seek(0)
        f.write("0")
        f.truncate()
        pass

    time.sleep(10)

    f.seek(0)
    f.write("2")
    f.truncate()

    f.close()
    return(random.choice([1,2,3,4,9]))

run()

# Valores de acompanhamento
# 0: Não rodando
# 1: Rodando
# 2: Concluído