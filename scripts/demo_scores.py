"""Reproducible example scores with course and topic variation, no fixed quotas."""
def topic_targets(points, rng):
    strengths={course:rng.uniform(0.45,0.90) for course in sorted({p['id']//10000 for p in points})}
    targets={}
    for point in sorted(points,key=lambda p:p['id']):
        probability=max(0.15,min(0.98,rng.gauss(strengths[point['id']//10000],0.17)))
        targets[point['id']]=sum(rng.random()<probability for _ in range(10))
    return targets
