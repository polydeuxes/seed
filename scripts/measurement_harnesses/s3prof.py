import sys, time, cProfile, pstats, io as _io, collections, shutil, os
sys.path.insert(0,"/home/user/seed-visitor")
shutil.copy("/dev/shm/lab/s3.db","/dev/shm/lab/s3run.db")
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.assertion_comparison import record_positional_result_comparison_layer
gets=collections.Counter(); integ=collections.Counter(); ids=collections.Counter()
rg,ri,rk = SQLiteEventLedger.get, SQLiteEventLedger.integrity_of, SQLiteEventLedger.iter_session_kind_ids
SQLiteEventLedger.get=lambda s,i:(gets.update([i]),rg(s,i))[1]
SQLiteEventLedger.integrity_of=lambda s,i:(integ.update([i]),ri(s,i))[1]
def cki(self,w,se,k,**kw):
    ids.update([(se,k)]); return rk(self,w,se,k,**kw)
SQLiteEventLedger.iter_session_kind_ids=cki
led=SQLiteEventLedger("/dev/shm/lab/s3run.db")
pr=cProfile.Profile(); pr.enable(); t=time.perf_counter()
c=record_positional_result_comparison_layer(led, workspace_id="local",
    source_session_ids=tuple(f"b{i:02d}" for i in range(1,7)), recording_session_id="cmp")
el=time.perf_counter()-t; pr.disable()
print(f"  {c:,} Compares in {el:,.0f}s   ({el/max(c,1)*1000:.2f} ms each)")
print(f"  ledger.get             {sum(gets.values()):>9,}  distinct {len(gets):>8,}  repeat {sum(gets.values())/max(len(gets),1):5.2f}x")
print(f"  integrity_of           {sum(integ.values()):>9,}  distinct {len(integ):>8,}  repeat {sum(integ.values())/max(len(integ),1):5.2f}x")
print(f"  iter_session_kind_ids  {sum(ids.values()):>9,}  distinct keys {len(ids)}")
s=_io.StringIO(); pstats.Stats(pr,stream=s).sort_stats("cumulative").print_stats(14)
print("\n".join(s.getvalue().splitlines()[4:20]))
led.close()
