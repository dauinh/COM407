import random
from random import choices

GEN = 100       # number of generations
POPULATION = 400       # size of population
CHROMOSOME = 64     # size of chromosome
CROSSOVER_PROB = 1
MUTATE_PROB = 0.001

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

def fitness(chrom):
  return sum(chrom)

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
  data = []
  generations = []

  for i in range(GEN):
    # Calculate fitness for each individual
    fitness_list = []
    new_pop = []
    for j in range(len(pop)):
      x = fitness(pop[j])
      fitness_list.append(x)
    
    data.append(sum(fitness_list)/len(pop))
    generations.append(i)

    best = fitness_list.index(max(fitness_list))
    elite = pop[best]
    new_pop.append(elite)


    # Generate new population
    while(len(new_pop) < POPULATION):
      # Select 2 chromosomes
      parents = select(pop, fitness_list)
      # Generate new child
      children = breed(parents)
      new_pop.append(children[0])
      new_pop.append(children[1])

    pop = new_pop

  return pop

def main():
  output = GA()

  outfile = open('final_pop.txt', 'w', encoding='utf8')

  fin = ''
  for i in range(len(output)):
  	chromo = ''
  	for j in range(CHROMOSOME):
  		chromo += str(output[i][j])
  	fin += chromo + '\n\n'
  outfile.write(fin)
  #print(output)

main()
