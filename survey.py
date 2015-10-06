import os
import numpy

cwd = os.getcwd()
al = os.listdir(cwd)

# read ects data from file 'ects.csv'
ects = {}
f = open('ects.csv','r')
for line in f:
    helper = line.split('\n')[0].split(';')
    ects[helper[0]] = float(helper[1])

# load data from each file
# structure: entry in dict [semester, finished, [work per semester; lenght = semester], {course1:[success,hours,{tried; 1:1, 2:1},attendance], course2:[success,hours,{tried; 1:1, 2:1},attendance],...}]
# anwesenheit code -1: no information, 0: never, 1: sometimes, 2: often, 3:always
data = {}

numberstud = 0 # keeps count how many students are load into the data
courses = range(10,20) + range(22,31) + range(33,45) + range(47,57) + range(59,70) + range(72,83) + range(85,97) 

for i in al:
    if i != 'survey.py' and i != 'ects.csv' and i != 'README.txt':
        numberstud += 1
        data[numberstud] = [0,0,[],{}] # initialize data
        f = open(i,'r')
        numberline = 0
        
        for line in f:    #read every line in the file 
            helper = line.split('/n')[0].split(';') # remove first /n and then split line        
            
            if numberline == 1: # current semester
                data[numberstud][0] = int(helper[1])
            
            if numberline == 2: # bachelor finished?  
                data[numberstud][1] = helper[1]  
            
            if numberline == 5: #hours worked?
                for i in range(1,data[numberstud][0]+2):
                    data[numberstud][2].append(helper[i])                       
            
            if numberline in courses: # course
                if helper[6] == 'Yes' or helper[6] == 'No': # take only if active in this course
                    data[numberstud][3][helper[0]] = [] # add array for this course
                    data[numberstud][3][helper[0]].append(helper[6]) # add success
                    if helper[5] != '': # add hours worked
                        data[numberstud][3][helper[0]].append(int(helper[5]))
                    else:
                        data[numberstud][3][helper[0]].append(0)
                    data[numberstud][3][helper[0]].append({}) # add dictionary for tries    
                    for j in range(7,27): #add tries
                        if helper[j] != '':
                            data[numberstud][3][helper[3]][2][j-6] = int(helper[j])
                    data[numberstud][3][helper[0]].append(-1) # add attendance       
                    if helper[1] == 'x':
                        data[numberstud][3][helper[0]][3] = 0
                    if helper[2] == 'x':
                        data[numberstud][3][helper[0]][3] = 1
                    if helper[3] == 'x':
                        data[numberstud][3][helper[0]][3] = 2
                    if helper[4] == 'x':
                        data[numberstud][3][helper[0]][3] = 3

            numberline += 1
            
# a couple of different function that are used to access the scanned data                    
                                                                                                                                                                                                                 
def passed(name): # for entered course: when did people pass it?                              
    result = [0]*20 # ends at 20+
    for i in data: # for each student
        try: # student already had contact with course?
            helper = data[i][3][name]
            if helper[0] == 'Yes':
                result[max(helper[2])] += 1
        except:
            pass        
    print(result)

def whattry(name): # for entered course: passed after how many tries?
    result = [0]*5
    for i in data:
        try:
            helper = data[i][3][name]
            fails = 0
            for j in helper[2]:
                fails += helper[2][j]
            if helper[0] == 'Yes':
                result[fails-2] += 1 #last try passed
            else:
                result[fails-1] += 1               
        except:
            pass
    print(result)           
        
def hours(name): # for entered course: how long learned, splitted in failed and passed
    result1 = []
    result2 = []
    for i in data:
        try:
            if data[i][3][name][1][0] == 'Yes':
                result1.append(data[i][3][name][1])
            if data[i][3][name][1][0] == 'No':  
                result2.append(data[i][3][name][1])
        except:
            pass
    print(result1) # PRINT HISTOGRAM
    print(result2)        

def studycurve(): # provides average ects for each semester 
    data1 = [0]*20 # array of length 20 with how many ects a student has in a semester
    mean = []
    stdev = []
    val1 = []
    val2 = []
    for i in data: # each student
        ectssem = [0]*20
        for j in data[i][3]: # for each course
            if data[i][3][j][0] =='Ja': # course passed
                ectssem[max(data[i][3][j][2])] += ects[j]
        for j in range(0,20): # get individual data in whole data
            data1[j].append(ectssem[j]) 
    for i in range(0,20):
        mean.append(numpy.mean(data1[i]))
        stdev.append(numpy.std(data1[i])) 
        val1.append(mean[-1] - stdev[-1])
        val2.append(mean[-1] + stdev[-1])
    print mean

def work_versus_credits(): # generated a x,y - pair for each semester/student and plots it (x: hours worked, y:credits gotten) 
   result = []
   for i in data:
       ectssem = [0]*20
       for j in data[i][3]: # for each course
            if data[i][3][j][0] =='Ja': # course passed
                ectssem[max(data[i][3][j][2])] += ects[j]
       for j in range(0,20):
           if ectssem[j] != 0 or data[i][2][j] != 0:
               result.append([ectssem[j], data[i][2][j]])  
   print(result)            
