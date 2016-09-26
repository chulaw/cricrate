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

for i in range(1, 2):
    odi = pandas.read_csv("odiML" + `(i+1)` + ".csv")
    numOdis = odi['Id'].max() - odi['Id'].min()
    trainTestSplit = odi['Id'].min() + int(numOdis * 0.7)
    odiNums = list(range(trainTestSplit, odi['Id'].max()+1))
    odi.loc[odi["MatchOdds"] == "None", "MatchOdds"] = 0.5
    odi.loc[odi["MatchOddsAdj"] == "None", "MatchOddsAdj"] = 0.5
    odiPR = pandas.read_csv("odiML" + `(i+1)` + "PR.csv")
    odi = odi.merge(odiPR, on=['Id', 'Overs'])
    odi[['MatchOdds','MatchOddsAdj']] = odi[['MatchOdds','MatchOddsAdj']].apply(pandas.to_numeric)
    odi['RunRate'] = odi['Runs'] / odi['Overs']
    if i == 1:
        odi = odi[odi['BallsRem'] > 0]
        odi['ReqRunRate'] = odi['RunsReq'] * 6 / odi['BallsRem']
        # odi['RRRW'] = odi['ReqRunRate'] / (1 + odi['Wkts'].apply(np.sqrt))
    odi = odi.fillna(0)
    odi['TeamRatingDiff'] = odi['Team1Rating'] - odi['Team2Rating']
    odi['BatBowlDiff'] = odi['BattingRating'] - odi['BowlingRating']
    preds = []
    probPreds = []
    for j in range(0, len(odiNums)):
        # print odiNums[j]
        odi_train = odi[odi['Id'] < odiNums[j]]
        odi_test = odi[odi['Id'] == odiNums[j]]
        if len(odi_test) == 0: continue

        if i == 0:
            predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "Overs", "HomeAway", "Momentum", "BattingRating", "BowlingRating", "ExpRuns1", "ExpRuns2", "RuleChg", "MatchOdds",
                            "MatchOddsAdj", "RunRate", "TeamRatingDiff", "BatBowlDiff"]
            # predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "HomeAway", "Momentum", "BattingRating", "BowlingRating", "MatchOdds",
            #               "MatchOddsAdj", "RunRate", "TeamRatingDiff", "BatBowlDiff"]
        else:
            predictors = ["Overs", "Runs", "RunsReq", "Wkts", "Team1Rating", "Team2Rating", "BallsRem", "HomeAway", "MatchOdds", "MatchOddsAdj", "ExpRuns1", "ExpRuns2", "RuleChg", "BattingRating",
                        "BowlingRating", "RunRate", "ReqRunRate", "TeamRatingDiff", "BatBowlDiff"]
            #predictors = ["RunsReq", "Wkts", "Team1Rating", "Team2Rating", "HomeAway", "MatchOdds", "MatchOddsAdj", "ExpRuns1", "ExpRuns2", "RuleChg", "BattingRating", "BowlingRating"]

        # Predict probabilities
        if i == 0:
            #alg = LogisticRegression()
            alg = xgb.XGBClassifier(n_estimators=10, max_depth=2, learning_rate=0.1)
        else:
            # alg = LogisticRegression()
            #alg = GradientBoostingClassifier(n_estimators=50, min_samples_split=2, max_depth=2)
            alg = xgb.XGBClassifier(n_estimators=50, max_depth=2, learning_rate=0.1)

        # selector = SelectKBest(f_classif, k="all")
        # selector.fit(odi_train[predictors], odi_train["Result"])
        # print predictors
        # print selector.scores_
        # asd

        # param_grid = {
        #     'n_estimators': [10, 15, 20, 30, 40, 50, 100],
        #     'min_samples_split': [2, 3, 4, 5],
        #     'max_depth': [2, 3, 4, 5]
        # }
        # param_grid = {
        #     'n_estimators': [5, 10, 15, 20, 30, 50, 100],
        #     'learning_rate': [0.01, 0.025, 0.05, 0.1, 0.2],
        #     'max_depth': [2, 3, 4, 5]
        # }
        #
        # gridSearch = GridSearchCV(estimator=alg, param_grid=param_grid)
        # gridSearch.fit(odi_train[predictors], odi_train["Result"])
        # print gridSearch.best_params_
        # asd

        # Fit the algorithm using the full training data.
        alg.fit(odi_train[predictors], odi_train["Result"])

        # Predict using the test dataset.
        pred = alg.predict(odi_test[predictors])
        preds.extend(pred)
        probPred = alg.predict_proba(odi_test[predictors].astype(float))[:,1] * 100.0

        probPredDf = pandas.DataFrame({
                    "Id": odi_test["Id"],
                    "Innings": (i+1),
                    "Overs": odi_test["Overs"],
                    "PredOdds": probPred,
                    "Result": odi_test["Result"]
                    #"MatchOddsAdj": odi_test["MatchOddsAdj"]
            })

        # # if i == 1:
        # #     predDF["MatchOddsAdj"] = np.where(predDF["MatchOddsAdj"] == "None", predDF["PredOdds"], predDF['MatchOddsAdj'])
        # #     predDF["PredOdds"] = np.where(predDF['Overs'] >= 34, predDF['MatchOddsAdj'], predDF["PredOdds"])
        #
        # del probPredDf['MatchOddsAdj']
        probPreds.append(probPredDf)

    actuals = odi[odi['Id'] >= odiNums[0]]["Result"].tolist()
    f1_score = f1_score(actuals, preds)
    roc_auc_score = roc_auc_score(actuals, preds)
    print "ODI Innings " + `(i+1)`+ " - F1 Score: " + `round(f1_score * 100, 2)` + ", ROC AUC Score: " + `round(roc_auc_score * 100, 2)`
    dump = pandas.concat(probPreds)
    dump.to_csv("odiMLPred"+`(i+1)`+".csv", index=False)

elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
