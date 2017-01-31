from re import finditer, findall
import re
from itertools import tee, islice, izip, chain, repeat

def extract_context(strs, target):
    spl = strs.split()
    for ind,x in enumerate(spl):
       if x.strip(",'.!")==target or x.strip(',".!')==target:
           break
    print(" ".join(spl[ind-20:ind]+spl[ind:ind+20]))



def kwic(text, tgtword, width=10):
    'Find all occurrences of tgtword and show the surrounding context'
    # res = []
    # w = "[\#\.\-\+\)\!\@\ \_\*\(\[\]\{\}\'\"]*"
    # for word in tgtword:
    #     if len(word) == 1:
    #         res.append(word)
    #         continue
    #     spl = word.split()
    #
    #     tmp = spl[0]
    #     for j in range(1, len(spl)):
    #         tmp += w
    #         tmp += spl[j]
    #
    #     tmp = "([^.]*?" + tmp + "[^.]*\.)"
    #     res.append(tmp)
    #
    # allstr = '|'.join(res)
    # matches = (mo.span() for mo in finditer(allstr, text, flags=re.DOTALL|re.IGNORECASE))
    matches = (mo.span() for mo in finditer(r".*[A-Za-z\#\.\-\+\)\!\@\ \_\*\(\[\]\{\}\'\"].*", text))
    padded = chain(repeat((0,0), width), matches, repeat((-1,-1), width))
    t1, t2, t3 = tee((padded), 3)
    t2 = islice(t2, width, None)
    t3 = islice(t3, 2*width, None)
    for (start, _), (i, j), (_, stop) in izip(t1, t2, t3):
        if text[i: j] == tgtword:
        # if re.match(allstr, text[i: j], flags = re.DOTALL):
            context = text[start: stop]
            yield context

# print list(kwic(text, 'Snow-White'))
ans = list(kwic(txt, 'Genetically modified Aedes aegypti'))