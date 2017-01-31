from IPython import embed
import re
import pandas as pd
from numpy import array


def contain_keyword(input, word_list, path_to_file):

    df = pd.read_csv(input, encoding = 'latin-1', )

    # cascading keywords with regex
    result = []
    w = "[\#\.\-\+\)\!\@\ \_\*\(\[\]\{\}" + "\'" + '\"]*'
    for word in word_list:
        if len(word) == 1:
            result.append(word)
            continue

        spl = word.split()

        tmp = spl[0]
        for j in range(1, len(spl)):

            tmp += w
            tmp += spl[j]

        tmp = "([^.]*?" + tmp + "[^.]*\.)"
        result.append(tmp)

    allstr = '|'.join(result)

    # df = df[0:10]

    df_res = pd.DataFrame()

    for i in range(len(df)):

        res = re.findall(allstr, df.Contents[i], flags=re.IGNORECASE|re.DOTALL)
        content = []
        for x in res:
            for y in x:
                if y:
                    content.append(y)
        # contents = ''.join(str(x) for x in content)
        newcontent=""

        for x in content:
            try:
                newcontent += str(x)
            except Exception:
                print "Encoding error"
                continue


        df_res = df_res.append(df.loc[i], ignore_index=True)
        df_res.loc[i, 'Contents'] = newcontent
        del content, newcontent
    df_res = df_res[df.columns]
    # rm = [df_res.Contents != '']
    # df_res = df_res[rm]

    df_res.to_csv(path_to_file, encoding='latin-1', index=False)

    return df_res, allstr


words=['GM mosquito','GMO mosquito',
                              'genetically modified mosquito',
                              'genetically engineered mosquito',
                              'genetically altered mosquito',
                              'transgenic mosquito',
                              'GM aedes aegypti',
                              'GMO aedes aegypti',
                              'genetically engineered aedes aegypti',
                              'genetically modified aedes aegypti',
                              'genetically altered aedes aegypti',
                              'transgenic aedes aegypti', 'OX513A']
df_res, _ = contain_keyword('mmr_media_sample.csv', words, 'extract/res1.csv')
rows = 0
for x in df_res.Contents:
    if x != '':
        rows += 1
print "%d of rows returned." %(rows)

embed()