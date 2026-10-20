"""Generate additive, repeatable example questions grouped by knowledge point.

Existing questions and practice history are not overwritten. Execute the
generated sql/04_expand_question_bank.sql after the original seed scripts.
"""
from pathlib import Path

# Each knowledge point gets three additional original examples: single,
# multiple and true/false. The original examples remain available.
groups = {
11: [
('SINGLE','函数 f(x)=x^3 的导数是？',['3x^2','x^2','3x','x^3'],'A','幂函数求导公式为 (x^n)\'=nx^(n-1)。'),
('MULTIPLE','以下哪些函数的导数恒为 2？',['2x','2x+1','x^2','2'],'AB','一次函数 2x 加任意常数的导数均为 2。'),
('JUDGE','两个可导函数之和的导数等于它们导数之和。',[],'A','求导具有加法法则。')],
12: [
('SINGLE','函数 f(x)=1 的一个原函数是？',['x','0','x^2','1'],'A','x 的导数为 1。'),
('MULTIPLE','以下哪些是函数 f(x)=2x 的原函数？',['x^2','x^2+3','2x','x^3'],'AB','两个函数求导均得到 2x，原函数可以相差一个常数。'),
('JUDGE','同一函数的两个原函数在同一区间上可以相差一个常数。',[],'A','不定积分的结果包含任意常数。')],
13: [
('SINGLE','函数 f(x)=x^4 的导数是？',['4x^3','x^3','4x','x^4'],'A','使用幂函数求导公式得到 4x^3。'),
('MULTIPLE','以下哪些求导结果正确？',['(x^2)\'=2x','(x^3)\'=3x^2','(x^4)\'=x^3','(x)\'=0'],'AB','幂函数求导时指数成为系数，指数减一。'),
('JUDGE','函数 f(x)=5x^2 的导数是 10x。',[],'A','常数倍法则与幂函数求导法则给出 10x。')],
21: [
('SINGLE','SQL 中用于排序的子句是？',['ORDER BY','GROUP BY','WHERE','HAVING'],'A','ORDER BY 用于对查询结果排序。'),
('MULTIPLE','以下哪些聚合函数可用于 SQL 统计？',['COUNT','SUM','AVG','WHERE'],'ABC','COUNT、SUM 和 AVG 是聚合函数，WHERE 是筛选子句。'),
('JUDGE','SQL 中 DELETE 语句用于向表中新增一条记录。',[],'B','DELETE 删除记录，INSERT 新增记录。')],
22: [
('SINGLE','事务全部成功或全部撤销主要体现什么性质？',['原子性','隔离性','排序性','可见性'],'A','原子性要求事务操作作为整体完成或撤销。'),
('MULTIPLE','以下哪些语句直接用于事务的结束控制？',['COMMIT','ROLLBACK','SELECT','ORDER BY'],'AB','COMMIT 提交事务，ROLLBACK 回滚事务。'),
('JUDGE','事务提交后的结果应在系统故障恢复后仍然保留，这体现持久性。',[],'A','持久性要求已提交结果持久保存。')],
23: [
('SINGLE','查询 student 表的所有列，可使用哪条语句？',['SELECT * FROM student','DELETE FROM student','UPDATE student','DROP TABLE student'],'A','SELECT * FROM 表名用于查询所有列。'),
('MULTIPLE','查询时，以下哪些条件可用于 WHERE 子句？',['score > 60','name = \'张三\'','age >= 18','ORDER BY score'],'ABC','比较表达式可以作为筛选条件，ORDER BY 是排序子句。'),
('JUDGE','SELECT name FROM student 会只选择 name 这一列。',[],'A','SELECT 后面的列清单决定返回的列。')],
31: [
('SINGLE','两个字节一共包含多少位？',['16','2','8','32'],'A','一个字节 8 位，两个字节为 16 位。'),
('MULTIPLE','以下哪些说法正确？',['一个字节通常是8位','四位二进制可以表示16种状态','二进制包含数码2','一位只能表示十种状态'],'AB','一个字节 8 位，四位有 2^4=16 种组合。'),
('JUDGE','无符号的 8 位二进制数可以表示 0 到 255。',[],'A','8 位可以表示 256 种状态，范围为 0 至 255。')],
32: [
('SINGLE','读取按键引脚电平通常需要配置为什么模式？',['输入模式','程序下载模式','任意高压模式','无限输出模式'],'A','读取外部电平通常使用输入模式。'),
('MULTIPLE','使用 GPIO 驱动外设时，以下哪些因素需要关注？',['允许的电压范围','允许的输出电流','外设是否需要驱动电路','只看引脚颜色'],'ABC','GPIO 使用必须符合芯片电气参数及外设负载要求。'),
('JUDGE','按键输入电路可以使用上拉或下拉电阻形成确定的默认电平。',[],'A','上拉或下拉可以避免未按下时输入悬空。')],
33: [
('SINGLE','四个字节一共包含多少位？',['32','4','16','64'],'A','4 乘以 8 等于 32 位。'),
('MULTIPLE','以下哪些换算正确？',['1字节=8位','2字节=16位','4字节=4位','8位=8字节'],'AB','字节与位的换算比例是 1 比 8。'),
('JUDGE','一个二进制位可以表示 0 或 1。',[],'A','位是二进制信息单位，具有两种状态。')],
41: [
('SINGLE','队列依次入队 1、2、3，首次出队得到？',['1','2','3','0'],'A','普通队列遵循先进先出。'),
('MULTIPLE','以下哪些说法正确？',['栈通常后进先出','队列通常先进先出','栈只能保存整数','队列必然自动排序'],'AB','栈与队列的主要区别是允许的访问次序。'),
('JUDGE','链表结点在内存中必须连续存放。',[],'B','链表通过链接关系组织结点，不要求连续存储。')],
42: [
('SINGLE','二叉树的中序遍历顺序是？',['左子树、根、右子树','根、左子树、右子树','左子树、右子树、根','根、右子树、左子树'],'A','中序遍历在左子树后、右子树前访问根。'),
('MULTIPLE','以下哪些属于二叉树的常见遍历方式？',['前序遍历','中序遍历','后序遍历','冒泡遍历'],'ABC','前序、中序和后序是三种常见深度优先遍历。'),
('JUDGE','没有孩子的树结点称为叶子结点。',[],'A','叶子结点的度为零。')],
43: [
('SINGLE','栈顶元素被移除的操作称为？',['出栈','入队','排序','分组'],'A','出栈移除当前栈顶元素。'),
('MULTIPLE','以下哪些场景常用到栈？',['括号匹配','函数调用管理','撤销操作记录','按优先级自动排序所有元素'],'ABC','栈适合保存需要按相反次序恢复或处理的信息。'),
('JUDGE','空栈没有可以直接出栈的元素。',[],'A','出栈前应检查栈是否为空。')],
51: [
('SINGLE','IP 协议通常属于哪一层？',['网络层','应用层','表示层','会话层'],'A','IP 属于网络层。'),
('MULTIPLE','以下哪些属于应用层协议？',['HTTP','DNS','TCP','IP'],'AB','HTTP 和 DNS 属于应用层，TCP 属于传输层，IP 属于网络层。'),
('JUDGE','TCP 和 UDP 都属于传输层协议。',[],'A','二者为应用提供不同的传输服务。')],
52: [
('SINGLE','普通以太网交换机通常根据什么地址转发帧？',['MAC地址','文件名','网页标题','CPU型号'],'A','普通二层交换机主要根据 MAC 地址表转发帧。'),
('MULTIPLE','以下哪些属于常见网络设备？',['交换机','路由器','集线器','文本编辑器'],'ABC','交换机、路由器和集线器属于网络设备。'),
('JUDGE','路由器可以连接不同 IP 网络。',[],'A','路由器在不同 IP 网络间转发数据包。')],
53: [
('SINGLE','用于将域名解析为相关资源记录的协议是？',['DNS','TCP','UDP','IP'],'A','DNS 提供域名解析服务。'),
('MULTIPLE','以下哪些属于应用层常见功能？',['网页内容传输','域名解析','发送电子邮件','在链路上传输电气信号'],'ABC','网页、域名解析和电子邮件是应用层功能，电气信号传输属于物理层。'),
('JUDGE','HTTP 可以用于浏览器与 Web 服务器之间传输请求和响应。',[],'A','HTTP 定义 Web 请求和响应的语义。')],
}
names={13:'幂函数求导',23:'数据查询',33:'位与字节',43:'栈的操作',53:'应用层协议'}
def quote(v):return 'NULL' if v is None else "'"+str(v).replace("'","''")+"'"
sql=['-- Additive topic-based examples. Existing question text and answers are preserved.', 'USE learning_analysis;','START TRANSACTION;']
for k,name in names.items():sql.append(f'UPDATE knowledge_point SET name={quote(name)} WHERE id={k};')
qid=1000
for knowledge,rows in groups.items():
 chapter=knowledge if knowledge%10!=3 else knowledge-2
 for kind,stem,options,correct,explanation in rows:
  qid+=1
  if kind=='JUDGE':options=['正确','错误',None,None]
  values=[str(qid),str(chapter),quote(kind),quote(stem),*map(quote,options),quote(correct),quote(explanation)]
  sql.append('INSERT INTO question(id,chapter_id,question_type,stem,option_a,option_b,option_c,option_d,correct_answer,explanation) SELECT '+','.join(values)+f' WHERE NOT EXISTS(SELECT 1 FROM question WHERE id={qid});')
  sql.append(f'INSERT INTO question_knowledge(question_id,knowledge_id) SELECT {qid},{knowledge} WHERE NOT EXISTS(SELECT 1 FROM question_knowledge WHERE question_id={qid} AND knowledge_id={knowledge});')
sql.append('COMMIT;')
root=Path(__file__).resolve().parents[1]
(root/'sql'/'04_expand_question_bank.sql').write_text('\n'.join(sql)+'\n',encoding='utf-8')
print(f'Generated {qid-1000} additional questions across {len(groups)} knowledge points.')
