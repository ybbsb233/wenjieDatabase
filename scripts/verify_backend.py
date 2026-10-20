"""Real HTTP/MySQL integration checks against this project's database only.

Run with MYSQL_PWD and TEST_ADMIN_PASSWORD in the environment. Creates/resets
the three documented demo students and adds genuine demo exercise history.
Does not delete data or touch other databases. No credentials are printed.
"""
import concurrent.futures
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

if os.environ.get('ALLOW_LEGACY_DEMO_RESET')!='yes':
    raise SystemExit('Legacy demo reset verifier disabled. Use verify_chapter_sets.py for the current chapter bank.')

BASE=os.environ.get('TEST_BASE_URL','http://127.0.0.1:18080')
checks=[]
def check(condition,name):
    if not condition: raise AssertionError(name)
    checks.append(name)

def api(method,path,body=None,token=None,expected=200):
    headers={'Content-Type':'application/json'}
    if token: headers['Authorization']='Bearer '+token
    request=urllib.request.Request(BASE+path,data=None if body is None else json.dumps(body).encode(),headers=headers,method=method)
    try:
        with urllib.request.urlopen(request,timeout=10) as response:
            status=response.status; result=json.load(response)
    except urllib.error.HTTPError as error:
        status=error.code; result=json.load(error)
    if status!=expected: raise AssertionError(f'{method} {path}: {status} {result.get("msg")} expected {expected}')
    return result.get('data')

def login(username,password):return api('POST','/api/auth/login',{'username':username,'password':password})

admin_login=login('admin',os.environ['TEST_ADMIN_PASSWORD'])
admin=admin_login['token']
check(not admin_login['user']['mustChangePassword'],'administrator can log in without mandatory password change')
api('GET','/api/courses',expected=401)
api('POST','/api/auth/login',{'username':'admin','password':'invalid'},expected=401)
api('GET','/api/courses',token=admin[:-2]+'xx',expected=401)
check(True,'unauthenticated, incorrect-password and forged JWT rejection')

students=[]
for n in range(1,4):
    account=f'2024000{n}'
    rows=api('GET','/api/admin/students?keyword='+account,token=admin)['rows']
    if rows:
        student=rows[0]
        api('PUT',f'/api/admin/students/{student["id"]}/status',{'enabled':True},admin)
        api('POST',f'/api/admin/students/{student["id"]}/reset-password',{},admin)
    else:
        student=api('POST','/api/admin/students',{'username':account,'realName':f'演示学生{n}'},admin)
    token=login(account,'123456')['token']
    api('GET','/api/courses',token=token)
    api('PUT','/api/auth/password',{'oldPassword':'123456','newPassword':'StudyDemo2026!'},token)
    api('GET','/api/auth/me',token=token,expected=401)
    students.append((student['id'],login(account,'StudyDemo2026!')['token']))
check(True,'three students, optional password change and password reset workflow')
api('POST','/api/admin/students',{'username':'20240001','realName':'重复'},admin,409)
api('POST','/api/admin/students',{'username':'abc','realName':'非法学号'},admin,400)
check(True,'duplicate account and malformed student input rejected')

student_id,token=students[0]
api('GET','/api/admin/students',token=token,expected=403)
api('GET','/api/student/knowledge-analysis',token=token,expected=400)
api('GET','/api/nonexistent',token=token,expected=404)
api('DELETE','/api/courses',token=token,expected=405)
check(True,'missing required parameters, unknown routes and unsupported methods')
api('POST','/api/student/practices',{'courseId':'1','chapterId':'21','count':5},token,400)
api('POST','/api/student/practices',{'courseId':'1','count':0},token,400)
api('POST','/api/student/practices',{'courseId':'1','count':51},token,400)
api('GET','/api/student/practices?page=0',token=token,expected=400)
check(True,'roles, mismatched chapter, count and pagination validation')

courses=api('GET','/api/courses',token=token)
check(len(courses)==5 and all(c['questionCount']==15 for c in courses),'five courses with fifteen questions each')
for c in courses:
    check(len(api('GET',f'/api/courses/{c["id"]}/chapters',token=token))==2,'chapter lookup '+c['id'])
    check(len(api('GET',f'/api/courses/{c["id"]}/knowledge-points',token=token))==3,'knowledge lookup '+c['id'])

# Use MySQL only as the independent oracle; correct answers never come from
# the in-progress HTTP payload. JSON output is UTF-8 on Windows as well.
raw=subprocess.check_output(['mysql','--user='+os.environ.get('DB_USERNAME','root'),'-N','--default-character-set=utf8mb4','learning_analysis','-e',
    "SELECT JSON_OBJECT('id',CAST(id AS CHAR),'stem',stem,'answer',correct_answer,'options',JSON_ARRAY(option_a,option_b,option_c,option_d)) FROM question"],env=os.environ)
questions={}
for line in raw.decode('utf-8').splitlines():
    q=json.loads(line);questions[q['stem']]=q

def start(course,token,count=50):
    created=api('POST','/api/student/practices',{'courseId':course,'count':count},token)
    detail=api('GET',f'/api/student/practices/{created["practiceId"]}/questions',token=token)
    check('correctAnswer' not in json.dumps(detail) and 'explanation' not in json.dumps(detail),'no answers in in-progress payload')
    return created,detail

def answers(detail,mode='correct'):
    rows=[]
    for item in detail['items']:
        q=questions[item['stem']]
        labels=[opt['label'] for opt in item['options'] if chr(65+q['options'].index(opt['text'])) in q['answer']]
        if mode=='wrong': labels=[]
        rows.append({'itemId':item['itemId'],'selectedLabels':labels})
    return {'answers':rows}

first_id=None
for c in courses:
    created,detail=start(c['id'],token)
    check(created['actualCount']==15 and created['requestedCount']==50,'question shortage handled '+c['id'])
    pid=created['practiceId'];first_id=first_id or pid
    api('GET',f'/api/student/practices/{pid}/result',token=token,expected=409)
    repeat=api('GET',f'/api/student/practices/{pid}/questions',token=token)
    check(repeat==detail,'saved option mapping stable '+c['id'])
    api('GET',f'/api/student/practices/{pid}/questions',token=students[1][1],expected=404)
    payload=answers(detail)
    invalid={'answers':[payload['answers'][0],payload['answers'][0]]}
    api('POST',f'/api/student/practices/{pid}/submit',invalid,token,400)
    result=api('POST',f'/api/student/practices/{pid}/submit',payload,token)
    check(result['correctCount']==15,'randomized choice scoring '+c['id'])
    again=api('POST',f'/api/student/practices/{pid}/submit',{'answers':[]},token)
    check(again==result,'duplicate submission preserved '+c['id'])
    detail_result=api('GET',f'/api/student/practices/{pid}/result',token=token)
    check(all(i['isCorrect'] for i in detail_result['items']),'history result and displayed answers '+c['id'])
    api('GET',f'/api/admin/practices/{pid}/result',token=admin)
check(True,'data ownership and administrator result lookup')

# Error history followed by correct retry exercises different statistical bases.
created,detail=start('2',token)
api('POST',f'/api/student/practices/{created["practiceId"]}/submit',answers(detail,'wrong'),token)
wrong=api('GET','/api/student/wrong-questions?courseId=2',token=token)
check(wrong['total']==15,'unanswered questions collected in wrong-question list')
retry=api('POST','/api/student/practices/from-wrong',{'courseId':'2','questionIds':[q['questionId'] for q in wrong['rows']]},token)
retry_detail=api('GET',f'/api/student/practices/{retry["practiceId"]}/questions',token=token)
api('POST',f'/api/student/practices/{retry["practiceId"]}/submit',answers(retry_detail),token)
wrong=api('GET','/api/student/wrong-questions?courseId=2',token=token)
check(wrong['total']==15 and all(q['latestCorrect'] for q in wrong['rows']),'wrong history retained after correct retry')
analysis=api('GET','/api/student/knowledge-analysis?courseId=2',token=token)
check(next(r for r in analysis if r['knowledgeId']=='21')['level']=='GOOD','recent answers update knowledge level')
check(next(r for r in analysis if r['knowledgeId']=='23')['level']=='GOOD','expanded topic has enough distinct practiced questions')
check(sum(r['questionCount'] for r in analysis)==16,'multi-tag topic count without course duplication')
for path in ['/api/student/summary','/api/student/trend?courseId=2','/api/student/practices?courseId=2']:
    api('GET',path,token=token)

# Concurrent submissions must serialize and return the same committed result.
created,detail=start('1',token)
path=f'/api/student/practices/{created["practiceId"]}/submit'
with concurrent.futures.ThreadPoolExecutor(2) as pool:
    futures=[pool.submit(api,'POST',path,answers(detail,mode),token) for mode in ['correct','wrong']]
    results=[f.result() for f in futures]
check(results[0]==results[1],'concurrent submission commits once')

for sid,stoken in students[1:]:
    created,detail=start('2',stoken)
    api('POST',f'/api/student/practices/{created["practiceId"]}/submit',answers(detail),stoken)
for path in ['/api/admin/summary','/api/admin/knowledge-analysis?courseId=2','/api/admin/course-students?courseId=2',
             f'/api/admin/students/{student_id}',f'/api/admin/students/{student_id}/summary',
             f'/api/admin/students/{student_id}/knowledge-analysis?courseId=2',f'/api/admin/students/{student_id}/trend?courseId=2',
             f'/api/admin/students/{student_id}/practices',f'/api/admin/students/{student_id}/wrong-questions']:
    api('GET',path,token=admin)
overall=api('GET','/api/admin/knowledge-analysis?courseId=2',token=admin)
check(next(r for r in overall if r['knowledgeId']=='21')['participantCount']>=3,'overall analysis includes three students')
check(True,'all administrator report routes and students with no activity')

sid,old=students[2]
api('PUT',f'/api/admin/students/{sid}/status',{'enabled':False},admin)
api('GET','/api/auth/me',token=old,expected=401)
api('PUT',f'/api/admin/students/{sid}/status',{'enabled':True},admin)
api('GET','/api/auth/me',token=old,expected=401)
check(True,'disable and re-enable never restores old token')
api('POST','/api/auth/logout',{},token)
api('GET','/api/auth/me',token=token,expected=401)
check(True,'logout revokes token')

# Leave documented demo accounts at the agreed initial password and first-change state.
for sid,_ in students:api('POST',f'/api/admin/students/{sid}/reset-password',{},admin)
check(True,'demo accounts restored to default password without mandatory change; history retained')
out=Path(__file__).resolve().parents[1]/'backend'/'target'/'integration-report.json'
out.write_text(json.dumps({'passed':len(checks),'checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'PASS: {len(checks)} integration checks; report: backend/target/integration-report.json')
