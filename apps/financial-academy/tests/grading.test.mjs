import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
import test from 'node:test';
import { grade, publicQuestion, makeProgress } from '../lib/grading.ts';
const course=JSON.parse(readFileSync(new URL('../lib/curriculum.json',import.meta.url),'utf8'));
const questions=[...course.modules.flatMap(m=>m.questions),...course.finalQuestions];
const answers=Object.fromEntries(questions.map(q=>[q.id,q.answer]));
const wrong=999999;
test('12 chapters, 72 concepts, 48 chapter questions and 24 final questions have valid keys and sources',()=>{
 assert.equal(course.modules.length,12);assert.equal(course.modules.reduce((n,m)=>n+m.concepts.length,0),72);
 assert.equal(questions.length,72);assert.equal(course.finalQuestions.length,24);
 assert.equal(new Set(questions.map(q=>q.id)).size,questions.length);
 assert.equal(course.finalQuestions.filter(q=>q.critical).length,4);
 for(const m of course.modules){assert.equal(m.questions.length,4);for(const id of m.sourceIds)assert.ok(course.sources.some(s=>s.id===id));}
 for(const q of questions){assert.ok(Number.isFinite(q.answer));assert.ok(q.explanation);if(q.type==='single')assert.ok(q.options[q.answer]);else{assert.equal(q.type,'number');assert.ok(q.unit);}}
});
test('public questions hide answers, tolerance and explanations',()=>{
 for(const q of questions){const safe=publicQuestion(q);for(const key of ['answer','tolerance','explanation'])assert.equal(key in safe,false);assert.equal(safe.id,q.id);}
});
test('chapter passes with 3/4 but fails with 2/4',()=>{
 for(const m of course.modules){const a={...answers,[m.questions[0].id]:wrong};assert.equal(grade(m.questions,a,'module').passed,true);a[m.questions[1].id]=wrong;assert.equal(grade(m.questions,a,'module').passed,false);}
});
test('final requires at least 21/24 and rejects every critical error even at 23/24',()=>{
 assert.equal(grade(course.finalQuestions,answers,'final').passed,true);
 const ordinary=course.finalQuestions.filter(q=>!q.critical);const a={...answers};ordinary.slice(0,3).forEach(q=>a[q.id]=wrong);
 assert.equal(grade(course.finalQuestions,a,'final').passed,true);a[ordinary[3].id]=wrong;assert.equal(grade(course.finalQuestions,a,'final').passed,false);
 for(const q of course.finalQuestions.filter(q=>q.critical))assert.equal(grade(course.finalQuestions,{...answers,[q.id]:wrong},'final').passed,false);
});
test('numeric answers reject blank or coercible non-numbers, accept numeric text and obey tolerance',()=>{
 const q={id:'numeric-test',type:'number',prompt:'test',concept:'test',answer:0,tolerance:.01};
 for(const raw of ['',null,'abc',[],{},true,Infinity,NaN])assert.equal(grade([q],{[q.id]:raw},'review').passed,false);
 assert.equal(grade([q],{[q.id]:'0'},'review').passed,true);assert.equal(grade([q],{[q.id]:.009},'review').passed,true);assert.equal(grade([q],{[q.id]:.011},'review').passed,false);
});
test('review clears a wrong answer but cannot substitute for passing final',()=>{
 const q=questions[0],base={id:'1',kind:'review',moduleId:null,score:0,passed:false,createdAt:'2026-11-15T00:00:00Z'};
 const failed={...base,result:grade([q],{[q.id]:wrong},'review')};const fixed={...base,id:'2',passed:true,result:grade([q],answers,'review')};
 assert.equal(makeProgress([],[failed]).wrong.length,1);const state=makeProgress([],[failed,fixed]);assert.equal(state.wrong.length,0);assert.equal(state.graduated,false);
 const final={...base,id:'3',kind:'final',passed:true,result:grade(course.finalQuestions,answers,'final')};assert.equal(makeProgress([],[failed,fixed,final]).graduated,true);
});
