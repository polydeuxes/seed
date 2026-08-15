"""Does homogeneity revision the hierarchical-pointer curve?

Supplied testimony: eight heterogeneous books gave marginal 68 KB -> 44 KB and
flattening. A real library is not heterogeneous. Two arms bracket it:

  same-work    consecutive chunks of ONE book — the upper bound on homogeneity
  same-kind    chunks of different English prose works — the realistic case
"""
import glob, os, collections, sys

def repair(symbols, min_count=2, max_rounds=40):
    rules={}; nxt=256
    for _ in range(max_rounds):
        pairs=collections.Counter(); i=0; prev=None
        while i < len(symbols)-1:
            p=(symbols[i],symbols[i+1])
            if p==prev: prev=None; i+=1; continue
            pairs[p]+=1; prev=p; i+=1
        chosen={p for p,c in pairs.items() if c>=min_count}
        if not chosen: break
        assigned={}; out=[]; i=0
        while i < len(symbols):
            if i < len(symbols)-1 and (symbols[i],symbols[i+1]) in chosen:
                p=(symbols[i],symbols[i+1])
                if p not in assigned: assigned[p]=nxt; rules[nxt]=p; nxt+=1
                out.append(assigned[p]); i+=2
            else: out.append(symbols[i]); i+=1
        if len(out)==len(symbols): break
        symbols=out
    return symbols, rules

def span(s, rules, memo):
    if s < 256: return 1
    if s in memo: return memo[s]
    a,b=rules[s]; memo[s]=span(a,rules,memo)+span(b,rules,memo); return memo[s]

CHUNK=50_000
def run(label, bodies):
    print(f"\n  {label}\n")
    print(f"  {'bodies':>7}{'material':>11}{'rules':>9}{'account':>11}{'mean span':>11}{'references/MB':>14}{'marginal':>11}")
    prev=0
    for n in range(1,len(bodies)+1):
        data=b"".join(bodies[:n])
        seq, rules = repair(list(data))
        memo={}
        mean=sum(span(s,rules,memo) for s in seq)/len(seq)
        account=len(seq)*3+len(rules)*6
        refs_per_mb=len(seq)/(len(data)/1e6)
        print(f"  {n:>7}{len(data):>11,}{len(rules):>9,}{account:>11,}{mean:>11.1f}{refs_per_mb:>11,.0f}{account-prev:>11,}")
        prev=account

src=open("/home/user/seed/corpus/prose_dickens_copperfield.txt","rb").read()
same_work=[src[3000+i*CHUNK:3000+(i+1)*CHUNK] for i in range(8)]
run("SAME WORK — eight consecutive chunks of one book", same_work)

names=["prose_austen_pride","prose_dickens_copperfield","prose_emerson_essays","prose_hume_enquiry",
       "prose_franklin_autobiog","english_grimm_fairy_tales","bible_kjv","fiction_alice"]
same_kind=[]
for nm in names:
    m=[f for f in glob.glob("/home/user/seed/corpus/*") if os.path.basename(f).startswith(nm)]
    if m: same_kind.append(open(m[0],"rb").read()[3000:3000+CHUNK])
run(f"SAME KIND — {len(same_kind)} English prose works", same_kind)
