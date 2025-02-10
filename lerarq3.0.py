

########## VERSÃO ANTI INCESTO ####################

import random
vet = []
taxamut = 5         ########
populacao = 500
pop = populacao +1
r = ''
turma = []
profe = []
ativi = []
protur = []
tst = []
conatividades = 26     #######
valordeloop = 50
pid = 0
tid = 0
aid = 0
IDV = -1

with open ("novapae.txt", "r") as arquivo:
    linhas = arquivo.readlines()
    linhas = str(linhas)
    linhas = linhas.replace("\\t","','")
    linhas = linhas.replace("\\n',","'],[")
    linhas = "vet = ["+str(linhas)+"]"
    exec (linhas)

for a in range (0,len(vet),1):
    t = vet[a][0]
    p = vet[a][1]
    A = vet[a][2]
    ch =vet[a][3]
    ob =vet[a][4]
    ID =vet[a][5]
    t = t.replace(" ","_")
    t = t.replace(".","")
    p = p.replace(" ","_")
    p = p.replace(".","")
    A = A.replace(" ","_")
    A = A.replace(".","")
    if p not in globals():
        profe.append(p)
        exe = str(p)+"="+str(pid)
        exec (exe)
        pid = pid + 1
    if t not in globals():
        turma.append(t)
        exe = str(t)+"="+str(tid)
        exec (exe)
        tid = tid + 1
    if A not in globals():
        ativi.append(A)
        exe = str(A)+"="+str(aid)
        exec (exe)
        aid = aid + 1

for a in range (0,len(vet),1):
    ID = vet[a][5]
    X = vet[a][1]
    Y = vet[a][0]
    Z = vet[a][2]
    ch = vet[a][3]
    ob = vet[a][4]
    X = X.replace(" ","_")
    X = X.replace(".","")
    Y = Y.replace(" ","_")
    Y = Y.replace(".","")
    Z = Z.replace(" ","_")
    Z = Z.replace(".","")
    nlinp = "nlinp = " + X
    nlint = "nlint = " + Y
    exec (nlinp)
    exec (nlint)
    linp = "["+str(nlinp)+"]"
    lint = "["+str(nlint)+"]"
    vetor = "veto = ["+str(lint)+","+str(linp)+",'"+str(Z)+"',"+ch+",'"+ob+"',"+ID+"]"
    exec (vetor)
    protur.append(veto)

a = 1

prot = []
junt1 = []
junt2 = []
gatprof = 0
gatturm = 0

while a < len(protur):
    if protur[a-1][5] == protur[a][5]:
        if protur[a-1][0] != protur[a][0]:
            junt1 = [protur[a-1][0][0],protur[a][0][0]]
            gatprof = 1
        if protur[a-1][1] != protur[a][1]:
            junt2 = [protur[a-1][1][0],protur[a][1][0]]
            gatturm = 1
    if protur[a-1][5] != protur[a][5]:
        if gatprof == 1 and gatturm == 1:
            prot.append([junt1,junt2,protur[a-1][2],protur[a-1][3],protur[a-1][4]])
        if gatprof == 1 and gatturm == 0:
            prot.append([junt1,protur[a-1][1],protur[a-1][2],protur[a-1][3],protur[a-1][4]])
        if gatprof == 0 and gatturm == 1:
            prot.append([protur[a-1][0],junt2,protur[a-1][2],protur[a-1][3],protur[a-1][4]])
        if gatprof == 0 and gatturm == 0:
            prot.append([protur[a-1][0],protur[a-1][1],protur[a-1][2],protur[a-1][3],protur[a-1][4]])
        gatprof = 0
        gatturm = 0
    if a+1 == len(protur):
        if gatprof == 1 and gatturm == 1:
            prot.append([junt1,junt2,protur[a][2],protur[a][3],protur[a][4]])
        if gatprof == 1 and gatturm == 0:
            prot.append([junt1,protur[a][1],protur[a][2],protur[a][3],protur[a][4]])
        if gatprof == 0 and gatturm == 1:
            prot.append([protur[a][0],junt2,protur[a][2],protur[a][3],protur[a][4]])
        if gatprof == 0 and gatturm == 0:
            prot.append([protur[a][0],protur[a][1],protur[a][2],protur[a][3],protur[a][4]])
        
    a = a + 1

protur = prot.copy()
protur = [protur]

tmut = (conatividades*populacao)/taxamut
t = 0
p = 0
a = 0

# ['Turma', 'Professor', 'Atividade', 'CH', 'Obs']
#
# [[turma[atividade,ch,modo],turma,[atividade,ch,modo]],[turma,[atividade,ch,modo]]]
# (x[0][0][(x[0][0].find('_and_'))+5:])

profbase = []
repvet = []
for i in range (0,len(protur[0]),1):
    for j in range (i,len(protur[0]),1):
        if i != j:
            if protur[0][i] == protur[0][j]:
                repvet.append(j)

repvet.sort(reverse=True)

remvet = []
a = 0
for i in range (0,len(repvet),1):
    if a == 0:
        remvet.append(repvet[i])
        a = a + 1
    if a > 0:
        if repvet[i] != remvet[a-1]:
            remvet.append(repvet[i])
            a = a + 1

for i in (remvet):
    del protur[0][i]


SOL = []
crom = "crom-1=  "
N = -1
n = 0
for rep in range (0,pop,1):
    for a in range(len(protur[0])):
        SOL.append([0]*20)
        for i in range(int(protur[0][a][3])):
            SOL[a][i]=1
        random.shuffle(SOL[a])
    crom = crom.replace(str(N),str(n))
    crom = str(crom) + str(SOL)
    exec (crom)
    N = N + 1
    n = n + 1
    crom = crom[:8]
    SOL = []

#a = 0
#for s in SOL:
   #Imprime para cada atividades a alocação na solução, obs, ch, turmas e profs.
   #print("%s %s %2d %s %s" % (s,protur[0][a][4],protur[0][a][3],protur[0][a][0], protur[0][a][1]))
   #a = a + 1

########################################################################################################################
#### CALCULO DE CUSTO ###############################################################
for repeticao in range (0,valordeloop,1):

    vpon = []
    crom = "SOL = crom-1"
    cromrec = "crom-1 = SOL"
    N = -1
    #pathx -> usados
    for n in range (0,pop,1):
        crom = crom.replace(str(N), str(n))
        cromrec = cromrec.replace(str(N), str(n))
        exec (crom)
        N = N + 1
        total = 0
        a = 0
        marcador = 0
        for temporario in protur[0]:
            if temporario[4] == "G": # GERMINADA PESO = 10
                for p in range(len(SOL[a])-1):
                    if p not in [3, 7, 11, 15]:
                        if SOL[a][p] + SOL[a][p+1] != 2:
                            marcador = 1
                if marcador == 1:
                    total = total + 10
                    marcador = 0
            if temporario[4] == "S": # SEPARADA PESO = 50
                x = 0
                for p in range(len(SOL[a])):
                    if p in [4,8,12,16]:
                        x = 0
                    x = x + SOL[a][p]
                    if x >= 2:
                        marcador = 1
                if marcador == 1:
                    total = total + 50
                    marcador = 0
            a = a + 1

        for p in range(20):
            histograma = [0]*len(turma)
            a = 0
            for temporario in protur[0]:
                if SOL[a][p] == 1:
                    for t in protur[0][a][0]:
                        histograma[t] = int(histograma[t])+1
                a = a + 1

            for h in histograma:
                if h >= 2:
                    total = total + (h-1)*1000 ##### PESO CONFLITO = 1000

        for p in range(20):
            histograma = [0]*len(profe)
            a = 0
            for temporario in protur[0]:
                if SOL[a][p] == 1:
                    for t in protur[0][a][1]:
                        histograma[t] = histograma[t]+1
                a = a + 1

            for h in histograma:
                if h >= 2:
                    total = total + (h-1)*1000 ##### PESO CONFLITO = 1000
        for p in range (len(SOL)):
            chtot = 0
            for q in range (len(SOL[p])):
                if SOL[p][q] == 1:
                    chtot = chtot+1
            if chtot != protur[0][p][3]:
                Pos = 0
                chtot = chtot - protur[0][p][3]
                if chtot < 0:
                    while chtot < 0:
                        if SOL[Pos] == 0:
                            SOL[Pos] = 1
                            chtot = chtot + 1
                        Pos = Pos + 1
                        if Pos == 20:
                            break
                if chtot > 0:
                    while chtot > 0:
                        if SOL[Pos] == 1:
                            SOL[Pos] = 0
                            chtot = chtot - 1
                        Pos = Pos + 1
                        if Pos == 20:
                            break
        exec (cromrec)
        vpon.append([total,n])
    result = "result =" + str(vpon)
    exec(result)
    result.sort()
    vpon.sort() ### VETOR DE PONTUAÇÃO
    vma = []
    vpa = []
    for i in range (0,len(vpon)-40,2):
        generopai = 0
        generomae = 0
        trava = 0
        troca = 0
        gene = 0
        vetfilho = []
        vetfilha = []
        while trava == 0:
            if result[generomae-1][1]%2 == 0:#adiciona -1
                trava = 1
                vma.append(result[generomae-1][1])#adiciona -1
            else:
                generomae = generomae+1
        trava = 0
        while trava == 0:
            if result[generopai-1][1]%2 != 0:#adiciona -1
                trava = 1
                vpa.append(result[generopai-1][1])#adiciona -1
            else:
                generopai = generopai+1
        vetmae = "vetmae = crom"+str(result[generomae][1])
        vetpai = "vetpai = crom"+str(result[generopai][1])
        exec(vetmae)
        exec(vetpai)
        for j in range (0,len(vetmae),1):
            fotem = []
            fatem = []
            troca = 0
            gene = 0
            for k in range (0,len(vetmae[j]),1):
                if troca >= 4:
                    troca = 0
                    gene = (gene-1)*-1
                if gene == 0:
                    troca = troca + 1
                    fotem.append(vetmae[j][k])
                    fatem.append(vetpai[j][k])
                if gene == 1:
                    troca = troca + 1
                    fotem.append(vetpai[j][k])
                    fatem.append(vetmae[j][k])
            vetfilho.append(fotem)
            vetfilha.append(fatem)
        for j in range (0,len(vetfilho),1):
            for k in range (0,len(vetfilho[j])):
                mutar = random.randint(0, int(tmut))
                if mutar == 1:
                    if vetfilho[j][k] == 1:
                        vetfilho[j][k] = 0
                    else:
                        vetfilho[j][k] = 1
                mutar = random.randint(0, int(tmut))
                if mutar == 1:
                    if vetfilha[j][k] == 1:
                        vetfilha[j][k] = 0
                    else:
                        vetfilha[j][k] = 1
        crom = "crom"+str(result[generomae][1])+"= vetfilha"
        exec (crom)
        crom = "crom"+str(result[generopai][1])+"= vetfilho"
        exec (crom)
        result.pop(generomae)
        result.pop(generopai)
    print (vpon[0])

#############################################################################################
######### CALCULO DE CUSTO ########################################################

cromossomofinal = "print (crom" + str(vpon[0][1])+"[a])"
for a in range (0,len(crom1),1):
    exec (cromossomofinal)
