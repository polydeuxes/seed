import sys, os, time
TREE=sys.argv[1]; sys.path.insert(0,"/home/user/seed-visitor")
if TREE=="before":
    import seed_runtime.adjacent_pair_measurement as _apm
    _orig=_apm._support_for
    _apm._support_for=lambda **kw: _orig(**{**kw, "declared_support": None})
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.event import Event
from seed_runtime.ids import new_id
from seed_runtime.preserved_material_measurement import record_measurement_findings, INGRESS_OCCURRED_KIND
from seed_runtime.adjacent_pair_measurement import measure_at_displacement, record_adjacent_pair_measurement_layer, _positions
DB=f"/dev/shm/lab/ab_{TREE}.db"
if os.path.exists(DB): os.remove(DB)
led=SQLiteEventLedger(DB); W="local"; S="b"
lines=[l for l in open("/home/user/seed/corpus/prose_austen_pride.txt",encoding="utf-8").read().split("\n")[3000:] if l.strip()][:700]
b=[Event(id=new_id("evt"),kind=INGRESS_OCCURRED_KIND,workspace_id=W,session_id=S,
         payload={"decoded_text":l,"material_origin":"operator","text_representation":{"available":True}}) for l in lines]
for i in range(0,len(b),500): led.append_many(b[i:i+500])
occ=[e for e in led.list(W) if e.kind==INGRESS_OCCURRED_KIND]
reps=sorted({p for e in occ for p in _positions(e.payload["decoded_text"])})
acc=[]
for r in reps:
    acc.append((measure_at_displacement(occ, r, displacement=1, counting_scope="s"), None))
    if len(acc)==500: record_measurement_findings(led, workspace_id=W, session_id=S, findings=acc); acc=[]
if acc: record_measurement_findings(led, workspace_id=W, session_id=S, findings=acc)
t=time.perf_counter(); k=record_adjacent_pair_measurement_layer(led, workspace_id=W, session_id=S, counting_scope="s")
el=time.perf_counter()-t
led.close()
print(f"{TREE},{k},{el:.1f},{os.path.getsize(DB)}")
