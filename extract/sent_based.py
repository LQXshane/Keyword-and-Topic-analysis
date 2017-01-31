import re
import pandas as pd
from IPython import embed
from numpy import array

def contain_keyword(df, words):

    # rm = np.logical_or.reduce([df['Contents'].str.contains(word, na=False, case=False) for word in words])
    # rm = []
    result=[]
    w = "[\#\.\-\+\)\!\@\ \_\*\(\[\]\{\}\'\"]"
    for word in words:
        if len(word)==1:
            result.append(word)
            continue
        sp = word.split()
        temp=sp[0]
        for j in range(1,len(sp)):
            temp+=w
            temp+=sp[j]
        # temp=".*"+temp+".*"
        temp = "([^.]*?"+temp+"[^.]*\.)"

        result.append(temp)

        allstring='|'.join(result)

    df2 = pd.DataFrame()
    for i in range(len(df['Contents'])):
        res = re.findall(allstring, df.Contents[i], flags=re.IGNORECASE | re.DOTALL)
        sent = ''

        while res:

            sent = sent + res.pop()[0]

        df2 = df2.append(df[i:i+1], ignore_index = True)
        df2.loc[i, 'Contents'] = sent

    return df2, allstring





df = pd.read_csv('../mmr_media_sample.csv', encoding = 'latin-1')
# embed()
df1 = df[0:10]
# words=['GM mosquito','GMO mosquito',
#                               'genetically modified mosquito',
#                               'genetically engineered mosquito',
#                               'genetically altered mosquito',
#                               'transgenic mosquito',
#                               'GM aedes aegypti',
#                               'GMO aedes aegypti',
#                               'genetically engineered aedes aegypti',
#                               'genetically modified aedes aegypti',
#                               'genetically altered aedes aegypti',
#                               'transgenic aedes aegypti', 'OX513A']
words = ['genetically engineered aedes aegypti']
df2, strs = contain_keyword(df1, words)
df2.to_csv('res1.csv', encoding = 'latin-1', index = False)

embed()


