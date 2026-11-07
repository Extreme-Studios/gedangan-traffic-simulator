"""Queue observations; no claim of spillback from queue length alone."""
def observe(vehicles, lengths):
    queues={}
    for v in vehicles:
        if v['speed']<0.3 and not v['lane'].startswith(':'):
            q=queues.setdefault(v['lane'],{'count':0,'tail_position':1e12,'head_position':0,'waiting_seconds':0})
            q['count']+=1;q['tail_position']=min(q['tail_position'],v['pos']);q['head_position']=max(q['head_position'],v['pos']);q['waiting_seconds']+=v['wait']
    for lane,q in queues.items():
        q['extent_m']=q['head_position']-q['tail_position'];q['lane_start_reached']=q['tail_position']<5;q['boundary_censored']=False
    return queues
def spillback_candidate(downstream_queue, upstream_stopped, movement_available, seconds):
    return bool(downstream_queue and downstream_queue['tail_position']<5 and upstream_stopped and movement_available and seconds>=5)
