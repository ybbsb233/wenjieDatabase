"""Populate 20240002..20240020 using varied chapter-based demonstration answers.

Archives prior attempts without deleting them. Does not change 20240001,
accounts, passwords or the question bank. Requires --apply to run the update.
"""
import argparse,hashlib,itertools,json,os,random,subprocess
from datetime import datetime,timedelta
from pathlib import Path
from chapter_bank import build,quote
from demo_scores import topic_targets

root=Path(__file__).resolve().parents[1]
def sql(text):
    return subprocess.check_output(['mysql','--user='+os.environ.get('DB_USERNAME','root'),'--default-character-set=utf8mb4','--batch','--raw','--skip-column-names','learning_analysis'],input=text.encode('utf-8'),env=os.environ)

def preserved_data():
    queries={
      'accounts':'SELECT * FROM app_user ORDER BY id;',
      'first_student_practice':"SELECT p.* FROM practice p JOIN app_user u ON u.id=p.student_id WHERE u.username='20240001' ORDER BY p.id;",
      'first_student_answers':"SELECT i.* FROM practice_item i JOIN practice p ON p.id=i.practice_id JOIN app_user u ON u.id=p.student_id WHERE u.username='20240001' ORDER BY i.id;",
    }
    return {name:hashlib.sha256(sql(query)).hexdigest() for name,query in queries.items()}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true',help='Archive and replace the nineteen students demo attempts')
    args=parser.parse_args()
    if not args.apply:parser.error('Specify --apply to populate the demonstration data.')
    usernames=[str(20240000+n) for n in range(2,21)]
    names=','.join(quote(u) for u in usernames)
    assert int(sql(f"SELECT COUNT(*) FROM app_user WHERE role='STUDENT' AND username IN ({names});"))==19
    before=preserved_data()
    chapters,points,questions=build()
    assert int(sql('SELECT COUNT(*) FROM question q JOIN chapter c ON c.id=q.chapter_id WHERE c.is_current=1;'))==500
    statements=['USE learning_analysis;','START TRANSACTION;',f"UPDATE practice p JOIN app_user u ON u.id=p.student_id SET p.archived=1 WHERE u.role='STUDENT' AND u.username IN ({names}) AND p.archived=0;"]
    report=[]
    now=datetime.now()
    for username in usernames:
        rng=random.Random(20261019+int(username)*7919)
        targets=topic_targets(points,rng)
        statements.append(f"SET @sid=(SELECT id FROM app_user WHERE username={quote(username)} AND role='STUDENT');")
        start=now-timedelta(days=rng.randint(7,11),minutes=rng.randint(0,120))
        student={'username':username,'practiceCount':25,'answerCount':500,'courses':{}}
        for course in range(1,6):
            values=[v for k,v in targets.items() if k//10000==course]
            student['courses'][course]={'WEAK':sum(v<6 for v in values),'REVIEW':sum(6<=v<8 for v in values),'GOOD':sum(v>=8 for v in values),'accuracy':sum(values)}
        for c in chapters:
            pool=[q for q in questions if q['chapterId']==c['id']]
            assert len(pool)==20
            correct_ids=set()
            for knowledge in [p['id'] for p in points if p['chapterId']==c['id']]:
                ids=[q['id'] for q in pool if q['knowledgeId']==knowledge]
                correct_ids.update(rng.sample(ids,targets[knowledge]))
            submitted=start+timedelta(days=c['order']-1,hours=c['courseId'],minutes=rng.randint(0,55))
            started=submitted-timedelta(minutes=rng.randint(5,23))
            statements.append(f"INSERT INTO practice(student_id,course_id,chapter_id,source_type,status,question_count,correct_count,started_at,submitted_at,archived) VALUES(@sid,{c['courseId']},{c['id']},'CHAPTER','SUBMITTED',20,{len(correct_ids)},{quote(started.strftime('%Y-%m-%d %H:%M:%S'))},{quote(submitted.strftime('%Y-%m-%d %H:%M:%S'))},0);")
            statements.append('SET @pid=LAST_INSERT_ID();')
            for index,q in enumerate(pool,1):
                order=list('AB' if q['kind']=='JUDGE' else 'ABCD')
                if q['kind']!='JUDGE':rng.shuffle(order)
                right=''.join(chr(65+i) for i,o in enumerate(order) if o in q['answer'])
                correct=q['id'] in correct_ids
                selected=right
                if not correct:
                    alphabet=[chr(65+i) for i in range(len(order))]
                    if q['kind']=='MULTIPLE':
                        alternatives=[''.join(items) for size in range(1,5) for items in itertools.combinations(alphabet,size) if ''.join(items)!=right]
                    else:alternatives=[letter for letter in alphabet if letter!=right]
                    selected=rng.choice(alternatives)
                original=''.join(sorted(order[ord(c)-65] for c in selected))
                assert (original==q['answer'])==correct
                statements.append(f"INSERT INTO practice_item(practice_id,question_id,order_no,option_order,selected_answer,is_correct) VALUES(@pid,{q['id']},{index},{quote(''.join(order))},{quote(selected)},{int(correct)});")
        report.append(student)
    statements.append('COMMIT;')
    text='\n'.join(statements)
    output=root/'.local/backups/remaining_students_seed.sql'
    output.write_text(text,encoding='utf-8')
    sql(text)
    assert preserved_data()==before,'The first student or an account was modified unexpectedly'
    # Independently inspect all twenty students, checking exact coverage and stored marks.
    rows=[json.loads(line) for line in sql("SELECT JSON_OBJECT('username',u.username,'practiceId',p.id,'chapterId',p.chapter_id,'knowledgeId',qk.knowledge_id,'questionId',i.question_id,'order',i.option_order,'selected',i.selected_answer,'correct',i.is_correct,'answer',q.correct_answer) FROM practice_item i JOIN practice p ON p.id=i.practice_id JOIN app_user u ON u.id=p.student_id JOIN question q ON q.id=i.question_id JOIN question_knowledge qk ON qk.question_id=q.id WHERE p.archived=0 AND p.status='SUBMITTED' AND u.username BETWEEN '20240001' AND '20240020' ORDER BY u.username,i.id;").splitlines()]
    for username in ['20240001',*usernames]:
        own=[r for r in rows if r['username']==username]
        assert len(own)==500 and len({r['practiceId'] for r in own})==25
        assert len({r['questionId'] for r in own})==500
        assert len({r['chapterId'] for r in own})==25
        for point in points:assert sum(r['knowledgeId']==point['id'] for r in own)==10
    for row in rows:
        actual=''.join(sorted(row['order'][ord(c)-65] for c in row['selected']))
        assert (actual==row['answer'])==bool(row['correct'])
    signatures={tuple((cid,*r['courses'][cid].values()) for cid in range(1,6)) for r in report}
    assert len(signatures)==19,'Students should not share a copied score profile'
    (root/'.local/backups/remaining_students_report.json').write_text(json.dumps({'students':report,'firstStudentAndAccountsUnchanged':True,'verifiedAnswers':len(rows)},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS: 19 students updated, 475 completed chapter practices, 9500 new answers.')
    print('Verified all 10000 current answers, full topic coverage for all twenty students, and nineteen distinct score profiles.')
    print('20240001 and all accounts/passwords unchanged; previous attempts retained in archive.')

if __name__=='__main__':main()
