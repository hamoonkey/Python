"""
『進化とは何か』p98にあったプログラム

参考：
https://www.sist.ac.jp/~kanakubo/research/evolutionary_computing/genetic_algorithms.html
"""

import random
import bisect
import numpy as np

target = "MORE GIDDY IN MY DESIRES THAN A MONKEY"
GENE_LEN = len(target)
MOJI = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ']
LITTER_SIZE = 50
G = 0.2 #エリート率：上位Gはそのままコピー
CROSSOVER_RATE = 0.95
MUTATION_RATE = 0.05
MAX_GENERATION = 2000
CHUKEI = np.floor(MAX_GENERATION/20) #CHUKEI毎に途中経過をprint()する


#print("初期個体群を生成")
darwin_list = []
for j in range(LITTER_SIZE):
    darwin = ""
    for i in range(GENE_LEN):
        darwin = darwin + MOJI[random.randint(0,len(MOJI)-1)]
    darwin_list.append(darwin)
"""
for j in range(LITTER_SIZE):
    print(darwin_list[j])
print()
"""

hoyle = ""
for i in range(GENE_LEN):
    hoyle = hoyle + MOJI[random.randint(0,len(MOJI)-1)]


for generation in range(MAX_GENERATION):
    if (generation%CHUKEI == 0):
        print("---第", generation,"世代---")

    #print("個体群の成績評価")
    darwin_fitness_list = []
    for i in range(LITTER_SIZE):
        darwin_fitness_list.append(0)

    for i in range(GENE_LEN):
        for j in range(LITTER_SIZE):
            if(target[i] == darwin_list[j][i]):
                darwin_fitness_list[j] = darwin_fitness_list[j] + 1
    """
    for j in range(LITTER_SIZE):
        print(darwin_list[j], darwin_fitness_list[j])
    print()
    """
    if (generation%CHUKEI == 0):
        index_max = darwin_fitness_list.index(max(darwin_fitness_list))
        print("Darwin:")
        print(darwin_list[index_max], darwin_fitness_list[index_max])
    
    hoyle_fitness = 0
    for i in range(GENE_LEN):
        if(target[i] == hoyle[i]):
            hoyle_fitness = hoyle_fitness + 1
    if (generation%CHUKEI == 0):
        print("Hoyle:")
        print(hoyle, hoyle_fitness)

        print()
    

    #収束判定
    if (max(darwin_fitness_list)==GENE_LEN):
        print("---第", generation,"世代---")
        print("Darwinが収束した")
        index_max = darwin_fitness_list.index(max(darwin_fitness_list))
        print("Darwin:")
        print(darwin_list[index_max], darwin_fitness_list[index_max])
        print("Hoyle:")
        print(hoyle, hoyle_fitness)

        break
    
    if (hoyle_fitness==GENE_LEN):
        print("---第", generation,"世代---")
        print("Hoyleが収束した")
        index_max = darwin_fitness_list.index(max(darwin_fitness_list))
        print("Darwin:")
        print(darwin_list[index_max], darwin_fitness_list[index_max])
        print("Hoyle:")
        print(hoyle, hoyle_fitness)

        break

    
    #print("選択淘汰により次世代生成")
    ##print("エリート選択")
    elite_index = np.sort(np.argsort(darwin_fitness_list)[::-1][:int(np.floor(G*LITTER_SIZE))])[::-1]
    elite_list = []
    for i in elite_index:
        elite_list.append(darwin_list[i])
    """
    for elite in elite_list:
        print(elite)
    print()
    """

    #print("ルーレット選択")
    def roulet_choice(candidate_list, fitness_list):
        """
        docstring
        """
        ruiseki = [0]
        for i in range(len(fitness_list)):
            ruiseki.append(ruiseki[-1]+fitness_list[i])

        p = random.random()*ruiseki[-1]
        #print(p)

        roulette = bisect.bisect_left(ruiseki, p) -1
        return candidate_list[roulette]
    non_elite_list = []
    for i in range(LITTER_SIZE-int(np.floor(G*LITTER_SIZE))):
        non_elite_list.append(roulet_choice(darwin_list,darwin_fitness_list))
    """
    for non_elite in non_elite_list:
        print(non_elite)
    print()
    """

    #print("GAオペレータ")
    ##print("交叉")
    ##隣り合うペアで交差
    for i in range(len(non_elite_list)-1):
        if (random.random()<=CROSSOVER_RATE):#CROSSOVER_RATEの確率で交差する
            #どこで交差するか
            cross_point = random.randint(1,GENE_LEN-1)
            temp = non_elite_list[i]
            non_elite_list[i] = non_elite_list[i][:cross_point] + non_elite_list[i+1][cross_point:]
            non_elite_list[i+1] = non_elite_list[i+1][:cross_point] + temp[cross_point:]
    """
    for non_elite in non_elite_list:
        print(non_elite)
    print()
    """

    ##print("突然変異")
    for i in range(len(non_elite_list)):
        for j in range(GENE_LEN):
            if (random.random()<=MUTATION_RATE):#MUTATION_RATEの確率で突然変異する
                non_elite_list[i] = non_elite_list[i][:j]+ MOJI[random.randint(0,len(MOJI)-1)] +non_elite_list[i][j+1:]
    """
    for non_elite in non_elite_list:
        print(non_elite)
    print()
    """

    darwin_list = elite_list + non_elite_list

    hoyle = ""
    for i in range(GENE_LEN):
        hoyle = hoyle + MOJI[random.randint(0,len(MOJI)-1)]