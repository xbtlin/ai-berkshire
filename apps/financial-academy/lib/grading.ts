import type {Question,Grade,Attempt,Progress} from './types';
export function publicQuestion(q:Question):Question{const {answer,explanation,tolerance,...safe}=q;return safe;}
export function grade(questions:Question[],answers:Record<string,unknown>,kind:string):Grade{
 const results=questions.map(q=>{
  const raw=answers[q.id];
  const allowed=(typeof raw==='number'&&Number.isFinite(raw))||(typeof raw==='string'&&raw.trim()!==''&&/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(raw.trim()));
  const value=allowed?Number(raw):NaN;
  const correct=Number.isFinite(value)&&typeof q.answer==='number'&&(q.type==='single'?Number.isInteger(value)&&value===q.answer:Math.abs(value-q.answer)<=(q.tolerance??0.01)+Number.EPSILON*10);
  return {...q,correct,given:typeof raw==='string'||typeof raw==='number'?raw:null};
 });
 const correct=results.filter(q=>q.correct).length;
 const criticalPassed=results.filter(q=>q.critical).every(q=>q.correct);
 const passed=questions.length>0&&(kind==='final'?correct>=Math.ceil(questions.length*.85)&&criticalPassed:kind==='review'?correct===questions.length:correct>=Math.ceil(questions.length*.75));
 return {correct,total:questions.length,score:questions.length?Math.round(correct/questions.length*100):0,passed,criticalPassed,results};
}
export function makeProgress(reads:string[],attempts:Attempt[]):Progress{
 const best:Record<string,number>={};const wrong=new Map<string,any>();let graduatedAt:string|null=null;
 for(const a of attempts){
  if(a.kind==='module'&&a.moduleId)best[a.moduleId]=Math.max(best[a.moduleId]??0,a.score);
  if(a.kind==='final'&&a.passed&&!graduatedAt)graduatedAt=a.createdAt;
  for(const q of a.result.results){if(q.correct)wrong.delete(q.id);else wrong.set(q.id,q);}
 }
 return {reads,attempts,best,wrong:[...wrong.values()],graduated:!!graduatedAt,graduatedAt};
}
