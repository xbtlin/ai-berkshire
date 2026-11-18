from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets/tencent-q3-2026'; OUT.mkdir(parents=True,exist_ok=True)
font=font_manager.FontProperties(fname='/System/Library/Fonts/STHeiti Medium.ttc')
plt.rcParams.update({'font.family':font.get_name(),'axes.unicode_minus':False,'font.size':13,'figure.facecolor':'#faf9f6','axes.facecolor':'#faf9f6','axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.edgecolor':'#cccccc'})
navy='#163b4e'; red='#b94a48'; green='#397b70'; gray='#667783'
fig,ax=plt.subplots(figsize=(11,6.6));fig.subplots_adjust(left=.08,right=.98,top=.78,bottom=.2)
labels=['2025Q3\n经营利润','新增\n毛利润','销售费用\n增加','一般行政\n费用增加','其他收益\n变化','2026Q3\n经营利润']
vals=[635.54,71.13,-6.76,-98.18,-10.26,591.47]
cur=vals[0]
for i,v in enumerate(vals):
 if i in (0,5): bottom=0; height=v; color=navy
 else: bottom=min(cur,cur+v);height=abs(v);color=green if v>0 else red;cur+=v
 ax.bar(i,height,bottom=bottom,color=color,width=.62,zorder=3)
 y=bottom+height+12
 ax.text(i,y,('' if i in (0,5) else '+')+f'{v:.2f}' if v>=0 else f'{v:.2f}',ha='center',va='bottom',fontsize=13,fontweight='bold',color=color)
ax.set_xticks(range(6),labels);ax.set_ylim(0,790);ax.set_yticks([0,200,400,600,800]);ax.grid(axis='y',alpha=.15,zorder=0);ax.tick_params(axis='both',length=0);ax.set_ylabel('人民币亿元',loc='top',color=gray)
fig.text(.08,.94,'毛利润增加，仍未覆盖费用增长',size=22,weight='bold',color=navy)
fig.text(.08,.86,'腾讯 2026Q3 IFRS 经营利润同比桥接',size=14,color=gray)
fig.text(.08,.08,'一般及行政开支增加 98.18 亿元，其中研发开支增加 95.40 亿元。',size=12,color=gray)
fig.text(.08,.035,'来源：腾讯 2026Q3 业绩公告第 5、28 页；作者计算。口径与归母净利润不同。',size=10,color=gray)
fig.savefig(OUT/'profit-bridge.png',dpi=200);plt.close(fig)
fig,(a,b)=plt.subplots(1,2,figsize=(11,7));fig.subplots_adjust(left=.08,right=.97,top=.76,bottom=.25,wspace=.35)
fig.text(.08,.94,'现金已付出，未来回报还需验证',size=22,weight='bold',color=navy)
fig.text(.08,.87,'预付款影响现金时点；资本开支与现金付款不是同一个数字',size=14,color=gray)
a.bar([0,1],[-691,169],color=[red,green],width=.5,zorder=3);a.axhline(0,color=gray,lw=.8)
a.set_xticks([0,1],['报告自由现金流','剔除算力预付款']);a.set_ylim(-850,350);a.set_yticks([-800,-400,0,200]);a.set_title('Q3 自由现金流｜约亿元',loc='left',pad=20,color=navy)
a.text(0,-725,'-691',ha='center',va='top',size=19,weight='bold',color=red);a.text(1,190,'+169',ha='center',size=19,weight='bold',color=green)
a.text(.5,-430,'差额约 860 亿元\n仍是真实现金支出',ha='center',size=13,color=navy,bbox=dict(facecolor='#faf9f6',edgecolor='none',pad=5))
b.bar(range(3),[129.83,527.84,814.33],color=[gray,gray,navy],width=.52,zorder=3)
b.set_xticks(range(3),['2025Q3','2026Q2','2026Q3']);b.set_ylim(0,1000);b.set_yticks([0,250,500,750]);b.set_title('资本开支｜权责口径，亿元',loc='left',pad=20,color=navy)
for i,v in enumerate([129.83,527.84,814.33]):b.text(i,v+20,f'{v:.2f}',ha='center',size=13,weight='bold',color=navy)
for ax in [a,b]:ax.grid(axis='y',alpha=.15,zorder=0);ax.tick_params(length=0,labelsize=11)
fig.text(.08,.13,'Q3 资本开支付款约 651 亿元；814.33 亿元为公司披露的资本开支。',size=12,color=gray)
fig.text(.08,.085,'两者不能相加后再从利润中扣除；预付款也不能无条件加回为“可分红现金”。',size=11,color=gray)
fig.text(.08,.035,'来源：腾讯 2026Q3 业绩公告第 12、17 页。左图使用公告取整值；差额为作者推算。',size=10,color=gray)
fig.savefig(OUT/'cash-and-capex.png',dpi=200);plt.close(fig)
print(OUT)
fig,ax=plt.subplots(figsize=(10.5,6.7));fig.subplots_adjust(left=.09,right=.97,top=.77,bottom=.23)
fig.text(.09,.94,'新 AI 产品的净拖累扩大',size=22,weight='bold',color=navy)
fig.text(.09,.86,'调整经营利润，人民币亿元；剔除新 AI 产品的数值为公告取整值',size=13,color=gray)
x=[0,1];w=.3
ax.bar([v-w/2 for v in x],[861,833],width=w,color=gray,label='剔除新 AI 产品')
ax.bar([v+w/2 for v in x],[756.36,680.73],width=w,color=navy,label='包含新 AI 产品')
for xx,y in zip([-.15,.85],[861,833]):ax.text(xx,y+18,f'约{y}',ha='center',size=14,color=gray)
for xx,y in zip([.15,1.15],[756.36,680.73]):ax.text(xx,y+18,f'{y:.2f}',ha='center',size=14,color=navy)
ax.set_xticks(x,['2026Q2：差约105亿元','2026Q3：差约152亿元']);ax.set_ylim(0,1100);ax.set_yticks([0,250,500,750,1000]);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True);ax.tick_params(length=0);ax.legend(loc='upper left',frameon=False,ncol=2,fontsize=12)
fig.text(.09,.12,'差额是收入、成本和费用的净贡献，不是集团 AI 支出总额。',size=12,color=navy)
fig.text(.09,.07,'原有广告等业务仍包含 AI 成本；“剔除新 AI”不等于“完全不做 AI”。',size=11,color=gray)
fig.text(.09,.025,'来源：腾讯 2026Q2、Q3 业绩公告；作者计算。Q3 公告第8、11页。',size=10,color=gray)
fig.savefig(OUT/'ai-profit-comparison.png',dpi=200);plt.close(fig)
