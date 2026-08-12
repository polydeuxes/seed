import sys, os, glob, time
sys.path.insert(0,"/home/user/seed-visitor")
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.event import Event
from seed_runtime.ids import new_id
from seed_runtime.preserved_material_measurement import record_measurement_findings, INGRESS_OCCURRED_KIND
from seed_runtime.adjacent_pair_measurement import measure_at_displacement, record_adjacent_pair_measurement_layer, _positions
DB="/dev/shm/lab/s3.db"
if os.path.exists(DB): os.remove(DB)
led=SQLiteEventLedger(DB); W="local"
BODIES=["prose_austen_pride","prose_dickens_copperfield","prose_emerson_essays",
        "prose_hume_enquiry","english_grimm_fairy_tales","bible_kjv"]
for i,name in enumerate(BODIES,1):
    s=f"b{i:02d}"
    p=[f for f in glob.glob("/home/user/seed/corpus/*") if os.path.basename(f).startswith(name)][0]
    lines=[l for l in open(p,encoding="utf-8",errors="replace").read().split("\n")[3000:] if l.strip()][:300]
    b=[Event(id=new_id("evt"),kind=INGRESS_OCCURRED_KIND,workspace_id=W,session_id=s,
             payload={"decoded_text":l,"material_origin":"operator","text_representation":{"available":True}}) for l in lines]
    for k in range(0,len(b),500): led.append_many(b[k:k+500])
    occ=[e for e in led.list(W) if e.session_id==s and e.kind==INGRESS_OCCURRED_KIND]
    reps=sorted({x for e in occ for x in _positions(e.payload["decoded_text"])})
    acc=[]
    for r in reps:
        acc.append((measure_at_displacement(occ, r, displacement=1, counting_scope="s"), None))
        if len(acc)==500: record_measurement_findings(led, workspace_id=W, session_id=s, findings=acc); acc=[]
    if acc: record_measurement_findings(led, workspace_id=W, session_id=s, findings=acc)
    n=record_adjacent_pair_measurement_layer(led, workspace_id=W, session_id=s, counting_scope="s")
    print(f"  {s} {name[:24]:<24} {n:>7,} results", flush=True)
led.close()
print(f"  db {os.path.getsize(DB)/1e6:.0f} MB, 6 bodies = 15 body-pairs")
