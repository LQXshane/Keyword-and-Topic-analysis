# -*- coding: latin-1 -*-
import pandas as pd
import sys
import numpy as np
from IPython import embed
import re

def contain_keyword(df, words):

    # rm = np.logical_or.reduce([df['Contents'].str.contains(word, na=False, case=False) for word in words])
    rm = []
    result=[]
    w = "[\#\.\-\+\)\!\@\ \_\*\(\[\]\{\}"+"\'"+'\"]*'
    for word in words:
        if len(word)==1:
            result.append(word)
            continue
        sp = word.split()
        temp=sp[0]
        for j in range(1,len(sp)):
            temp+=w
            temp+=sp[j]
        temp=".*"+temp+".*"
        # temp = "([^.]*?"+temp+"[^.]*\.)"

        result.append(temp)

        allstring='|'.join(result)
# ([^.]*?apple[^.]*\.)

    for i in range(len(df['Contents'])):
        if re.match(allstring, df.Contents[i], flags=re.IGNORECASE  | re.DOTALL):
            rm.append(True)
        else:
            rm.append(False)
    return df[rm], rm, allstring






if __name__ == '__main__':

    df = pd.read_csv(sys.argv[1], encoding='latin-1')
    # df_tran = contain_keyword(df, "GM mosquito",
    #             "GMO mosquito",
    #             "genetically modified mosquito",
    #             "genetically engineered mosquito",
    #             "GMO aedes aegypti",
    #             "genetically engineered aedes aegypti",
    #             "genetically modified aedes aegypti")

    df_tran, tf, strs = contain_keyword(df, ["GM mosquito", "GMO mosquito", #"\(GMO\) mosquito",
                                 #"\(GM\) mosquito", "#GM", "#Mosquito", "#GMO", "G.M. Mosquito", "GM-mosquito", "GMO-mosquito", "G.M.O. Mosquito",
                              "genetically modified mosquito",
                                           #"genetically-modified mosquito",
                              "genetically engineered mosquito",
                                           # "genetically-engineered mosquito",
                              "genetically altered mosquito",
                                          # "genetically-altered mosquito",
                              "transgenic mosquito",
                                       # "transgenic-mosquito",
                              "GM aedes aegypti",# "\(GM\) aedes aegypti",
                              "GMO aedes aegypti", #"\(GMO\) aedes aegypti",
                              "genetically engineered aedes aegypti",
                                           #"genetically-engineered aedes aegypti",
                              "genetically modified aedes aegypti",
                                           #"genetically-modified aedes aegypti",
                              "genetically altered aedes aegypti",
                                           #"genetically-altered aedes aegypti",
                              "transgenic aedes aegypti", "OX513A"]) # updated keywords: 13


    embed()

    df_tran.to_csv(sys.argv[2], index = False, encoding='latin-1')

    embed()
