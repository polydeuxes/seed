import sys, os, time, cProfile, pstats, io as _io, collections
sys.path.insert(0,"/home/user/seed-visitor")
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.event import Event
from seed_runtime.ids import new_id
from seed_runtime.preserved_material_measurement import record_measurement_findings, INGRESS_OCCURRED_KIND
from seed_runtime.adjacent_pair_measurement import measure_at_displacement, record_adjacent_pair_measurement_layer, _positions
DB="/dev/shm/lab/prof.db"
if os.path.exists(DB): os.remove(DB)
led=SQLiteEventLedger(DB); W="local"; S="b"
lines=[l for l in open("/home/user/seed/corpus/prose_austen_pride.txt",encoding="utf-8").read().split("\n")[3000:] if l.strip()][:700]
batch=[Event(id=new_id("evt"),kind=INGRESS_OCCURRED_KIND,workspace_id=W,session_id=S,
             payload={"decoded_text":l,"material_origin":"operator","text_representation":{"available":True}}) for l in lines]
for i in range(0,len(batch),500): led.append_many(batch[i:i+500])
occ=[e for e in led.list(W) if e.kind==INGRESS_OCCURRED_KIND]
reps=sorted({p for e in occ for p in _positions(e.payload["decoded_text"])})
print(f"  {len(lines)} lines, {len(reps)} representations")

pr=cProfile.Profile(); pr.enable(); t=time.perf_counter()
b=[]
for r in reps:
    b.append((measure_at_displacement(occ, r, displacement=1, counting_scope="s"), None))
    if len(b)==500: record_measurement_findings(led, workspace_id=W, session_id=S, findings=b); b=[]
if b: record_measurement_findings(led, workspace_id=W, session_id=S, findings=b)
s1=time.perf_counter()-t; pr.disable()
s=_io.StringIO(); pstats.Stats(pr,stream=s).sort_stats("cumulative").print_stats(9)
print(f"\n  STAGE 1  {s1:.1f}s"); print("\n".join(s.getvalue().splitlines()[4:15]))

pr=cProfile.Profile(); pr.enable(); t=time.perf_counter()
k=record_adjacent_pair_measurement_layer(led, workspace_id=W, session_id=S, counting_scope="s")
s2=time.perf_counter()-t; pr.disable()
s=_io.StringIO(); pstats.Stats(pr,stream=s).sort_stats("cumulative").print_stats(11)
print(f"\n  STAGE 2  {s2:.1f}s  {k:,} results"); print("\n".join(s.getvalue().splitlines()[4:17]))
led.close()
