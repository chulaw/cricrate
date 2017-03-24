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

for i in range(0,  2):
    t20 = pandas.read_csv("t20ML" + `(i+1)` + "UnqRRHMLT.csv")
    numt20s = t20['Id'].max() - t20['Id'].min()
    trainTestSplit = t20['Id'].min() + int(numt20s * 0.7)
    t20Nums = list(range(trainTestSplit, t20['Id'].max()+1))
    t20.loc[t20["MatchOdds"] == "None", "MatchOdds"] = 0.5
    t20.loc[t20["MatchOddsAdj"] == "None", "MatchOddsAdj"] = 0.5
    t20[['MatchOdds','MatchOddsAdj']] = t20[['MatchOdds','MatchOddsAdj']].apply(pandas.to_numeric)
    t20['RunRate'] = t20['Runs'] / t20['Overs']
    if i == 1:
        t20 = t20[t20['BallsRem'] > 0]
        t20['ReqRunRate'] = t20['RunsReq'] * 6 / t20['BallsRem']
        # t20['RRRW'] = t20['ReqRunRate'] / (1 + t20['Wkts'].apply(np.sqrt))
    t20 = t20.fillna(0)
    t20['TeamRatingDiff'] = t20['Team1Rating'] - t20['Team2Rating']
    preds = []
    probPreds = []
    for j in range(0, len(t20Nums)):
        # if t20Nums[j] < 1819: continue
        # print t20Nums[j]
        # t20_train = t20[(t20['Id'] < t20Nums[j]) & (t20['Id'] > (t20Nums[j]-1000))]
        t20_train = t20[t20['Id'] < t20Nums[j]]
        t20_test = t20[t20['Id'] == t20Nums[j]]
        if len(t20_test) == 0: continue

        if i == 0:
            predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "HomeAway", "Momentum", "MatchOdds",
                            "MatchOddsAdj", "RunRate", "TeamRatingDiff"]
            # predictors = ["Runs", "Wkts", "HomeAway", "MatchOddsAdj", "RunRate", "TeamRatingDiff", "BatBowlDiff"]
        else:
            predictors = ["Overs", "RunsReq", "Wkts", "Team1Rating", "Team2Rating", "BallsRem", "MatchOdds", "MatchOddsAdj", "RunRate", "ReqRunRate"]
            # predictors = ["RunsReq", "Wkts", "HomeAway", "MatchOdds", "MatchOddsAdj", "ReqRunRate", "TeamRatingDiff", "BatBowlDiff"]

        # Predict probabilities
        if i == 0:
        #     #alg = LogisticRegression()
        #     # alg = xgb.XGBClassifier(n_estimators=20, max_depth=2, learning_rate=0.05)
            alg = xgb.XGBClassifier(n_estimators=30, max_depth=2, learning_rate=0.025)
        else:
        #     # alg = LogisticRegression()
        #     #alg = GradientBoostingClassifier(n_estimators=50, min_samples_split=2, max_depth=2)
        #     # alg = xgb.XGBClassifier(n_estimators=20, max_depth=4, learning_rate=0.025)
            alg = xgb.XGBClassifier(n_estimators=100, max_depth=2, learning_rate=0.05)

        # selector = SelectKBest(f_classif, k="all")
        # selector.fit(t20_train[predictors], t20_train["Result"])
        # print predictors
        # print selector.scores_
        # asd

        # param_grid = {
        #     'n_estimators': [10, 15, 20, 30, 40, 50, 100],
        #     'min_samples_split': [2, 3, 4, 5],
        #     'max_depth': [2, 3, 4, 5]
        # }
        # param_grid = {
        #     'n_estimators': [5, 10, 15, 20, 30, 50, 100, 150, 200],
        #     'learning_rate': [0.01, 0.025, 0.05, 0.1, 0.2],
        #     'max_depth': [2, 3, 4, 5]
        # }
        #
        # gridSearch = GridSearchCV(estimator=alg, param_grid=param_grid)
        # gridSearch.fit(t20_train[predictors], t20_train["Result"])
        # print gridSearch.best_params_
        # asd

        #Fit the algorithm using the full training data.
        alg.fit(t20_train[predictors], t20_train["Result"])
        # # # # Predict using the test dataset.
        pred = alg.predict(t20_test[predictors])
        preds.extend(pred)
        probPred = alg.predict_proba(t20_test[predictors].astype(float))[:,1] * 100.0

        # preds.extend(np.round(np.array(t20_test["MatchOddsAdj"]) / 100, 0))
        # asd

        probPredDf = pandas.DataFrame({
                    "Id": t20_test["Id"],
                    "Innings": (i+1),
                    "Overs": t20_test["Overs"],
                    # "MatchOddsAdj": t20_test["MatchOddsAdj"],
                    "PredOdds": probPred,
                    # "PredOdds": np.array(t20_test["MatchOddsAdj"]),
                    "Result": t20_test["Result"]
            })

        probPreds.append(probPredDf)
        # if i == 1:
        # #    probPredDf["MatchOddsAdj"] = np.where(probPredDf["MatchOddsAdj"] == "None", probPredDf["PredOdds"], probPredDf['MatchOddsAdj'])
        #    probPredDf["PredOdds"] = np.where(probPredDf['Overs'] >= 45, probPredDf['MatchOddsAdj'], probPredDf["PredOdds"])
        #
        # del probPredDf['MatchOddsAdj']

    actuals = t20[t20['Id'] >= t20Nums[0]]["Result"].tolist()
    f1_score = f1_score(actuals, preds)
    roc_auc_score = roc_auc_score(actuals, preds)
    print "t20 Innings " + `(i+1)`+ " - F1 Score: " + `round(f1_score * 100, 2)` + ", ROC AUC Score: " + `round(roc_auc_score * 100, 2)`
    dump = pandas.concat(probPreds)
    dump.to_csv("t20MLPred"+`(i+1)`+"UnqRRHMLT.csv", index=False)

elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
