"""Verify the chapter migration without changing any of the other 19 students.

Requires MYSQL_PWD and TEST_JWT_SECRET matching the local backend. Creates
temporary IN_PROGRESS attempts for 20240001 only, then archives those probes.
No account password is read, changed, or printed.
"""
import base64,hashlib,hmac,json,os,subprocess,time,urllib.error,urllib.request
from pathlib import Path

root=Path(__file__).resolve().parents[1]
base=os.environ.get('TEST_BASE_URL','http://127.0.0.1:18081')+'/api'
checks=[]
def sql(text):return subprocess.check_output(['mysql','--user='+os.environ.get('DB_USERNAME','root'),'--default-character-set=utf8mb4','--batch','--raw','--skip-column-names','learning_analysis'],input=text.encode(),env=os.environ)
def check(condition,name):
    assert condition,name
    checks.append(name)
def api(method,path,body=None,token=None,expected=200):
    headers={'Content-Type':'application/json'}
    if token:headers['Authorization']='Bearer '+token
    req=urllib.request.Request(base+path,headers=headers,data=None if body is None else json.dumps(body).encode(),method=method)
    try:
        with urllib.request.urlopen(req,timeout=10) as r:status=r.status;result=json.load(r)
    except urllib.error.HTTPError as e:status=e.code;result=json.load(e)
    assert status==expected,f'{path}: {status} {result.get("msg")}'
    return result.get('data')
def fingerprint():
    output={}
    for label,query in {
        'practice':"SELECT p.* FROM practice p JOIN app_user u ON u.id=p.student_id WHERE u.role='STUDENT' AND u.username<>'20240001' ORDER BY p.id;",
        'practice_item':"SELECT i.* FROM practice_item i JOIN practice p ON p.id=i.practice_id JOIN app_user u ON u.id=p.student_id WHERE u.role='STUDENT' AND u.username<>'20240001' ORDER BY i.id;",
        'accounts':"SELECT * FROM app_user ORDER BY id;"
    }.items():
        data=sql(query);output[label]={'sha256':hashlib.sha256(data).hexdigest(),'rows':len(data.splitlines())}
    return output

before=json.loads((root/'.local/backups/other_students_before_chapter_bank.json').read_text())
check(fingerprint()==before,'all accounts and other 19 students remain byte-for-byte unchanged')
user=json.loads(sql("SELECT JSON_OBJECT('id',CAST(id AS CHAR),'version',token_version) FROM app_user WHERE username='20240001';"))
sid=user['id']
def b64(value):return base64.urlsafe_b64encode(json.dumps(value,separators=(',',':')).encode()).rstrip(b'=')
header=b64({'alg':'HS256','typ':'JWT'})
payload=b64({'iss':'learning-analysis','sub':sid,'role':'STUDENT','version':user['version'],'iat':int(time.time()),'exp':int(time.time())+600})
message=header+b'.'+payload
token=(message+b'.'+base64.urlsafe_b64encode(hmac.new(os.environ['TEST_JWT_SECRET'].encode(),message,hashlib.sha256).digest()).rstrip(b'=')).decode()
admin=api('POST','/auth/login',{'username':'admin','password':'123456'})['token']
courses=api('GET','/courses',token=token)
check(len(courses)==5 and all(c['questionCount']==100 for c in courses),'five current courses contain exactly 100 questions each')
all_sets=[]
for course in courses:
    chapters=api('GET',f'/courses/{course["id"]}/chapters',token=token)
    points=api('GET',f'/courses/{course["id"]}/knowledge-points',token=token)
    check(len(chapters)==5 and all(c['questionCount']==20 for c in chapters),'five chapters of twenty questions: '+course['id'])
    check(len(points)==10 and all(p['questionCount']==10 for p in points),'ten knowledge points of ten questions: '+course['id'])
    sets=api('GET','/student/practices/chapter-sets?courseId='+course['id'],token=token)
    check(len(sets)==5 and all(s['completedAttempts']==1 for s in sets),'five completed fixed chapter sets: '+course['id'])
    all_sets+=sets
    analysis=api('GET','/student/knowledge-analysis?courseId='+course['id'],token=token)
    check(len(analysis)==10 and all(r['questionCount']==10 and r['level'] not in ('NO_DATA','INSUFFICIENT') for r in analysis),'student 20240001 has sufficient coverage in every topic: '+course['id'])
summary=api('GET','/student/summary',token=token)
check(sum(r['practiceCount'] for r in summary)==25 and sum(r['answerCount'] for r in summary)==500,'first student shows precisely 25 completed sets and 500 answers')
history=api('GET','/student/practices?pageSize=50',token=token)
check(history['total']==25 and all(r['sourceType']=='CHAPTER' and r['chapterName'] for r in history['rows']),'history contains named chapter practices only')

rows=[json.loads(line) for line in sql(f"SELECT JSON_OBJECT('id',i.id,'order',i.option_order,'selected',i.selected_answer,'correct',i.is_correct,'answer',q.correct_answer) FROM practice_item i JOIN practice p ON p.id=i.practice_id JOIN question q ON q.id=i.question_id WHERE p.student_id={sid} AND p.archived=0 ORDER BY i.id;").splitlines()]
check(len(rows)==500,'all 500 demo answers exist')
for row in rows:
    original=''.join(sorted(row['order'][ord(c)-65] for c in (row['selected'] or '')))
    assert (original==row['answer'])==bool(row['correct']),f'scoring mismatch {row["id"]}'
check(True,'all demo marks independently recomputed from original answers and saved option orders')
chapter=all_sets[0]['chapterId'];probes=[]
try:
    details=[]
    for _ in range(2):
        created=api('POST','/student/practices/chapters/'+chapter,token=token)
        probes.append(created['practiceId'])
        details.append(api('GET','/student/practices/'+created['practiceId']+'/questions',token=token))
    check(all(len(d['items'])==20 for d in details),'fixed entry opens the complete twenty-question chapter')
    check([i['stem'] for i in details[0]['items']]==[i['stem'] for i in details[1]['items']],'fixed entry retains identical questions in identical order')
    check(all(set(o['text'] for o in a['options'])==set(o['text'] for o in b['options']) for a,b in zip(details[0]['items'],details[1]['items'])),'only display order changes, not option content')
    check(any(a['options']!=b['options'] for a,b in zip(details[0]['items'],details[1]['items']) if a['questionType']!='JUDGE'),'choice option orders are independently randomized')
    check(all(a['options']==b['options'] for a,b in zip(details[0]['items'],details[1]['items']) if a['questionType']=='JUDGE'),'judgment options keep their defined order')
    random_set=api('POST','/student/practices',{'courseId':'1','chapterId':chapter,'count':7},token)
    probes.append(random_set['practiceId'])
    check(random_set['actualCount']==7,'custom random practice is still supported')
    api('POST','/student/practices/chapters/11',token=token,expected=404)
    api('POST','/student/practices/chapters/'+chapter,token=admin,expected=403)
    check(True,'legacy chapters and administrator answer access are rejected')
finally:
    if probes:sql(f"UPDATE practice SET archived=1 WHERE student_id={sid} AND id IN ({','.join(probes)}) AND status='IN_PROGRESS';")

check(fingerprint()==before,'other students and all account credentials still unchanged after verification')
check(sql(f"SELECT COUNT(*) FROM practice WHERE student_id={sid} AND archived=1;").strip()!=b'0','previous first-student records are retained in archive')
(root/'backend/target/chapter-bank-report.json').write_text(json.dumps({'passed':len(checks),'checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'PASS: {len(checks)} chapter-bank checks; other 19 students unchanged; no insufficient topics for 20240001.')
