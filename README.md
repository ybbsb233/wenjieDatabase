# 多课程学习薄弱项分析系统

数据库系统课程设计。前端使用 HTML、CSS、原生 JavaScript 和 Nginx；后端使用 Spring Boot、Java、MyBatis、MySQL 和 Maven。

## 当前完成情况

已完成需求、8 张表的数据库设计、E-R 图、页面与接口设计、数据库脚本、500 道当前题库题目、后端接口、16 个前端页面和 Nginx 本地部署脚本。已通过静态资源和接口联调；2026年10月20日补充登录、学生首页、章节目录、结果、薄弱项与管理页面的浏览器检查，运行截图见实验报告。

后端覆盖 JWT 登录、自愿改密、学生账号管理、课程目录、随机抽题及随机选项、自动评分、练习历史、错题重练、薄弱项、趋势和管理员统计。题库只由 SQL 脚本预置，没有题目修改和版本管理功能。

## 整理后的目录

实验报告见 [课程设计实验报告](docs/report/多课程学习薄弱项分析系统课程设计报告.docx)，整理记录见 [文件整理说明](docs/文件整理说明.md)。

- docs/design：需求、数据库与页面设计及题库目录。
- docs/archive：按开发阶段保留的历史记录，早期说明不代表当前功能。
- docs/verification：测试结果留档。
- docs/report：实验报告、任务书参考副本与插图。
- archive：可恢复的开发中间产物和云部署材料，不参与日常启动。
- .local/backups：原数据库备份，恢复脚本依赖此路径，继续保留。

## 工程目录

- backend：单模块 Maven 后端，Controller、Service、Mapper 分层。
- frontend：原生前端页面与共享 CSS、JavaScript。
- deploy：Nginx 配置模板。
- sql：建表脚本与五门课程的示例题。
- scripts：启动、示例数据生成和验证脚本。
- docs/design/需求文档.md、docs/design/数据库设计.md、docs/design/数据库ER图.mmd、docs/design/页面与接口设计.md：项目设计依据。

## 环境与构建

已在 Windows、Java 25.0.1、Maven 4.0.0-rc-5、MySQL Server 9.6.0 上实际运行。后端 Java 编译目标为 17，Spring Boot 4.0.5，MyBatis Starter 4.0.1。Maven 候选版本在本机已完成构建，不要求更换本机工具。

```powershell
cd backend
mvn package
```

## 初始化数据库

### 恢复完整成果（含全部账号与学习记录）

`sql/00_full_database.sql` 是从已部署服务器导出的完整数据库快照，同时包含建库、8张表的建表语句、约束、索引和全部数据，包括当前及归档题库、账号密码哈希、练习及逐题答案。新环境恢复现有成果时只需执行这个文件，**不要再执行01至06或初始化脚本**。

在 MySQL 命令行客户端登录后执行（路径改成项目实际位置）：

```sql
SOURCE C:/your-path/wenjieDatabase/sql/00_full_database.sql;
```

建议使用 MySQL 8.4 或更新版本，保持utf8mb4字符集。此完整快照含 `DROP TABLE IF EXISTS`，会替换同名数据库中的项目表，仅用于全新环境或明确需要恢复的项目库。请先备份已有数据。数据为课程设计演示数据，包含现有账号哈希和作答记录；管理员演示密码见账号说明，恢复后可自行修改。

### 仅创建空白账号环境和基础题库

下面的初始化脚本与01至06用于从零创建基础题库，不含完整学生成绩；与上面的完整快照恢复方式二选一。


全新环境推荐在项目根目录运行一键初始化脚本：

```powershell
.\scripts\init-database.ps1
```

按提示输入新电脑的 MySQL 密码。脚本依次执行 01、02、03、04、06，自动跳过仅用于旧结构升级的 05，并核验 5 门课程、25 个当前章节、500 道当前题目。要求 MySQL 客户端可用；不需要 Python 或 Maven。数据库 learning_analysis 已存在时停止，不覆盖已有数据。

如果 mysql 未加入 PATH，或使用其他连接参数：

```powershell
.\scripts\init-database.ps1 -MySqlPath "D:\mysql\bin\mysql.exe" -DbHost 127.0.0.1 -DbPort 3306 -DbUser root
```

初始化不恢复已有学生成绩，也不启动服务；管理员由首次启动后端时创建。导入失败会立即停止，但 MySQL 建表语句不能整体回滚，应检查残留后再处理。


新环境中通过 MySQL 客户端依次执行 sql/01_schema.sql、sql/02_demo_data.sql、sql/03_optional_password_change.sql、sql/04_expand_question_bank.sql、sql/06_chapter_bank.sql。05_chapter_practices.sql 仅用于旧结构升级，最新 01 已包含对应字段，新建库不要重复执行 05。数据库名为 learning_analysis。建表和基础题库脚本不删除数据库或现有表，不应在已有数据上重复执行；03 与 04 是可重复执行的增量更新。已有本项目数据库已经完成这些更新，无需再次初始化。

当前题库包含五门课程，每门五章、每章二十题，共 500 道题；每章两个知识点，每个知识点十题。旧 75 道题仅为历史引用保留，不参与当前课程目录或新组卷。题目由项目内脚本生成，包含单选、多选、判断及多知识点关联。

## 启动后端

在项目根目录运行：

```powershell
.\scripts\start-backend.ps1
```

脚本在未设置环境变量时安全提示输入数据库密码和初始管理员密码，并生成随机 JWT 密钥。默认数据库账号 root，可通过 DB_USERNAME 覆盖；数据库地址通过 DB_URL 覆盖。密码不写入项目文件。

默认监听 127.0.0.1:8080。可通过脚本的 -Port 参数改变端口。JWT_SECRET 可自行设置为至少 32 字节的随机密钥；重启时换密钥会使旧令牌失效。

首次启动若没有 admin 账号，会使用 ADMIN_INITIAL_PASSWORD 创建管理员，不强制修改初始密码；已有账号不会被启动脚本覆盖。学生由管理员创建，学号登录，初始密码 123456，修改密码为可选操作。

当前本机已有 20 个学生账号，学号为 20240001 至 20240020。新增账号的初始密码为 123456，可直接登录且修改密码为可选操作；已有账号保留原密码和学习记录。当前本机管理员为 admin，演示密码为 123456，可直接登录。该密码仅用于本地课程演示，不是数据库密码。

## 启动整个网站

在项目根目录执行以下命令，可同时在后台启动 Java 后端与本项目 Nginx：

```powershell
.\scripts\start-site.ps1
```

按提示输入 MySQL 密码。初始管理员密码仅在数据库没有 admin 时使用，已有管理员不会被覆盖。本机当前 MySQL 密码使用之前确认的值即可。

默认访问 http://127.0.0.1:8081/login.html，后端为 127.0.0.1:8080。可通过 -Port 和 -BackendPort 改变端口。Nginx 默认使用本机已有 D:\nginx-1.22.0-web\nginx.exe，换环境时通过 -NginxPath 指定安装位置。

```powershell
# 示例：使用其他端口
.\scripts\start-site.ps1 -Port 18081 -BackendPort 18080
# 停止本项目服务，不停止 MySQL 或其他项目
.\scripts\stop-site.ps1
```

若后端已单独启动，也可以只运行 scripts/start-frontend.ps1。后台日志和 PID 位于系统临时目录下的 learning-analysis-nginx 文件夹。该目录中的 public 是指向本项目 frontend 的目录联接，解决 Windows Nginx 运行路径兼容问题，源码仍保存在项目中。

前端包括学生课程首页、练习选择、答题、结果、历史、错题和薄弱项，以及管理员统计、学生管理和学生详情。账号设置页面支持自愿修改密码；没有题库管理功能。

## 验证

mvn test 运行评分规则测试，包括全部 24 种四选项排列、单多选映射、非法选项及掌握等级边界。

真实 MySQL 和 HTTP 联调脚本：

```powershell
# 先启动后端，可使用 -Port 18080
# MYSQL_PWD 设置为本机 MySQL 密码，TEST_ADMIN_PASSWORD 设置为当前管理员密码。
# 可设置 TEST_BASE_URL，默认 http://127.0.0.1:18080。
python scripts/verify_backend.py
python scripts/verify_schema.py
python scripts/verify_frontend.py
```

verify_backend.py 会创建或重置上述三个演示学生，并追加演示作答历史，完成后将学生密码重置为 123456。测试使用 TEST_ADMIN_PASSWORD 指定当前管理员密码。只在演示环境运行。

verify_schema.py 检查实际表、数据关系和数据库约束，负面测试写入均在事务中回滚。验证结果记录见docs/archive/后端阶段验证记录.md。

verify_frontend.py 只检查静态源码引用、Nginx 内容与 MIME 类型和 HTTP 状态，不启动或控制浏览器。默认检查 18081 端口，可通过 TEST_WEB_URL 覆盖。前端与 Nginx 阶段验证记录.md 说明本阶段检查结果与浏览器验证限制。


## 当前固定练习与学生数据

开始练习页面现在提供固定章节练习与自主随机练习。共 25 套固定练习，每套二十道题，全体学生题目和题序一致，只有选择题选项顺序随机。

当前二十名学生均有 25 次完整固定练习、500 条作答，合计 500 次练习、10000 条作答，覆盖全部 50 个知识点。20240001 保留用户已确认的效果，其余十九人按不同随机种子生成各自的掌握分布。旧记录归档保留，账号密码不变，没有删除数据。章节目录见docs/design/固定练习题库目录.md，批量更新验证见docs/archive/全部学生演示数据更新记录.md。

scripts/chapter_bank.py 生成 06_chapter_bank.sql。scripts/seed_student_20240001.py 只为该学生生成演示数据，重新运行会归档其现有练习；请勿在日常启动时运行。迁移与验证结果见docs/archive/固定章节练习重构记录.md。

原 verify_backend.py 为旧题库的演示重置脚本，不适用于本轮保留其他学生的场景，已默认停用。当前回归脚本为 verify_chapter_sets.py，需要 TEST_JWT_SECRET 与启动后端的 JWT_SECRET 一致，仅为 20240001 创建并归档验证用未提交记录，不修改其他学生。


## 管理员快捷入口

管理员首页的学生账号卡片进入学生管理，课程卡片进入课程概览，累计练习与累计作答进入全部练习记录。课程概览的整张卡片进入该课程的整体分析，练习记录按钮独立进入该课程已提交记录。

全部练习记录支持按课程、学生筛选和自定义每页条数。学生详情中的统计卡片也可以进入对应课程的练习历史或知识点分析。管理员分页列表统一提供默认 10 条、可调整 1 至 50 条的输入框；下拉箭头使用统一留白。

## AWS 公网部署（2026年10月20日）

访问地址：https://13.228.18.200/login.html 。已将本地完整数据库迁移至服务器，含20名学生、500次当前已提交练习、10000条当前作答。公网管理员与学生登录、统计接口已验证。

服务器为 Debian 13，使用 Java 21、Nginx 和 Docker MySQL 8.4。部署目录 `/opt/learning-analysis`，前端为其 `frontend` 子目录，后端为 `app.jar`。后端使用独立系统账号运行。服务器已有的8080端口服务未修改。

- Nginx 公网监听80和443，HTTP自动跳转HTTPS，站点配置 `/etc/nginx/sites-available/learning-analysis`。
- 后端仅监听本机18080，服务名 `learning-analysis`。
- MySQL 容器名 `learning-analysis-mysql`，仅映射本机13306；数据卷 `learning-analysis-mysql`，删除容器前必须保留该卷。
- 数据库账号、随机密码与JWT密钥位于 `/etc/learning-analysis`，文件权限600，不写入代码仓库。
- Java服务、Nginx、Docker已设开机自启，数据库容器设为 `unless-stopped`。
- 此次迁移原始SQL保留在 `/opt/learning-analysis/database.sql`（仅root可读），发布包保留在 `/root/learning-analysis-release.tar.gz`。

登录服务器后的维护命令：

```bash
sudo systemctl status learning-analysis nginx
sudo systemctl restart learning-analysis
sudo journalctl -u learning-analysis -n 100 --no-pager
sudo docker logs --tail 100 learning-analysis-mysql
sudo nginx -t && sudo systemctl reload nginx
```

公网无需运行本地服务。已启用 Let’s Encrypt 公网IP HTTPS证书；证书路径 `/etc/letsencrypt/live/learning-analysis-ip/`。`learning-analysis-cert-renew.timer` 每天两次检查续期，成功续期自动重载Nginx。80端口保留ACME验证入口，443提供HTTPS。续期检查：`sudo /opt/certbot/bin/certbot renew --cert-name learning-analysis-ip --dry-run`。官方IP证书说明：https://letsencrypt.org/2026/03/11/shorter-certs-certbot 。演示账号密码随数据库保留，管理员可在账号设置中修改密码。服务器SSH密码不保存在项目文件中。

## 局部导航与浏览器回归（2026-10-20）

项目仍采用原生 JavaScript 和现有页面渲染函数。已知业务页面的普通站内链接通过 History API 切换；侧栏、顶栏保留，主内容在数据完成后一次替换。学生详情页的标签及统计卡片链接只更新下方内容，标签和课程写入地址栏。练习方式切换也支持历史记录。读取数据保留旧内容，提供加载状态；失败保留当前页面并可重试。旧 GET 请求通过 AbortController 取消，写操作进行期间阻止业务页面切换；离开未提交练习或修改中的表单会提醒。滚动条空间固定保留。

登录、退出、密码修改后重新登录、登录失效、外部链接、下载、新窗口及未注册业务路径保持浏览器原生加载。直接打开业务 HTML 和刷新仍从服务端加载入口，再按 URL 渲染对应内容。

浏览器回归脚本 `scripts/verify_navigation.cjs` 使用 Playwright 启动真实 Chrome/Chromium、临时静态服务及可控 API 数据，不写入数据库。先提供可解析的 `playwright` 包，或通过 `PLAYWRIGHT_MODULE` 指定其模块路径；可选 `CHROME_EXECUTABLE` 指定浏览器，然后执行 `node scripts/verify_navigation.cjs`。本次验证涵盖学生与管理员侧栏、详情标签和卡片链接、长短页面宽度、前进后退、拒绝离开后的历史恢复、直接访问和刷新、加载期间保留内容、失败重试、快速导航和筛选、链接原生行为、权限限制、答题离开提醒及提交、登录失效和重新登录，同时检查未捕获浏览器错误。浏览器行为测试使用模拟 API；随后已启动真实后端，验证管理员登录、受保护课程查询，以及 49 项静态资源与 Nginx HTTP 检查通过。
