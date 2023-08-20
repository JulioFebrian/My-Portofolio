#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 08:07:55 2021

@author: jolipu
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

df = pd.read_csv("Boston.csv", usecols=range(1,15))
df.info()
df.describe()
df.head()

# Model regresi 
# tipe numerical/continuous/quantitative dan 
# tipe categorical/qualitative
# X: quantitative, Y: quantitative --> linear regression
# X: qualitative, Y: quantitative --> linear regression + dummy binary variable
# X: quantitative, Y: qualitative --> logistic regression

#check correlation
correlation = df.corr()
# for checking whether multi-collinearity?

# model Boston
# Y: medv
est = smf.ols("medv ~ rm + lstat", df).fit()
est.summary()
# Persamaan regresi linear: medv =  -1.3583 + 5.0948 * rm -0.6424 * lstat
# the resulted model can be used for prediction
new = pd.DataFrame([ [0,0], [1,0], [0,1], [ 6.575, 4.98] ], columns =[ "rm", "lstat"])
est.predict(new)

est2 = smf.ols("medv ~ rm + lstat + ptratio + indus + tax", df).fit()
est2.summary()

est3 = smf.ols("medv ~ rm + lstat + ptratio ", df).fit()
est3.summary()

# ANOVA : check model_1 vs model_2 vs model_3
sm.stats.anova_lm(est, est2, est3)
sm.stats.anova_lm(est2, est3)

est4 = smf.ols("medv ~ rm + lstat + ptratio + rm * lstat + rm * ptratio + lstat*ptratio", df).fit()
est4.summary()


# another way to compare model --> bias?
# split data --> train_data + test_data
# random_state --> seed random number
train_data = df.sample(253, random_state = 1)
test_data = df[~df.isin(train_data)].dropna(how='all')

# build model using test_data
est1 = smf.ols("medv ~ rm + lstat", train_data).fit()
est2 = smf.ols("medv ~ rm + lstat + ptratio + indus + tax", train_data).fit()
est3 = smf.ols("medv ~ rm + lstat + ptratio ", train_data).fit()
est4 = smf.ols("medv ~ rm + lstat + ptratio + rm * lstat + rm * ptratio + lstat*ptratio  ", train_data).fit()

# calculate prediction using train_data
pred1 = est1.predict(test_data)
pred2 = est2.predict(test_data)
pred3 = est3.predict(test_data)
pred4 = est4.predict(test_data)

# MAPE, MSE, MAD --> check error pakek MSE
error1 = np.mean(np.square(np.subtract(pred1, test_data["medv"])))
error2 = np.mean(np.square(np.subtract(pred2, test_data["medv"])))
error3 = np.mean(np.square(np.subtract(pred3, test_data["medv"])))
error4 = np.mean(np.square(np.subtract(pred4, test_data["medv"])))


# qualitative predictor
est5 = smf.ols("medv ~ chas + rm + lstat + ptratio + rm * lstat + rm * ptratio + lstat*ptratio  ", df).fit()
est5.summary()
# masih dianggap numerical/quantitative --> kita ubah dulu menjadi categorical
df["chas"] = df["chas"].astype("category")
est5 = smf.ols("medv ~ chas + rm + lstat + ptratio + rm * lstat + rm * ptratio + lstat*ptratio  ", df).fit()
est5.summary()

#categorical independent variables
df2 = pd.read_csv("Carseats.csv")
df2.head()
est3 = sm.OLS.from_formula(" Sales ~ ShelveLoc + Price ", df2).fit()
est3.summary()

# Sales = 12.0018 + 4.8958 * ShelveLoc[T.Good] +  1.8620 * ShelveLoc[T.Medium] -0.0567 * Price



# qualitative response variable --> logistic regression
df4 = pd.read_csv("Smarket.csv", usecols=range(1,10), index_col=0  )
# glm --> generalized linear model
est4 = sm.GLM.from_formula(formula="Direction ~ Lag1 + Lag2 + Lag3 + Lag4 + Lag5 + Volume", data=df4, family=sm.families.Binomial()).fit()
est4.summary()
# result:
# probability (Direction = Up) = 1 / ( 1 + exp(-( 0.126 + 0.0731 * Lag1 + ... + -0.1354 * Volume     )))







