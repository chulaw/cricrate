#!/usr/bin/env python
import time
import sqlite3
import csv
import pandas
#from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import KFold
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
#from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
start = time.clock()

preds = []
for  i in range(0, 4):
    print "Innings: " + `(i+1)`
    test = pandas.read_csv("testML" + `(i+1)` + ".csv")

    test.loc[test["WinOdds"] == "None", "WinOdds"] = 0.3333
    test.loc[test["DrawOdds"] == "None", "DrawOdds"] = 0.3333
    test_train = test[test['Id'] < 2069]
    test_test = test[test['Id'] >= 2069]

    #predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "Overs", "HomeAway", "MatchOdds", "MatchOddsAdj"] if i == 0 else ["RunsReq", "Wkts", "Team1Rating", "Team2Rating", "BallsRem", "HomeAway", "MatchOdds" , "MatchOddsAdj"]
    #predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "Overs", "BattingRating", "BowlingRating", "HomeAway", "Momentum", "MatchOdds" , "MatchOddsAdj"] if i == 0 else ["RunsReq", "Wkts", "Team1Rating", "Team2Rating", "BallsRem", "BattingRating", "BowlingRating", "HomeAway", "MatchOdds" , "MatchOddsAdj"]
    #predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "Overs", "MatchOdds" , "MatchOddsAdj"] if i == 0 else ["RunsReq", "Wkts", "Team1Rating", "Team2Rating", "BallsRem", "MatchOdds", "MatchOddsAdj"]
    #predictors = ["Runs", "Wkts", "Overs", "Team1Rating", "Team2Rating", "MatchOdds" , "MatchOddsAdj"] if i == 0 else ["RunsReq", "Wkts", "BallsRem", "Team1Rating", "Team2Rating", "MatchOdds" , "MatchOddsAdj"]
    if i == 0:
        winPredictors = ["OversRem", "Team1Rating", "Team2Rating", "HomeAway", "Runs", "Wkts", "Overs", "WinOdds", "DrawOdds"] # logistic
        drawPredictors = ["OversRem", "Team1Rating", "Team2Rating", "HomeAway", "Runs", "Wkts", "Overs", "WinOdds", "DrawOdds"] # random forest 150
    elif i == 1:
        winPredictors = ["OversRem", "RunsReq", "Team1Rating", "Team2Rating", "Runs", "Wkts", "Overs"] # logistic
        drawPredictors = ["OversRem", "RunsReq", "Team1Rating", "Team2Rating", "HomeAway", "Runs", "Wkts", "Overs", "WinOdds", "DrawOdds"] # logistic
    elif i == 2:
        winPredictors = ["RunsReq", "OversRem", "HomeAway", "Team1Rating", "Team2Rating", "Wkts", "Overs"] # logistic
        drawPredictors = ["RunsReq", "OversRem", "Wkts", "Runs"] # gradient 150
    elif i == 3:
        winPredictors = ["RunsReq", "OversRem", "Wkts"] # logistic
        drawPredictors = ["RunsReq", "OversRem", "Wkts", "Team1Rating", "Team2Rating", "Overs", "WinOdds", "DrawOdds"] # random forest 200

    # Predict probabilities
    alg = LogisticRegression(random_state=1)
    scores = cross_validation.cross_val_score(alg, test_train[winPredictors], test_train["WinResult"], cv=3)
    print("Win Logisitic Regression: " + `scores.mean()`)

    # Fit the algorithm using the full training data.
    alg.fit(test_train[winPredictors], test_train["WinResult"])

    # Predict using the test dataset.
    winPred = alg.predict_proba(test_test[winPredictors].astype(float))[:,1] * 100.0

    if i == 0:
        alg = RandomForestClassifier(random_state=1, n_estimators=150, min_samples_split=4, min_samples_leaf=2)
        scores = cross_validation.cross_val_score(alg, test_train[drawPredictors], test_train["DrawResult"], cv=3)
        print("Draw Random Forest: " + `scores.mean()`)
    elif i == 1:
        alg = LogisticRegression(random_state=1)
        scores = cross_validation.cross_val_score(alg, test_train[drawPredictors], test_train["DrawResult"], cv=3)
        print("Draw Logisitic Regression: " + `scores.mean()`)
    elif i == 2:
        alg = GradientBoostingClassifier(random_state=1, n_estimators=150, max_depth=2)
        scores = cross_validation.cross_val_score(alg, test_train[drawPredictors], test_train["DrawResult"], cv=3)
        print("Draw Gradient Boosting: " + `scores.mean()`)
    elif i == 3:
        alg = RandomForestClassifier(random_state=1, n_estimators=200, min_samples_split=4, min_samples_leaf=2)
        scores = cross_validation.cross_val_score(alg, test_train[drawPredictors], test_train["DrawResult"], cv=3)
        print("Draw Random Forest: " + `scores.mean()`)

    # Fit the algorithm using the full training data.
    alg.fit(test_train[drawPredictors], test_train["DrawResult"])

    # Predict using the test dataset.
    drawPred = alg.predict_proba(test_test[drawPredictors].astype(float))[:,1] * 100.0

    predDF = pandas.DataFrame({
            "Id": test_test["Id"],
            "Innings": (i+1),
            "OversRem": int(test_test["OversRem"]),
            "PredWinOdds": winPred,
            "PredDrawOdds": drawPred,
            "WinResult": test_test["WinResult"],
            "DrawResult": test_test["DrawResult"],
            #"MatchOddsAdj": test_test["MatchOddsAdj"]
        })

    #if i == 1:
    #    predDF["MatchOddsAdj"] = np.where(predDF["MatchOddsAdj"] == "None", predDF["PredOdds"], predDF['MatchOddsAdj'])
    #    predDF["PredOdds"] = np.where(predDF['Overs'] >= 34, predDF['MatchOddsAdj'], predDF["PredOdds"])

    #del predDF['MatchOddsAdj']
    preds.append(predDF)

concatPreds = pandas.concat(preds)
concatPreds.to_csv("testMLPred.csv", index=False)

elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'