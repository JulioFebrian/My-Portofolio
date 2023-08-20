#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 08:02:18 2021

@author: jolipu
"""

# pwd() --> print working directory
# cd '/Users/jolipu/Downloads' atau kanan atas

# "data.csv"
# "/Users/jolipu/Documents/data.csv"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn; seaborn.set()

import sklearn.linear_model as skl_lm
from sklearn.preprocessing import scale

import statsmodels.api as sm
import statsmodels.formula.api as smf


president_heights = pd.read_csv("president_heights.csv")

help(pd.read_csv)

president_heights.head()
president_heights.tail()
president_heights.max()
president_heights.describe()

# access individual column
president_heights["height(cm)"]
president_heights.name


# slicing data
president_heights["height(cm)"] > 182
president_heights[president_heights["height(cm)"] > 182]
president_heights[(president_heights["height(cm)"] > 182) &  (president_heights["height(cm)"] < 185       ) ]
president_heights[(president_heights["height(cm)"] < 170) | (president_heights["height(cm)"] > 188       ) ]

president_heights.iloc[5:10,:]

president_heights[president_heights.name.str.contains("Thomas|Komar|George")]

# outlier?
# outlier --> Q1 - 1.5 IQR or Q3 + 1.5IQR
Q1 = president_heights["height(cm)"].quantile(0.25)
Q2 = president_heights["height(cm)"].quantile(0.5)
Q3 = president_heights["height(cm)"].quantile(0.75)
IQR = Q3 - Q1
president_heights[president_heights["height(cm)"] > Q3 + 1.5 * IQR]

# missing value
president_heights["height(cm)"][president_heights["height(cm)"] > Q3 + 1.5 * IQR]
president_heights["height(cm)"][president_heights["height(cm)"] > Q3 + 1.5 * IQR] = Q2



Advertising = pd.read_csv("Advertising.csv")
Advertising.describe()
Advertising.corr()
Advertising.iloc[:,1:].corr()

# regression linear model
est = smf.ols("Sales ~ TV + Radio + Newspaper", Advertising).fit()
est.summary()

est2 = smf.ols("Sales ~ TV + Radio", Advertising).fit()
est2.summary()

# Sales = 2.9389 + 0.0458 TV + 0.1885 Radio

# tambahkan data 
Advertising["TV2"] = Advertising.TV ** 2
Advertising["Radio2"] = Advertising.Radio ** 2

est3 = smf.ols("Sales ~ TV + Radio + TV2 + Radio2", Advertising).fit()
est3.summary()



