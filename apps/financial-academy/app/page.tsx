import Academy from './academy';
import curriculum from '../lib/curriculum.json';
import { publicQuestion } from '../lib/grading';
import type { Course } from '../lib/types';
export default function Home() {
 const data=curriculum as Course;
 const safe={...data, modules:data.modules.map(m=>({...m,questions:m.questions.map(publicQuestion)})),finalQuestions:data.finalQuestions.map(publicQuestion)};
 return <Academy course={safe as Course}/>;
}
