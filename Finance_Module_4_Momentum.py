
# coding: utf-8

# In[103]:


# -*- coding: utf-8 -*-
"""
Author: Michael Wentz
Class: Finance 7023
Module 4
4/5/2018
"""
import pandas as pd

import numpy as np

import math 

import matplotlib.pyplot as plt

file = "Return Data.xlsx"

# Load Spreadsheet
xl = pd.ExcelFile(file)

# Print the sheet names
print(xl.sheet_names)


# In[104]:


# Load a sheet into a DataFrame by name: df1
df1 = xl.parse("Return Data")
df1.head
df1.info()

df1.set_index("Date", inplace=True)
df1.head()


# In[105]:


# gets 12 month rolling average return
df2 = df1
df2 = df2.rolling(window=12, min_periods=12).mean()
df3 = df2
df3


# In[106]:


# Shifts rolling average down one month to make it the previous
# 12 months average
df3 = df3.shift(periods=1)
df3


# In[107]:


#Removes non-industry columns
df3.drop(columns=["Mkt-RF", "SMB", "HML", "RF"], inplace=True)
df3.head()


# In[108]:


#removes first 12 blank months
df3 = df3[12:]
df3


# In[109]:


#rank industry return by month, hihger number means better return
df4 = df3.rank(axis=1)
ind_rank = df3.rank(axis=1)
df4


# In[110]:


# Compute Industry average ranks
df5 = df4.mean()
print(df5.sort_values(ascending=False))


# In[111]:


#Gets dataframe of Autos vs. Date
df6 = df4.T
df6 = df6[14:15]
df6 = df6.T
df6


# In[112]:


#Plot Autos Rank vs. Time
ax = df6.plot(kind="line", legend=False, color="lightblue", figsize=(16,12), alpha=0.7)
ax.set_ylabel("Autos")


# In[113]:


df4


# In[114]:


# Get winners (rank >= 16)
winners = df4
winners[winners < 16] = 0
winners = winners.replace(0, np.NaN)
winners


# In[115]:


#Get winners return
winners[winners > 0] = 1
winners_id = winners
winners = winners*df1
winners = winners[12:]
winners.head()


# In[116]:


# get avg winners return by month
winnersavg = winners.mean(axis= 1)
winnersavg


# In[117]:


# get winners avg. excess return by month
winnerex = winnersavg
rf = df1[12:]
rf = rf["RF"]
winnerex = winnerex - rf


# In[118]:


#winner summary Statistics
winnerex.describe()


# In[119]:


#monthly sharpe ratio
winnerex_sharpeM = winnerex.mean()/winnerex.std()
print(winnerex_sharpeM)


# In[120]:


#annual sharpe ratio
winnerex_sharpeA = winnerex_sharpeM*math.sqrt(12)
winnerex_sharpeA


# In[121]:


#Repeat for losers but modify winners 0/1 dataframe
losers = winners_id
print(losers)
losers = losers.replace(np.NaN, 2)
losers = losers.replace(1, np.NaN)
losers = losers.replace(2, 1)
print(losers)
#Get winners return
losers[losers > 0] = 1
losers = losers*df1
losers = losers[12:]
print(losers)
losersavg = losers.mean(axis= 1)
print(losersavg)
loserex = losersavg
loserex = loserex - rf
print(loserex)
loserex.describe()


# In[122]:


#monthly sharpe ratio
loserex_sharpeM = loserex.mean()/loserex.std()
loserex_sharpeM


# In[123]:


#annual sharpe ratio
loserex_sharpeA = loserex_sharpeM*math.sqrt(12)
loserex_sharpeA


# In[124]:


#Compute long winner & short loser each month
ind_mom = winnerex - loserex
ind_mom = pd.DataFrame(ind_mom, columns=["ind-mom"])
print(ind_mom)
ind_mom.describe()


# In[125]:


#ind_mom sharpe ratio
ind_momsharpeA = (ind_mom.mean()/ind_mom.std())*math.sqrt(12)
ind_momsharpeA


# In[126]:


#Create excess market data frame & 3 Fama Factor Dataframe
market_ex = df1[12:]
market_ex = market_ex["Mkt-RF"]
print(market_ex)
Fama3 = df1[12:]
print(Fama3)
Fama3.drop(Fama3.columns[0:30], axis=1, inplace=True)
Fama3.drop("RF", axis=1, inplace=True)
print(Fama3)


# In[127]:


#Regression on to Excess Market Return
import statsmodels.api as sm

# Set dependent variable
y = ind_mom

# Set independent variable and add a constant variable
x = market_ex
x = sm.add_constant(x)

# Run regression
CAPM_Model = sm.OLS(y, x).fit()
print(CAPM_Model.summary())


# In[128]:


#Regression on to 3 Fama - French Factors
# Set dependent variable
y = ind_mom

# Set independent variable and add a constant variable
x = Fama3
x = sm.add_constant(x)

# Run regression
FAMA3_Model = sm.OLS(y, x).fit()
print(FAMA3_Model.summary())


# In[129]:


#Compute cumulative return of winners, losers, ind_mom, and the market
winnersC = np.cumsum(winnerex + rf)
print(winnersC)
losersC = np.cumsum(loserex + rf)
ind_momC = np.cumsum(ind_mom)
marketC = np.cumsum(market_ex + rf)
plt.Figure(figsize= (15,20))
plt.plot(winnersC, label= "Winners")
plt.plot(losersC, label= "Losers")
plt.plot(ind_momC, label= "Industry Momentum")
plt.plot(marketC, label= "Market")
plt.grid(True)
plt.legend(loc=0)
plt.axis("tight")
plt.xlabel("Time (YYYYMM)")
plt.ylabel("Cumulative Return")


# In[130]:


#Plot log cumulative return of winners, losers, ind_mom, and the market
winnersC = np.cumsum(winnerex + rf)
print(winnersC)
losersC = np.cumsum(loserex + rf)
ind_momC = np.cumsum(ind_mom)
marketC = np.cumsum(market_ex + rf)
plt.Figure(figsize= (15,20))
plt.semilogy(winnersC, label= "Winners")
plt.semilogy(losersC, label= "Losers")
plt.semilogy(ind_momC, label= "Industry Momentum")
plt.semilogy(marketC, label= "Market")
plt.grid(True)
plt.legend(loc=0)
plt.axis("tight")
plt.xlabel("Time (YYYYMM)")
plt.ylabel("Cumulative Return")

