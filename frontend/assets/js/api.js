import {requestSignal,exitSession} from './navigation.js?v=20261020-navigation-1';
let redirecting=false;
export const tokenKey='learning-token';
export class ApiError extends Error{constructor(message,status){super(message);this.status=status;}}
async function request(path,{method='GET',body}={}){
 const signal=method==='GET'?requestSignal():undefined;
 const token=sessionStorage.getItem(tokenKey),headers={'Content-Type':'application/json'};
 if(token)headers.Authorization=`Bearer ${token}`;
 let response;
 try{response=await fetch('/api'+path,{method,headers,signal,body:body===undefined?undefined:JSON.stringify(body)});}catch(error){if(signal?.aborted)throw new DOMException('','AbortError');throw new ApiError('无法连接服务器，请检查服务后重试',0);}
 let result;try{result=await response.json();}catch{if(signal?.aborted)throw new DOMException('','AbortError');throw new ApiError('服务器响应异常，请稍后重试',response.status);}
 if(signal?.aborted)throw new DOMException('','AbortError');
 if(!response.ok||result.code!==1){
   if(response.status===401){sessionStorage.removeItem(tokenKey);if(location.pathname!=='/login.html'&&!redirecting){redirecting=true;exitSession('/login.html?expired=1');}}
   throw new ApiError(result.msg||'操作失败',response.status);
 }
 return result.data;
}
export function query(values){const p=new URLSearchParams();for(const[k,v]of Object.entries(values))if(v!==null&&v!==undefined&&v!=='')p.set(k,String(v));const s=p.toString();return s?'?'+s:'';}

let reading=0;
export async function api(path,options={}){
 const read=!options.method||options.method==='GET';
 if(read)window.dispatchEvent(new CustomEvent('app:loading',{detail:++reading}));
 try{return await request(path,options);}finally{if(read)window.dispatchEvent(new CustomEvent('app:loading',{detail:--reading}));}
}
