// Shared lifecycle for the existing page renderers. No HTML fetching or second renderer.
let root=document,controller=new AbortController(),guard=()=>false,cleanup=()=>{};
let localNavigation=null,allowUnload=false;
export const viewRoot=()=>root;
export const setViewRoot=value=>{root=value;};
export const requestSignal=()=>controller.signal;
export function cancelReads(){controller.abort();controller=new AbortController();}
export const cancelled=error=>error?.name==='AbortError';
export function setLeaveGuard(check,dispose=()=>{}){guard=check;cleanup=dispose;}
export function canLeave(){return !guard()||confirm('有未保存的内容或未提交的练习，确定离开吗？');}
export function disposeView(){cleanup();cleanup=()=>{};guard=()=>false;localNavigation=null;}
export const setLocalNavigation=handler=>{localNavigation=handler;};
export const updateLocalNavigation=url=>localNavigation?.(url);
export function go(url,replace=false){window.dispatchEvent(new CustomEvent('app:navigate',{detail:{url,replace,completed:true}}));}
export function updateQuery(values,replace=false){const url=new URL(location.href);for(const [key,value] of Object.entries(values)){if(value===null||value===undefined||value==='')url.searchParams.delete(key);else url.searchParams.set(key,value);}writeHistory(url,replace);window.dispatchEvent(new Event('app:address'));}
window.addEventListener('beforeunload',event=>{if(!allowUnload&&(guard()||document.querySelector('[data-working]'))){event.preventDefault();event.returnValue='';}});

export const saveLifecycle=()=>({guard,cleanup,localNavigation});
export function restoreLifecycle(saved){({guard,cleanup,localNavigation}=saved);}

export function exitSession(url){allowUnload=true;disposeView();location.replace(url);}

let entryIndex=history.state?.navigationIndex??0;
history.replaceState({...history.state,navigationIndex:entryIndex},'',location.href);
export function writeHistory(url,replace=false){if(!replace)entryIndex++;history[replace?'replaceState':'pushState']({navigationIndex:entryIndex},'',url);}
export function adoptHistory(){entryIndex=history.state?.navigationIndex??entryIndex;return entryIndex;}
