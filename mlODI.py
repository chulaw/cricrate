#!/usr/bin/env python
import time
import sqlite3
import csv
import pandas
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.metrics import f1_score, roc_auc_score
import numpy as np
# import xgboost as xgb
start = time.clock()
overRange = [1, 50]
for i in range(0,  2):
    odi = pandas.read_csv("odiML" + `(i+1)` + "Live.csv")
    numOdis = odi['Id'].max() - odi['Id'].min()
    trainTestSplit = odi['Id'].min() + int(numOdis * 0.7)
    odiNums = list(range(trainTestSplit, odi['Id'].max()+1))
    odi.loc[odi["MatchOdds"] == "None", "MatchOdds"] = 0.5
    odi.loc[odi["MatchOddsAdj"] == "None", "MatchOddsAdj"] = 0.5
    odiPR = pandas.read_csv("odiML" + `(i+1)` + "PRLive2.csv")
    odi = odi.merge(odiPR, on=['Id', 'Overs'])
    odi[['MatchOdds','MatchOddsAdj']] = odi[['MatchOdds','MatchOddsAdj']].apply(pandas.to_numeric)
    odi['RunRate'] = odi['Runs'] / odi['Overs']
    if i == 1:
        odi = odi[odi['BallsRem'] > 0]
        odi['ReqRunRate'] = odi['RunsReq'] * 6 / odi['BallsRem']
        # odi['RRRW'] = odi['ReqRunRate'] / (1 + odi['Wkts'].apply(np.sqrt))
    odi = odi.fillna(0)
    odi['TeamRatingDiff'] = odi['Team1Rating'] - odi['Team2Rating']
    odi['PlayerRatingDiff'] = odi['BattingRating'] - odi['BowlingRating']
    # odi['ExpRunsDiff'] = odi['ExpRuns2'] - odi['ExpRuns1']
    # odi['RandNum'] = np.random.rand(len(odi),1)
    preds = []
    trainPreds = []
    probPreds = []
    odi = odi[(odi['Overs'] >= overRange[0]) & (odi['Overs'] <= overRange[1])]
    for j in range(0, len(odiNums)):
        # if odiNums[j] < 1819: continue
        # print odiNums[j]
        # odi_train = odi[(odi['Id'] < odiNums[j]) & (odi['Id'] > (odiNums[j]-1000))]
        odi_train = odi[odi['Id'] < odiNums[j]]
        odi_test = odi[odi['Id'] == odiNums[j]]
        if len(odi_test) == 0: continue

        if i == 0:
            # predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "Overs", "HomeAway", "Momentum", "BattingRating", "BowlingRating", "ExpRuns1", "ExpRuns2", "RuleChg", "MatchOdds",
            #                 "MatchOddsAdj", "RunRate", "TeamRatingDiff", "PlayerRatingDiff", "RandNum"]
            # predictors = ["Runs", "Wkts", "MatchOdds", "RunRate", "TeamRatingDiff", "PlayerRatingDiff", "RandNum"]
            predictors = ["Runs", "Wkts", "MatchOdds", "RunRate", "TeamRatingDiff", "PlayerRatingDiff"]
        else:
            # predictors = ["Overs", "Runs", "RunsReq", "Wkts", "Team1Rating", "Team2Rating", "BallsRem", "HomeAway", "MatchOdds", "MatchOddsAdj", "ExpRuns1", "ExpRuns2", "RuleChg", "BattingRating",
            #             "BowlingRating", "RunRate", "ReqRunRate", "TeamRatingDiff", "PlayerRatingDiff", "RandNum", "ExpRunsDiff"]
            # predictors = ["RunsReq", "Wkts", "MatchOdds", "ReqRunRate", "TeamRatingDiff", "PlayerRatingDiff", "RandNum"]
            predictors = ["RunsReq", "Wkts", "BallsRem", "MatchOdds", "RunRate", "ReqRunRate", "TeamRatingDiff", "PlayerRatingDiff"]

        # Predict probabilities
        if i == 0:
            # alg = LogisticRegression()
            alg = GradientBoostingClassifier(n_estimators=50, min_samples_split=2, max_depth=2)
            # alg = GradientBoostingClassifier(n_estimators=50, min_samples_split=10, max_depth=3)
        #     # alg = xgb.XGBClassifier(n_estimators=20, max_depth=2, learning_rate=0.05)
            # alg = xgb.XGBClassifier(n_estimators=30, max_depth=2, learning_rate=0.05)
            # alg = xgb.XGBClassifier(n_estimators=100, max_depth=2, learning_rate=0.01)
        else:
            # alg = LogisticRegression()
            alg = GradientBoostingClassifier(n_estimators=50, min_samples_split=2, max_depth=2)
        #     # alg = xgb.XGBClassifier(n_estimators=20, max_depth=4, learning_rate=0.025)
            # alg = xgb.XGBClassifier(n_estimators=20, max_depth=2, learning_rate=0.2)
            # alg = xgb.XGBClassifier(n_estimators=10, max_depth=2, learning_rate=0.2)
        #
        # selector = SelectKBest(f_classif, k="all")
        # selector.fit(odi_train[predictors], odi_train["Result"])
        # print predictors
        # print selector.scores_
        # asd

        param_grid = {
            'n_estimators': [5, 10, 15, 20, 30, 50, 100, 150, 200],
            # 'learning_rate': [0.01, 0.025, 0.05, 0.1, 0.2],
            'min_samples_split': [2, 5, 10, 25],
            'max_depth': [2, 3, 4, 5]
        }

        # gridSearch = GridSearchCV(estimator=alg, param_grid=param_grid)
        # gridSearch.fit(odi_train[predictors], odi_train["Result"])
        # print gridSearch.best_params_
        # print gridSearch.best_score_
        # asd

        #Fit the algorithm using the full training data.
        alg.fit(odi_train[predictors], odi_train["Result"])
        # # # # Predict using the test dataset.
        pred = alg.predict(odi_test[predictors])
        if j == (len(odiNums)-1):
            trainPred = alg.predict(odi_train[predictors])
            trainPreds.extend(trainPred)
        # pred = np.where(odi_test["MatchOdds"] >= 0.5, 1, 0)
        preds.extend(pred)
        probPred = alg.predict_proba(odi_test[predictors].astype(float))[:,1] * 100.0

        # preds.extend(np.round(np.array(odi_test["MatchOddsAdj"]) / 100, 0))
        # asd

        probPredDf = pandas.DataFrame({
                    "Id": odi_test["Id"],
                    "Innings": (i+1),
                    "Overs": odi_test["Overs"],
                    # "MatchOddsAdj": odi_test["MatchOddsAdj"],
                    "PredOdds": probPred,
                    # "PredOdds": np.array(odi_test["MatchOddsAdj"]),
                    "Result": odi_test["Result"]
            })

        probPreds.append(probPredDf)
        # if i == 1:
        # #    probPredDf["MatchOddsAdj"] = np.where(probPredDf["MatchOddsAdj"] == "None", probPredDf["PredOdds"], probPredDf['MatchOddsAdj'])
        #    probPredDf["PredOdds"] = np.where(probPredDf['Overs'] >= 45, probPredDf['MatchOddsAdj'], probPredDf["PredOdds"])
        #
        # del probPredDf['MatchOddsAdj']


    actuals = odi[odi['Id'] >= odiNums[0]]["Result"].tolist()
    trainActuals = odi[odi['Id'] < odiNums[len(odiNums)-1]]["Result"].tolist()
    # print trainActuals
    # print trainPreds
    train_f1_score = f1_score(trainActuals, trainPreds)
    train_roc_auc_score = roc_auc_score(trainActuals, trainPreds)
    test_f1_score = f1_score(actuals, preds)
    test_roc_auc_score = roc_auc_score(actuals, preds)
    print "ODI Innings " + `(i+1)`+ " - Over Range: "+ `overRange[0]` + "-" + `overRange[1]` + " - F1 Score: Train " + `round(train_f1_score * 100, 2)` + ", Test " +`round(test_f1_score * 100, 2)` + ", ROC AUC Score: Train " + `round(train_roc_auc_score * 100, 2)` + ", Test " + `round(test_roc_auc_score * 100, 2)`
    asd
    dump = pandas.concat(probPreds)
    # dump.to_csv("odiMLPred"+`(i+1)`+"UnqRRHML1000T.csv", index=False)

# 1st innings 1-50 = gradientboosting 50,2,2 72.47 F1, 71.73 ROCAUC
# 1st innings 1-10 = logistic = 67.36 F1, 68.06 ROCAUC ***
# 1st innings 11-50 = gradientboosting 50,2,2 = 74.07 F1, 72.97 ROCAUC ***
# 2nd innings 1-50 = gradientboosting 15,2,4 = 81 F1, 82.54 ROCAUC
# 2nd innings 1-39 = logistic = 80.21 F1, 81.77 ROCAUC ***
# 2nd innings 40-50 = logistic = 89.17 F1, 90.72 ROCAUC ***

elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
