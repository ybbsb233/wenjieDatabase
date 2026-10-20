import {requestSignal,writeHistory,adoptHistory,exitSession,saveLifecycle,restoreLifecycle,setViewRoot,cancelReads,cancelled,canLeave,disposeView,setLeaveGuard,updateLocalNavigation} from './navigation.js?v=20261020-navigation-1';
import {api,tokenKey} from './api.js?v=20261020-navigation-1';
import {$,esc,toast,busy,errorBox,heading} from './common.js?v=20261020-navigation-1';
import {studentPage} from './student.js?v=20261020-navigation-1';
import {adminPage} from './admin.js?v=20261020-navigation-1';

let page=document.body.dataset.page;
const titles={home:'学习首页',courses:'课程列表',practice:'开始练习',answer:'练习进行中',history:'练习记录',wrong:'错题本',analysis:'薄弱项分析',dashboard:'整体统计','admin-courses':'课程概览','admin-practices':'全部练习记录',students:'学生管理','student-detail':'学生详情',account:'账号设置',result:'练习结果'};
export let currentUser;

async function login(){
 const expired=new URLSearchParams(location.search).has('expired');
 if(expired)$('#login-message').innerHTML=errorBox('登录已失效，请重新登录。');
 $('#login-form').onsubmit=async e=>{e.preventDefault();const button=$('button[type=submit]',e.target);await busy(button,async()=>{
   $('#login-message').textContent='';
   try{const result=await api('/auth/login',{method:'POST',body:{username:$('#username').value.trim(),password:$('#password').value}});sessionStorage.setItem(tokenKey,result.token);redirect(result.user);}
   catch(error){$('#login-message').innerHTML=errorBox(error.message);}
 });};
}
function redirect(user){exitSession(user.role==='ADMIN'?'/admin/dashboard.html':'/student/home.html');}
function shell(user){
 const admin=user.role==='ADMIN';
 const links=admin?[['dashboard','◫','整体统计','/admin/dashboard.html'],['admin-courses','▤','课程概览','/admin/courses.html'],['admin-practices','≡','练习记录','/admin/practices.html'],['students','♧','学生管理','/admin/students.html']]:[['home','◫','学习首页','/student/home.html'],['practice','＋','开始练习','/student/practice.html'],['history','≡','练习记录','/student/history.html'],['wrong','◇','错题本','/student/wrong.html'],['analysis','↗','薄弱项分析','/student/analysis.html']];
 links.push(['account','⚙','账号设置','/account.html']);
 document.body.innerHTML=`<div class="app"><aside class="sidebar"><a class="brand" href="${admin?'/admin/dashboard.html':'/student/home.html'}"><span class="brand-mark">知</span><span><strong>知序学习</strong><small>LEARNING INSIGHTS</small></span></a><div class="nav-label">${admin?'教学管理':'我的学习'}</div><nav aria-label="主导航">${links.map(([id,icon,title,url])=>`<a class="nav-link ${page===id||(page==='answer'&&id==='practice')||(page==='courses'&&id==='home')||(page==='student-detail'&&id==='students')?'active':''}" href="${url}"><span class="nav-icon" aria-hidden="true">${icon}</span>${title}</a>`).join('')}</nav><div class="sidebar-bottom"><strong>让每次练习都有方向</strong>多课程学习薄弱项分析系统<br>数据库系统课程设计</div></aside><div class="workspace"><header class="topbar"><div class="breadcrumb">${admin?'管理工作台':'学习空间'} <span aria-hidden="true"> / </span> ${titles[page]||''}</div><div class="profile"><span class="avatar">${esc(user.realName.slice(0,1))}</span><span>${esc(user.realName)}</span><span class="badge">${admin?'管理员':'学生'}</span><button id="logout" class="text small">退出</button></div></header><main id="main" class="main"><div class="loading">正在加载…</div></main></div></div>`;
 $('#logout').onclick=event=>{if(!canLeave())return;return busy(event.currentTarget,async()=>{await api('/auth/logout',{method:'POST'});sessionStorage.removeItem(tokenKey);exitSession('/login.html');});};
}
async function account(user){
 $('#main').innerHTML=heading('ACCOUNT','账号设置','管理个人信息与登录密码。')+`<div class="card account-card"><div class="notice">修改密码为可选操作，你可以继续使用当前密码。</div><div class="row between"><div><h2>${esc(user.realName)}</h2><p class="muted">${user.role==='ADMIN'?'管理员账号':'学生学号'}：${esc(user.username)}</p></div><span class="badge">${user.role==='ADMIN'?'管理员':'学生'}</span></div><hr style="border:0;border-top:1px solid var(--line);margin:20px 0 25px"><form id="password-form"><div class="field"><label for="old-password">原密码</label><input id="old-password" type="password" required autocomplete="current-password"></div><div class="field"><label for="new-password">新密码</label><input id="new-password" type="password" required minlength="6" maxlength="72" autocomplete="new-password"><small>至少 6 位，不能继续使用默认密码 123456。</small></div><div class="field"><label for="confirm-password">确认新密码</label><input id="confirm-password" type="password" required autocomplete="new-password"></div><button type="submit">修改密码并重新登录</button></form></div>`;
 $('#password-form').onsubmit=e=>{e.preventDefault();if($('#new-password').value!==$('#confirm-password').value)return toast('两次输入的新密码不一致');busy($('button[type=submit]',e.target),async()=>{await api('/auth/password',{method:'PUT',body:{oldPassword:$('#old-password').value,newPassword:$('#new-password').value}});sessionStorage.removeItem(tokenKey);exitSession('/login.html');});};
}
async function result(user){
 const signal=requestSignal();
 const id=new URLSearchParams(location.search).get('id');
 if(!id)throw new Error('缺少练习编号');
 const prefix=user.role==='ADMIN'?'/admin':'/student';
 const data=await api(`${prefix}/practices/${encodeURIComponent(id)}/result`);
 const {renderResult}=await import('./student.js?v=20261020-navigation-1');
 signal.throwIfAborted();
 renderResult(data,user);
}
async function main(){
 if(page==='login'){await login();return;}
 if(!sessionStorage.getItem(tokenKey)){location.replace('/login.html');return;}
 currentUser=await api('/auth/me');
 if(page==='index'){redirect(currentUser);return;}
 if(location.pathname.startsWith('/admin/')&&currentUser.role!=='ADMIN'){redirect(currentUser);return;}
 if(location.pathname.startsWith('/student/')&&currentUser.role!=='STUDENT'){redirect(currentUser);return;}
 shell(currentUser);
 await navigate(location.href,{initial:true});
}
const routes={'/student/home.html':'home','/student/courses.html':'courses','/student/practice.html':'practice','/student/answer.html':'answer','/student/history.html':'history','/student/wrong.html':'wrong','/student/analysis.html':'analysis','/admin/dashboard.html':'dashboard','/admin/courses.html':'admin-courses','/admin/practices.html':'admin-practices','/admin/students.html':'students','/admin/student-detail.html':'student-detail','/account.html':'account','/practice-result.html':'result'};
let navigationId=0,shownURL=location.href,dirty=false,shownIndex=adoptHistory(),restoringHistory=false;
const nativeQuery=selector=>document.querySelector(selector);
function updateShell(){
 const active=page==='answer'?'practice':page==='courses'?'home':page==='student-detail'?'students':page;
 document.querySelectorAll('.nav-link').forEach(link=>{const selected=routes[new URL(link.href).pathname]===active;link.classList.toggle('active',selected);if(selected)link.setAttribute('aria-current','page');else link.removeAttribute('aria-current');});
 nativeQuery('.breadcrumb').textContent=(currentUser.role==='ADMIN'?'管理工作台':'学习空间')+' / '+titles[page];
 document.title=titles[page]+' · 知序学习';document.body.dataset.page=page;
}
function scrollToAddress(){if(location.hash){try{document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView();}catch{}}else window.scrollTo(0,0);}
async function navigate(address,{initial=false,pop=false,replace=false,completed=false}={}){
 const url=new URL(address,location.href),target=routes[url.pathname];
 if(!target)return;
 const working=!completed&&Boolean(nativeQuery('[data-working]'));
 if(working)toast('操作正在处理中，请稍候再切换页面。');
 if(!initial&&(working||!canLeave())){if(pop){const delta=shownIndex-(history.state?.navigationIndex??shownIndex);if(delta){restoringHistory=true;history.go(delta);}else writeHistory(shownURL,true);}return;}
 if((url.pathname.startsWith('/admin/')&&currentUser.role!=='ADMIN')||(url.pathname.startsWith('/student/')&&currentUser.role!=='STUDENT')){toast('无权访问该页面');if(pop){writeHistory(shownURL,true);shownIndex=adoptHistory();}return;}
 const oldURL=shownURL,oldLifecycle=saveLifecycle(),oldDirty=dirty;
 if(!initial&&!pop)writeHistory(url,replace);else adoptHistory();
 const id=++navigationId;cancelReads();
 let status=nativeQuery('#navigation-status');if(!status){status=document.createElement('div');status.id='navigation-status';status.className='navigation-status';status.setAttribute('role','status');document.body.append(status);}status.textContent='正在加载…';status.hidden=false;
 try{
  if(!initial&&new URL(oldURL).pathname===url.pathname&&await updateLocalNavigation(url)){
   if(id!==navigationId)return;shownURL=url.href;shownIndex=adoptHistory();if(url.hash)scrollToAddress();return;
  }
  if(id!==navigationId)return;
  disposeView();dirty=false;
  const previous=nativeQuery('#main'),staging=document.createElement('main');staging.id='main';staging.className='main';
  previous.inert=true;previous.setAttribute('aria-busy','true');setViewRoot(staging);
  // Existing renderers build into a detached main; publish only after all data is ready.
  if(target==='account')await account(currentUser);
  else if(target==='result')await result(currentUser);
  else if(currentUser.role==='ADMIN')await adminPage(target,currentUser);
  else await studentPage(target,currentUser);
  if(id!==navigationId)return;
  previous.replaceWith(staging);setViewRoot(document);page=target;shownURL=url.href;shownIndex=adoptHistory();updateShell();
  if(target!=='answer')setLeaveGuard(()=>dirty);
  scrollToAddress();
 }catch(error){
  if(id!==navigationId||cancelled(error)||error.status===401)return;
  setViewRoot(document);const main=nativeQuery('#main');main.inert=false;main.removeAttribute('aria-busy');
  restoreLifecycle(oldLifecycle);dirty=oldDirty;
  writeHistory(oldURL,true);shownIndex=adoptHistory();
  status.textContent='加载失败：'+error.message+' ';const retry=document.createElement('button');retry.className='secondary small';retry.textContent='重试';retry.onclick=()=>navigate(url.href,{replace:true});status.append(retry);
  if(initial)main.innerHTML=errorBox(error.message);
  return;
 }finally{if(id===navigationId){setViewRoot(document);nativeQuery('#main')?.removeAttribute('aria-busy');if(status.textContent==='正在加载…')status.hidden=true;}}
}
document.addEventListener('click',event=>{
 const link=event.target.closest('a[href]');if(!link||event.defaultPrevented||event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||link.hasAttribute('download')||(link.target&&link.target!=='_self')||link.relList.contains('external'))return;
 const url=new URL(link.href);if(url.origin!==location.origin||!routes[url.pathname]||!currentUser)return;
 if(url.pathname===location.pathname&&url.search===location.search&&url.hash)return;
 event.preventDefault();navigate(url.href);
});
window.addEventListener('app:navigate',event=>navigate(event.detail.url,{replace:event.detail.replace,completed:event.detail.completed}));
window.addEventListener('popstate',()=>{if(restoringHistory){restoringHistory=false;adoptHistory();return;}const old=new URL(shownURL);if(old.pathname===location.pathname&&old.search===location.search){shownURL=location.href;shownIndex=adoptHistory();scrollToAddress();return;}navigate(location.href,{pop:true});});
window.addEventListener('app:address',()=>{shownURL=location.href;shownIndex=adoptHistory();});
document.addEventListener('input',event=>{if(event.target.closest('#password-form,#new-student'))dirty=true;});
document.addEventListener('reset',()=>{dirty=false;});
// Each filter/page action supersedes prior reads. Aborted continuations never publish stale data.
for(const type of ['change','click','submit'])document.addEventListener(type,event=>{
 if(type==='change'||(type==='click'&&event.target.closest('.pagination button,[data-tab]'))||(type==='submit'&&event.target.closest('#search-form')))cancelReads();
},true);

main().catch(e=>{const root=$('#main')||$('#login-message')||document.body;root.innerHTML=errorBox(e.message)+`<button class="secondary" id="retry">重新加载</button>`;$('#retry').onclick=()=>location.reload();});

window.addEventListener('app:loading',event=>{
 if(!nativeQuery('.app'))return;
 let status=nativeQuery('#data-status');if(!status){status=document.createElement('span');status.id='data-status';status.className='data-status';status.setAttribute('role','status');nativeQuery('.breadcrumb').append(status);}
 status.textContent=event.detail?'正在更新…':'';
});
