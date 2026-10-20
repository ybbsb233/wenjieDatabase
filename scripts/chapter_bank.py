"""Build the current 5 x 5 x 20 chapter bank without altering old questions.

Every chapter has two knowledge points with ten questions each. Each topic
has five single-choice, two multiple-choice, and three judgment questions.
Fixed chapter sets always use all twenty questions in their stored ID order.
"""
import json
from pathlib import Path

def fact(label, correct, *wrong):
    assert len(wrong)==3 and len(set((correct,*wrong)))==4
    return (label,correct,*wrong)

def topic(name,*facts):
    assert len(facts)==5
    return name,list(facts)

def arithmetic_topic(name,label,values):
    return topic(name,*[fact(label.format(n=n),str(answer),str(answer+1),str(answer+2),str(answer+3)) for n,answer in values])

bank=[
('高等数学',[
 ('极限与连续',[
  arithmetic_topic('基本极限','当 x 趋于 {n} 时，函数 x+2 的极限',[(n,n+2) for n in range(1,6)]),
  topic('连续性',
   fact('函数在某点连续时，函数值与该点极限的关系','相等','必不相等','互为相反数','必须都为零'),
   fact('多项式函数在实数范围内的连续性','处处连续','处处不连续','只在零点连续','只在整数点连续'),
   fact('两个在某点连续的函数之和在该点的性质','连续','一定不连续','一定为零','一定无定义'),
   fact('函数在某点连续的必要条件之一','该点函数值存在','该点函数值必须为零','函数必须为常数','导数必须为正'),
   fact('函数 f(x)=3 在 x=2 处的函数值','3','0','2','6'))]),
 ('导数与微分',[
  arithmetic_topic('幂函数求导','函数 f(x)=x^{n} 在 x=1 处的导数',[(n,n) for n in range(2,7)]),
  topic('导数的应用',
   fact('可导函数在某区间内导数恒大于零时的单调性','严格递增','严格递减','恒为零','必为常数'),
   fact('曲线在某点切线斜率对应的量','该点导数','该点横坐标','函数周期','定积分下限'),
   fact('可导函数在区间内导数恒为零时的函数类型','常数函数','严格递增函数','严格递减函数','任意不连续函数'),
   fact('路程函数对时间求导得到的量','瞬时速度','累计路程','物体质量','时间间隔'),
   fact('可导函数内点取得局部极值时导数满足的必要条件','导数为零','导数必为一','导数必为负','导数不存在'))]),
 ('不定积分',[
  topic('基本积分公式',
   fact('函数 2x 的一个原函数','x^2','2','x','2x^2'),
   fact('函数 3x^2 的一个原函数','x^3','x^2','3x','3x^3'),
   fact('函数 cos(x) 的一个原函数','sin(x)','cos(x)','-sin(x)','x'),
   fact('函数 1 的一个原函数','x','0','1','x^2'),
   fact('函数 e^x 的一个原函数','e^x','x','ln(x)','x^2')),
  topic('积分性质',
   fact('同一区间上同一函数的两个原函数之差','常数','必为零','必为自变量','必为无穷大'),
   fact('不定积分结果中 C 通常表示的量','任意常数','固定为零的量','积分上限','函数导数'),
   fact('不定积分与求导的关系','互为逆运算','完全相同的运算','无任何联系','都只适用于常数'),
   fact('常数倍函数积分的常数因子处理方式','可提出积分号','必须平方','必须变成零','必须取倒数'),
   fact('函数和的不定积分的计算规则','可分别积分再相加','必须将结果相乘','只积分第一项','必须先求极值'))]),
 ('定积分',[
  arithmetic_topic('定积分计算','常数函数 f(x)=1 在区间 [0,{n}] 上的定积分',[(n,n) for n in range(1,6)]),
  topic('定积分的性质与应用',
   fact('积分上限与下限相同时的定积分值','0','1','无穷大','无法确定'),
   fact('交换定积分上下限后结果的变化','变为相反数','保持不变','变为平方','变为倒数'),
   fact('非负连续函数在区间上的定积分可表示的几何量','曲线下方的面积','曲线长度的平方','函数最大值','区间中点'),
   fact('积分区间可加性中的分割点位置','原积分区间内','必须在区间外','必须是零','必须是极值点'),
   fact('速度恒为正时，对速度关于时间积分得到的量','该时间段路程','瞬时加速度','物体质量','时间倒数'))]),
 ('多元函数基础',[
  arithmetic_topic('偏导数','函数 f(x,y)=x+{n}y 对 y 的偏导数',[(n,n) for n in range(1,6)]),
  topic('二重积分基础',
   fact('对变量 x 求偏导时，其他独立变量的处理方式','视为常量','都视为零','都视为 x','必须全部求导'),
   fact('二重积分的积分区域所在空间','二维平面','只能是一条直线','必须为三维球面','只能是单个点'),
   fact('函数 1 在平面区域上的二重积分所表示的量','区域面积','区域周长','区域中心横坐标','区域最高点'),
   fact('连续函数在矩形区域上的二重积分常用计算形式','累次积分','只求一次导数','只求最大值','只求边界长度'),
   fact('矩形区域 [0,2]×[0,3] 的面积','6','5','8','9'))])]),
('数据库系统原理',[
 ('关系模型与完整性',[
  topic('关系模型',
   fact('关系数据库中一张二维表通常称为','关系','进程','线程','文件夹'),
   fact('关系表中的一行通常称为','元组','属性名','数据库实例','索引页'),
   fact('关系表中的一列通常称为','属性','元组','事务','数据文件'),
   fact('属性允许取值的集合通常称为','域','主码','日志','锁'),
   fact('关系数据库用于组织数据的主要结构','二维表','音频波形','屏幕像素','CPU寄存器')),
  topic('键与完整性',
   fact('主键值应满足的基本要求','唯一且非空','允许全部重复','必须是中文','必须为零'),
   fact('外键主要用于表示的联系','表之间的引用关系','页面颜色关系','文件大小关系','程序编译关系'),
   fact('实体完整性主要约束的对象','主键','页面标题','CSS样式','服务器端口'),
   fact('参照完整性主要维护的关系','外键与被引用键','字体与字号','线程与颜色','文件与图标'),
   fact('禁止年龄为负数属于','用户定义完整性','页面布局','网络路由','字符编码转换'))]),
 ('SQL 数据查询',[
  topic('基础查询',
   fact('SQL 查询数据使用的关键字','SELECT','DELETE','UPDATE','INSERT'),
   fact('SQL 指定数据来源表使用的子句','FROM','ORDER BY','LIMIT','HAVING'),
   fact('SQL 筛选记录常用的子句','WHERE','VALUES','SET','CREATE'),
   fact('SQL 对查询结果排序的子句','ORDER BY','GROUP BY','INSERT','ALTER'),
   fact('SQL 消除查询结果重复行的关键字','DISTINCT','ALL','VALUES','DROP')),
  topic('分组与聚合',
   fact('SQL 统计记录条数常用的聚合函数','COUNT','SUM','MAX','AVG'),
   fact('SQL 计算数值总和的聚合函数','SUM','COUNT','MIN','AVG'),
   fact('SQL 计算平均值的聚合函数','AVG','MAX','MIN','SUM'),
   fact('SQL 按列分组使用的子句','GROUP BY','ORDER BY','VALUES','SET'),
   fact('SQL 对分组结果进行条件筛选的子句','HAVING','INSERT','UPDATE','DROP'))]),
 ('SQL 更新与约束',[
  topic('数据修改',
   fact('向表中新增记录使用的关键字','INSERT','SELECT','DROP','ALTER'),
   fact('修改表中已有记录使用的关键字','UPDATE','CREATE','SELECT','DROP'),
   fact('删除表中记录使用的关键字','DELETE','SELECT','CREATE','ALTER'),
   fact('UPDATE 中指定修改内容使用的关键字','SET','FROM','GROUP BY','ORDER BY'),
   fact('执行无 WHERE 条件的 DELETE 对记录的通常影响','删除表中所有记录','只删第一条','自动新增一条','只修改表名')),
  topic('表结构与约束',
   fact('创建数据表使用的 SQL 命令','CREATE TABLE','UPDATE TABLE','SELECT TABLE','COMMIT TABLE'),
   fact('修改已有表结构使用的命令','ALTER TABLE','INSERT TABLE','SELECT TABLE','ROLLBACK TABLE'),
   fact('限制字段不能为 NULL 的约束','NOT NULL','ORDER BY','GROUP BY','DEFAULT NULL'),
   fact('限制字段组合不重复的约束','UNIQUE','VALUES','LIMIT','HAVING'),
   fact('定义字段取值条件常用的约束','CHECK','FROM','WHERE JOIN','OFFSET'))]),
 ('函数依赖与规范化',[
  topic('函数依赖',
   fact('X 的值唯一确定 Y 的值时通常记作','X→Y','Y→X 必然成立','X=0','Y=0'),
   fact('学生学号唯一确定姓名时，学号到姓名的联系','函数依赖','网络连接','排序关系','文件包含'),
   fact('若 X→Y 且 Y→Z，则可推出','X→Z','Z→X 必然成立','X必须为空','Y必须重复'),
   fact('复合键的一部分决定非主属性通常涉及','部分函数依赖','页面继承','物理寻址','字符排序'),
   fact('分析函数依赖的主要用途之一','设计合理关系模式','选择网页配色','调整网速','压缩图片')),
  topic('范式与冗余',
   fact('第一范式对属性值的基本要求','不可再分的原子值','必须全为数字','必须全为中文','必须全为NULL'),
   fact('规范化设计希望减少的问题','数据冗余与更新异常','浏览器窗口数量','屏幕分辨率','网络协议数量'),
   fact('第二范式需要消除的典型问题','非主属性对候选键的部分依赖','所有外键','所有主键','所有字符串'),
   fact('第三范式需要消除的典型问题','非主属性对候选键的传递依赖','所有查询','所有索引','所有表联系'),
   fact('规范化拆表后通常用于恢复数据联系的方式','通过键连接查询','拼接页面颜色','删除主键','禁用外键'))]),
 ('事务与并发控制',[
  topic('事务性质',
   fact('事务操作全部成功或全部撤销体现的性质','原子性','排序性','可打印性','图形性'),
   fact('事务提交后结果应持久保存体现的性质','持久性','临时性','可重复性','随机性'),
   fact('提交事务使用的 SQL 关键字','COMMIT','ROLLBACK','SELECT','WHERE'),
   fact('撤销未提交事务使用的关键字','ROLLBACK','COMMIT','GROUP BY','ORDER BY'),
   fact('并发事务之间按隔离级别控制相互影响体现的性质','隔离性','字符性','文件性','排序性')),
  topic('并发与锁',
   fact('读取其他事务尚未提交的数据通常称为','脏读','索引扫描','表连接','数据压缩'),
   fact('同一事务两次读取同一行得到不同已提交值通常称为','不可重复读','语法错误','主键冲突','字符截断'),
   fact('多个事务循环等待彼此持有的资源通常称为','死锁','分组','排序','投影'),
   fact('并发控制中锁的主要作用','协调对共享数据的访问','改变字体','生成图片','提高屏幕亮度'),
   fact('读取已提交数据这一隔离级别的英文名称','READ COMMITTED','READ IMAGE','WRITE ONLY','SORTED DATA'))])]),
('单片机',[
 ('数制与存储',[
  arithmetic_topic('二进制换算','二进制数 {n:b} 对应的十进制数',[(n,n) for n in range(4,9)]),
  arithmetic_topic('位与字节','{n} 个字节包含的二进制位数',[(n,n*8) for n in range(1,6)])]),
 ('GPIO 输入输出',[
  topic('输入与电平',
   fact('GPIO 读取按键状态通常使用的模式','输入模式','程序下载模式','高压供电模式','内存清空模式'),
   fact('上拉电阻通常将未被拉低的输入连接到的电平','高电平','必为负电平','任意超高电压','完全悬空'),
   fact('下拉电阻通常用于建立的默认电平','低电平','任意超高电平','交流市电','未知悬空状态'),
   fact('GPIO 电压范围应参考的资料','芯片数据手册','网页字体表','图片尺寸','键盘布局'),
   fact('机械按键短时间多次跳变通常需要的处理','消抖','图片压缩','更改网关','磁盘格式化')),
  topic('输出与驱动',
   fact('GPIO 输出模式主要用于','输出高低电平','存储无限数据','自动提供任意大电流','改变操作系统'),
   fact('LED 串联电阻的常见作用','限制电流','无限增大电流','存储程序','生成串口协议'),
   fact('GPIO 驱动大功率负载通常需要','额外驱动电路','直接忽略电流限制','只修改变量名','只改变注释'),
   fact('输出电流超过芯片允许值可能造成的后果','损坏器件','自动扩大存储器','提高代码正确率','增加指令集'),
   fact('PWM 调光常通过改变的参数','占空比','源文件名字','引脚颜色','注释长度'))]),
 ('定时器与中断',[
  topic('定时与计数',
   fact('定时器常用来实现的功能','周期事件','任意电压转换','无限数据存储','网页排版'),
   fact('计数器通常用于统计的量','输入事件次数','程序员人数','图片颜色数','文件后缀数'),
   fact('定时器计数达到上限并回绕常称为','溢出','主键冲突','域名解析','链表插入'),
   fact('计数频率固定时，计数次数增多对应的时间','更长','必为零','必为负','完全无关'),
   fact('软件延时相较硬件定时器的常见不足','占用CPU执行时间','不需要CPU','一定更精准','可以无限并行')),
  topic('中断基础',
   fact('CPU 响应中断时通常转去执行的程序','中断服务程序','网页样式表','数据库安装程序','磁盘分区工具'),
   fact('中断服务程序结束后通常的执行方向','返回被打断的流程','永久停止所有程序','自动重装系统','删除源代码'),
   fact('多个中断请求同时出现时用于区分处理先后的机制','中断优先级','变量颜色','图片大小','文件排序'),
   fact('中断服务程序通常应遵循的原则','尽量简短','无限循环等待','包含所有业务逻辑','始终阻塞其他任务'),
   fact('用于记录某中断事件已发生的标志通常称为','中断标志位','主键','域名','文件扩展名'))]),
 ('串行通信',[
  topic('UART 通信',
   fact('UART 常用的发送引脚标记','TX','RX','GND','VCC'),
   fact('UART 常用的接收引脚标记','RX','TX','GND','VCC'),
   fact('两设备进行 UART 通信时需匹配的参数之一','波特率','源代码行数','外壳颜色','文件夹名称'),
   fact('常见异步串口数据帧中标识开始的位','起始位','主键位','页码位','索引位'),
   fact('两设备通过单端串口连接通常需要共享的参考','地线','网页标题','数据库表名','文本编码变量名')),
  topic('常用串行总线',
   fact('I2C 的串行数据线通常标记为','SDA','SCL','MOSI','MISO'),
   fact('I2C 的串行时钟线通常标记为','SCL','SDA','TX','RX'),
   fact('SPI 的主机输出从机输入线通常标记为','MOSI','MISO','SDA','GND'),
   fact('SPI 的主机输入从机输出线通常标记为','MISO','MOSI','SCL','VCC'),
   fact('SPI 用于选择目标从设备的信号通常称为','片选信号','主键信号','分组信号','回滚信号'))]),
 ('嵌入式程序基础',[
  topic('C 语言基础',
   fact('C 语言条件分支常用的关键字','if','while','return','break'),
   fact('C 语言按条件反复执行常用的关键字','while','if','return','sizeof'),
   fact('C 语言获取对象所占字节数常用的运算符','sizeof','return','break','continue'),
   fact('数组的首个元素下标通常为','0','1','-1','数组长度'),
   fact('C 语言函数返回值常用的关键字','return','while','for','switch')),
  topic('程序流程与资源',
   fact('嵌入式程序启动时通常首先进行的操作','硬件初始化','随机删除代码','断开全部电源','清空所有外设'),
   fact('主循环常用于执行的任务','反复检查和处理事件','永久停止CPU','直接产生无限电流','更换芯片引脚'),
   fact('看门狗定时器常用来处理的问题','程序失控或长时间卡死','网页字体过小','图片分辨率过高','学号重复'),
   fact('单片机程序设计需要关注的限制','存储器与处理资源','只有网页颜色','只有变量名字','只有文件后缀'),
   fact('调试串口输出常用于','观察运行状态','扩大物理内存','替代所有电路','直接修复硬件短路'))])]),
('数据结构',[
 ('线性表',[
  topic('顺序表',
   fact('顺序表中元素的典型存储方式','连续存储','任意分散且无索引','只存磁带','必须放入不同机器'),
   fact('顺序表按合法下标访问元素的时间复杂度','O(1)','O(n)','O(n^2)','O(2^n)'),
   fact('顺序表中间插入元素常需执行的操作','移动后续元素','删除全部元素','更改网络地址','重新编译数据库'),
   fact('顺序表逻辑上表示的数据结构类型','线性结构','一般图','多叉树','随机文件集'),
   fact('顺序表当前存放元素个数通常称为','长度','树高','图的度','根结点')),
  topic('链表',
   fact('链表连接结点主要依赖的机制','指针或链接','连续下标必相邻','网页超链接文字','磁盘文件名'),
   fact('单链表结点通常包含的数据之外的字段','后继链接','根目录名','完整路由表','屏幕坐标'),
   fact('链表结点在内存中的位置要求','不要求连续','必须全部连续','必须在同一字节','必须在不同机器'),
   fact('单链表访问第 k 个结点通常需要','从起点沿链接查找','直接用地址公式恒定访问','删除前k个结点','对所有结点排序'),
   fact('单链表最后一个结点的后继链接通常为','空链接','必须指向自身','必须指向任意对象','必须为整数1'))]),
 ('栈与队列',[
  topic('栈',
   fact('栈的典型访问次序','后进先出','先进先出','自动按值排序','随机访问'),
   fact('向栈中添加元素的操作名称','入栈','出队','回滚','分组'),
   fact('移除栈顶元素的操作名称','出栈','入队','排序','映射'),
   fact('依次将 1、2、3 压入空栈后首次弹出的值','3','1','2','0'),
   fact('括号匹配算法常用的辅助结构','栈','任意二叉搜索树','邻接矩阵','路由表')),
  topic('队列',
   fact('普通队列的典型访问次序','先进先出','后进先出','按值自动排序','随机出队'),
   fact('普通队列新增元素所在的一端','队尾','队头','任意中间位置','根结点'),
   fact('普通队列移除元素所在的一端','队头','队尾','任意中间位置','叶子结点'),
   fact('依次将 1、2、3 加入空队列后首次取出的值','1','2','3','0'),
   fact('广度优先搜索常用的辅助结构','队列','只读常量','排序函数名','主键索引名'))]),
 ('树与二叉树',[
  topic('二叉树基础',
   fact('二叉树每个结点最多拥有的孩子数','2','1','3','4'),
   fact('没有孩子的树结点通常称为','叶子结点','父结点','根目录','祖先结点'),
   fact('树中没有父结点的起始结点称为','根结点','叶子结点必然成立','后继结点','尾结点'),
   fact('非空树中边数与结点数 n 的关系','n-1','n+1','2n','n^2'),
   fact('二叉树左孩子与右孩子的区别','位置有区别','永远相同','不允许右孩子','不允许左孩子')),
  topic('二叉树遍历',
   fact('前序遍历的访问顺序','根左右','左根右','左右根','右根左'),
   fact('中序遍历的访问顺序','左根右','根左右','左右根','根右左'),
   fact('后序遍历的访问顺序','左右根','根左右','左根右','根右左'),
   fact('层序遍历常用的辅助结构','队列','后缀字符串','随机哈希键','文件扩展名'),
   fact('前序遍历最先访问的结点','根结点','最右叶子必然成立','最左叶子必然成立','最后插入结点必然成立'))]),
 ('图',[
  topic('图的基本概念',
   fact('图的基本组成','顶点和边','行和列名','像素和颜色','页面和字体'),
   fact('边有方向的图通常称为','有向图','无向图','空栈','循环队列'),
   fact('表示顶点之间连接情况的二维结构通常称为','邻接矩阵','字符数组长度','栈顶指针','函数参数表'),
   fact('邻接表通常用于存储的内容','每个顶点的相邻顶点','单个顶点颜色','数据库密码','程序编译记录'),
   fact('无向图所有顶点度数之和与边数 m 的关系','2m','m','m+1','m^2')),
  topic('图的遍历',
   fact('DFS 的中文名称','深度优先搜索','广度优先搜索','直接插入排序','二分查找'),
   fact('BFS 的中文名称','广度优先搜索','深度优先搜索','快速排序','顺序查找'),
   fact('深度优先搜索可使用的典型机制','递归或栈','只使用一条SQL','只使用平均值','只使用字符编码'),
   fact('广度优先搜索通常使用的结构','队列','主键约束','文本编辑器','常量字符串'),
   fact('图遍历中访问标记的常见用途','避免重复访问','修改顶点名称','改变边权单位','扩大磁盘容量'))]),
 ('查找与排序',[
  topic('查找',
   fact('二分查找对线性表的关键要求','按关键字有序','必须全为相同值','必须全为字符串','必须无元素'),
   fact('顺序查找的基本方法','逐个比较','始终只看中间值','自动删除目标','先反转所有字符'),
   fact('有序数组二分查找的时间复杂度','O(log n)','O(n^2)','O(2^n)','O(n!)'),
   fact('哈希查找主要依赖的映射','关键字到存储位置','字体到颜色','时间到屏幕大小','页码到注释'),
   fact('查找失败通常表示的情况','没有找到匹配关键字','数据必须为空','CPU已经损坏','排序已经完成')),
  topic('排序',
   fact('冒泡排序反复比较的元素','相邻元素','仅首尾元素','仅最大元素','所有元素与零'),
   fact('选择排序每轮通常确定的元素','剩余范围的最小或最大元素','任意随机元素','永远第一个元素','所有重复元素'),
   fact('插入排序每轮将元素插入的部分','已排序部分','任意外部文件','空白数据库','完全无关数组'),
   fact('升序排序后元素的基本关系','从小到大','从大到小','全部相等','完全随机'),
   fact('排序稳定性关注的对象','相同关键字元素的相对次序','CPU主频','文件颜色','数据库用户名'))])]),
('计算机网络',[
 ('网络体系结构',[
  topic('分层结构',
   fact('HTTP 通常所属层次','应用层','网络层','数据链路层','物理层'),
   fact('TCP 通常所属层次','传输层','物理层','数据链路层','应用层'),
   fact('IP 通常所属层次','网络层','应用层','物理层','表示层'),
   fact('以太网 MAC 帧主要所属层次','数据链路层','应用层','会话层','传输层'),
   fact('电气信号传输主要对应的层次','物理层','应用层','网络层','传输层')),
  topic('协议基础',
   fact('网络协议主要规定的内容','通信规则','网页美术风格','显示器尺寸','文件夹图标'),
   fact('封装过程中通常添加的信息','各层协议头部等控制信息','随机删除数据','只添加图片','只修改文件名'),
   fact('接收端按层解析协议控制信息的过程通常称为','解封装','磁盘分区','函数重载','数据规范化'),
   fact('网络分层的一个主要目的','降低设计复杂度','保证永不丢包','消除所有硬件','不再需要协议'),
   fact('网络中通信端点交换的基本内容','按协议组织的数据','只能是纸张','只能是电池','只能是源代码注释'))]),
 ('数据链路层',[
  topic('以太网与MAC',
   fact('常见以太网 MAC 地址的长度','48位','8位','16位','128位'),
   fact('MAC 地址主要用于的通信范围','局域网链路','只用于邮件标题','只用于网页排版','只用于数据库表名'),
   fact('以太网帧携带的地址类型','源MAC和目的MAC','只有文件名','只有邮箱密码','只有CPU型号'),
   fact('链路层数据单位通常称为','帧','事务','元组','函数'),
   fact('交换机学习 MAC 地址主要观察的信息','接收帧的源MAC与入端口','网页标题','数据库主键','文件大小')),
  topic('交换机转发',
   fact('普通二层交换机主要依据的转发表','MAC地址表','域名列表','用户密码表','网页样式表'),
   fact('已知目的 MAC 所在端口时交换机通常的动作','转发到对应端口','永远发往所有端口','删除整个地址表','重装操作系统'),
   fact('交换机 MAC 表记录的重要对应关系','MAC地址与端口','字体与字号','文件名与扩展名','学生与成绩'),
   fact('普通以太网交换机典型工作的层次','数据链路层','应用层','表示层','会话层'),
   fact('广播帧在同一 VLAN 内通常的转发方式','向其他适用端口泛洪','只发送给原入端口','只发给管理员邮箱','自动转换成SQL'))]),
 ('网络层',[
  topic('IPv4 地址',
   fact('IPv4 地址的长度','32位','8位','48位','128位'),
   fact('常见 IPv4 点分十进制地址的段数','4','2','6','8'),
   fact('IPv4 每个十进制段的数值范围','0到255','0到999','1到1000','负128到127'),
   fact('用于区分 IPv4 网络部分与主机部分的参数','子网掩码','网页标题','MAC表名称','TCP载荷长度'),
   fact('127.0.0.1 常用于表示的地址类型','本机回环地址','任意公网广播地址','MAC地址','DNS域名')),
  topic('路由基础',
   fact('路由器的主要任务','在不同网络间转发数据包','生成网页样式','给所有设备充电','保存所有数据库密码'),
   fact('路由转发常查阅的信息','路由表','字体表','SQL表结构','浏览器收藏夹'),
   fact('主机访问外部网络常配置的转发出口','默认网关','默认字体','默认文件名','默认注释'),
   fact('IP 数据包在网络层的主要寻址依据','IP地址','文件创建时间','图片像素数量','字符行数'),
   fact('路由表中下一跳通常指向的对象','后续转发设备','必须为网页服务器','必须为数据库用户','必须为显示器'))]),
 ('传输层',[
  topic('TCP',
   fact('TCP 的连接特点','面向连接','只提供广播','没有端口','只用于图片'),
   fact('TCP 建立连接的常见握手次数','3','1','2','6'),
   fact('TCP 为应用提供的典型数据形式','字节流','数据库表','屏幕像素','磁盘分区'),
   fact('TCP 使用端口号主要用于区分的对象','应用通信端点','显示器型号','CPU核心颜色','文件后缀'),
   fact('TCP 发现数据丢失时常用的可靠性机制','重传','自动删除所有应用','修改MAC地址长度','关闭全部路由器')),
  topic('UDP',
   fact('UDP 的连接特点','无连接','必须三次握手','必须四次握手','只支持有线网'),
   fact('UDP 传输时保留的应用数据边界','报文边界','SQL表边界','网页布局边界','文件夹边界'),
   fact('UDP 头部的长度','8字节','1字节','32字节','64字节'),
   fact('UDP 本身对可靠交付的保证','不保证可靠交付','保证永不丢包','保证永不乱序','保证无限带宽'),
   fact('UDP 相比 TCP 的协议头部开销通常','更小','必定更大','为零','无限大'))]),
 ('应用层',[
  topic('HTTP',
   fact('浏览器访问网页常使用的应用层协议','HTTP','IP','以太网','ARP'),
   fact('HTTP 获取资源常用的方法','GET','DROP','COMMIT','ALTER'),
   fact('HTTP 提交请求数据常用的方法','POST','SELECT','ROLLBACK','TRUNCATE'),
   fact('HTTP 状态码 200 的通常含义','请求成功','资源未找到','未认证','服务器内部错误'),
   fact('HTTP 状态码 404 的通常含义','资源未找到','请求成功','永久认证成功','数据库提交完成')),
  topic('DNS',
   fact('DNS 的主要功能','域名解析','压缩图片','数据库排序','设置字体'),
   fact('DNS A 记录通常对应的地址类型','IPv4地址','MAC地址','磁盘地址','进程地址'),
   fact('DNS AAAA 记录通常对应的地址类型','IPv6地址','IPv4地址','MAC地址','物理内存地址'),
   fact('DNS 缓存的主要目的之一','减少重复查询','永久禁止联网','强制修改所有域名','删除所有记录'),
   fact('域名 www.example.com 中最右侧的 com 属于','顶级域名','主机端口','子网掩码','MAC前缀'))])])]

def quote(v):
    return 'NULL' if v is None else "'"+str(v).replace("'","''")+"'"

def build():
    rows=[];chapters=[];points=[]
    for cid,(course,chapter_list) in enumerate(bank,1):
        assert len(chapter_list)==5
        for cno,(name,topics) in enumerate(chapter_list,1):
            chapter_id=cid*100+cno
            chapters.append(dict(id=chapter_id,courseId=cid,name=name,order=cno))
            for tno,(topic_name,facts) in enumerate(topics,1):
                knowledge_id=cid*10000+cno*10+tno
                points.append(dict(id=knowledge_id,chapterId=chapter_id,name=topic_name,order=tno))
                generated=[]
                for label,correct,*wrong in facts:
                    generated.append(('SINGLE',label+'是？',[correct,*wrong],'A',f'{label}是{correct}。'))
                for n in range(2):
                    indices=[n,(n+1)%5,(n+2)%5,(n+3)%5]
                    valid={0,1} if n==0 else {1,3}
                    options=[f'{facts[j][0]}：{facts[j][1 if i in valid else 2]}' for i,j in enumerate(indices)]
                    generated.append(('MULTIPLE',f'关于{topic_name}，'+('下列对应关系正确的有哪些？' if n==0 else '请选择正确的表述。'),options,''.join('ABCD'[i] for i in sorted(valid)),'正确对应包括：'+'；'.join(options[i] for i in sorted(valid))+'。'))
                for n in range(3):
                    label,correct,*wrong=facts[n]
                    truth=n!=1
                    generated.append(('JUDGE',f'{label}是{correct if truth else wrong[0]}。',['正确','错误',None,None],'A' if truth else 'B',f'{label}是{correct}。'))
                assert len(generated)==10
                for index,(kind,stem,options,answer,explanation) in enumerate(generated,1):
                    order=(tno-1)*10+index
                    rows.append(dict(id=cid*10000+cno*100+order,chapterId=chapter_id,knowledgeId=knowledge_id,kind=kind,stem=stem,options=options,answer=answer,explanation=explanation))
    assert len(rows)==500 and len(chapters)==25 and len(points)==50
    assert len({r['id'] for r in rows})==500
    return chapters,points,rows

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    chapters,points,rows=build()
    sql=['-- Current chapter bank. Old rows and all practice references are preserved.','USE learning_analysis;','START TRANSACTION;','UPDATE chapter SET is_current=0 WHERE id NOT BETWEEN 101 AND 505;']
    for c in chapters:
        sql.append(f"INSERT INTO chapter(id,course_id,name,sort_order,is_current) VALUES({c['id']},{c['courseId']},{quote(c['name'])},{c['order']},1) ON DUPLICATE KEY UPDATE is_current=1;")
    for k in points:
        sql.append(f"INSERT INTO knowledge_point(id,chapter_id,name,sort_order) SELECT {k['id']},{k['chapterId']},{quote(k['name'])},{k['order']} WHERE NOT EXISTS(SELECT 1 FROM knowledge_point WHERE id={k['id']});")
    for q in rows:
        values=[str(q['id']),str(q['chapterId']),quote(q['kind']),quote(q['stem']),*map(quote,q['options']),quote(q['answer']),quote(q['explanation'])]
        sql.append('INSERT INTO question(id,chapter_id,question_type,stem,option_a,option_b,option_c,option_d,correct_answer,explanation) SELECT '+','.join(values)+f" WHERE NOT EXISTS(SELECT 1 FROM question WHERE id={q['id']});")
        sql.append(f"INSERT INTO question_knowledge SELECT {q['id']},{q['knowledgeId']} WHERE NOT EXISTS(SELECT 1 FROM question_knowledge WHERE question_id={q['id']} AND knowledge_id={q['knowledgeId']});")
    sql.append('COMMIT;')
    (root/'sql'/'06_chapter_bank.sql').write_text('\n'.join(sql)+'\n',encoding='utf-8')
    outline=['# 固定章节练习题库','', '当前题库共 5 门课、25 章、50 个知识点、500 道题。每章固定 20 题，每个知识点 10 题。','']
    for course,chapters_data in bank:
        outline+=['## '+course,'']
        outline += [f"{i}. {name}："+'、'.join(t[0] for t in topics)+'；20 题。' for i,(name,topics) in enumerate(chapters_data,1)]
        outline+=['']
    (root/'固定练习题库目录.md').write_text('\n'.join(outline),encoding='utf-8')
    print('Generated 25 chapters, 50 knowledge points and 500 questions.')
