import {getChatGPTUser} from '../../chatgpt-auth';
import {getDb} from '../../../db';
import {readings,submissions} from '../../../db/schema';
import {eq,asc} from 'drizzle-orm';
import curriculum from '../../../lib/curriculum.json';
import {grade,makeProgress} from '../../../lib/grading';
import type {Course,Question,Attempt} from '../../../lib/types';
export const dynamic='force-dynamic';
const course=curriculum as Course;
const json=(data:unknown,status=200)=>Response.json(data,{status,headers:{'Cache-Control':'no-store'}});
async function state(userId:string){
 const db=getDb();const [r,a]=await Promise.all([db.select().from(readings).where(eq(readings.userId,userId)),db.select().from(submissions).where(eq(submissions.userId,userId)).orderBy(asc(submissions.createdAt),asc(submissions.id))]);
 return makeProgress(r.map(x=>x.conceptId),a.map(x=>({...x,result:JSON.parse(x.resultJson)})) as Attempt[]);
}
export async function GET(){const user=await getChatGPTUser();if(!user)return json({error:'请登录后保存学习进度。'},401);try{return json(await state(user.userId));}catch{return json({error:'暂时无法读取进度，请稍后重试。'},503);}}
export async function POST(req:Request){
 const user=await getChatGPTUser();if(!user)return json({error:'请先登录，学习记录会随账号保存。'},401);
 const origin=req.headers.get('origin');if(origin&&origin!==new URL(req.url).origin)return json({error:'请求来源不匹配。'},403);
 let body:any;try{const text=await req.text();if(text.length>30000)return json({error:'请求过大。'},413);body=JSON.parse(text);}catch{return json({error:'请求格式无效。'},400);}
 if(!body||typeof body!=='object')return json({error:'请求格式无效。'},400);
 try{
  const db=getDb(),userId=user.userId;
  if(body.action==='read'){
   const m=course.modules.find(m=>m.id===body.moduleId);if(!m||!Number.isInteger(body.index)||body.index<0||body.index>=m.concepts.length)return json({error:'知识点不存在。'},400);
   await db.insert(readings).values({userId,conceptId:`${m.id}:${body.index}`,createdAt:new Date().toISOString()}).onConflictDoNothing();return json({progress:await state(userId)});
  }
  if(body.action!=='submit'||!['module','final','review'].includes(body.kind)||!body.answers||typeof body.answers!=='object'||Array.isArray(body.answers))return json({error:'答题格式无效。'},400);
  const current=await state(userId);let questions:Question[]=[];let moduleId:string|null=null;
  if(body.kind==='module'){
   const m=course.modules.find(m=>m.id===body.moduleId);if(!m)return json({error:'章节不存在。'},400);
   if(!m.concepts.every((_,i)=>current.reads.includes(`${m.id}:${i}`)))return json({error:'请先完成本章所有知识点，再参加闯关。'},403);
   questions=m.questions;moduleId=m.id;
  }else if(body.kind==='final'){
   if(!course.modules.every(m=>(current.best[m.id]??0)>=75))return json({error:'通过全部章节后，才能开始出师考试。'},403);
   questions=course.finalQuestions;
  }else{
   const id=body.questionId;if(typeof id!=='string'||!current.wrong.some(q=>q.id===id))return json({error:'这道题已不在待复习列表。'},400);
   questions=[...course.modules.flatMap(m=>m.questions),...course.finalQuestions].filter(q=>q.id===id);
  }
  if(questions.some(q=>body.answers[q.id]===undefined||String(body.answers[q.id]).trim()===''))return json({error:'请答完所有题目后再提交。'},400);
  const result=grade(questions,body.answers,body.kind);
  await db.insert(submissions).values({id:crypto.randomUUID(),userId,kind:body.kind,moduleId,score:result.score,passed:result.passed,resultJson:JSON.stringify(result),createdAt:new Date().toISOString()});
  return json({result,progress:await state(userId)});
 }catch{return json({error:'保存未成功，你的答案仍在当前页面。请重试。'},503);}
}
