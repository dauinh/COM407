from doctest import testfile
import subprocess as sub
import random
from random import choices
import time
import csv

GEN = 100       # number of generations
POPULATION = 20       # size of population
CHROMOSOME = 100     # size of chromosome
CROSSOVER_PROB = 1
MUTATE_PROB = 0.001

# Uyen
def binary2decimal(chrom):
	#wall: 6 bit; speed: 6 bit; angle: 6bit; risk 7 bit
  res = []
	#wall: [10, 631]
  for i in range(0, 24, 6):
    w = chrom[i:i+6]
    w = int(''.join([str(j) for j in w]), 2)

    res.append(1+w*10)

  #speed: [1, 64]
  for i in range(24, 48, 6):
    s = chrom[i:i+6]
    s = int(''.join([str(j) for j in s]), 2)

    res.append(1+s)

	#angle: [1, 316]
  for i in range(48, 72, 6):
    a = chrom[i:i+6]
    a = int(''.join([str(j) for j in a]), 2)

    res.append(1+a*5)

	#risk: [1, 128]
  for i in range(72, 100, 7):
    r = chrom[i:i+7]
    r = int(''.join([str(j) for j in r]), 2)

    res.append(1+r)

  for i in range(1, len(res), 2):
	  res[i] = res[i] + res[i-1]
  
  return res


def fitness():
  f = open('agentScore.txt', 'r').read()
  if f == "":
    return -1000
  return float(f)


def initial_gen():
  bitList = []
  for i in range(POPULATION):
    bit = []
    for j in range(CHROMOSOME):
      x = (random.randint(0, 1))
      bit.append(x)
    # bitString = ''.join(bit)
    bitList.append(bit)

  return bitList

# crossover and mutate
def breed(parents):
  # crossover
  crossover_or_not = random.random()
  mom = parents[0]
  dad = parents[1]
  if crossover_or_not < CROSSOVER_PROB:
    crossover_point = random.randrange(0, CHROMOSOME)
    
    son = mom[:crossover_point] + dad[crossover_point:]
    daughter = dad[:crossover_point] + mom[crossover_point:]

    # mutate
    for i in range(len(son)):
      mutate_or_not = random.random()
      if mutate_or_not < MUTATE_PROB:
        if son[i] == 0:
          son[i] = 1
        else:
          son[i] = 0

    for i in range(len(daughter)):
      mutate_or_not = random.random()
      if mutate_or_not < MUTATE_PROB:
        if daughter[i] == 0:
          daughter[i] = 1
        else:
          daughter[i] = 0

    return son, daughter

  else:
    return parents

# standard wheel selection
def select(population, fitness_list):
  total = sum(fitness_list)
  fitness_ratio = []
  for i in range(len(population)):
    ratio = fitness_list[i] / total
    ratio = round(ratio, 3)
    fitness_ratio.append(ratio)
  
  parents = []
  dad = choices(population, fitness_ratio)
  mom = choices(population, fitness_ratio)

  parents.append(dad[0])
  parents.append(mom[0])
  
  return parents

def GA():
  results = open('results.csv', 'w')
  csv_writer = csv.writer(results)
  headers = ['Generation','Id','Chromosome','Fitness']
  csv_writer.writerow(headers)

  # Generate a population
  pop = initial_gen()
  # data = []
  # generations = []
  p1 = sub.Popen("./xpilots -map maps/simple.xp -noQuit -switchBase 1 +teamPlay -reset -worldLives 1 -limitedLives", shell=True)
  #sub.run("python3 Test.py", shell=True)

  for i in range(GEN):

    # DO THIS
    fitness_list = []
    new_pop = []
    for j in range(len(pop)):
      print('gen:', i)
      print('chromosome:', j)
      print()

      # Sylvia
      # insert value into Final.py
      template = open('agent_template.txt', 'r').read()
      vals = binary2decimal(pop[j])
      agent = template.format(*tuple(vals))
      testfile = open('agent.py', 'w')
      testfile.write(agent)

      # test this
      try:
        p2 = sub.run("python3 agent.py & python3 Test.py", shell=True)
      except Exception as e:
        sub.run("pkill xpilots", shell=True)
        print("Error:", e)

      x = fitness()
      fitness_list.append(x)
      chromo = ''
      for k in range(len(pop[j])):
        chromo += str(pop[j][k])
      agent = [str(i), str(j), chromo, str(x)]
      csv_writer.writerow(agent)
    
    # data.append(sum(fitness_list)/len(pop))
    # generations.append(i)

    #best = fitness_list.index(max(fitness_list))
    #elite = pop[best]
    #new_pop.append(elite)


    # Generate new population
    while(len(new_pop) < POPULATION):
      # Select 2 chromosomes
      parents = select(pop, fitness_list)
      # Generate new child
      children = breed(parents)
      new_pop.append(children[0])
      new_pop.append(children[1])

    pop = new_pop

  outfile = open('final_pop.txt', 'w', encoding='utf8')
  fin = ''
  for i in range(len(pop)):
    chromo = ''
    for j in range(CHROMOSOME):
      chromo += str(pop[i][j])
    fin += chromo + '\n\n'
  outfile.write(fin)

GA()
