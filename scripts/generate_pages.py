"""Create the small HTML entry points; the application stays buildless."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'frontend'
pages={'index.html':'index','account.html':'account','practice-result.html':'result',
       'student/home.html':'home','student/courses.html':'courses','student/practice.html':'practice','student/answer.html':'answer',
       'student/history.html':'history','student/wrong.html':'wrong','student/analysis.html':'analysis',
       'admin/dashboard.html':'dashboard','admin/courses.html':'admin-courses','admin/practices.html':'admin-practices','admin/students.html':'students','admin/student-detail.html':'student-detail'}
for path,page in pages.items():
    file=root/path;file.parent.mkdir(parents=True,exist_ok=True)
    file.write_text(f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="多课程学习练习与知识点薄弱项分析">
  <title>知序学习 · 学习薄弱项分析系统</title>
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/css/common.css?v=20261019-admin-links-8">
  <script type="module" src="/assets/js/app.js?v=20261019-admin-links-8"></script>
</head>
<body data-page="{page}"><div class="loading">正在加载学习空间…</div><noscript>请启用 JavaScript 后使用本网站。</noscript></body>
</html>
''',encoding='utf-8')
print(f'Created {len(pages)} HTML entry pages.')
