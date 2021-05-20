"""
Author: Diarmuid Grimes, based on code of Alejandro Arbelaez
Insertion heuristics for quickly generating (non-optimal) solution to TSP
File contains two heuristics. 
First heuristic inserts the closest unrouted city to the previous city 
added to the route.
Second heuristic inserts randomly chosen unrouted city directly after its 
nearest city on the route
file: lab_tsp_insertion.py
"""

import random
import sys
import time
from os import listdir
from math import sqrt
#random.seed(12345)

def readInstance(fName):
    file = open(fName, 'r')
    size = int(file.readline())
    inst = {}
#    for line in file:
    for i in range(size):
        line=file.readline()
        (myid, x, y) = line.split()
        inst[int(myid)] = (int(x), int(y))
    file.close()
    return inst


def euclideanDistance(cityA, cityB):
    ##Euclidean distance
    #return sqrt( (cityA[0]-cityB[0])**2 + (cityA[1]-cityB[1])**2 )
    ##Rounding nearest integer
    return round( sqrt( (cityA[0]-cityB[0])**2 + (cityA[1]-cityB[1])**2 ) )


# Choose first city randomly, thereafter append nearest unrouted city to last city added to rpute
def insertion_heuristic1(instance):
    cities = list(instance.keys())
    cIndex = random.randint(0, len(instance)-1)

    tCost = 0

    solution = [cities[cIndex]]
    
    del cities[cIndex]

    current_city = solution[0]
    while len(cities) > 0:
        bCity = cities[0]
        bCost = euclideanDistance(instance[current_city], instance[bCity])
        bIndex = 0
#        print(bCity,bCost)
        for city_index in range(1, len(cities)):
            city = cities[city_index]
            cost = euclideanDistance(instance[current_city], instance[city])
#            print(cities[city_index], "Cost: ",cost)
            if bCost > cost:
                bCost = cost
                bCity = city
                bIndex = city_index
        tCost += bCost
        current_city = bCity
        solution.append(current_city)
        del cities[bIndex]
    tCost += euclideanDistance(instance[current_city], instance[solution[0]])
    #print(tCost)
    return solution, tCost


# Choose unrouted city randomly, insert into route after nearest routed city 
def insertion_heuristic2(instance):
    cities = list(instance.keys())
    nCities=len(cities)
    cIndex = random.randint(0, len(instance)-1)

    tCost = 0

    solution = [cities[cIndex]]
    
    del cities[cIndex]

    while len(cities) > 0:
        cIndex = random.randint(0, len(cities)-1)
        nextCity = cities[cIndex]
        del cities[cIndex]
        bCost = euclideanDistance(instance[solution[0]], instance[nextCity])
        bIndex = 0
#        print(nextCity,bCost)
        for city_index in range(1, len(solution)):
            city = solution[city_index]
            cost = euclideanDistance(instance[nextCity], instance[city])
#            print(solution[city_index], "Cost: ",cost)
            if bCost > cost:
                bCost = cost
                bIndex = city_index
        solution.insert(bIndex+1, nextCity)
    for i in range(nCities):
        tCost+=euclideanDistance(instance[solution[i]], instance[solution[(i+1)%nCities]])
    #print(tCost)
    return solution, tCost    

def randomTours(instance):
    cities=list(instance.keys())
    random.shuffle(cities)
    nCities=len(cities)
    tCost=0
    for i in range(nCities):
        tCost+=euclideanDistance(instance[cities[i]], instance[cities[(i+1)%nCities]])
    #print(tCost)
    return cities, tCost    
    

def saveSolution(fName, solution, cost):
    file = open(fName, 'w')
    file.write(str(cost)+"\n")
    for city in solution:
        file.write(str(city)+"\n")
    file.close()

def main():
    directory = sys.argv[1]
    output = sys.argv[2]
    if len(sys.argv)>3:
        runs = int(sys.argv[3])
    else:
        runs = 100
    for filename in listdir(directory):
        if filename.endswith(".tsp"):
            tspInst=readInstance(directory+"/"+filename)
            startTime = int(round(time.time() * 1000))
            solution = insertion_heuristic1(tspInst)
            h1minCost, avgCost = solution[1], solution[1]
            for i in range(1,runs):
                solution = insertion_heuristic1(tspInst)
                avgCost += solution[1]
                if(solution[1]<h1minCost):
                    h1minCost = solution[1]
            stopTime = int(round(time.time() * 1000))
            h1Cost = avgCost/runs
            h1Time = (stopTime - startTime)
            # print('-'*50,'-'*50)
            # print("Heuristic 1:", avgCost/runs, stopTime - startTime)
            # print('-'*50,'-'*50)
            startTime = int(round(time.time() * 1000))
            solution = insertion_heuristic2(tspInst)
            h2minCost, avgCost = solution[1], solution[1]
            for i in range(1,runs):
                solution = insertion_heuristic2(tspInst)
                avgCost += solution[1]
                if(solution[1]<h2minCost):
                    h2minCost = solution[1]
            stopTime = int(round(time.time() * 1000))
            h2Cost = avgCost/runs
            h2Time = (stopTime - startTime)
            # print('-'*50,'-'*50)
            # print("Alternative Heuristic:", avgCost/runs, stopTime - startTime)
            # print('-'*50,'-'*50)
            startTime = int(round(time.time() * 1000))
            solution = randomTours(tspInst)
            rminCost, avgCost = solution[1], solution[1]
            for i in range(1,runs):
                solution = randomTours(tspInst)
                avgCost += solution[1]
                if(solution[1]<rminCost):
                    rminCost = solution[1]
            stopTime = int(round(time.time() * 1000))
            rCost = avgCost/runs
            rTime = (stopTime - startTime)
            # print('-'*50,'-'*50)
            # print("Random:", avgCost/runs, stopTime - startTime)
            # print ("===================")
            print(filename,"\t",h1Cost,h2Cost,rCost,"\t",h1minCost,h2minCost,rminCost,"\t",h1Time,h2Time,rTime)
        #    print ("Input :", filename)
        #    print ("Solution: ",solution)
        #    saveSolution(output, solution[0], solution[1])
    
main()





