# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:51:39 2020

@author: Karsyn
"""
#TASK 5: MINIMIZE HOLDING COST
#make t =21 
#Xit is 26 products(i) and 21 shift(t) or time periods: 26x21
#cumalitive production = sum of that product up to that time period
#demand is the order size at period 
# cumalitive demand is the sum of demand up to that period
#inventory is cumalitive production-cumalitive demand
#production constraint is the sumproduct of the Xit and the time it takes at that station 
from csv import reader
from gurobipy import *
from math import ceil
order = []   
parts = []
# Read in necessary parts data(processing times per station) from csv file 
with open('parts.csv', 'r') as read_obj1:
        csv_reader1 = reader(read_obj1)
        next(csv_reader1)
        next(csv_reader1)
        for row in csv_reader1:
                data = (row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]))
                parts.append(data)
read_obj1.close()  

# Read in necessary part information (due dates, amount, etc) from csv file 
with open('orders.csv', 'r') as read_obj2:
        csv_reader2 = reader(read_obj2)
        header = next(csv_reader2)
        for row in csv_reader2:
                data = (int(row[0]), row[1], int(row[2]), int(row[3]))
                order.append(data)
read_obj2.close()
#sort so that we can keep up with the periods better and are easier to put into variables and summing makes it easier 
order.sort(key=lambda x:x[3])

#cumalitive production = sum of that product up to that time period
alphabet_dic = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H', 9:'I', 10:'J', 11:'K', 12:'L', 13:'M', 14:'N', 15:'O', 16:'P', 17:'Q', 18:'R', 19:'S', 20:'T', 21:'U', 22:'V', 23:'W', 24:'X', 25:'Y', 26:'Z'}
alphabet = alphabet_dic.values()

cumulative_demands = []
for i in range(21):
        cumulative_demands.append([])
        for letter in alphabet:
                cumulative_demands[i].append((letter, 0))
# At each period, we calculate the cumulative demand for each of the products where the product and demand are represented in a tuple
for t in range(1,22):
        for row in order:
                product = row[1]
                amount = row[2]
                shift = row[3]
                if shift > t:
                        break
                for index in range(26):
                        count = cumulative_demands[t-1][index]
                        if count[0] == product:
                                temp = list(count).copy()
                                temp[1] = temp[1] + amount
                                new_count = tuple(temp)
                                cumulative_demands[t-1][index] = new_count
x = []
for i in range(26):
        x.append([])

# Initialize Gurobi Variables for product a-z and period 1-21
mod = Model("Minimize Holding Cost Model")
for i in range(1,27):
        for j in range(1,22):
                x[i-1].append(mod.addVar(vtype="C", name = "X"+str(alphabet_dic[i])+str(j)))
mod.params.timelimit=1000

mod.update()

station1 = []
station2 = []
station3 = []
station4 = []
station5 = []
station6 = []
station7 = []


# Calculate cumulative processinng times for all stations over all perdiods and for all parts. Each station's cumulative processing times are stored in a list
column = 0
for period in range(1,22):
        sum1 = 0
        row = 0
        for part in parts:
                sum1 = part[1]*x[row][column] + sum1
                row = row+1
        station1.append(sum1)
        column = column + 1      
column = 0
for period in range(1,22):
        sum1 = 0
        row = 0
        for part in parts:
                sum1 = part[2]*x[row][column] + sum1
                row = row+1
        station2.append(sum1)
        column = column + 1
        
column = 0
for period in range(1,22):
        sum1 = 0
        row = 0
        for part in parts:
                sum1 = part[3]*x[row][column] + sum1
                row = row+1
        station3.append(sum1)
        column = column + 1
        
column = 0
for period in range(1,22):
        sum1 = 0
        row = 0
        for part in parts:
                sum1 = part[4]*x[row][column] + sum1
                row = row+1
        station4.append(sum1)
        column = column + 1

column = 0
for period in range(1,22):
        sum1 = 0
        row = 0
        for part in parts:
                sum1 = part[5]*x[row][column] + sum1
                row = row+1
        station5.append(sum1)
        column = column + 1

column = 0
for period in range(1,22):
        sum1 = 0
        row = 0
        for part in parts:
                sum1 = part[6]*x[row][column] + sum1
                row = row+1
        station6.append(sum1)
        column = column + 1

column = 0
for period in range(1,22):
        sum1 = 0
        row = 0
        for part in parts:
                sum1 = part[7]*x[row][column] + sum1
                row = row+1
        station7.append(sum1)
        column = column + 1
 
# Combine all stations' cumulative demands into a single list        
allStations = [station1, station2, station3, station4, station5, station6, station7]

# Find cumulative inventory for all stations over all periods
cumulative_inventory = []
for i in range(21):
        cumulative_inventory.append([])
for period in range(1,22):
        for prod in range(1,27):
                sum1 = 0
                for index in range(1,27):
                        if index > period:
                                break
                        sum1 = x[prod-1][index-1] + sum1
                cumulative_inventory[period-1].append(sum1)

# Determine objective function by multiplying the holding cost to the subtraction of cumulative demand from cumulative inventory for all stations and periods 
totalSum = 0
for period in range(1,22):
        sum1 = 0
        h = parts[period-1][8]
        for index in range(26):
                sum1 = cumulative_inventory[period-1][index] - cumulative_demands[period-1][index][1] + sum1
        product = h*sum1
        totalSum = totalSum + product
mod.setObjective(totalSum, GRB.MINIMIZE)

# Set constraint to not allow lateness
for period in range(1,22):
        for index in range(26):               
                mod.addConstr(cumulative_inventory[period-1][index] >= cumulative_demands[period-1][index][1])
# Set constraint to not go over the availability of each station
for station in allStations:
        for period in range(21):
                mod.addConstr(station[period] <= 480)

# Solve the optimization problem
mod.optimize()

# Write the results to a txt file
index = 1
file = open("ExtraCredit.txt", 'w')

resultStr = "Our objective function is {}".format(mod.ObjVal)
file.write(resultStr + "\n")
while (index <= 21):
        for i in range(26):
                for j in range(21):
                        if x[i][j].X > 0: 
                                if int(x[i][j].VarName[2:]) == index:
                                        resultStr = "make {} amount of part {} in period {}".format(ceil(x[i][j].X), x[i][j].VarName[1], x[i][j].VarName[2:])
                                        file.write(resultStr + "\n")
        index = index + 1
file.close()

                
                
                
                