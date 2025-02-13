import datetime

def run(response_data):
    f = open("oi.txt", "r+")
    tstamp = open("oi-tstamp.txt", "r+")

    status = f.read()

    if (status == "0" or status == "2"):
        # Po rodar

        # Determina estado como rodando
        f.seek(0)
        f.write("1")
        f.truncate()
        
        # Esse programa implementa um algoritmo genético para resolver
        # o problema de High School Timetabling (HSTP), garantindo que as restrições
        # fortes sejam atendidas e tentando minimizar as violações da restrição fraca.
        
        #### Restrições fortes:
        # H1 - A carga horária de cada atividade deve ser atendida.
        # H2 - Um professor não pode ter mais de uma aula ao mesmo tempo.
        # H3 - Uma turma não pode ter mais de uma aula simultânea.
        
        #### Restrição fraca:
        # S1 - Deve-se minimizar o número de aulas duplas não atendidas
        # (duas aulas seguidas para a mesma atividade).
        
        #### Etapas do programa:
        # 1) Criação de soluções iniciais aleatórias.
        # 2) Avaliação das soluções com a função fitness().
        # 3) Seleção das melhores soluções usando torneio().
        # 4) Geração de novas soluções através de crossover().
        # 5) Repetição do processo até encontrar um horário adequado.
        
        import random
        import copy
        
        #### Definição de parâmetros
        TURNOS = 1 #NÚMERO DE TURNOS
        PERIODOS = 4  # Número de períodos de aula por turno
        DIAS = 5  # Número de dias na semana
        TIMESLOTS = PERIODOS * DIAS * TURNOS  # Total de horários disponíveis na semana
        
        
        # Peso atribuído a conflitos (para penalização na função fitness)
        PESO_CONFLITOS = 1000
        
        # Peso atribuído às aulas duplas não atendidas
        PESO_AULAS_DUPLAS = 1
        
        #### Lista de atividades, cada uma contendo:
        # - Turma associada
        # - Professor responsável
        # - Carga horária total da disciplina
        # - Número mínimo de aulas duplas desejadas
        # - Recurso a ser usado
        
        ATIV = [item for item in response_data if item['turma'] is not None and item['prof'] is not None]
        
        # Imprime a matriz de horários gerada
        # Cada linha representa uma atividade e os horários onde está alocada
        # Cada coluna representa um timeslot
        
        def imprimir(sol):
            linha = ""
            for i in range(len(ATIV)):              # Percorre cada atividade
                for j in range(TIMESLOTS):          # Percorre cada timeslot
                    linha += str(sol[i][j]) + " "   # Converte o valor do elemento da matriz para string
                linha += str(ATIV[i]) + "\n"        # Adiciona o valor da atividade no final da linha
            print(linha)
        
        # Função de avaliação (fitness)
        # Calcula a quantidade de conflitos no horário gerado
        # Contabiliza conflitos de turma e professor compartilhando o mesmo horário
        
        def fitness(sol):
            total_conflitos = 0
            for t in range(TIMESLOTS):
                c = []
                for i in range(len(ATIV)):
                    if sol[i][t] == 1:
                        c.append("T" + str(ATIV[i]["turma"]))  # Identifica a turma
                        c.append("P" + str(ATIV[i]["prof"]))  # Identifica o professor
                        if ATIV[i] ["recurso"] is not None:
                          c.append("R" + str(ATIV[i]["recurso"]))
                        if ATIV[i] ["prof2"] is not None:
                          c.append("P" + str(ATIV[i]["prof2"]))
        
                total_conflitos += len(c) - len(set(c))  # Conta os conflitos
        
            # Cálculo das aulas duplas não atendidas
            total_duplas_faltando = 0
            for i, atividade in enumerate(ATIV):
                duplas_desejadas = atividade["duplas"]
                duplas_atendidas = 0
        
                for d in range(DIAS):
                    for t in range(TURNOS):
                        for p in range(PERIODOS - 1):  # Verificar pares consecutivos de períodos
                            t1 = d * (TURNOS * PERIODOS) + t * PERIODOS + p
                            t2 = t1 + 1  # Período imediatamente seguinte
                            if sol[i][t1] == 1 and sol[i][t2] == 1:
                                duplas_atendidas += 1
        
                total_duplas_faltando += max(0, duplas_desejadas - duplas_atendidas)
        
            return PESO_CONFLITOS * total_conflitos + PESO_AULAS_DUPLAS * total_duplas_faltando
        
        # Mutação: altera aleatoriamente horários em uma solução
        #def mutacao(sol, prob_mutacao):
        #    if random.random() < prob_mutacao:
        #      i = random.choice(range(len(ATIV)))
        
        #      horarios_alocados = [t for t in range(TIMESLOTS) if sol[i][t] == 1]
        #      t_remover = random.choice(horarios_alocados)
        #      sol[i][t_remover] = 0
        
              # Aloca um novo horário aleatório
        #      t_novo = random.choice([t for t in range(TIMESLOTS) if sol[i][t] == 0 and t != t_remover])
        #      sol[i][t_novo] = 1
        
        # Nova Mutação:
        def mutacao(filho, taxa):
            if random.random() < taxa:
              i = random.randint(0,len(ATIV)-1)
              random.shuffle(filho[i])
        
        
        # Exibe o relatório final do horário formatado
        # Mostra os horários e quais professores estão alocados para cada turma
        def relatorio(sol):
            # Obter todos os IDs únicos das turmas
            turmas_ids = sorted(set(ativ["turma"] for ativ in ATIV))  
            
            # Imprime o cabeçalho
            linha = "Horário    "
            for t in range(TIMESLOTS):
                linha += f"{t:<2} "
            print(linha)

            # Imprimir o horário de cada turma
            for turma in turmas_ids:  # Itera sobre os IDs reais das turmas
                linha = f"Turma {turma:<2} | "

                for t in range(TIMESLOTS):
                    profs = []  # Guarda os professores com aula na turma no timeslot t
                    for i in range(len(ATIV)):
                        if ATIV[i]["turma"] == turma and sol[i][t] == 1:
                            profs.append(ATIV[i]["prof"])

                    celula = "."
                    if len(profs) == 1:
                        celula = str(profs[0])
                    elif len(profs) > 1:
                        celula = "X"

                    linha += f"{celula:<2} "
                print(linha)

        def gerar_matriz(sol):
            # Criar matriz com 20 entradas, uma para cada período
            matriz = [[] for _ in range(TIMESLOTS)]
            
            # Preencher a matriz
            for i, atividade in enumerate(ATIV):
                for t in range(TIMESLOTS):
                    if sol[i][t] == 1:
                        matriz[t].append([atividade["prof"], atividade["turma"], atividade["prof2"], atividade["atv"],])
            
            return matriz
        
        # Cria uma solução inicial aleatória
        # Distribui as aulas pelos horários de forma aleatória
        def criar():
            sol = []
            for i in range(len(ATIV)):
                sol.append([0] * TIMESLOTS)        # Cria uma linha zerada
                for j in range(ATIV[i]["ch"]):     # Distribui as aulas pelo horário
                    sol[i][j] = 1
                random.shuffle(sol[i])             # Mistura os horários aleatoriamente
            return sol
        
        # Seleção por torneio: escolhe o melhor entre dois indivíduos aleatórios
        def torneio(populacao):
            sorteados = random.sample(populacao,2)              # Escolhe dois horários aleatoriamente
            if fitness(sorteados[0]) < fitness(sorteados[1]):   # O melhor é aquele com menor número de conflitos
               return sorteados[0]
            else:
               return sorteados[1]
        
        # Crossover: cria um novo indivíduo combinando características do pai e da mãe
        def crossover(pai, mae):
            filho = []
            for i in range(len(ATIV)):      # Para cada atividade (linha da matriz)
                if random.random() < 0.5:   # 50% de chance de herdar do pai
                   filho.append(pai[i])
                else:                       # 50% de chance de herdar da mãe
                   filho.append(mae[i])
            return copy.deepcopy(filho)
        
        # Algoritmo Genético principal
        def algoritmo_genetico(tam_pop, num_geracoes):
        
        # Cria uma população inicial de horários aleatórios
        # Seleciona os melhores horários e cria novas combinações
        # Avalia os horários até encontrar um que não tenha conflitos
            melhor_valor = 99999999
            melhor_sol = []
            populacao = []
            for i in range(tam_pop):
               populacao.append(criar())
        
            for g in range(num_geracoes):
                nova_populacao = []
                for i in range(tam_pop):
                    pai = torneio(populacao)         # Escolhe um pai
                    mae = torneio(populacao)         # Escolhe uma mãe
                    filho = crossover(pai, mae)      # Gera um filho misturando os horários do pai e da mãe
                    mutacao(filho,0.001)             # Aplica mutação ao filho
                    nova_populacao.append(filho)
                populacao = nova_populacao           # Substitui a população antiga pela nova
        
                # retorna o valor da melhor e pior solução da população
                melhor = min([fitness(s) for s in populacao ])
                if melhor < melhor_valor:
                  melhor_valor = melhor
                  for pop in populacao:
                    if fitness(pop) <= melhor_valor:
                      melhor_sol =copy.deepcopy(pop)
                pior = max([fitness(s) for s in populacao ])
                print(f" Geração {g}: pior/melhor = {pior}/{melhor}    {melhor_valor}")
                if melhor == 0:  # Se encontra um horário perfeito sem conflitos, pára
                   break
        
            return melhor_sol # Retorna a melhor solução encontrada
        
        
        S = algoritmo_genetico(5000, 100)
        imprimir(S)
        relatorio(S)

        print(gerar_matriz(S))
        
        print("Z=", fitness(S))

        f.seek(0)
        f.write("2")
        f.truncate()

        f.close()

        # tstamp = open("oi-tstamp.txt", "r+")

        tstamp.seek(0)
        tstamp.write(str(datetime.datetime.now()))
        tstamp.truncate()

        tstamp.close()

        return gerar_matriz(S)
        
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

    f.seek(0)
    f.write("2")
    f.truncate()

    f.close()

# Valores de acompanhamento
# 0: Não rodando
# 1: Rodando
# 2: Concluído