"""Generate small, original teaching examples. Does not connect to a database."""
from pathlib import Path

courses = [
    ('高等数学', [('极限与导数', '基本导数'), ('积分', '基本积分')], [
        ('SINGLE', '函数 f(x)=x^2 的导数是？', ['2x','x','2','x^2'], 'A', '幂函数求导得到 2x。'),
        ('MULTIPLE', '以下哪些函数的导数恒为 0？', ['f(x)=1','f(x)=5','f(x)=x','f(x)=x^2'], 'AB', '常数函数的导数为零。'),
        ('JUDGE', '函数 f(x)=x 的导数恒为 1。', [], 'A', '一次函数 x 的导数是 1。'),
        ('SINGLE', '函数 f(x)=3x 的导数是？', ['3','x','3x','0'], 'A', '常数倍的求导规则得到 3。'),
        ('SINGLE', '函数 f(x)=2x 的一个原函数是？', ['x^2','2','2x^2','x'], 'A', 'x^2 的导数为 2x。'),
        ('JUDGE', '连续函数在区间上的定积分可以表示带符号的面积。', [], 'A', '曲线在横轴下方的部分以负面积计入。'),
    ]),
    ('数据库系统原理', [('关系数据库与 SQL', 'SQL 基础'), ('事务', '事务性质')], [
        ('SINGLE', '查询数据通常使用哪条 SQL 语句？', ['SELECT','INSERT','UPDATE','DELETE'], 'A', 'SELECT 用于查询数据。'),
        ('MULTIPLE', '以下哪些 SQL 语句会修改表中的数据？', ['INSERT','UPDATE','SELECT','DELETE'], 'ABD', 'INSERT 插入，UPDATE 修改，DELETE 删除。'),
        ('JUDGE', 'WHERE 子句可以筛选满足条件的记录。', [], 'A', 'WHERE 指定记录筛选条件。'),
        ('SINGLE', 'SQL 中按列分组使用哪个子句？', ['GROUP BY','ORDER BY','WHERE','LIMIT'], 'A', 'GROUP BY 用于分组，ORDER BY 用于排序。'),
        ('MULTIPLE', '以下哪些属于事务 ACID 性质？', ['原子性','一致性','隔离性','持久性'], 'ABCD', 'ACID 包括原子性、一致性、隔离性、持久性。'),
        ('JUDGE', '事务回滚会撤销该事务尚未提交的更改。', [], 'A', '回滚用于撤销未提交事务的更改。'),
    ]),
    ('单片机', [('数字基础', '二进制与存储'), ('输入输出', 'GPIO 基础')], [
        ('SINGLE', '一个字节通常包含多少位？', ['8','4','16','32'], 'A', '一个字节为 8 位。'),
        ('MULTIPLE', '以下哪些是二进制数码？', ['0','1','2','8'], 'AB', '二进制只使用 0 和 1。'),
        ('JUDGE', '十六进制的 F 对应十进制的 15。', [], 'A', '十六进制数码 A 至 F 分别表示 10 至 15。'),
        ('SINGLE', '二进制 1010 对应的十进制数是？', ['10','8','12','5'], 'A', '按位权展开为 8+2=10。'),
        ('MULTIPLE', 'GPIO 引脚在芯片支持及正确配置下可以用于哪些操作？', ['读取按键电平','输出高低电平','直接存放无限数据','无需驱动直接带动任意大功率电机'], 'AB', 'GPIO 可以读取和输出电平，大功率负载需适当驱动电路。'),
        ('JUDGE', '所有单片机的 GPIO 引脚都能直接承受任意电压。', [], 'B', 'GPIO 必须遵守芯片规定的电气范围。'),
    ]),
    ('数据结构', [('线性结构', '栈与队列'), ('树', '二叉树基础')], [
        ('SINGLE', '栈的典型访问顺序是？', ['后进先出','先进先出','按值排序','随机访问'], 'A', '栈在同一端入栈和出栈，后进先出。'),
        ('MULTIPLE', '以下哪些是线性数据结构？', ['顺序表','链表','栈','一般树'], 'ABC', '顺序表、链表和栈均属于线性结构。'),
        ('JUDGE', '普通队列通常遵循先进先出规则。', [], 'A', '队列在一端入队，在另一端出队。'),
        ('SINGLE', '向一个空栈依次压入 1、2、3，第一次出栈得到？', ['3','1','2','0'], 'A', '最后压入的 3 首先出栈。'),
        ('SINGLE', '二叉树每个结点最多有几个孩子？', ['2','1','3','不限'], 'A', '二叉树每个结点至多两个孩子。'),
        ('JUDGE', '二叉树的前序遍历先访问根结点。', [], 'A', '前序顺序为根、左子树、右子树。'),
    ]),
    ('计算机网络', [('网络基础', '协议与分层'), ('网络设备', '设备功能')], [
        ('SINGLE', 'HTTP 通常属于哪一层协议？', ['应用层','网络层','物理层','数据链路层'], 'A', 'HTTP 是应用层协议。'),
        ('MULTIPLE', '以下哪些属于传输层协议？', ['TCP','UDP','IP','HTTP'], 'AB', 'TCP 和 UDP 属于传输层。'),
        ('JUDGE', 'IPv4 地址的长度为 32 位。', [], 'A', 'IPv4 使用 32 位地址。'),
        ('SINGLE', 'DNS 的主要用途是？', ['域名解析','压缩图片','编辑网页','给 CPU 供电'], 'A', 'DNS 将域名解析为相关资源记录。'),
        ('SINGLE', '路由器的主要功能是？', ['在不同网络间转发数据包','打印文件','存储网页样式','将所有信号转换成声音'], 'A', '路由器根据路由信息转发网络层数据包。'),
        ('JUDGE', '交换机和路由器在所有场景下功能都完全相同。', [], 'B', '二者典型工作的层次和转发依据不同。'),
    ]),
]

def quote(v):
    return 'NULL' if v is None else "'" + str(v).replace("'", "''") + "'"

sql = ['-- Original minimal demonstration questions; no account passwords in this file.',
       'USE learning_analysis;', 'START TRANSACTION;']
qid = 0
for cid, (name, chapters, questions) in enumerate(courses, 1):
    sql.append(f'INSERT INTO course(id,name,description,sort_order) VALUES({cid},{quote(name)},{quote("课程设计示例题库")},{cid});')
    for pos, (ch, kp) in enumerate(chapters, 1):
        ident = cid * 10 + pos
        sql.append(f'INSERT INTO chapter(id,course_id,name,sort_order) VALUES({ident},{cid},{quote(ch)},{pos});')
        sql.append(f'INSERT INTO knowledge_point(id,chapter_id,name,sort_order) VALUES({ident},{ident},{quote(kp)},1);')
    # Extra knowledge tag demonstrates a question belonging to multiple points.
    extra=cid*10+3
    sql.append(f'INSERT INTO knowledge_point(id,chapter_id,name,sort_order) VALUES({extra},{cid*10+1},{quote("基础概念辨析")},2);')
    for n, (typ, stem, opts, answer, explanation) in enumerate(questions):
        qid += 1
        ch = cid*10 + (1 if n<4 else 2)
        if typ == 'JUDGE': opts=['正确','错误',None,None]
        values = [str(qid), str(ch), quote(typ), quote(stem), *map(quote,opts), quote(answer), quote(explanation)]
        sql.append('INSERT INTO question(id,chapter_id,question_type,stem,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES('+','.join(values)+');')
        sql.append(f'INSERT INTO question_knowledge VALUES({qid},{ch});')
        if n==0: sql.append(f'INSERT INTO question_knowledge VALUES({qid},{extra});')
sql.append('COMMIT;')
root=Path(__file__).resolve().parents[1]
(root/'sql'/'02_demo_data.sql').write_text('\n'.join(sql)+'\n',encoding='utf-8')
print(f'Generated {len(courses)} courses and {qid} questions.')
