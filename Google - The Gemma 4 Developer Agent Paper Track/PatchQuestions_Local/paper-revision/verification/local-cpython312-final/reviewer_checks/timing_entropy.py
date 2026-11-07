"""Offline, executable API-contract recovery benchmark. Python >=3.11."""
import base64, binascii, csv, fnmatch, hashlib, io, itertools, json, math, random, re
import statistics, textwrap
from collections import Counter, defaultdict
from functools import lru_cache
from urllib.parse import parse_qsl, quote, quote_plus
from pathlib import Path

def product(*axes):
    return list(itertools.product(*axes))

def outcome(f, config, x):
    try:
        return json.dumps(["return", f(config,x)], ensure_ascii=True, sort_keys=True, allow_nan=False)
    except (ValueError, csv.Error, UnicodeError, binascii.Error) as exc:
        return json.dumps(["raise",type(exc).__name__])

def families():
    # Each row contains candidate configurations, one smoke input, finite universe, implementation.
    return {
        "url_quote": (product([0,1],["","/","/:","@","/@"],["strict","replace"]), "cat",
            [a+b for a,b in product(["hi","a b","/x","@",":","\ud800"],[""," b","/x","@y",":z","é","+"])],
            lambda c,x:(quote,quote_plus)[c[0]](x,safe=c[1],errors=c[2])),
        "query_pairs": (product([False,True],[False,True],["&",";"],["latin1","utf8"]), "a=1",
            [a+b for a,b in product(["a=1","b=","bare","x=%C3%A9","x=%FF",""],["","&q",";b=",";x=%FF","&b=2","+%2B"])],
            lambda c,x:parse_qsl(x,keep_blank_values=c[0],strict_parsing=c[1],separator=c[2],encoding=c[3])),
        "csv_fields": (product([",",";","\t"],[False,True],[False,True],[None,"\\"]), "x",
            [a+d+b for a,d,b in product(['x','"a"','"a""b"','a\\'],[',',';','\t'],[' y','"x','z','\\q'])],
            lambda c,x:list(csv.reader([x],delimiter=c[0],skipinitialspace=c[1],strict=c[2],escapechar=c[3]))),
        "wrap": (product([6,9],[False,True],[False,True],[False,True]), "hi",
            [a+s+b for a,s,b in product(["ab","abcdefgh","a-bcd","abcde"],[" ","  ","-","\t"],["z","efghijk","abc-def"])],
            lambda c,x:textwrap.wrap(x,width=c[0],break_long_words=c[1],break_on_hyphens=c[2],drop_whitespace=c[3])),
        "json_wire": (product([False,True],[False,True],[False,True],[False,True]), "1",
            [json.dumps({a:v,"a":w},ensure_ascii=False) for a,v,w in product(["z","é","B"],["é",[1,2],0],["x",["雪"],{}])] + ['[]','{}','"é"','[1, 2]'],
            lambda c,x:json.dumps(json.loads(x),ensure_ascii=c[0],sort_keys=c[1],separators=((',' if c[2] else ', '),(':' if c[3] else ': ')))),
        "regex_search": (product([0,re.I],[0,re.M],[0,re.S],[0,re.A]), "a|a",
            [p+'|'+s for p,s in product(["a","^b","a.b",r"\w+",r"\d+","[a-z]+","^a.b"],["A","a\nb","x\nb","é","９","aXb","K","!x"])],
            lambda c,x:[m.span() for m in re.finditer(x.split('|')[0],x.split('|')[1],flags=int(c[0]|c[1]|c[2]|c[3]))]),
        "base64_read": (product([None,b'-_',b'._'],[False,True]), "YQ==",
            [a+b for a,b in product(["AA","-_","._","+/","a!","//","ab","YWJj"],["==","/w==","\n==","!","_w==","", "==x"])],
            lambda c,x:base64.b64decode(x,altchars=c[0],validate=c[1]).hex()),
        "hex_format": (product([":","-"," "],[-3,-2,-1,1,2,3],[False,True]), "",
            [bytes((v+i)%256 for i in range(k)).hex() for k,v in product(range(1,12),[0,10,120,230])],
            lambda c,x:bytes.fromhex(x).hex(c[0],c[1]).upper() if c[2] else bytes.fromhex(x).hex(c[0],c[1]))
    }

def signature(row, cols):
    return tuple(row[j] for j in cols)

def evaluate(name, spec, seed, replacements=(), transfer_inputs=None):
    configs, smoke, inputs, f=spec
    inputs=sorted(set(inputs)-{smoke})
    random.Random(seed).shuffle(inputs)
    probes,hold=inputs[:min(16,len(inputs)//2)],inputs[min(16,len(inputs)//2):]
    if replacements:
        assert len(set(replacements)) == len(replacements)
        assert not set(replacements).intersection(inputs+[smoke])
        probes=probes[:-len(replacements)]+list(replacements)
    if transfer_inputs is not None:
        assert not set(transfer_inputs).intersection(probes+[smoke])
        hold=list(transfer_inputs)
    smokevals=[outcome(f,c,smoke) for c in configs]
    query=[tuple(outcome(f,c,x) for x in probes) for c in configs]
    hidden=[tuple(outcome(f,c,x) for x in hold) for c in configs]
    @lru_cache(None)
    def partition(ids,j):
        bins=defaultdict(list)
        for i in ids: bins[query[i][j]].append(i)
        return tuple(tuple(v) for v in bins.values())
    @lru_cache(None)
    def tree(ids,depth,frugal):
        # Maximize leaf count, optionally breaking ties by total path length over targets.
        best=(1,0,None)
        if depth==0: return best
        for j in range(len(probes)):
            parts=partition(ids,j)
            if len(parts)<2: continue
            children=[tree(p,depth-1,frugal) for p in parts]
            leaves=sum(child[0] for child in children)
            cost=len(ids)+sum(child[1] for child in children)
            if leaves>best[0] or (frugal and leaves==best[0] and cost<best[1]):
                best=(leaves,cost,j)
        return best
    methods=['entropy']
    rows=[]
    for target in range(len(configs)):
        initial=tuple(i for i in range(len(configs)) if smokevals[i]==smokevals[target])

        @lru_cache(None)
        def score_state(ids, available, depth, method):
            if depth:
                if method=='random':
                    choices=available
                else:
                    informative=tuple(j for j in available if len(partition(ids,j))>1)
                    if method=='random_split':
                        choices=informative
                    elif method in ('lookahead','frugal'):
                        _,_,j=tree(ids,depth,method=='frugal')
                        choices=() if j is None else (j,)
                    else:
                        def utility(j):
                            sizes=[len(p) for p in partition(ids,j)]
                            if method=='diversity':
                                return len(sizes)
                            return -sum(n*math.log2(n) for n in sizes)
                        choices=(max(informative,key=utility),) if informative else ()
                if choices:
                    results=[]
                    for j in choices:
                        survivors=next(p for p in partition(ids,j) if target in p)
                        remaining=tuple(k for k in available if k!=j)
                        results.append(score_state(survivors,remaining,depth-1,method))
                    held,probe,count,used=map(statistics.fmean,zip(*results))
                    return held,probe,count,used+1
            return (sum(hidden[i]==hidden[target] for i in ids)/len(ids),
                    sum(query[i]==query[target] for i in ids)/len(ids),len(ids),0)
        for method in methods:
            for budget in [3]:
                metrics=score_state(initial,tuple(range(len(probes))),budget,method)
                rows.append([name,seed,target,method,budget,*metrics])
        score_state.cache_clear()
    tree.cache_clear(); partition.cache_clear()
    return rows

def run():
    rows=[]
    for name,spec in families().items():
        for seed in [19,43,73,101,137]:
            rows.extend(evaluate(name,spec,seed))
    return rows

def summarize(rows):
    grouped=defaultdict(list)
    for family,seed,target,method,budget,held,probe,n,used in rows:
        grouped[family,method,budget].append(held)
    means={k:statistics.mean(v) for k,v in grouped.items()}
    return {m:{b:statistics.mean(means[f,m,b] for f in families()) for b in [0,1,2,3]}
            for m in ['random','random_split','diversity','entropy','lookahead','frugal']},means

if __name__=='__main__':
    rows=run()
    with open('scores.csv','w',newline='') as out:
        w=csv.writer(out);w.writerow(['family','split','target','policy','budget','heldout_exact','probe_exact','survivors','queries_used']);w.writerows(rows)
    print(json.dumps(summarize(rows)[0],indent=2))
