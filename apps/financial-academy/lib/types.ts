export type Question={id:string;type:'single'|'number';prompt:string;options?:string[];answer?:number;tolerance?:number;unit?:string;explanation?:string;concept:string;critical?:boolean;moduleId?:string};
export type Concept={title:string;body:string;formula?:string;pitfall:string;example:string};
export type Module={id:string;title:string;subtitle:string;stage:string;minutes:number;objective:string;concepts:Concept[];checklist:string[];sourceIds:string[];questions:Question[]};
export type Course={modules:Module[];finalQuestions:Question[];sources:{id:string;title:string;url:string;note:string;checkedAt:string}[]};
export type MarkedQuestion=Question & {correct:boolean;given:string|number|null};
export type Grade={correct:number;total:number;score:number;passed:boolean;criticalPassed:boolean;results:MarkedQuestion[]};
export type Attempt={id:string;kind:string;moduleId:string|null;score:number;passed:boolean;result:Grade;createdAt:string};
export type Progress={reads:string[];attempts:Attempt[];best:Record<string,number>;wrong:MarkedQuestion[];graduated:boolean;graduatedAt:string|null};
