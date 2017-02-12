import pandas as pd
from IPython import embed
doc = 'res_stage2.csv'

df = pd.read_csv(doc, encoding = 'latin-1')
# embed()
df_res = pd.DataFrame()
for i in range(len(df)):
    # print i
    if type(df.Contents[i]) == float:
        continue
    for content in df.Contents[i].split('.'):
        line = str(content)
        if line  == "":
            continue
        df_res = df_res.append(df.loc[i], ignore_index=True)
        df_res.loc[i, 'Contents'] = line
        del line
df_res = df_res[df.columns]

df_res.to_csv('res_stage2_split.csv', encoding='latin-1', index=False)

