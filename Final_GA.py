from doctest import testfile
import subprocess as sub
import random
from random import choices
import time

GEN = 10       # number of generations
POPULATION = 10       # size of population
CHROMOSOME = 24     # size of chromosome
CROSSOVER_PROB = 1
MUTATE_PROB = 0.001

# Uyen
def binary2decimal(chrom):

  res = []
  for i in range(0, 24, 6):
    r = chrom[i:i+6]
    r = int(''.join([str(j) for j in r]), 2)

    res.append(r)
  
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

  #outfile = open('final_pop.txt', 'w', encoding='utf8')
  #fin = ''
  #for i in range(len(pop)):
  #	chromo = ''
  #  for j in range(CHROMOSOME):
  #    chromo += str(pop[i][j])
  #  fin += chromo + '\n\n'
  #outfile.write(fin)

GA()
