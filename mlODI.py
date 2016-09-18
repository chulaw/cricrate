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

odiNums = list(range(3315, 3713))
preds = []
for i in range(0, 2):
    odi = pandas.read_csv("odiML" + `(i+1)` + ".csv")
    odi.loc[odi["MatchOdds"] == "None", "MatchOdds"] = 0.5
    odi.loc[odi["MatchOddsAdj"] == "None", "MatchOddsAdj"] = 0.5
    for j in range(0, len(odiNums)):
        odi_train = odi[odi['Id'] < odiNums[j]]
        #odi_train = odi_train[odi_train['Overs'] >= 42]
        odi_test = odi[odi['Id'] == odiNums[j]]
        #odi_test = odi_test[odi_test['Overs'] >= 42]
        if len(odi_test) == 0: continue

        #predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "Overs", "HomeAway", "MatchOdds", "MatchOddsAdj"] if i == 0 else ["RunsReq", "Wkts", "Team1Rating", "Team2Rating", "BallsRem", "HomeAway", "MatchOdds" , "MatchOddsAdj"]
        #predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "Overs", "HomeAway", "Momentum", "BattingRating", "BowlingRating"] if i == 0 else ["RunsReq", "Wkts", "Team1Rating", "Team2Rating", "BallsRem", "HomeAway", "MatchOdds", "MatchOddsAdj", "BattingRating", "BowlingRating"]
        predictors = ["Runs", "Wkts", "Team1Rating", "Team2Rating", "Overs", "HomeAway", "BattingRating", "BowlingRating"] if i == 0 else ["RunsReq", "Wkts", "Team1Rating", "Team2Rating", "BallsRem", "HomeAway", "BattingRating", "BowlingRating", "MatchOdds", "MatchOddsAdj"]
        #predictors = ["RunsReq", "Wkts", "BallsRem", "Team1Rating", "Team2Rating", "HomeAway", "MatchOdds", "MatchOddsAdj"]

        # Predict probabilities
        alg = LogisticRegression(random_state=1)
        scores = cross_validation.cross_val_score(alg, odi_train[predictors], odi_train["Result"], cv=3)
        print(`odiNums[j]` + " " + `scores.mean()`)

        # alg = GradientBoostingClassifier(random_state=1, n_estimators=100, max_depth=2)
        # scores = cross_validation.cross_val_score(alg, odi_train[predictors], odi_train["Result"], cv=3)
        # print("Gradient Boosting: " + `scores.mean()`)
        # alg = RandomForestClassifier(random_state=1, n_estimators=150, min_samples_split=4, min_samples_leaf=2)
        # scores = cross_validation.cross_val_score(alg, odi_train[predictors], odi_train["Result"], cv=3)
        # print("Random Forest: " + `scores.mean()`)

        # Fit the algorithm using the full training data.
        alg.fit(odi_train[predictors], odi_train["Result"])

        # Predict using the test dataset.
        pred = alg.predict_proba(odi_test[predictors].astype(float))[:,1] * 100.0

        predDF = pandas.DataFrame({
                "Id": odi_test["Id"],
                "Innings": (i+1),
                "Overs": odi_test["Overs"],
                "PredOdds": pred,
                "Result": odi_test["Result"],
                "MatchOddsAdj": odi_test["MatchOddsAdj"]
            })

        # if i == 1:
        #     predDF["MatchOddsAdj"] = np.where(predDF["MatchOddsAdj"] == "None", predDF["PredOdds"], predDF['MatchOddsAdj'])
        #     predDF["PredOdds"] = np.where(predDF['Overs'] >= 34, predDF['MatchOddsAdj'], predDF["PredOdds"])

        del predDF['MatchOddsAdj']
        preds.append(predDF)

dump = pandas.concat(preds)
dump.to_csv("odiMLPred.csv", index=False)

elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

#alg = LinearRegression()
        #kf = KFold(odi_train.shape[0], n_folds=3, random_state=1)
# predictions = np.concatenate(predictions, axis=0)
    # predictions[predictions >= 0.5] = 1
    # predictions[predictions < 0.5] = 0
    # accuracy = sum(predictions[predictions == odi["Result"]]) / len(predictions)
    # print("Linear Regression: " + `accuracy`)

    # alg = LogisticRegression(random_state=1)
    # scores = cross_validation.cross_val_score(alg, odi_train[predictors], odi_train["Result"], cv=3)
    # print("Logistic Regression: " + `scores.mean()`)
    #
    # #n_estimators is the number of trees we want to make
    # #min_samples_split is the minimum number of rows we need to make a split
    # #min_samples_leaf is the minimum number of samples we can have at the place where a tree branch ends (the bottom points of the tree)
    # alg = RandomForestClassifier(random_state=1, n_estimators=150, min_samples_split=4, min_samples_leaf=2)
    # scores = cross_validation.cross_val_score(alg, odi_train[predictors], odi_train["Result"], cv=3)
    # print("Random Forest 1: " + `scores.mean()`)
    #
    # alg = RandomForestClassifier(random_state=1, n_estimators=250, min_samples_split=4, min_samples_leaf=2)
    # scores = cross_validation.cross_val_score(alg, odi_train[predictors], odi_train["Result"], cv=3)
    # print("Random Forest 2: " + `scores.mean()`)

    # for train, test in kf:
    #     train_predictors = (odi[predictors].iloc[train,:])
    #     train_target = odi_train["Result"].iloc[train]
    #     alg.fit(train_predictors, train_target)
    #     test_predictions = alg.predict(odi_train[predictors].iloc[test,:])
    #     predictions.append(test_predictions)

    #selector = SelectKBest(f_classif, k=7)
    #selector.fit(odi_train[predictors], odi_train["Result"])

    # Get the raw p-values for each feature, and transform from p-values into scores
    # scores = -np.log10(selector.pvalues_)
    # print predictors
    # print scores

    #elapsedSec = (time.clock() - start)
    #elapsedMin =  elapsedSec / 60
    #print 'Time elapsed: ' + `elapsedMin` + 'min'

# algorithms = [
#     [GradientBoostingClassifier(random_state=1, n_estimators=100, max_depth=3), predictors],
#     [LogisticRegression(random_state=1), predictors]
# ]
#
# # Initialize the cross validation folds
# kf = KFold(odi.shape[0], n_folds=3, random_state=1)
#
# predictions = []
# for train, test in kf:
#     train_target = odi["Result"].iloc[train]
#     full_test_predictions = []
#     # Make predictions for each algorithm on each fold
#     for alg, predictors in algorithms:
#         # Fit the algorithm on the training data.
#         alg.fit(odi[predictors].iloc[train,:], train_target)
#         # Select and predict on the test fold.
#         # The .astype(float) is necessary to convert the dataframe to all floats and avoid an sklearn error.
#         test_predictions = alg.predict_proba(odi[predictors].iloc[test,:].astype(float))[:,1]
#         full_test_predictions.append(test_predictions)
#     # Use a simple ensembling scheme -- just average the predictions to get the final classification.
#     test_predictions = (full_test_predictions[0] + full_test_predictions[1]) / 2
#     # Any value over .5 is assumed to be a 1 prediction, and below .5 is a 0 prediction.
#     test_predictions[test_predictions <= .5] = 0
#     test_predictions[test_predictions > .5] = 1
#     predictions.append(test_predictions)
#
# # Put all the predictions together into one array.
# predictions = np.concatenate(predictions, axis=0)
#
# # Compute accuracy by comparing to the training data.
# accuracy = sum(predictions[predictions == odi["Result"]]) / len(predictions)
# print("Ensemble: " + `accuracy`)

