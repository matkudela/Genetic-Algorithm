import random


class TravellingSalesman:
    def __init__(self):
        # list with distances between cities
        self.__distances = []
        self.__number_of_cities = 0
        self.__population = []
        # size of population (number of individuals in population array)
        self.__n = 40
        # distance of every individual from population in one list
        self.__calculated_paths = []

        self.__open_file_and_set_distances()
        self.__generate_population()
        self.__fill_calculated_paths()
        self.__roulette_selection()

    @property
    def __population(self):
        return self.population

    @__population.setter
    def __population(self, value):
        self.population = value

    @property
    def __distances(self):
        return self.distances

    @__distances.setter
    def __distances(self, value):
        self.distances = value

    def __open_file_and_set_distances(self):
        file = open("berlin52.txt", "r")
        # read first line from file - its the number of cities travelling trader has to visit
        self.__number_of_cities = int(file.readline().rstrip())

        while True:
            # read line, split it, and convert strings to integers
            line = file.readline()
            if line == "":
                break
            line = list(map(int, line.rstrip().split(" ")))
            self.__distances.append(line)
        file.close()

        # make mirror image of values in distances (to make square matrix)
        for x in range(len(self.__distances)):
            y = 0
            while len(self.__distances[x]) < self.__number_of_cities:
                self.__distances[x].append(self.__distances[x+1+y][len(self.__distances[x])-1-y])
                y += 1

    # method that creates one invidual - list of cities in specific order that travelling salesman has to visit
    def __generate_individual(self):
        individual = []
        while len(individual) < self.__number_of_cities:
            random_number = random.randint(0, self.__number_of_cities-1)
            if random_number not in individual:
                individual.append(random_number)
            else:
                continue
        return individual

    # method that checks distance from one city to another in distances matrix
    def __check_distance(self, first_city, second_city):
        return self.__distances[first_city][second_city]

    # method that calculates whole distance of trip of travelling salesman using distances matrix
    def __calculate_distance(self, individual):
        distance = 0
        for x in range(len(individual)-1):
            distance += self.__check_distance(x, x+1)
        # add distance from last city to first
        distance += self.__check_distance(individual[-1], individual[0])
        return distance

    def __generate_population(self):
        for x in range(self.__n):
            self.__population.append(self.__generate_individual())

    # method that calculates distance of every individual in population and append it into list
    def __fill_calculated_paths(self):
        for x in range(len(self.__population)):
            self.__calculated_paths.append(self.__calculate_distance(self.__population[x]))

    def __roulette_selection(self):
        # roulette selection - we want to select individuals for new population - the lower overall distance
        # of individual the better (individuals with better distance will have higher chance to be rolled for next
        # population)
        # find max value
        max_path = max(self.__calculated_paths)

        # recalculate paths (to make lower value better)
        for x in range(len(self.__calculated_paths)):
            self.__calculated_paths[x] = max_path + 1 - self.__calculated_paths[x]

        # calculate sum of distances
        distances_in_total = 0
        for x in range(len(self.__calculated_paths)):
            distances_in_total += self.__calculated_paths[x]

        # create ranges, they will be used for rolling, every individual has lower and upper bound
        # eg. when first and second individuals have distances 9 and 31. First individual gets bound from 0 to 9
        # second one from 9 to 40 (9+31) and so on...
        ranges = []
        lower_bound = 0
        upper_bound = 0
        for x in range(len(self.__calculated_paths)):
            upper_bound += self.__calculated_paths[x]
            tmp = [lower_bound, upper_bound]
            ranges.append(tmp)
            lower_bound = upper_bound

        # now generate random number, when it will be between lower and upper-1 bound, individual with the same
        # index will be copied to next population
        new_population = []
        for x in range(len(self.__population)):
            generated = random.randint(0, distances_in_total)
            for y in range(len(ranges)):
                if ranges[y][0] <= generated < ranges[y][1]:
                    index = y
            new_population.append(self.__population[index])

        self.__population = new_population

    def print_distances(self):
        pass
        # for d in self.__population:
        #     print(d)


t1 = TravellingSalesman()
