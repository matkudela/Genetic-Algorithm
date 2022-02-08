import random

class TravellingSalesman:
    def __init__(self):
        # list with distances between cities
        self.__distances = []
        self.__number_of_cities = 0
        self.__open_file_and_set_distances()

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

    #method that checks distance from one city to another in distances matrix
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

    def print_distances(self):
        # for d in self.__distances:
        #     print(d)
        ind = self.__generate_individual()
        print(ind)
        print(self.__calculate_distance(ind))


t1 = TravellingSalesman()
t1.print_distances()
