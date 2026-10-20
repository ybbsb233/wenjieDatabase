import {viewRoot,cancelled} from './navigation.js?v=20261020-navigation-1';
export const $=(selector,root=viewRoot())=>root.matches?.(selector)?root:root.querySelector(selector);
export const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const pct=value=>value===null||value===undefined?'—':Number(value).toFixed(1)+'%';
export const time=value=>value?String(value).replace('T',' ').slice(0,16):'—';
export const number=value=>Number(value||0).toLocaleString('zh-CN');
export const kinds={SINGLE:'单选题',MULTIPLE:'多选题',JUDGE:'判断题'};
export const levels={NO_DATA:'暂无记录',INSUFFICIENT:'练习不足',WEAK:'优先复习',REVIEW:'需要巩固',GOOD:'掌握较好'};
export function badge(level){return `<span class="badge ${String(level).toLowerCase()}">${esc(levels[level]||level)}</span>`;}
export function empty(title='暂无数据',description='完成一次练习后，这里将展示你的学习记录。',action=''){return `<div class="empty"><strong>${esc(title)}</strong><p>${esc(description)}</p>${action}</div>`;}
export function toast(message){if(!message)return;document.querySelector('.toast')?.remove();const el=document.createElement('div');el.className='toast';el.setAttribute('role','status');el.textContent=message;document.body.append(el);setTimeout(()=>el.remove(),4000);}
export function errorBox(message){return `<div class="error-box" role="alert">${esc(message)}</div>`;}
export async function busy(button,action){const label=button.textContent;button.disabled=true;button.dataset.working='true';button.textContent='处理中…';try{return await action();}catch(e){if(!cancelled(e))toast(e.message);}finally{delete button.dataset.working;button.disabled=false;button.textContent=label;}}
export function heading(eyebrow,title,subtitle,action=''){return `<div class="page-heading"><div><div class="eyebrow">${esc(eyebrow)}</div><h1>${esc(title)}</h1><p class="subtitle">${esc(subtitle)}</p></div>${action}</div>`;}
export function stats(items){return `<div class="grid ${items.length===3?'three':'four'}">${items.map(x=>{const tag=x.href?'a':'div';return `<${tag} class="stat${x.href?' stat-link':''}"${x.href?` href="${esc(x.href)}"`:''}><div class="stat-label">${esc(x.label)}${x.href?'<span class="stat-arrow" aria-hidden="true">↗</span>':''}</div><div class="stat-value">${esc(x.value)}${x.unit?`<small>${esc(x.unit)}</small>`:''}</div><div class="stat-foot">${esc(x.note||'')}</div></${tag}>`;}).join('')}</div>`;}
export function table(headers,rows){return `<div class="table-wrap"><table><thead><tr>${headers.map(h=>`<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.join('')}</tbody></table></div>`;}
export function pagination(container,total,page,size,onPage,onSizeChange){
 const pages=Math.max(1,Math.ceil(total/size));
 container.innerHTML=`<div class="pagination">${onSizeChange?`<form class="page-size-form"><label>每页 <input type="number" name="pageSize" min="1" max="50" step="1" value="${size}" required aria-label="每页显示条数"> 条</label></form>`:''}<span>共 ${number(total)} 条 · ${page} / ${pages} 页</span><button class="secondary small" data-dir="-1" ${page===1?'disabled':''}>上一页</button><button class="secondary small" data-dir="1" ${page>=pages?'disabled':''}>下一页</button></div>`;
 container.querySelectorAll('[data-dir]').forEach(b=>b.onclick=()=>onPage(page+Number(b.dataset.dir)));
 if(onSizeChange){
  const form=container.querySelector('.page-size-form'),input=form.elements.pageSize;
  const apply=()=>{if(!input.reportValidity())return;const value=Number(input.value);if(value!==size)onSizeChange(value);};
  input.onchange=apply;form.onsubmit=e=>{e.preventDefault();apply();};
 }
}
export function courseOptions(courses,all=false){return (all?'<option value="">全部课程</option>':'')+courses.map(c=>`<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('');}
export function bar(value){return `<div class="bar" aria-hidden="true"><span style="width:${Math.max(0,Math.min(100,Number(value)||0))}%"></span></div>`;}
export function trendChart(rows){if(!rows.length)return empty('还没有练习趋势','完成练习后，将按时间展示最近 20 次表现。');const w=700,h=180,pad=30,points=rows.map((r,i)=>[pad+(w-2*pad)*(rows.length===1?.5:i/(rows.length-1)),h-pad-(h-2*pad)*Number(r.accuracy)/100]);return `<svg viewBox="0 0 ${w} ${h}" class="chart" role="img" aria-label="最近练习正确率趋势">${[0,50,100].map(v=>`<line x1="${pad}" x2="${w-pad}" y1="${h-pad-(h-2*pad)*v/100}" y2="${h-pad-(h-2*pad)*v/100}" stroke="#e9ede4"/><text x="0" y="${h-pad-(h-2*pad)*v/100+4}" class="chart-label">${v}%</text>`).join('')}<polyline class="chart-line" points="${points.map(p=>p.join(',')).join(' ')}"/>${points.map((p,i)=>`<circle cx="${p[0]}" cy="${p[1]}" r="4" class="chart-dot"><title>${esc(time(rows[i].submittedAt))}，${rows[i].questionCount} 题，正确率 ${pct(rows[i].accuracy)}</title></circle>`).join('')}</svg><p class="small-text muted">${esc(time(rows[0].submittedAt))} 至 ${esc(time(rows.at(-1).submittedAt))} · 最近 ${rows.length} 次练习；题目和题量可能不同，曲线仅反映练习表现。</p>`;}
