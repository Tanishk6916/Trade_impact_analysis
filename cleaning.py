#%%
import pandas as pd 
# %%
import numpy as np 
# %%
df=pd.read_csv('combined_trade_data.csv')
df.head()
# %%
df.isnull().sum()

# %%
print(df['isAggregate'].head(10))
# %%
df.head()

# %% filling the nan values of 'isaggregate'
df['isAggregate']=df['isAggregate'].fillna(0)

# %%
df.isnull().sum()
# %%

