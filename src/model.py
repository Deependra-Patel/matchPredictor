#!/usr/bin/python
import math
import random
import numpy as np
from sklearn import linear_model, svm
from sklearn.svm import SVR
from sets import Set
from sklearn.ensemble import GradientBoostingRegressor
from classes import *
import warnings
warnings.filterwarnings("ignore")


#map for storing stats
batsmen = {}
bowlers = {}
teams = {}

#Populate the team, batsman and bowler statistics from reading corresponding .dat files
def init():
    team_file = open("../data/teams.dat", 'r')
    lines = team_file.readlines()
    for line in lines:
        info = line[0:-1].split(' ')
        teams[info[0]] = Team(info[0], int(info[1]), int(info[2]), int(info[3]), int(info[4]), int(info[5]), int(info[6]))

    batsmen_file = open("../data/batsmen.dat", 'r')
    lines = batsmen_file.readlines()
    for line in lines:
        info = line[0:-1].split(' ')
        if info[1] == "0" or info[3] == "0":
            batsmen[info[0]] = Batsman(info[0], 1, 1, 10, 0, 0)
        else:
            batsmen[info[0]] = Batsman(info[0], int(info[1]), int(info[2]), int(info[3]), 0, 0)

    bowler_file = open("../data/bowlers.dat", 'r')
    lines = bowler_file.readlines()
    for line in lines:
        info = line[0:-1].split(' ')
        if info[3] == "0" or info[4] == "0":
            bowlers[info[0]] = Bowler(info[0], 3, 50, 1, 25, 0, 0, 0)
        else:
            bowlers[info[0]] = Bowler(info[0], int(info[1]), int(info[2]), int(info[3]), int(info[4]), 0, 0, 0)


#generating feature vector from team configurations
def transformData(rawData):
    data = []
    outcome = []
    for entire_row in rawData:
        row = entire_row[0:-1].split(' ')
        new_row = []
        new_row += teams[row[0]].features()
        new_row += teams[row[1]].features()
        for i in range(11):
            new_row += batsmen[row[2+i]].features()

        for i in range(5):
            new_row += bowlers[row[13 + i]].features()

        for i in range(11):
            new_row += batsmen[row[18 + i]].features()

        for i in range(5):
            new_row += bowlers[row[29 + i]].features()

        outcome.append(int(row[34]))
        data.append(new_row)
    return data, outcome

#calculating probability of winning 
def prob(val):
    e = 2.71828
    return 1/(1+e**(-val+0.5))

#first trains the model and then tests. 80:20 partition is done
def train_and_test():
    raw_data = open("../data/matches.dat", 'r').readlines()
    random.shuffle(raw_data)
    x = int(0.8*len(raw_data))
    data, Output = transformData(raw_data[:x])
    test_data, expected_output = transformData(raw_data[x:])

    trainData = np.array(data)
    testData = np.array(test_data)
    X = trainData[:, :]
    # regr = svm.LinearSVC()
    regr = linear_model.LinearRegression()
    # regrCasual = linear_model.Ridge(alpha = 0.2)
    # regrCasual = SVR(C=1.0, epsilon=200)
    # regr = GradientBoostingRegressor(n_estimators=90).fit(X, Output)

    regr.fit(X, Output)

    error = 0
    correct = 0

    #testing the model
    for i in range(len(test_data)):
        if (regr.predict(testData[i]) <= 0.5 and expected_output[i]==0) or (regr.predict(testData[i])>=0.5 and expected_output[i]==1):
            correct += 1
        else :
            error += 1
    print "Succes rate of model on train data", 100*float(correct)/float(correct + error), "%"

    #special test case
    test_data_special = "Australia India ML_Hayden SM_Katich RT_Ponting DR_Martyn A_Symonds BJ_Haddin MEK_Hussey GB_Hogg B_Lee SR_Clark GD_McGrath SR_Clark GD_McGrath B_Lee A_Symonds GB_Hogg V_Sehwag SR_Tendulkar M_Kaif R_Dravid D_Mongia SK_Raina MS_Dhoni AB_Agarkar Harbhajan_Singh RP_Singh MM_Patel V_Sehwag AB_Agarkar D_Mongia MM_Patel RP_Singh 1\n"
    x_special, expected = transformData([test_data_special])
    print "Probability of winning of Australia over India for match:\n ", test_data_special, prob(regr.predict(x_special))
    return regr

def main():
    init()
    regr = train_and_test()

main()
