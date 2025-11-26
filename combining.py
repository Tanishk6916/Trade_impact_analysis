#%%
import pandas as pd
import numpy as np 
# %%
import numpy as np 
# %%
df1=pd.read_csv('aluminiumrecent.csv')
df1.head()

# %%
df2=pd.read_csv('pharmarecent.csv')
df2.head()

# %%

import pandas as pd
import os

folder_path = r"D:\tradeimpact"
csv_files = [
    "aluminiumrecent.csv",
    "rawhidesrecent.csv",
    "steelrecent.csv",
    "pharmarecent.csv"
]

df_list = []
for file in csv_files:
    full_path = os.path.join(folder_path, file)
    df = pd.read_csv(full_path)
    df['SourceFile'] = file
    df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)

combined_df.to_csv(r"D:\tradeimpact\combined_trade_data.csv", index=False)
print(" CSVs combined successfully!")
print("Total rows in combined file:", len(combined_df))

# %%

