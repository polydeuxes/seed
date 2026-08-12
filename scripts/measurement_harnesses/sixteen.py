"""Feed sixteen works to a Seed through the system path, and time every stage."""
import sys, os, glob, time, io, re
sys.path.insert(0,"/home/user/seed-visitor")
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.event import Event
from seed_runtime.ids import new_id
from seed_runtime.system_material import (
    DeclaredInvocation, declare_invocation, preserve_system_material, system_material_bytes,
    SYSTEM_MATERIAL_OCCURRED_KIND)
from seed_runtime.preserved_material_measurement import record_measurement_findings, INGRESS_OCCURRED_KIND
from seed_runtime.adjacent_pair_measurement import (
    measure_at_displacement, record_adjacent_pair_measurement_layer, _positions)
from seed_runtime.assertion_comparison import record_positional_result_comparison_layer
from seed_runtime.equality_signature_measurement import record_equality_signature_layer
from seed_runtime.equality_signature_recurrence import record_equality_signature_count_layer

DB="/dev/shm/lab/sixteen.db"; W="local"; LINES=1200
HARNESS="operator system-material harness"
BODIES=["grammar_goold_brown","roget_thesaurus","grammar_kittredge","webster_dictionary",
 "algebra_rivenburg","boole_laws_of_thought","euclid_elements","bash_abs_guide",
 "cookbook_farmer","french_les_miserables","latin_apicius","prose_austen_pride",
 "prose_dickens_copperfield","prose_emerson_essays","prose_hume_enquiry","spanish_don_quijote"]
def log(*a): print(*a, flush=True)
def path(n):
    return [f for f in glob.glob("/home/user/seed/corpus/*") if os.path.basename(f).startswith(n) and os.path.isfile(f)][0]
if os.path.exists(DB): os.remove(DB)
led=SQLiteEventLedger(DB); T0=time.perf_counter()

log(f"SIXTEEN WORKS, {LINES} lines each, entering through the system path\n")
sessions=[]
for i,name in enumerate(BODIES,1):
    s=f"sys_{i:03d}"; sessions.append(s)
    lines=[]
    with open(path(name),encoding="utf-8",errors="replace") as fh:
        for j,l in enumerate(fh):
            if j<3000: continue
            lines.append(l)
            if len(lines)>=LINES: break
    body="".join(lines).encode("utf-8")
    t=time.perf_counter()
    declare_invocation(led, workspace_id=W, session_id=s,
        declared=DeclaredInvocation(invocation=f"read {name}", declared_performer=HARNESS, on_behalf_of="this Seed"))
    occ=preserve_system_material(led, workspace_id=W, session_id=s, exact_bytes=body,
                                 observed_boundary="operator harness, file read")
    log(f"  ingest {i:>2} {name[:26]:<26} {len(body):>8,} B  {time.perf_counter()-t:5.2f}s")

log("")
for i,s in enumerate(sessions,1):
    ev=[e for e in led.list(W) if e.session_id==s and e.kind==SYSTEM_MATERIAL_OCCURRED_KIND][0]
    if not ev.payload["text_representation"]["available"]:
        log(f"  skip   {s} — no text representation"); continue
    text=system_material_bytes(ev).decode("utf-8")
    lines=[l for l in text.split("\n") if l.strip()]
    batch=[Event(id=new_id("evt"), kind=INGRESS_OCCURRED_KIND, workspace_id=W, session_id=s,
                 payload={"decoded_text": l, "material_origin":"operator",
                          "text_representation":{"available":True}}) for l in lines]
    for k in range(0,len(batch),500): led.append_many(batch[k:k+500])
    t=time.perf_counter()
    o=[e for e in led.list(W) if e.session_id==s and e.kind==INGRESS_OCCURRED_KIND]
    reps=sorted({p for e in o for p in _positions(e.payload["decoded_text"])})
    b=[]
    for r in reps:
        b.append((measure_at_displacement(o, r, displacement=1, counting_scope="one bounded exchange"), None))
        if len(b)==500: record_measurement_findings(led, workspace_id=W, session_id=s, findings=b); b=[]
    if b: record_measurement_findings(led, workspace_id=W, session_id=s, findings=b)
    st1=time.perf_counter()-t
    t=time.perf_counter()
    k=record_adjacent_pair_measurement_layer(led, workspace_id=W, session_id=s, counting_scope="one bounded exchange")
    log(f"  measure {i:>2} {s} {len(lines):>5,} lines {len(reps):>6,} reps {k:>8,} results  s1 {st1:6.1f}s  s2 {time.perf_counter()-t:7.1f}s  db {os.path.getsize(DB)/1e9:.2f} GB")

log("")
t=time.perf_counter(); c=record_positional_result_comparison_layer(led, workspace_id=W, source_session_ids=tuple(sessions), recording_session_id="cmp")
log(f"  stage3 {c:>9,} Compares    {time.perf_counter()-t:8.1f}s   db {os.path.getsize(DB)/1e9:.2f} GB")
t=time.perf_counter(); g=record_equality_signature_layer(led, workspace_id=W, source_session_ids=("cmp",), recording_session_id="sig")
log(f"  stage4 {g:>9,} signatures  {time.perf_counter()-t:8.1f}s")
t=time.perf_counter(); n=record_equality_signature_count_layer(led, workspace_id=W, source_session_ids=("sig",), recording_session_id="cnt")
log(f"  stage5 {n:>9} groups      {time.perf_counter()-t:8.1f}s")
log(f"\nTOTAL {time.perf_counter()-T0:,.0f}s   db {os.path.getsize(DB)/1e9:.2f} GB")
led.close()
