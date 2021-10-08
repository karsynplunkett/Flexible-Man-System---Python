# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 14:29:47 2020

Group 15: Karsyn Plunkett and Ashlyn Long
"""
# CASE STUDY 2 TASK 4
from csv import reader
import prettytable
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

order.sort(key=lambda x:x[3]) #Sort orders by due date 

batches = []
# Each batch is categorized by: (id, remaining_time[], jobs[])
# remaining_time[] contains the time left for each station (Station 1 index 0, Station 2 index 1, etc)
# jobs[] contains the order ID and amount assigned to the batch represented as a tuple (order, amount)

# Open first batch 
currBatch = 1
batches.append([currBatch, [480, 480, 480, 480, 480, 480, 480], []])
numBatches = 1
 
# Consider all orders in sorted order
for item in order:
        # Determine current order ID, product, and amount
        orderID = item[0]
        product = item[1]
        amount = item[2]
        # Loop through the widgets in PartsToPlan to determine the station times for the current product
        for part in parts:
                if product == part[0]: 
                        stationTimes = part[1:8]
        counts = 0
        iteration = 1
        currBatch = 1 # Always start at batch 1 to see if partial orders can go here
        
        # Consider each station time individually to account for partial orders being assigned to batches
        while (iteration <= amount):
                fits = True
                temp = batches[currBatch-1][1].copy()
                index = 0
                # Determine loop through all station times in the batch (initially 480 min) to determine if there is enough time remaining to assign the order to this batch
                for time in stationTimes:
                        if time <= temp[index]:
                                temp[index] = round(temp[index] - time, 2)
                        else:
                                fits = False
                        index = index + 1
                # If there is enough time at each station for the current iteration, update all of the remaining station times and update count (current amount for this order)
                if (fits):
                        batches[currBatch-1][1] = temp
                        counts = counts + 1
                        iteration = iteration + 1
                
                else:
                        # If some of the order can be assigned to this current batch, assign it
                        if counts > 0:
                             batches[currBatch-1][2].append((orderID, product, counts))
                        # Go to the next batch (1->2, 2->3, etc)
                        currBatch = currBatch + 1
                        counts = 0
                        # If the next batch to try and assign orders to does not exist, open a new batch
                        if currBatch > numBatches:
                                batches.append([currBatch, [480, 480, 480, 480, 480, 480, 480], []])
                                #counts = 0
                                numBatches = numBatches + 1
        # Assign remaining order amount to the current batch
        batches[currBatch-1][2].append((orderID, product, counts))
print(batches)
# Create output table of results
x = prettytable.PrettyTable(["Batch ID", "Order", "Product", "Amount"])
for batch in batches:
        row1 = [batch[0], batch[2][0][0], batch[2][0][1], batch[2][0][2]]
        x.add_row(row1)
        
        for data in batch[2]:
                if data == (batch[2][0][0], batch[2][0][1], batch[2][0][2]):
                        continue
                x.add_row(["", data[0], data[1], data[2]])
        x.add_row(["-----------", "-----------", "-----------", "-----------"])
#print(x)
      
# Write results table to file         
File = open(r"Algorithm_Solution.txt","w+")
File.write(str(x))
File.close()




