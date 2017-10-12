#!/usr/bin/env python
from random import shuffle
from random import randint
from random import sample
from collections import defaultdict
import itertools
import time

infinity = float('inf')

romania_map = dict( Bucharest=dict(Craiova= 200, Fagaras=211, Giurgiu=90 ,Pitesti=105,Rimnicu= 240,Sibiu= 360),
    Craiova=dict(Bucharest=200 , Fagaras=195, Giurgiu=150, Rimnicu=146, Pitesti=138, Sibiu= 280),
    Fagaras=dict(Bucharest=211 ,Craiova= 195, Giurgiu=296 , Rimnicu=80, Pitesti=87,Sibiu=99),
    Giurgiu=dict(Bucharest=90 ,Craiova= 150, Fagaras=296 , Rimnicu=350, Pitesti=172,Sibiu=420),
    Pitesti=dict(Bucharest=105 ,Craiova= 138, Fagaras=87, Giurgiu=172 ,Rimnicu=97,Sibiu=148),
    Rimnicu=dict(Bucharest=240 ,Craiova= 146, Fagaras=80, Giurgiu=350 ,Pitesti=97,Sibiu=80),
    Sibiu = dict(Bucharest=360 ,Craiova= 280, Fagaras=99, Giurgiu=420 ,Pitesti=148,Rimnicu=80))

heuristics = dict( Bucharest=dict(Craiova= 160, Fagaras=176, Giurgiu=77 ,Pitesti=100,Rimnicu= 193,Sibiu= 253),
    Craiova=dict(Bucharest=160 , Fagaras=120, Giurgiu=80, Rimnicu=110, Pitesti=104, Sibiu= 170),
    Fagaras=dict(Bucharest=176 ,Craiova= 120, Giurgiu=240 , Rimnicu=20, Pitesti=36,Sibiu=60),
    Giurgiu=dict(Bucharest=77 ,Craiova= 80, Fagaras=240 , Rimnicu=279, Pitesti=127,Sibiu=293),
    Pitesti=dict(Bucharest=100 ,Craiova= 104, Fagaras=36, Giurgiu=127 ,Rimnicu=52,Sibiu=103),
    Rimnicu=dict(Bucharest=193 ,Craiova= 110, Fagaras=20, Giurgiu=279 ,Pitesti=52,Sibiu=30),
    Sibiu = dict(Bucharest=253 ,Craiova= 170, Fagaras=60, Giurgiu=293 ,Pitesti=103,Rimnicu=30))

cities = ["Bucharest","Craiova","Fagaras","Giurgiu","Pitesti","Rimnicu","Sibiu"]
tot_city = len(cities)

def routeExpander(state,closed):
    print "Cities are visited in the following order:"
    for city in state:
        print cities[city]
    if closed:
        print "and back to ",cities[state[0]]

class GeneticAlgorithm:
    def __init__(self):
        #create initial population
        self.population = [];
        self.AvgFitnessScore = 0;
        #To generate random population with strength of 1000
        self.tot_population = 1000
        self.max_population = self.tot_population
        self.mutation = 0
        self.mutation_rate = 0.05

        self.GeneratePopulation()
        self.fitnessFunction()
        print "Inital Average Fitness Score :", -1*self.AvgFitnessScore
        print "Fitness Score : ", -1*max(self.FitnessScore)
        for z in range(10):
            self.selection()
            # adopted order crossover (OX1) propossed by Davis in 1985
            self.RegulatePopulation()
            #self.fitnessFunction()
        print "\nResult"
        print "Total Mutation :",self.mutation
        print "Fitness Score : ", -1*max(self.FitnessScore)
        print "Average Fitness Score : ", -1*self.AvgFitnessScore

        tsp_route =  self.population[self.FitnessScore.index(max(self.FitnessScore))]
        #print "Final Average Fitness Score :", self.AvgFitnessScore
        print "TSP ROUTE GA City Indices:", tsp_route
        routeExpander(tsp_route,True)

    def GeneratePopulation(self):
        for i in range(self.tot_population):
            string = []
            string = range(tot_city)
            shuffle(string)
            self.population.append(string)

    def fitnessFunction(self):
        self.FitnessScore = [];
        for i in range(self.tot_population):
            self.FitnessScore.append(0);
            current_route = self.population[i]
            #print "Current Route"
            #print current_route
            for z in range(tot_city):
                # position - gives when the given city is visited
                position = current_route.index(z);
                # we get the index of the cities and we can use this in "cities" list
                current_city = current_route[position]
                if position == (tot_city-1):
                    next_city = current_route[0]
                else:
                    next_city = current_route[position+1]
                # we need to maximize the FitnessScore
                self.FitnessScore[i] -= romania_map[cities[current_city]][cities[next_city]]
            self.AvgFitnessScore += self.FitnessScore[i]
            #print current_route
            #print self.FitnessScore[i]
        self.AvgFitnessScore/=self.tot_population
        #print self.AvgFitnessScore
        #print "\n\n"

    def selection(self):
        # to select,crossover and mutate
        #selection
        fittest = [False,True]
        # most fittest parent in the present population
        fit_parent = self.population[self.FitnessScore.index(max(self.FitnessScore))]
        parents = sample(self.population,int(self.tot_population/20))
        # no of reproductions
        for z in range(int(self.tot_population/20)):
            child1 = [-1]*tot_city
            child0 = [-1]*tot_city
            parent = sample(parents,2)
            # choosing cut points
            cuts = [randint(1,tot_city-1), randint(1,tot_city-1)]
            while cuts[0]==cuts[1]:
                cuts[1] = randint(1,tot_city-1)
            cuts.sort()
            # print cuts
            # use the fittest parent or not
            if sample(fittest,1)[0]:
                #print "fit"
                parent[0] = fit_parent
            child0[cuts[0]:cuts[1]] = parent[0][cuts[0]:cuts[1]]
            child1[cuts[0]:cuts[1]] = parent[1][cuts[0]:cuts[1]]

            index1= parent[1].index(child0[cuts[1]-1]) + 1
            index0= parent[0].index(child1[cuts[1]-1]) + 1

            i = index0
            j = cuts[1]
            """print "Before"
            print parent[0]
            print child0
            print parent[1]
            print child1
            """
            #crossovers
            while min(child1) < 0:
                if i == tot_city:
                    i=0
                if j == tot_city:
                    j=0
                if child1[j] == -1 and child1.count(parent[0][i])==0:
                    child1[j] = parent[0][i]
                    j+=1
                i+=1
            i = index1
            j = cuts[1]
            while min(child0) < 0:
                if i == tot_city:
                    i=0
                if j == tot_city:
                    j=0
                if child0[j] == -1 and child0.count(parent[1][i])==0:
                    child0[j] = parent[1][i]
                    j+=1
                i+=1
            """print "After"
            print child0
            print child1
            """

            # Mutation
            # Displacement Mutation is applied
            x = randint(0,1000);
            if x < (1000*self.mutation_rate):
                self.mutation +=1;
                #print "Mutation"
                y =randint(0,1);
                cuts = [randint(1,tot_city-1), randint(1,tot_city-1)]
                while cuts[0]==cuts[1]:
                    cuts[1] = randint(1,tot_city-1)
                cuts.sort()
                if y:
                    child = child1[cuts[0]:cuts[1]]
                    for city in child:
                        child1.remove(city)
                    pos = randint(0,len(child1))
                    for city in child:
                        child1.insert(pos,city)
                        pos+=1
                    #print child1
                else:
                    child = child0[cuts[0]:cuts[1]]
                    for city in child:
                        child0.remove(city)
                    pos = randint(0,len(child1))
                    for city in child:
                        child0.insert(pos,city)
                        pos+=1
                    #print child0
            self.population.append(child0)
            self.population.append(child1)

    def RegulatePopulation(self):
        # Now calculate the fitness function  to remove the least fittest
        self.tot_population = len(self.population)
        self.fitnessFunction()
        for i in range(self.tot_population-self.max_population):
            minimumFitnessScore =min(self.FitnessScore)
            weakPopulation = self.population[self.FitnessScore.index(minimumFitnessScore)]
            self.population.remove(weakPopulation)
            self.FitnessScore.remove(minimumFitnessScore)

class HillClimbing:
    def __init__(self):
        self.evaluation_value_state = 0;
        self.evaluation_value_nxtstate = 0;
        # change and check the climbhill
        # having higher values of iterations produces the optimal path
        self.iterations = 100;
        self.state = range(tot_city);
        shuffle(self.state)
        self.next_state = self.state
        print "Initial State :", self.state
        self.evaluation_value_state  = self.EvaluationFunction(self.state)
        print "Evaluation Value :",-1*self.evaluation_value_state
        self.ClimbHill()
        print "\nResult"
        print "Evaluation Value : ",-1*self.evaluation_value_state
        print "TSP ROUTE Hill Climbing Algorithm City Indices:", self.state
        routeExpander(self.state,True)

    # finds the distance travelled for the given order
    def EvaluationFunction(self,state_evaluate):
        evaluation_value = 0
        for z in range(tot_city):
            # position - gives when the given city is visited
            position = state_evaluate.index(z);
            # we get the index of the cities and we can use this in "cities" list
            current_city = state_evaluate[position]
            if position == (tot_city-1):
                next_city = state_evaluate[0]
            else:
                next_city = state_evaluate[position+1]
            # we need to maximize the evaluation_value
            evaluation_value -= romania_map[cities[current_city]][cities[next_city]]
        return evaluation_value

    def ClimbHill(self):
        while True:
            shuffle(self.next_state)
            for i in range(tot_city):
                    #for j in range(i+1,tot_city):
                    j = randint(i,tot_city-1)
                    self.next_state[i],self.next_state[j] =self.state[j],self.state[i]
                    self.evaluation_value_nxtstate = self.EvaluationFunction(self.next_state)
                    if self.evaluation_value_nxtstate >= self.evaluation_value_state:
                        self.state = self.next_state
                        self.evaluation_value_state = self.evaluation_value_nxtstate
                        #print "Moving to new state...",self.state
                        #print "Evaluation Value :",self.evaluation_value_state
                    else:
                        if self.iterations==0:
                            break
                        #print self.iterations
                        self.iterations -=1
            if self.iterations ==0:
                break

class Astar:
    def __init__(self):
        # used Dijkstra's algorithm, another form of prim's minimal spanning tree algorithm
        # randomly choose a inital city
        self.states = range(tot_city)
        #  stores optimal path for different intial city
        self.paths = []
        self.totdists =[]
        #self.initial_state = randint(0,tot_city-1)

        for self.initial_state in self.states:
            self.unexplored = []

            #self.dist = [0]*tot_city
            self.path=[self.initial_state]
            self.totdist = 0
            print "Starting City :", cities[self.initial_state]
            self.intialize()
            self.explorecity()
            self.paths.append(self.path)
            self.totdists.append(self.totdist)
        self.totdist = min(self.totdists)
        self.path = self.paths[self.totdists.index(self.totdist)]

        print "\nResult\nTSP ROUTE A-Star (MST heuristics) Algorithm City Indices:", self.path
        print "Total Distance :", self.totdist
        routeExpander(self.path,False)

    def intialize(self):
        for city in range(tot_city):
            self.unexplored.append(city)
        #print self.unexplored
        #print self.dist

    def explorecity(self):
        self.current_city = self.unexplored[self.initial_state]
        NextCity =""
        while len(self.unexplored) > 1:
            self.unexplored.remove(self.current_city)
            mindist = infinity
            combinations = itertools.permutations(self.unexplored,len(self.unexplored))
            for city in combinations:
                # tuple to list and adding the current city to the initial node
                citi = [self.current_city]
                citi.extend(city)
                #print "SEQ", citi
                # estimating the cost (dist) to complete the tour
                dist = self.totdist
                #dist += self._h(citi[0],citi[len(citi)-1])

                for i in range(len(citi)-1):
                    dist += self._h(citi[i],citi[i+1])
                #print "DIST",dist
                #print "DIST",dist
                #print "MIN",mindist
                if mindist > dist:
                    NextCity = citi[1]
                    mindist = dist
            #print "Next City", NextCity
            self.path.append(NextCity)
            self.totdist +=self._g(self.current_city,NextCity)
            self.current_city = NextCity

    def _h(self,current_city,next_city):
        return heuristics [cities[current_city]][cities[next_city]]
    def _g(self,current_city,next_city):
        return romania_map[cities[current_city]][cities[next_city]]

if __name__== "__main__":
    print "\n\nTravelling Salesman Problem"
    print "\nGenetic Algorithm Starting..."
    start = time.time()
    ga = GeneticAlgorithm()
    end =time.time()
    print "Total time taken : %f Seconds "%float(end-start)

    print "\nHill Climbing Algorithm Starting..."
    start = time.time()
    hc = HillClimbing()
    end =time.time()
    print "Total time taken : %f Seconds "%float(end-start)

    print "\nA-Star Algorithm Starting..."
    start = time.time()
    astar = Astar()
    end =time.time()
    print "Total time taken : %f Seconds "%float(end-start)
