#%%
import numpy as np 
# %%
import pandas as pd
# %%
df=pd.read_csv('combined_trade_data.csv')
print(df)

# %%
print('Information about the DS:')
df.info()
# %%
print('Description of the DS:')
df.describe()

# %% yearly exports 
yearly_exports= df.groupby('refPeriodId')['fobvalue'].sum()
# %% yearly imports 
yearly_imports = df.groupby('refPeriodId')['cifvalue'].sum()
# %%
import matplotlib.pyplot as plt
# %%
plt.figure(figsize=(10,6))
plt.plot(yearly_exports,label='exports')
plt.plot(yearly_imports,label='Imports')
plt.title('yearly trade metrics')
plt.xlabel('trade year')
plt.ylabel('trade value')
plt.show






# %%
df.head(50)
# %%
yearly_exports_industrywise= df.groupby(['refPeriodId','SourceFile'])['fobvalue'].sum().reset_index()
yearly_imports_industrywise= df.groupby(['refPeriodId','SourceFile'])['cifvalue'].sum().reset_index()


# %% yearly exports for every industry 
for industry in yearly_exports_industrywise['SourceFile'].unique():
    data1= yearly_exports_industrywise[yearly_exports_industrywise['SourceFile']==industry]
    plt.plot(data1['refPeriodId'],data1['fobvalue'],label=industry)


plt.title('Yearly Exports by Industry', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Export Value (FOB)', fontsize=12)
plt.legend(title='Industry', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()    





# %% for yealry imports 
for industry in yearly_imports_industrywise['SourceFile'].unique():
    data2=yearly_imports_industrywise[yearly_imports_industrywise['SourceFile']==industry]
    plt.plot(data2['refPeriodId'],data2['cifvalue'],label=industry)



plt.title('Yearly Imports by Industry', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Imports Value (FOB)', fontsize=12)
plt.legend(title='Industry', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()    




# %%
df.head(100)

# %%
# CAGR function already defined
def CAGR(series):
    n = len(series) - 1  # number of years - 1
    return (series.iloc[-1] / series.iloc[0])**(1/n) - 1

# Apply CAGR per industry using yearly_exports_industrywise
cagr = yearly_exports_industrywise.groupby('SourceFile')['fobvalue'].apply(CAGR).reset_index()
cagr.columns = ['SourceFile', 'CAGR']

print(cagr)

# %%
# %% Top and Bottom industries based on CAGR
top_export_industries = cagr.sort_values(by='CAGR', ascending=False).head(5)


print("Top 5 Export Industries by CAGR:")
print(top_export_industries)




# %% Export/Import ratio per industry
# First, calculate total export and import per industry
total_exports = df.groupby('SourceFile')['fobvalue'].sum()
total_imports = df.groupby('SourceFile')['cifvalue'].sum()

trade_ratio = (total_exports / total_imports).reset_index()
trade_ratio.columns = ['SourceFile', 'Export_to_Import_Ratio']

print("\nExport to Import Ratio per Industry:")
print(trade_ratio.sort_values(by='Export_to_Import_Ratio', ascending=False))


# %%  Merge CAGR and Trade Ratio for combined insight
industry_insights = pd.merge(cagr, trade_ratio, on='SourceFile')
industry_insights['Trade_Status'] = industry_insights['Export_to_Import_Ratio'].apply(
    lambda x: 'Export Surplus' if x > 1 else 'Import Dependent'
)

print("\nCombined Industry Insights:")
print(industry_insights.sort_values(by='CAGR', ascending=False))


# %%
#%% Prediction after 75% tariff impact
import pandas as pd

# Last year export per industry (2024)
last_exports = yearly_exports_industrywise[yearly_exports_industrywise['refPeriodId'] == yearly_exports_industrywise['refPeriodId'].max()]
last_exports = last_exports.set_index('SourceFile')['fobvalue']

# Create prediction dataframe
years = [2025, 2026, 2027]
predictions = pd.DataFrame(index=cagr['SourceFile'], columns=years)

# Apply CAGR with 75% growth reduction
for industry in cagr['SourceFile']:
    last_value = last_exports[industry]
    industry_cagr = cagr[cagr['SourceFile'] == industry]['CAGR'].values[0]
    adjusted_cagr = industry_cagr * (1 - 0.75)  # 75% impact
    for i, year in enumerate(years, start=1):
        predictions.loc[industry, year] = last_value * (1 + adjusted_cagr)**i

# Round for readability
predictions = predictions.round(2)
print("Predicted Exports (2025-2027) after 75% tariff impact:")
print(predictions)


# %%
#%% Plotting pre-tariff vs post-tariff predictions
import matplotlib.pyplot as plt

years = [2025, 2026, 2027]

# Last exports per industry
last_exports = {'Industry1':1000,'Industry2':500,'Industry3':1200}
# CAGR per industry
cagr = {'Industry1':0.05,'Industry2':0.08,'Industry3':0.03}

# Predictions
pre_tariff = {ind:[last_exports[ind]*(1+cagr[ind])**i for i in range(1,4)] for ind in last_exports}
post_tariff = {ind:[v*0.25 for v in pre_tariff[ind]] for ind in last_exports}

# Plot
plt.figure(figsize=(10,5))
for ind in last_exports:
    plt.plot(years, pre_tariff[ind], '--o', label=f'{ind} pre-tariff')
    plt.plot(years, post_tariff[ind], '-o', label=f'{ind} post-tariff')
plt.title('Exports Prediction')
plt.xlabel('Year'); plt.ylabel('Export Value'); plt.grid(alpha=0.3)
plt.legend(); plt.show()

# %%

