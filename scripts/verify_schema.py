"""Check the actual MySQL schema and demonstration constraints without committing test rows."""
import os
import subprocess

def sql(text):
    return subprocess.run(['mysql','--user='+os.environ.get('DB_USERNAME','root'),'--default-character-set=utf8mb4','-N','learning_analysis'],input=text.encode('utf-8'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)

checks=0
for statement,expected in [
    ('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE();','8'),
    ('SELECT COUNT(*) FROM question q JOIN chapter ch ON ch.id=q.chapter_id WHERE ch.is_current=1;','500'),
    ('SELECT COUNT(*) FROM question q WHERE NOT EXISTS(SELECT 1 FROM question_knowledge k WHERE k.question_id=q.id);','0'),
    ('SELECT COUNT(*) FROM question_knowledge qk JOIN question q ON q.id=qk.question_id JOIN knowledge_point k ON k.id=qk.knowledge_id WHERE q.chapter_id<>k.chapter_id;','0'),
    ("SELECT COUNT(*) FROM practice p WHERE p.question_count<>(SELECT COUNT(*) FROM practice_item i WHERE i.practice_id=p.id);",'0'),
    ("SELECT COUNT(*) FROM practice p WHERE status='SUBMITTED' AND p.correct_count<>(SELECT SUM(i.is_correct) FROM practice_item i WHERE i.practice_id=p.id);",'0'),
]:
    result=sql(statement)
    assert result.returncode==0 and result.stdout.decode().strip()==expected, 'Schema/data invariant failed'
    checks+=1

assert sql('SELECT COUNT(*) FROM (SELECT k.id FROM knowledge_point k JOIN chapter c ON c.id=k.chapter_id LEFT JOIN question_knowledge qk ON qk.knowledge_id=k.id WHERE c.is_current=1 GROUP BY k.id HAVING COUNT(qk.question_id)<3) sparse;').stdout.decode().strip()=='0'
checks+=1

invalid=[
    "INSERT INTO chapter(course_id,name) VALUES(999999999,'invalid');",
    "INSERT INTO course(name,sort_order) VALUES('constraint-test',-1);",
    "INSERT INTO question(chapter_id,question_type,stem,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES(11,'SINGLE','test','1','2',NULL,'4','A','test');",
    "INSERT INTO question(chapter_id,question_type,stem,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES(11,'SINGLE','test','1','2','3','4','AB','test');",
    "INSERT INTO question(chapter_id,question_type,stem,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES(11,'MULTIPLE','test','1','2','3','4','A','test');",
    "INSERT INTO app_user(username,real_name,password_hash,role) VALUES('constraint-test','test','not-real','SUPERADMIN');",
]
for statement in invalid:
    result=sql('START TRANSACTION;\n'+statement+'\nROLLBACK;')
    assert result.returncode!=0 and (b'3819' in result.stderr or b'1452' in result.stderr),'Expected CHECK or FK rejection'
    checks+=1
print(f'PASS: {checks} real MySQL schema and integrity checks; all test writes rolled back.')
