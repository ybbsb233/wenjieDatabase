"""Add chapter sets while preserving all old attempts and questions."""
import hashlib,json,os,subprocess
from pathlib import Path

root=Path(__file__).resolve().parents[1]
def sql(text):
    return subprocess.check_output(['mysql','--user='+os.environ.get('DB_USERNAME','root'),'--default-character-set=utf8mb4','--batch','--raw','--skip-column-names','learning_analysis'],input=text.encode('utf-8'),env=os.environ)
def column(table,name):
    return sql(f"SELECT COUNT(*) FROM information_schema.columns WHERE table_schema=DATABASE() AND table_name='{table}' AND column_name='{name}';").strip()==b'1'

commands=[]
if not column('chapter','is_current'):commands.append('ALTER TABLE chapter ADD COLUMN is_current TINYINT NOT NULL DEFAULT 1;')
if not column('practice','chapter_id'):commands.append('ALTER TABLE practice ADD COLUMN chapter_id BIGINT NULL, ADD CONSTRAINT fk_practice_chapter FOREIGN KEY(chapter_id) REFERENCES chapter(id);')
if not column('practice','archived'):commands.append('ALTER TABLE practice ADD COLUMN archived TINYINT NOT NULL DEFAULT 0 CHECK(archived IN (0,1));')
checks=sql("SELECT tc.CONSTRAINT_NAME FROM information_schema.TABLE_CONSTRAINTS tc JOIN information_schema.CHECK_CONSTRAINTS cc ON cc.CONSTRAINT_SCHEMA=tc.CONSTRAINT_SCHEMA AND cc.CONSTRAINT_NAME=tc.CONSTRAINT_NAME WHERE tc.TABLE_SCHEMA=DATABASE() AND tc.TABLE_NAME='practice' AND cc.CHECK_CLAUSE LIKE '%source_type%';").decode().splitlines()
for name in checks:commands.append(f'ALTER TABLE practice DROP CHECK `{name}`;')
commands.append("ALTER TABLE practice ADD CONSTRAINT ck_practice_source CHECK(source_type IN ('NORMAL','WRONG','CHAPTER'));")
for command in commands:sql(command)
(root/'sql'/'05_chapter_practices.sql').write_text('-- Upgrade statements executed against the original schema.\nUSE learning_analysis;\n'+'\n'.join(commands)+'\n',encoding='utf-8')

def fingerprints():
    out={}
    for label,query in {
        'practice':"SELECT p.* FROM practice p JOIN app_user u ON u.id=p.student_id WHERE u.role='STUDENT' AND u.username<>'20240001' ORDER BY p.id;",
        'practice_item':"SELECT i.* FROM practice_item i JOIN practice p ON p.id=i.practice_id JOIN app_user u ON u.id=p.student_id WHERE u.role='STUDENT' AND u.username<>'20240001' ORDER BY i.id;",
        'accounts':"SELECT * FROM app_user ORDER BY id;"
    }.items():
        data=sql(query);out[label]={'sha256':hashlib.sha256(data).hexdigest(),'rows':len(data.splitlines())}
    return out
snapshot=root/'.local'/'backups'/'other_students_before_chapter_bank.json'
if not snapshot.exists():snapshot.write_text(json.dumps(fingerprints(),indent=2),encoding='utf-8')
print('Schema upgraded; account and other-student fingerprints saved. No records deleted.')
