"""Vary the existing 25 chapter demo attempts; preserve IDs, times and option orders."""
import hashlib,itertools,json,os,random,subprocess
from pathlib import Path
from chapter_bank import build
from demo_scores import topic_targets

root=Path(__file__).resolve().parents[1]
def sql(text):
    return subprocess.check_output(['mysql','--user='+os.environ.get('DB_USERNAME','root'),'--default-character-set=utf8mb4','--batch','--raw','--skip-column-names','learning_analysis'],input=text.encode(),env=os.environ)
def other_data():
    statements=["SELECT * FROM app_user ORDER BY id;",
        "SELECT p.* FROM practice p JOIN app_user u ON u.id=p.student_id WHERE u.username<>'20240001' ORDER BY p.id;",
        "SELECT i.* FROM practice_item i JOIN practice p ON p.id=i.practice_id JOIN app_user u ON u.id=p.student_id WHERE u.username<>'20240001' ORDER BY i.id;"]
    return [hashlib.sha256(sql(s)).hexdigest() for s in statements]

before=other_data()
rows=[json.loads(line) for line in sql("SELECT JSON_OBJECT('id',i.id,'practiceId',p.id,'knowledgeId',qk.knowledge_id,'type',q.question_type,'order',i.option_order,'answer',q.correct_answer) FROM practice_item i JOIN practice p ON p.id=i.practice_id JOIN app_user u ON u.id=p.student_id JOIN question q ON q.id=i.question_id JOIN question_knowledge qk ON qk.question_id=q.id JOIN chapter ch ON ch.id=q.chapter_id WHERE u.username='20240001' AND p.archived=0 AND p.status='SUBMITTED' AND p.source_type='CHAPTER' AND ch.is_current=1 ORDER BY i.id;").splitlines()]
assert len(rows)==500 and len({r['practiceId'] for r in rows})==25,'Expected the 25 original chapter demos; refusing to change unrelated data.'
_,points,_=build()
rng=random.Random(20261019)
targets=topic_targets(points,rng)
correct_ids=set()
for k in points:
    group=[r for r in rows if r['knowledgeId']==k['id']]
    assert len(group)==10
    correct_ids.update(r['id'] for r in rng.sample(group,targets[k['id']]))
statements=['USE learning_analysis;','START TRANSACTION;']
expected=[]
for row in rows:
    correct=row['id'] in correct_ids
    labels=[chr(65+i) for i,original in enumerate(row['order']) if original in row['answer']]
    selected=''.join(labels)
    if not correct:
        alphabet=[chr(65+i) for i in range(len(row['order']))]
        if row['type']=='MULTIPLE':
            alternatives=[''.join(s) for n in range(1,len(alphabet)+1) for s in itertools.combinations(alphabet,n) if list(s)!=labels]
        else:alternatives=[x for x in alphabet if x not in labels]
        selected=rng.choice(alternatives)
    statements.append(f"UPDATE practice_item SET selected_answer='{selected}',is_correct={int(correct)} WHERE id={row['id']};")
    original=''.join(sorted(row['order'][ord(c)-65] for c in selected))
    assert (original==row['answer'])==correct
for pid in sorted({r['practiceId'] for r in rows}):
    score=sum(r['id'] in correct_ids for r in rows if r['practiceId']==pid)
    statements.append(f'UPDATE practice SET correct_count={score} WHERE id={pid};')
    expected.append({'practiceId':pid,'correctCount':score})
statements.append('COMMIT;')
text='\n'.join(statements)
(root/'.local/backups/randomize_20240001.sql').write_text(text,encoding='utf-8')
sql(text)
assert other_data()==before,'Other accounts or students changed unexpectedly'
summary={}
for course in range(1,6):
    values=[v for k,v in targets.items() if k//10000==course]
    summary[course]={'WEAK':sum(v<6 for v in values),'REVIEW':sum(6<=v<8 for v in values),'GOOD':sum(v>=8 for v in values),'accuracy':sum(values)}
assert len({tuple(s.values()) for s in summary.values()})>1
(root/'.local/backups/randomized_scores_report.json').write_text(json.dumps({'courses':summary,'practiceScores':expected,'otherStudentsUnchanged':True},indent=2),encoding='utf-8')
print(json.dumps(summary))
print('All 500 answers and 25 totals updated consistently. Other 19 students and all accounts unchanged.')
