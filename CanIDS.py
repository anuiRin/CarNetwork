import numpy as np
import os
import csv

#modify period value of ID 5A2(1000 to 20), 5A0(1000 to 100)
period = {'350' : 20, '1F1' : 20, '690' : 100, '260' : 10, '220' : 10, '5F0' : 100, '2A0' : 10, '18F' : 10, '5E4' : 100,
          '2B0' : 10, '165' : 10, '5A2' : 20, '2C0' : 100, '164' : 10, '5A0' : 100, '316' : 12, '153' : 10, '59B' : 100,
          '329' : 10, '120' : 200, '587' : 100, '370' : 10, '110' : 100, '545' : 10, '382' : 20, 'A1' : 100, '51A' : 200,
          '43F' : 10, 'A0' : 100, '517' : 200, '440' : 10, '81' : 10, '18' : 200, '510' : 100, '4B0' : 20, '80' : 10,
          '34' : 1000,'4F2' : 20, '4B1' : 20, '50' : 200, '42' : 1000, '4F1' : 100, '4F0' : 20, '44' : 1000, '43' : 1000 }

mean = {'370': 7.9997121600000085, '165': 9.999312131213115, '43F': 9.999243924392482, '440': 10.000047504750428, '81': 10.000047504750459, '18F': 9.999886488648881, '164': 9.999990099009866,
        '2B0': 8.999380918091804, '545': 9.999700970096995, '2A0': 9.999540954095362, '329': 9.99922092209216, '153': 9.999609360936121, '80': 9.999541154115422, '220': 9.999266126612667,
        '260': 10.999294169416949, '316': 11.999295247239457, '382': 20.0000938187637, '350': 20.00044468893765, '4F2': 20.00007221444286, '4B1': 20.000072214442923, '4B0': 20.0004456891378,
        '1F1': 16.59097403346814, '4F0': 19.999221444288878, '5A2': 19.99880716143227, '4F1': 99.997880880881, 'A1': 100.00213413413408, '510': 100.00110210210227, '5A0': 99.99869369369385,
        'A0': 99.99808508508502, '690': 99.9967177177176, '59B': 100.00163463463458, '587': 100.00095195195183, '110': 99.99292792792775, '5E4': 99.99638138138137, '2C0': 99.99842942942928,
        '5F0': 99.99797297297286, '51A': 200.0057134268539, '50': 200.0098216432867, '120': 200.0058577154313, '517': 199.98769338677366, '18': 199.98769338677317, '44': 1000.0305656565644,
        '43': 1000.0305656565666, '34': 1000.0224141414141, '42': 999.9959393939397}
time = {}
sum = {}
count = {}
cwd = os.getcwd()
file = "Attack_DataSet.asc"
path = cwd + "\\" + file
data = np.genfromtxt(path, encoding='ascii', names=('time', 'ID'), dtype=None, skip_header=4, usecols=(0, 2))

length = len(data)
error = 0.9


def calcSum(ID, diff):
    if ID in sum:
        sum[ID] += diff
        count[ID] += 1
    else:
        sum[ID] = diff
        count[ID] = 1

def calcMean():
    f = open('mean.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    mean = {}
    for k in sum.keys():
        mean[k] = sum[k] / count[k]
        wr.writerow([k, mean[k]])

    return mean

def detectAttack(ID, time, error):
    m = mean[ID]
    rate = time / m
    if rate > (1 + error):
        print("Detect slow packet...")
        print("ID (%s) mean (%f) time (%f) rate (%f) " % (ID, m, time, rate))
    elif rate < (1 - error):
        print("Detect fast packet...")
        print("ID (%s) mean (%f) time (%f) rate (%f)" % (ID, m, time, rate))


for i in range(length):
    if data[i][1] in time:
        ID = data[i][1]
        diff = (data[i][0] - time[ID]) * 1000
        if ID == "1F1" and diff > 10000.0:
            print("over")
            time[ID] = data[i][0]
            continue
        #calcSum(ID, diff)
        #print("ID (%s) : %f" % (data[i][1], diff))
        detectAttack(ID, diff, error)
        time[ID] = data[i][0]
    else:
        ID = data[i][1]
        if ID == "ErrorFrame":
            continue
        time[ID] = data[i][0]

mean = calcMean()
#print(mean)
'''
There are fast packet which have ID '1F1' and this ID also have one slow packet
'''







