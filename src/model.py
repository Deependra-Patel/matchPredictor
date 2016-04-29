#!/usr/bin/python
import math
import numpy as np
from sklearn import linear_model
from sklearn.svm import SVR
from sets import Set
from sklearn.ensemble import GradientBoostingRegressor
from classes import *

casualIndex = 34
registeredIndex = casualIndex + 1
totalIndex = casualIndex + 2

batsmen = {}
bowlers = {}
teams = {}

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



def train():
    raw_data = open("../data/matches.dat", 'r').readlines()
    data, Output = transformData(raw_data)
    trainData = np.array(data[:])
    X = trainData[:, :]
    regr = linear_model.LinearRegression()
    # regrCasual = linear_model.Ridge(alpha = 0.2)
    # regrCasual = SVR(C=1.0, epsilon=200)
    #regr = GradientBoostingRegressor(n_estimators=90).fit(X, Output)
    # regrRegistered = GradientBoostingRegressor(n_estimators=90).fit(X, Registered)

    regr.fit(X, Output)

    error = 0
    correct = 0
    for i in range(len(trainData)):
        if (regr.predict(X[i])<0.5 and Output[i]==0) or (regr.predict(X[i])>=0.5 and Output[i]==1):
            correct += 1
        else :
            error += 1
    print "Succes rate of model on train data", float(correct)/float(correct + error)

    return regr

def main():
    init()
    regr = train()

main()
