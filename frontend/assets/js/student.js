import {viewRoot,setLocalNavigation,go,setLeaveGuard,updateQuery} from './navigation.js?v=20261020-navigation-1';
import {api,query} from './api.js?v=20261020-navigation-1';
import {$,esc,pct,time,number,kinds,badge,empty,toast,busy,heading,stats,table,pagination,courseOptions,bar,trendChart} from './common.js?v=20261020-navigation-1';

let params;
const courseIcons=['∫','▤','⌘','⌗','⌁'];
export async function studentPage(page){
 params=new URLSearchParams(location.search);
 const pages={home,courses,practice,answer,history,wrong,analysis};
 if(pages[page])await pages[page]();
}
async function home(){
 const summary=await api('/student/summary');
 const practices=summary.reduce((s,r)=>s+Number(r.practiceCount),0),answers=summary.reduce((s,r)=>s+Number(r.answerCount),0),correct=summary.reduce((s,r)=>s+Number(r.correctCount),0);
 $('#main').innerHTML=heading('MY LEARNING','每一次练习，都更进一步','选择一门课程开始练习，找到值得优先复习的知识点。',`<a class="button" href="/student/practice.html">＋ 开始练习</a>`)+stats([{label:'可学习课程',value:summary.length,unit:'门',note:'查看全部课程 →',href:'/student/courses.html'},{label:'已完成练习',value:number(practices),unit:'次',note:'查看已提交练习 →',href:'/student/history.html'},{label:'累计作答',value:number(answers),unit:'题次',note:'含重复作答 · 查看记录 →',href:'/student/history.html'},{label:'累计正确率',value:answers?pct(correct*100/answers):'—',note:'查看各课程学习分析 →',href:'/student/analysis.html'}])+`<div class="section-title"><h2>我的课程</h2><span class="muted small-text">按课程查看学习情况</span></div>${courseCards(summary)}<div class="hero-note"><span class="note-icon">↗</span><div><h3>比起刷了多少题，更关注哪里还需要巩固</h3><p>薄弱项按每道题最近一次作答分析。样本不足的知识点会提示补充练习，帮助你更有针对性地复习。</p></div></div>`;
}
function courseCards(summary){
 return `<div class="grid three">${summary.map((c,i)=>`<article class="course-card"><div class="course-icon">${courseIcons[i%courseIcons.length]}</div><h3>${esc(c.courseName)}</h3><div class="course-metrics"><div><strong>${number(c.practiceCount)}</strong>完成练习</div><div><strong>${number(c.answerCount)}</strong>累计作答（含重复）</div><div><strong>${pct(c.accuracy)}</strong>正确率</div></div><div class="course-actions"><a class="course-analysis-link" href="/student/analysis.html?courseId=${esc(c.courseId)}" aria-label="查看${esc(c.courseName)}学习分析">查看学习分析 ↗</a><a class="button secondary small" href="/student/practice.html?courseId=${esc(c.courseId)}">去练习 →</a></div></article>`).join('')}</div>`;
}
async function courses(){
 const summary=await api('/student/summary');
 $('#main').innerHTML=heading('COURSES','课程列表','选择一门课程，开始练习或查看对应的学习分析。','<a class="button secondary" href="/student/home.html">← 返回学习首页</a>')+courseCards(summary);
}
async function practice(){
 const courses=await api('/courses');
 $('#main').innerHTML=heading('PRACTICE','选择你的练习方式','完成固定章节练习，或按自己的需要生成一组随机题。')+`<div class="tabs" role="tablist"><button data-practice-mode="fixed" role="tab" class="active" aria-selected="true">固定章节练习</button><button data-practice-mode="random" role="tab" aria-selected="false">自主随机练习</button></div><section id="fixed-mode"><div class="filters"><label for="fixed-course">选择课程</label><select id="fixed-course">${courseOptions(courses)}</select><span class="muted small-text">每门课 5 套练习 · 每套固定 20 题</span></div><div class="notice">同一章节的题目和题目顺序对所有学生一致，仅选择题的选项顺序随机。可重复练习，每次单独保存结果。</div><div id="fixed-list" class="chapter-sets"></div></section><section id="random-mode" hidden><div class="grid two"><section class="card"><h2>设置练习范围</h2><form id="start-form"><div class="field"><label for="course">课程</label><select id="course">${courseOptions(courses)}</select></div><div class="form-grid"><div class="field"><label for="chapter">章节</label><select id="chapter"><option value="">全部章节</option></select></div><div class="field"><label for="knowledge">知识点</label><select id="knowledge"><option value="">全部知识点</option></select></div></div><div class="field"><label for="count">题目数量</label><input id="count" type="number" min="1" max="50" value="5" required><small>可选 1—50 题；题目不足时，按实际可用数量出题。</small></div><div id="available" class="notice">正在读取题库…</div><button type="submit">生成练习 →</button></form></section><section><div class="card"><div class="eyebrow">HOW IT WORKS</div><h2>专注练习，提交后查看反馈</h2><p class="muted">每组练习混合抽取单选、多选和判断题。同次不重复出题，选择题选项随机排列。</p><p class="small-text">每题 1 分。多选题需全部选对，漏选或错选不得分。提交后统一展示答案与解析。</p><div class="notice">未提交的选择仅保存在当前页面，离开或刷新可能丢失。</div></div></section></div></section>`;
 const course=$('#course'),chapter=$('#chapter'),knowledge=$('#knowledge');
 course.value=params.get('courseId')||courses[0]?.id||'';
 if(!course.value&&courses.length)course.value=courses[0].id;
 let chapters=[],points=[];
 const updateAvailable=()=>{const point=points.find(x=>x.id===knowledge.value),ch=chapters.find(x=>x.id===chapter.value),c=courses.find(x=>x.id===course.value);const count=point?.questionCount??ch?.questionCount??c?.questionCount??0;$('#available').textContent=`当前范围共有 ${count} 道示例题。`;};
 async function loadPoints(selected=''){points=await api(`/courses/${course.value}/knowledge-points`+query({chapterId:chapter.value}));knowledge.innerHTML='<option value="">全部知识点</option>'+points.map(k=>`<option value="${esc(k.id)}">${esc(k.name)}</option>`).join('');knowledge.value=selected;updateAvailable();}
 async function loadCourse(){chapters=await api(`/courses/${course.value}/chapters`);chapter.innerHTML='<option value="">全部章节</option>'+chapters.map(c=>`<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('');await loadPoints();}
 course.onchange=()=>loadCourse().catch(e=>toast(e.message));chapter.onchange=()=>loadPoints().catch(e=>toast(e.message));knowledge.onchange=updateAvailable;
 await loadCourse();
 if(params.get('chapterId'))chapter.value=params.get('chapterId');
 await loadPoints(params.get('knowledgeId')||'');
 $('#start-form').onsubmit=e=>{e.preventDefault();busy($('button[type=submit]',e.target),async()=>{const created=await api('/student/practices',{method:'POST',body:{courseId:course.value,chapterId:chapter.value||null,knowledgeId:knowledge.value||null,count:Number($('#count').value)}});if(created.actualCount<created.requestedCount)sessionStorage.setItem('practice-notice',`可用题目不足，本次实际出题 ${created.actualCount} 道。`);go('/student/answer.html?id='+encodeURIComponent(created.practiceId));});};
 const fixedCourse=$('#fixed-course');
 fixedCourse.value=course.value;
 async function loadFixed(){
  const sets=await api('/student/practices/chapter-sets'+query({courseId:fixedCourse.value}));
  $('#fixed-list').innerHTML=sets.map(c=>`<article class="card chapter-set"><div class="card-header"><span class="badge">第 ${c.chapterNo} 章</span><span class="badge ${c.completedAttempts?'good':''}">${c.completedAttempts?'已完成':'待练习'}</span></div><h2>${esc(c.chapterName)}</h2><p class="muted small-text">固定 ${c.questionCount} 题 · 已完成 ${c.completedAttempts} 次</p><div class="chapter-set-footer"><span class="small-text">${c.completedAttempts?`最近得分 <strong>${c.latestCorrectCount} / ${c.questionCount}</strong> · ${pct(c.latestAccuracy)}`:'完成整章练习，覆盖本章全部知识点'}</span><div class="row">${c.latestPracticeId?`<a href="/practice-result.html?id=${esc(c.latestPracticeId)}">查看结果</a>`:''}<button class="small" data-chapter="${esc(c.chapterId)}">${c.completedAttempts?'再次练习':'开始练习'} →</button></div></div></article>`).join('');
  $('#fixed-list').querySelectorAll('[data-chapter]').forEach(b=>b.onclick=()=>busy(b,async()=>{
   const created=await api('/student/practices/chapters/'+b.dataset.chapter,{method:'POST'});
   go('/student/answer.html?id='+encodeURIComponent(created.practiceId));
  }));
 }
 function showMode(mode){
  $('#fixed-mode').hidden=mode!=='fixed';$('#random-mode').hidden=mode!=='random';
  viewRoot().querySelectorAll('[data-practice-mode]').forEach(b=>{const active=b.dataset.practiceMode===mode;b.classList.toggle('active',active);b.setAttribute('aria-selected',String(active));});
 }
 viewRoot().querySelectorAll('[data-practice-mode]').forEach(b=>b.onclick=()=>{showMode(b.dataset.practiceMode);updateQuery({mode:b.dataset.practiceMode});});
 fixedCourse.onchange=()=>loadFixed().catch(e=>toast(e.message));
 showMode(params.has('knowledgeId')||params.has('chapterId')||params.get('mode')==='random'?'random':'fixed');
 await loadFixed();
 setLocalNavigation(async url=>{const next=new URLSearchParams(url.search),previous=new URLSearchParams(params);next.delete('mode');previous.delete('mode');next.sort();previous.sort();if(next.toString()!==previous.toString())return false;showMode(url.searchParams.get('mode')||'fixed');return true;});

}
async function answer(){
 const id=params.get('id');if(!id)throw new Error('缺少练习编号，请重新开始练习');
 const data=await api(`/student/practices/${encodeURIComponent(id)}/questions`);
 const selections=new Map();let current=0,submitted=false;
 setLeaveGuard(()=>!submitted);
 $('#main').innerHTML=heading('IN PROGRESS','把注意力留给这一题',`${data.practiceName||'自主练习'} · 整组提交后查看答案与解析。`)+`<div class="notice" id="answer-notice">未提交答案仅保存在当前页面，请勿刷新或关闭。</div><div class="question-layout"><section class="card" id="question-panel"></section><aside class="answer-sidebar"><div class="card"><h2>答题进度</h2><div id="answer-progress" class="muted small-text"></div><div class="answer-grid" id="answer-grid"></div><p class="small-text muted">深色为已作答，描边为当前题。</p><button id="submit" class="full-width">提交本次练习</button></div></aside></div>`;
 const shortage=sessionStorage.getItem('practice-notice');if(shortage){$('#answer-notice').textContent=shortage+' 未提交答案仅保存在当前页面，请勿刷新或关闭。';sessionStorage.removeItem('practice-notice');}
 function progress(){const answered=[...selections.values()].filter(v=>v.length).length;$('#answer-progress').textContent=`已作答 ${answered} / ${data.items.length} 题`;$('#answer-grid').innerHTML=data.items.map((q,i)=>`<button class="${selections.get(q.itemId)?.length?'answered':''} ${i===current?'current':''}" data-index="${i}" aria-label="第 ${i+1} 题">${i+1}</button>`).join('');$('#answer-grid').querySelectorAll('button').forEach(b=>b.onclick=()=>{current=Number(b.dataset.index);render();});}
 function render(){const q=data.items[current],selected=selections.get(q.itemId)||[];$('#question-panel').innerHTML=`<div class="row between"><span class="badge">${kinds[q.questionType]}</span><span class="muted small-text">第 ${current+1} / ${data.items.length} 题 · 每题 1 分</span></div><div class="question-stem">${esc(q.stem)}</div>${q.options.map(o=>`<label class="option"><input type="${q.questionType==='MULTIPLE'?'checkbox':'radio'}" name="answer" value="${o.label}" ${selected.includes(o.label)?'checked':''}><span class="option-letter">${q.questionType==='JUDGE'?'':o.label+'.'}</span><span>${esc(o.text)}</span></label>`).join('')}<div class="row between" style="margin-top:28px"><button id="previous" class="secondary" ${current===0?'disabled':''}>← 上一题</button><button id="next" class="secondary" ${current===data.items.length-1?'disabled':''}>下一题 →</button></div>`;
 $('#question-panel').querySelectorAll('input').forEach(input=>input.onchange=()=>{selections.set(q.itemId,[...$('#question-panel').querySelectorAll('input:checked')].map(el=>el.value));progress();});$('#previous').onclick=()=>{current--;render();};$('#next').onclick=()=>{current++;render();};progress();}
 render();
 $('#submit').onclick=()=>{const unanswered=data.items.length-[...selections.values()].filter(v=>v.length).length;if(!confirm(unanswered?`还有 ${unanswered} 道题未作答，未答计 0 分。确定提交吗？`:'确定提交本次练习吗？提交后无法修改。'))return;busy($('#submit'),async()=>{await api(`/student/practices/${encodeURIComponent(id)}/submit`,{method:'POST',body:{answers:data.items.map(q=>({itemId:q.itemId,selectedLabels:selections.get(q.itemId)||[]}))}});submitted=true;go('/practice-result.html?id='+encodeURIComponent(id),true);});};
}
export function renderResult(data,user){
 const admin=user.role==='ADMIN',labels=(values,q)=>values.length?values.map(v=>q.questionType==='JUDGE'?(v==='A'?'正确':'错误'):v).join('、'):'未作答';
 $('#main').innerHTML=heading('PRACTICE RESULT','练习完成，看看这次的收获',`${data.practiceName||'练习结果'} · 提交于 ${time(data.submittedAt)} · 每题 1 分`,admin?`<a class="button secondary" href="/admin/student-detail.html?id=${esc(data.studentId)}">返回学生详情</a>`:`<a class="button" href="/student/analysis.html?courseId=${esc(data.courseId)}">查看薄弱项 →</a>`)+`<div class="card"><div class="row between"><div><div class="muted small-text">本次得分</div><div class="result-score">${data.correctCount}<small> / ${data.questionCount}</small></div></div><div><h2>${pct(data.accuracy)}</h2><div class="muted small-text">本次正确率</div></div><div><h2>${data.questionCount-data.correctCount} 题</h2><div class="muted small-text">需要回顾的题目</div></div></div></div><div class="section-title"><h2>逐题回顾</h2><span class="muted small-text">选项顺序与本次练习一致</span></div>${data.items.map(q=>`<article class="card result-item" id="item-${esc(q.itemId)}"><div class="row between"><span class="small-text">第 ${q.orderNo} 题 · ${kinds[q.questionType]}</span><span class="badge ${q.isCorrect?'good':'weak'}">${q.isCorrect?'回答正确':q.selectedLabels.length?'回答错误':'未作答'}</span></div><div class="question-stem">${esc(q.stem)}</div>${q.options.map(o=>`<div class="option ${q.correctLabels.includes(o.label)?'correct':q.selectedLabels.includes(o.label)?'wrong':''}"><span class="option-letter">${q.questionType==='JUDGE'?'':o.label+'.'}</span><span>${esc(o.text)}</span>${q.selectedLabels.includes(o.label)?'<span class="badge" style="margin-left:auto">你的选择</span>':''}</div>`).join('')}<p class="small-text">你的答案：<strong>${esc(labels(q.selectedLabels,q))}</strong>　正确答案：<strong>${esc(labels(q.correctLabels,q))}</strong></p><div class="explanation"><strong>答案解析</strong><p>${esc(q.explanation)}</p></div></article>`).join('')}<div class="row">${admin?'':`<a class="button secondary" href="/student/practice.html?courseId=${esc(data.courseId)}">再练一组</a><a class="button secondary" href="/student/wrong.html?courseId=${esc(data.courseId)}">去错题本</a>`}</div>`;

}
export function historyTable(rows){return table(['课程','提交时间','练习类型','题量','得分','正确率','操作'],rows.map(r=>`<tr><td>${esc(r.courseName)}${r.chapterName?`<span class="sub">${esc(r.chapterName)}</span>`:''}</td><td>${esc(time(r.submittedAt))}</td><td><span class="badge">${r.sourceType==='CHAPTER'?'固定章节练习':r.sourceType==='WRONG'?'错题重练':'自主随机练习'}</span></td><td>${number(r.questionCount)}</td><td>${r.correctCount} / ${r.questionCount}</td><td>${pct(r.accuracy)}${bar(r.accuracy)}</td><td><a href="/practice-result.html?id=${esc(r.practiceId)}">查看结果 →</a></td></tr>`));}
async function history(){
 const courses=await api('/courses');let page=1,pageSize=10;
 $('#main').innerHTML=heading('HISTORY','练习记录','每次提交都保留，回顾你的练习表现。')+`<div class="card"><div class="filters"><label for="course" class="muted">筛选课程</label><select id="course">${courseOptions(courses,true)}</select></div><div id="history-list"></div><div id="pagination"></div></div>`;$('#course').value=params.get('courseId')||'';
 async function load(){const data=await api('/student/practices'+query({courseId:$('#course').value,page,pageSize}));$('#history-list').innerHTML=data.rows.length?historyTable(data.rows):empty('还没有练习记录','开始一组练习，提交后在这里查看结果。','<a class="button secondary" href="/student/practice.html">开始练习</a>');pagination($('#pagination'),data.total,page,pageSize,p=>{page=p;load().catch(e=>toast(e.message));},size=>{pageSize=size;page=1;load().catch(e=>toast(e.message));});}
 $('#course').onchange=()=>{page=1;load().catch(e=>toast(e.message));};await load();
}
export function knowledgeTable(rows,admin=false){return table(['知识点','题库题量',admin?'参与人数':'已练不同题',admin?'有效组合':'答对题目','近期正确率','掌握情况',...(admin?[]:['复习'])],rows.map(r=>`<tr><td>${esc(r.knowledgeName)}</td><td>${number(r.bankCount)}</td><td>${number(admin?r.participantCount:r.questionCount)}</td><td>${number(admin?r.questionCount:r.correctCount)}</td><td>${pct(r.accuracy)}${bar(r.accuracy)}</td><td>${badge(r.level)}</td>${admin?'':`<td><a href="/student/practice.html${query({courseId:$('#course')?.value,chapterId:r.chapterId,knowledgeId:r.knowledgeId})}">去练习 →</a></td>`}</tr>`));}
async function analysis(){
 const courses=await api('/courses');
 $('#main').innerHTML=heading('LEARNING INSIGHTS','找到下一步的复习方向','用每道题最近一次作答，观察各个知识点的掌握情况。')+`<div class="filters"><label for="course" class="muted">当前课程</label><select id="course">${courseOptions(courses)}</select></div><div id="analysis-content"></div>`;$('#course').value=params.get('courseId')||courses[0]?.id;
 async function load(){const id=$('#course').value;const [rows,trend]=await Promise.all([api('/student/knowledge-analysis'+query({courseId:id})),api('/student/trend'+query({courseId:id}))]);const weak=rows.filter(r=>r.level==='WEAK').length,review=rows.filter(r=>r.level==='REVIEW').length,good=rows.filter(r=>r.level==='GOOD').length;
 $('#analysis-content').innerHTML=stats([{label:'优先复习',value:weak,unit:'个知识点',note:'正确率低于 60%'},{label:'需要巩固',value:review,unit:'个知识点',note:'正确率 60% 至不足 80%'},{label:'掌握较好',value:good,unit:'个知识点',note:'正确率达到 80%'}])+`<div class="spacer"></div><div class="card"><div class="card-header"><h2>知识点掌握情况</h2><span class="muted small-text">优先展示需要复习的内容</span></div><div class="notice">题库题量是该知识点可练的题数，已练不同题会去除重复作答，与首页累计题次不同。至少完成 3 道不同题才判断等级，近期正确率取各题最近一次结果。</div>${knowledgeTable(rows)}</div><div class="card"><h2>练习正确率趋势</h2>${trendChart(trend)}</div>`;}
 $('#course').onchange=()=>load().catch(e=>toast(e.message));await load();
}
async function wrong(){
 const courses=await api('/courses');
 let page=1,pageSize=10;
 const selected=new Set();
 $('#main').innerHTML=heading('REVIEW','错题本','把错误留作线索，让下一次练习更有针对性。')+`<div class="card"><div class="filters"><label for="course" class="visually-hidden">课程</label><select id="course">${courseOptions(courses)}</select><label for="knowledge" class="visually-hidden">知识点</label><select id="knowledge"><option value="">全部知识点</option></select><button id="retry-wrong" style="margin-left:auto">重练所选错题</button></div><p class="muted small-text">全选仅选择当前页，翻页后保留已选题目；同一课程最多选择 50 道。每页可显示 1—50 条，默认 10 条。</p><div id="wrong-list"></div><div id="pagination"></div></div>`;
 $('#course').value=params.get('courseId')||courses[0]?.id;
 function updateSelection(){
  const boxes=[...$('#wrong-list').querySelectorAll('[data-question]')];
  const chosen=boxes.filter(c=>selected.has(c.dataset.question)).length;
  const all=$('#select-page');
  if(all){all.checked=boxes.length>0&&chosen===boxes.length;all.indeterminate=chosen>0&&chosen<boxes.length;}
  $('#retry-wrong').textContent=selected.size?`重练所选错题（${selected.size}）`:'重练所选错题';
 }
 async function load(){
  const data=await api('/student/wrong-questions'+query({courseId:$('#course').value,knowledgeId:$('#knowledge').value,page,pageSize}));
  $('#wrong-list').innerHTML=data.rows.length?table(['选择','题目','历史错误次数','最近状态','回顾'],data.rows.map(r=>`<tr><td><input type="checkbox" aria-label="选择题目" data-question="${esc(r.questionId)}" ${selected.has(r.questionId)?'checked':''}></td><td class="table-stem">${esc(r.stem)}</td><td>${number(r.wrongCount)}</td><td><span class="badge ${r.latestCorrect?'good':'weak'}">${r.latestCorrect?'最近已答对':'仍需复习'}</span></td><td><a href="/practice-result.html?id=${esc(r.lastWrongPracticeId)}#item-${esc(r.lastWrongItemId)}">查看解析</a></td></tr>`)):empty('当前范围没有错题','可以继续练习，或切换课程与知识点。');
  if(data.rows.length){
   $('#wrong-list th').innerHTML='<label class="check-label select-page-label"><input type="checkbox" id="select-page">全选本页</label>';
   $('#select-page').onchange=e=>{
    const boxes=[...$('#wrong-list').querySelectorAll('[data-question]')];
    const additions=boxes.filter(c=>!selected.has(c.dataset.question));
    if(e.target.checked&&selected.size+additions.length>50){toast('最多选择 50 道题，请先取消部分已选题目');updateSelection();return;}
    for(const box of boxes){box.checked=e.target.checked;if(box.checked)selected.add(box.dataset.question);else selected.delete(box.dataset.question);}
    updateSelection();
   };
   $('#wrong-list').querySelectorAll('[data-question]').forEach(c=>c.onchange=()=>{
    if(c.checked&&selected.size>=50){c.checked=false;toast('每次最多选择 50 道题');}
    else if(c.checked)selected.add(c.dataset.question);else selected.delete(c.dataset.question);
    updateSelection();
   });
  }
  updateSelection();
  pagination($('#pagination'),data.total,page,pageSize,p=>{page=p;load().catch(e=>toast(e.message));},size=>{pageSize=size;page=1;load().catch(e=>toast(e.message));});
 }
 async function courseChange(){
  page=1;selected.clear();updateSelection();
  const points=await api(`/courses/${$('#course').value}/knowledge-points`);
  $('#knowledge').innerHTML='<option value="">全部知识点</option>'+points.map(k=>`<option value="${esc(k.id)}">${esc(k.name)}</option>`).join('');
  await load();
 }
 $('#course').onchange=()=>courseChange().catch(e=>toast(e.message));
 $('#knowledge').onchange=()=>{page=1;load().catch(e=>toast(e.message));};
 $('#retry-wrong').onclick=()=>{
  if(!selected.size)return toast('请先勾选要重练的错题');
  busy($('#retry-wrong'),async()=>{
   const data=await api('/student/practices/from-wrong',{method:'POST',body:{courseId:$('#course').value,questionIds:[...selected]}});
   go('/student/answer.html?id='+encodeURIComponent(data.practiceId));
  });
 };
 await courseChange();
}
