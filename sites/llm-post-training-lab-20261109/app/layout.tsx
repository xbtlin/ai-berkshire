import type {Metadata} from 'next';
import './globals.css';
export const metadata:Metadata={title:'后训练实验室 · 从 SFT 到 RLVR',description:'八周后训练路线、24 份一手资料、四个互动数学实验与实验手册。',icons:{icon:'/favicon.svg'}};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="zh-CN"><body>{children}</body></html>}
