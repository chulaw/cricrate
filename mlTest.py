#!/usr/bin/env python
import time
import sqlite3
import csv
import pandas
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import KFold
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.grid_search import GridSearchCV
import numpy as np
import xgboost as xgb
start = time.clock()

preds = []
for i in range(0, 4):
    print "Innings: " + `(i+1)`
    test = pandas.read_csv("testML" + `(i+1)` + ".csv")
    numTests = test['Id'].max() - test['Id'].min()
    trainTestSplit = test['Id'].min() + int(numTests * 0.7)
    testNums = list(range(trainTestSplit, test['Id'].max()+1))

    test.loc[test["WinOdds"] == "None", "WinOdds"] = 0.3333
    test.loc[test["DrawOdds"] == "None", "DrawOdds"] = 0.3333

    testPR = pandas.read_csv("testML" + `(i+1)` + "PR.csv")
    test = test.merge(testPR, on=['Id', 'Overs'])

    test[['WinOdds','DrawOdds']] = test[['WinOdds','DrawOdds']].apply(pandas.to_numeric)
    test = test.fillna(0)
    test['TeamRatingDiff'] = test['Team1Rating'] - test['Team2Rating']
    test['BatBowlDiff'] = test['BattingRating'] - test['BowlingRating']

    winPreds = []
    drawPreds = []
    probPreds = []
    for j in range(0, len(testNums)):
        # if odiNums[j] < 1819: continue
        # print odiNums[j]
        # odi_train = odi[(odi['Id'] < odiNums[j]) & (odi['Id'] > (odiNums[j]-1000))]
        test_train = test[test['Id'] < testNums[j]]
        test_test = test[test['Id'] == testNums[j]]
        if len(test_test) == 0: continue

        #predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "Overs", "HomeAway", "MatchOdds", "MatchOddsAdj"] if i == 0 else ["RunsReq", "Wkts", "Team1Rating", "Team2Rating", "BallsRem", "HomeAway", "MatchOdds" , "MatchOddsAdj"]
        #predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "Overs", "BattingRating", "BowlingRating", "HomeAway", "Momentum", "MatchOdds" , "MatchOddsAdj"] if i == 0 else ["RunsReq", "Wkts", "Team1Rating", "Team2Rating", "BallsRem", "BattingRating", "BowlingRating", "HomeAway", "MatchOdds" , "MatchOddsAdj"]
        #predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "Overs", "MatchOdds" , "MatchOddsAdj"] if i == 0 else ["RunsReq", "Wkts", "Team1Rating", "Team2Rating", "BallsRem", "MatchOdds", "MatchOddsAdj"]
        #predictors = ["Runs", "Wkts", "Overs", "Team1Rating", "Team2Rating", "MatchOdds" , "MatchOddsAdj"] if i == 0 else ["RunsReq", "Wkts", "BallsRem", "Team1Rating", "Team2Rating", "MatchOdds" , "MatchOddsAdj"]
        if i == 0:
            winPredictors = ["OversRem", "Team1Rating", "Team2Rating", "HomeAway", "Runs", "Wkts", "Overs", "WinOdds", "DrawOdds", 'TeamRatingDiff', 'BatBowlDiff'] # logistic
            drawPredictors = ["OversRem", "Team1Rating", "Team2Rating", "HomeAway", "Runs", "Wkts", "Overs", "WinOdds", "DrawOdds", 'TeamRatingDiff', 'BatBowlDiff'] # random forest 150
        elif i == 1:
            winPredictors = ["OversRem", "Team1Rating", "Team2Rating", "HomeAway", "Runs", "Wkts", "Overs", "WinOdds", "DrawOdds", "RunsReq", 'TeamRatingDiff', 'BatBowlDiff'] # logistic
            drawPredictors = ["OversRem", "Team1Rating", "Team2Rating", "HomeAway", "Runs", "Wkts", "Overs", "WinOdds", "DrawOdds", "RunsReq", 'TeamRatingDiff', 'BatBowlDiff'] # logistic
        elif i == 2:
            winPredictors = ["OversRem", "Team1Rating", "Team2Rating", "HomeAway", "Runs", "Wkts", "Overs", "WinOdds", "DrawOdds", "RunsReq", 'TeamRatingDiff', 'BatBowlDiff'] # logistic
            drawPredictors = ["OversRem", "Team1Rating", "Team2Rating", "HomeAway", "Runs", "Wkts", "Overs", "WinOdds", "DrawOdds", "RunsReq", 'TeamRatingDiff', 'BatBowlDiff'] # gradient 150
        elif i == 3:
            winPredictors = ["OversRem", "Team1Rating", "Team2Rating", "HomeAway", "Runs", "Wkts", "Overs", "WinOdds", "DrawOdds", "RunsReq", 'TeamRatingDiff', 'BatBowlDiff'] # logistic
            drawPredictors = ["OversRem", "Team1Rating", "Team2Rating", "HomeAway", "Runs", "Wkts", "Overs", "WinOdds", "DrawOdds", "RunsReq", 'TeamRatingDiff', 'BatBowlDiff'] # random forest 200

        # Predict probabilities
        if i == 0:
            # alg = xgb.XGBClassifier(n_estimators=100, max_depth=2, learning_rate=0.01)
            winAlg = xgb.XGBClassifier(n_estimators=5, max_depth=2, learning_rate=0.1)
            drawAlg = xgb.XGBClassifier(n_estimators=5, max_depth=2, learning_rate=0.025)
        elif i == 1:
            winAlg = xgb.XGBClassifier(n_estimators=50, max_depth=2, learning_rate=0.1)
            drawAlg = xgb.XGBClassifier(n_estimators=50, max_depth=2, learning_rate=0.1)
        elif i == 2:
            winAlg = xgb.XGBClassifier(n_estimators=150, max_depth=3, learning_rate=0.01)
            drawAlg = xgb.XGBClassifier(n_estimators=10, max_depth=3, learning_rate=0.05)
        else:
            winAlg = xgb.XGBClassifier(n_estimators=150, max_depth=2, learning_rate=0.01)
            drawAlg = xgb.XGBClassifier(n_estimators=5, max_depth=3, learning_rate=0.01)

        # selector = SelectKBest(f_classif, k="all")
        # selector.fit(test_train[winPredictors], test_train["WinResult"])
        # print winPredictors
        # print selector.scores_
        #
        # selector = SelectKBest(f_classif, k="all")
        # selector.fit(test_train[drawPredictors], test_train["DrawResult"])
        # print drawPredictors
        # print selector.scores_
        # asd

        # param_grid = {
        #     'n_estimators': [5, 10, 15, 20, 30, 50, 100, 150, 200],
        #     'learning_rate': [0.01, 0.025, 0.05, 0.1, 0.2],
        #     'max_depth': [2, 3, 4, 5]
        # }
        #
        # gridSearch = GridSearchCV(estimator=winAlg, param_grid=param_grid)
        # gridSearch.fit(test_train[winPredictors], test_train["WinResult"])
        # print gridSearch.best_params_
        #
        # gridSearch = GridSearchCV(estimator=drawAlg, param_grid=param_grid)
        # gridSearch.fit(test_train[drawPredictors], test_train["DrawResult"])
        # print gridSearch.best_params_
        # asd

        winAlg.fit(test_train[winPredictors], test_train["WinResult"])
        # # # # Predict using the test dataset.
        pred = winAlg.predict(test_test[winPredictors])
        winPreds.extend(pred)
        winProbPred = winAlg.predict_proba(test_test[winPredictors].astype(float))[:,1] * 100.0

        drawAlg.fit(test_train[drawPredictors], test_train["DrawResult"])
        # # # # Predict using the test dataset.
        pred = drawAlg.predict(test_test[drawPredictors])
        drawPreds.extend(pred)
        drawProbPred = drawAlg.predict_proba(test_test[drawPredictors].astype(float))[:,1] * 100.0

        # preds.extend(np.round(np.array(odi_test["MatchOddsAdj"]) / 100, 0))
        # asd
        probPredDf = pandas.DataFrame({
                    "Id": test_test["Id"],
                    "Innings": (i+1),
                    "OversRem": test_test["OversRem"],
                    # "MatchOddsAdj": odi_test["MatchOddsAdj"],
                    "PredWinOdds": winProbPred,
                    "PredDrawOdds": drawProbPred,
                    # "PredOdds": np.array(odi_test["MatchOddsAdj"]),
                    "WinResult": test_test["WinResult"],
                    "DrawResult": test_test["DrawResult"],
            })

        probPreds.append(probPredDf)
    winActuals = test[test['Id'] >= testNums[0]]["WinResult"].tolist()
    f1_score_win = f1_score(winActuals, winPreds)
    roc_auc_score_win = roc_auc_score(winActuals, winPreds)
    drawActuals = test[test['Id'] >= testNums[0]]["DrawResult"].tolist()
    f1_score_draw = f1_score(drawActuals, drawPreds)
    roc_auc_score_draw = roc_auc_score(drawActuals, drawPreds)
    print "Test Innings " + `(i+1)`+ " - F1 Score (Win): " + `round(f1_score_win * 100, 2)` + " - F1 Score (Draw): " + `round(f1_score_draw * 100, 2)` + ", ROC AUC Score (Win): " + `round(roc_auc_score_win * 100, 2)` + ", ROC AUC Score (Draw): " + `round(roc_auc_score_draw * 100, 2)`
    dump = pandas.concat(probPreds)
    dump.to_csv("testMLPred"+`(i+1)`+".csv", index=False)
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
