"""Prepare only student 20240001: archive previous attempts, then create 25 demos.

No DELETE statements are used. Every current chapter is answered once using
its full 20-question set. Other students, names and passwords are untouched.
"""
import importlib.util,json,os,random,subprocess
from demo_scores import topic_targets
from datetime import datetime,timedelta
from pathlib import Path

root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('chapter_bank',root/'scripts'/'chapter_bank.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
chapters,points,questions=module.build()
quote=module.quote
rng=random.Random(20261019)
all_targets=topic_targets(points,rng)
sql=['USE learning_analysis;','START TRANSACTION;',"SET @sid=(SELECT id FROM app_user WHERE username='20240001' AND role='STUDENT');",'UPDATE practice SET archived=1 WHERE student_id=@sid AND archived=0;']
start=datetime.now()-timedelta(days=6)
expected=[]
for c in chapters:
    pool=[q for q in questions if q['chapterId']==c['id']]
    assert len(pool)==20
    # Per-topic scores vary, showing weak, review and good levels.
    targets={k['id']:all_targets[k['id']] for k in points if k['chapterId']==c['id']}
    correct_ids=set()
    for knowledge,target in targets.items():
        ids=[q['id'] for q in pool if q['knowledgeId']==knowledge]
        correct_ids.update(rng.sample(ids,target))
    submitted=start+timedelta(days=c['order']-1,hours=c['courseId'],minutes=15)
    started=submitted-timedelta(minutes=10)
    total=len(correct_ids)
    sql.append(f"INSERT INTO practice(student_id,course_id,chapter_id,source_type,status,question_count,correct_count,started_at,submitted_at,archived) VALUES(@sid,{c['courseId']},{c['id']},'CHAPTER','SUBMITTED',20,{total},{quote(started.strftime('%Y-%m-%d %H:%M:%S'))},{quote(submitted.strftime('%Y-%m-%d %H:%M:%S'))},0);")
    sql.append('SET @pid=LAST_INSERT_ID();')
    for index,q in enumerate(pool,1):
        order=list('AB' if q['kind']=='JUDGE' else 'ABCD')
        if q['kind']!='JUDGE':rng.shuffle(order)
        labels=''.join(chr(65+i) for i,original in enumerate(order) if original in q['answer'])
        is_correct=q['id'] in correct_ids
        if not is_correct:
            # Use valid, explicitly wrong answers instead of leaving every error blank.
            alternatives=[chr(65+i) for i in range(len(order)) if chr(65+i)!=labels]
            labels=rng.choice(alternatives)
        sql.append(f"INSERT INTO practice_item(practice_id,question_id,order_no,option_order,selected_answer,is_correct) VALUES(@pid,{q['id']},{index},{quote(''.join(order))},{quote(labels)},{int(is_correct)});")
    expected.append({'chapterId':c['id'],'courseId':c['courseId'],'correctCount':total,'questionCount':20})
sql.append('COMMIT;')
result='\n'.join(sql)
(root/'.local'/'backups'/'student_20240001_chapter_seed.sql').write_text(result,encoding='utf-8')
subprocess.run(['mysql','--user='+os.environ.get('DB_USERNAME','root'),'--default-character-set=utf8mb4','learning_analysis'],input=result.encode('utf-8'),env=os.environ,check=True)
(root/'.local'/'backups'/'student_20240001_expected.json').write_text(json.dumps(expected,indent=2),encoding='utf-8')
print('Only 20240001 rebuilt: 25 completed chapter sets, 500 answers; old attempts archived, not deleted.')
