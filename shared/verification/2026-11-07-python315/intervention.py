"""Post-hoc regex probe-design intervention. All arms share identical hidden inputs."""
import json
from benchmark import evaluate, families
from statistics import fmean
single=['q|Q','^q|p\nq','q.z|q\nz',r'\w|Ж']
compound=['^q.\\w|q0a\nQ0b\nq\nЖ\nq0é\nQ\nz','^q.\\w|Q0Ж\nq\nx\nq0b',
          '^q.\\w|q\nЖ\nQ0b\nq1Ж','^q.\\w|Q0b\nq\ny\nq1Ж']
def transfer_suite():
    # Separate vocabulary, strings and patterns; fixed after the diagnostic analysis.
    return [p+'|'+s for p in [r"^r.\w",r"r.\d","^r","r.t",r"\w+",r"\d+"]
            for s in ["R1Ж","r\nЖ","u\nr0a","Ｒ","r0۷","r\nt","!R0z","r0x\nR1Ж"]]

def study(transfer=False):
    out={}
    for label,probes in [('original',[]),('single',single),('compound',compound)]:
        rows=[r for seed in [19,43,73,101,137] for r in evaluate('regex_search',families()['regex_search'],seed,probes,transfer_suite() if transfer else None)]
        out[label]={b:fmean(r[5] for r in rows if r[3]=='frugal' and r[4]==b) for b in (1,2,3)}
    return out
if __name__=='__main__':
    print(json.dumps({"original_holdout":study(),"transfer":study(True)},indent=2))
