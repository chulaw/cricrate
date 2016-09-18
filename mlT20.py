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
from sklearn.metrics import roc_auc_score
from sklearn.feature_selection import SelectKBest, f_classif
import numpy as np
start = time.clock()

preds = []
#t2012 = []
for  i in range(0, 2):
    # if i == 0:
    #     t20 = pandas.read_csv("t20ML" + `(i+1)` + ".csv")
    # else:
    #     t201 = pandas.read_csv("t20ML" + `i` + ".csv")
    #     t202 = pandas.read_csv("t20ML" + `(i+1)` + ".csv")
    #     t2012.append(t201)
    #     t2012.append(t202)
    #     t20 = pandas.concat(t2012)
    print "Innings: " + `(i+1)`
    t20 = pandas.read_csv("t20ML" + `(i+1)` + ".csv")

    t20.loc[t20["MatchOdds"] == "None", "MatchOdds"] = 0.5
    t20.loc[t20["MatchOddsAdj"] == "None", "MatchOddsAdj"] = 0.5
    t20_train = t20[t20['Id'] < 871]
    t20_test = t20[t20['Id'] >= 871]

    if i == 0:
        predictors = ["Runs", "Wkts", "Overs", "T20I", "BattingRating", "BowlingRating"]
        #predictors = ["Team1Rating", "Team2Rating"]
        #predictors = ["Runs", "Wkts", "MatchOdds", "MatchOddsAdj", "Overs", "Team1Rating", "Team2Rating", "T20I", "BattingRating", "BowlingRating", "HomeAway", "Momentum"]
    else:
        #predictors = ["Team1Rating", "Team2Rating"]
        predictors = ["RunsReq", "Wkts", "BallsRem", "T20I", "MatchOdds" , "MatchOddsAdj", "HomeAway"]
        #predictors = ["RunsReq", "Wkts", "BallsRem", "MatchOdds" , "MatchOddsAdj", "Team1Rating", "Team2Rating", "T20I", "BattingRating", "BowlingRating", "HomeAway", "Momentum"]

    # selector = SelectKBest(f_classif, k=5)
    # selector.fit(t20_train[predictors], t20_train["Result"])
    # # Transform from p-values into scores
    # scores = -np.log10(selector.pvalues_)
    # print(predictors)
    # print(scores)

    # Predict probabilities
    if i == 0:
        alg = GradientBoostingClassifier(random_state=1, learning_rate=0.1, n_estimators=500, max_depth=2)
    else:
        alg = GradientBoostingClassifier(random_state=1, learning_rate=0.03, n_estimators=500, max_depth=2)
    alg.fit(t20_train[predictors], t20_train["Result"])
    train_predictions = alg.predict(t20_train[predictors])
    train_auc = roc_auc_score(train_predictions, t20_train["Result"])
    test_predictions = alg.predict(t20_test[predictors])
    test_auc = roc_auc_score(test_predictions, t20_test["Result"])
    print("Gradient Boosting Train: " + `train_auc`)
    print("Gradient Boosting Test: " + `test_auc` + "\n")
    alg = RandomForestClassifier(random_state=1, n_estimators=300, min_samples_split=100, min_samples_leaf=25)
    alg.fit(t20_train[predictors], t20_train["Result"])
    train_predictions = alg.predict(t20_train[predictors])
    train_auc = roc_auc_score(train_predictions, t20_train["Result"])
    test_predictions = alg.predict(t20_test[predictors])
    test_auc = roc_auc_score(test_predictions, t20_test["Result"])
    print("Random Forest Train: " + `train_auc`)
    print("Random Forest Test: " + `test_auc` + "\n")
    alg = LogisticRegression(random_state=1)
    alg.fit(t20_train[predictors], t20_train["Result"])
    train_predictions = alg.predict(t20_train[predictors])
    train_auc = roc_auc_score(train_predictions, t20_train["Result"])
    test_predictions = alg.predict(t20_test[predictors])
    test_auc = roc_auc_score(test_predictions, t20_test["Result"])
    print("Logisitic Regression Train: " + `train_auc`)
    print("Logisitic Regression Test: " + `test_auc` + "\n")

    # Predict using the test dataset.
    pred = alg.predict_proba(t20_test[predictors].astype(float))[:,1] * 100.0

    predDF = pandas.DataFrame({
            "Id": t20_test["Id"],
            "Innings": (i+1),
            "Overs": t20_test["Overs"],
            "PredOdds": pred,
            "Result": t20_test["Result"],
            "MatchOddsAdj": t20_test["MatchOddsAdj"]
        })

    if i == 1:
       predDF["MatchOddsAdj"] = np.where(predDF["MatchOddsAdj"] == "None", predDF["PredOdds"], predDF['MatchOddsAdj'])
       #predDF["PredOdds"] = np.where(predDF['Overs'] >= 34, predDF['MatchOddsAdj'], predDF["PredOdds"])

    del predDF['MatchOddsAdj']
    preds.append(predDF)

concatPreds = pandas.concat(preds)
concatPreds.to_csv("t20MLPred.csv", index=False)

elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

#alg = LinearRegression()
        #kf = KFold(t20_train.shape[0], n_folds=3, random_state=1)
# predictions = np.concatenate(predictions, axis=0)
    # predictions[predictions >= 0.5] = 1
    # predictions[predictions < 0.5] = 0
    # accuracy = sum(predictions[predictions == t20["Result"]]) / len(predictions)
    # print("Linear Regression: " + `accuracy`)

    # alg = LogisticRegression(random_state=1)
    # scores = cross_validation.cross_val_score(alg, t20_train[predictors], t20_train["Result"], cv=3)
    # print("Logistic Regression: " + `scores.mean()`)
    #
    # #n_estimators is the number of trees we want to make
    # #min_samples_split is the minimum number of rows we need to make a split
    # #min_samples_leaf is the minimum number of samples we can have at the place where a tree branch ends (the bottom points of the tree)
    # alg = RandomForestClassifier(random_state=1, n_estimators=150, min_samples_split=4, min_samples_leaf=2)
    # scores = cross_validation.cross_val_score(alg, t20_train[predictors], t20_train["Result"], cv=3)
    # print("Random Forest 1: " + `scores.mean()`)
    #
    # alg = RandomForestClassifier(random_state=1, n_estimators=250, min_samples_split=4, min_samples_leaf=2)
    # scores = cross_validation.cross_val_score(alg, t20_train[predictors], t20_train["Result"], cv=3)
    # print("Random Forest 2: " + `scores.mean()`)

    # for train, test in kf:
    #     train_predictors = (t20[predictors].iloc[train,:])
    #     train_target = t20_train["Result"].iloc[train]
    #     alg.fit(train_predictors, train_target)
    #     test_predictions = alg.predict(t20_train[predictors].iloc[test,:])
    #     predictions.append(test_predictions)

    #selector = SelectKBest(f_classif, k=7)
    #selector.fit(t20_train[predictors], t20_train["Result"])

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
# kf = KFold(t20.shape[0], n_folds=3, random_state=1)
#
# predictions = []
# for train, test in kf:
#     train_target = t20["Result"].iloc[train]
#     full_test_predictions = []
#     # Make predictions for each algorithm on each fold
#     for alg, predictors in algorithms:
#         # Fit the algorithm on the training data.
#         alg.fit(t20[predictors].iloc[train,:], train_target)
#         # Select and predict on the test fold.
#         # The .astype(float) is necessary to convert the dataframe to all floats and avoid an sklearn error.
#         test_predictions = alg.predict_proba(t20[predictors].iloc[test,:].astype(float))[:,1]
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
# accuracy = sum(predictions[predictions == t20["Result"]]) / len(predictions)
# print("Ensemble: " + `accuracy`)

