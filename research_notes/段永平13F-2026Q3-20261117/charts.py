"""Static publication charts derived solely from comparison.json."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'assets/duan-13f-2026q3'
OUT.mkdir(parents=True,exist_ok=True)
data=json.loads((HERE/'comparison.json').read_text())
font=FontProperties(fname='/System/Library/Fonts/Hiragino Sans GB.ttc')
plt.rcParams.update({'axes.unicode_minus':False,'font.size':15,'figure.facecolor':'#f8f7f3','axes.facecolor':'#f8f7f3'})
NAVY='#243b53'; TEAL='#177e79'; RED='#b55145'; GRAY='#b9c3cc'

def base(title,sub):
    fig,ax=plt.subplots(figsize=(10,7.6))
    fig.subplots_adjust(left=.19,right=.90,top=.77,bottom=.15)
    fig.text(.055,.93,title,fontproperties=font,fontsize=27,color=NAVY,weight='bold')
    fig.text(.055,.866,sub,fontproperties=font,fontsize=13,color='#52616b')
    for sp in ax.spines.values():sp.set_visible(False)
    ax.tick_params(axis='both',length=0,pad=10,labelcolor=NAVY)
    return fig,ax

rows=sorted([r for r in data['changes'] if r['action'] in ('增加','减少')],key=lambda r:float(r['share_change_pct']),reverse=True)
fig,ax=base('股数变化：增持两项，减持六项','H&H International Investment｜2026年9月30日 对比 6月30日')
y=np.arange(len(rows)); vals=[float(r['share_change_pct']) for r in rows]
ax.barh(y,vals,color=[TEAL if v>0 else RED for v in vals],height=.56)
ax.set_yticks(y);ax.set_yticklabels([r['name'] for r in rows],fontproperties=font,fontsize=16)
ax.invert_yaxis();ax.axvline(0,color=GRAY,lw=1)
ax.set_xlim(-85,33);ax.set_xticks([-60,-40,-20,0,20]);ax.set_xticklabels(['-60%','-40%','-20%','0','+20%'])
for i,v in enumerate(vals):ax.text(v+1.2 if v>0 else v-1.2,i,f'{v:+.2f}%',va='center',ha='left' if v>0 else 'right',fontsize=14,color=NAVY)
fig.text(.055,.066,'口径：季末申报股数净变化；不包括新增披露、退出披露及股数未变的项目。',fontproperties=font,fontsize=11,color='#52616b')
fig.text(.055,.032,'来源：SEC 两季原始 13F 信息表；13f.info 逐行交叉核对。',fontproperties=font,fontsize=11,color='#52616b')
fig.savefig(OUT/'share-changes.png',dpi=200);plt.close(fig)

rows=data['changes'][:8]
fig,ax=base('股数减少，权重未必下降','苹果股数减少21.76%，组合权重仍约41%｜分母为当季13F申报总市值')
y=np.arange(len(rows))
v2=[float(r['q2_weight_pct']) for r in rows];v3=[float(r['q3_weight_pct']) for r in rows]
ax.barh(y-.17,v2,height=.28,color=GRAY,label='2026 Q2')
ax.barh(y+.17,v3,height=.28,color=NAVY,label='2026 Q3')
ax.set_yticks(y);ax.set_yticklabels([r['name'] for r in rows],fontproperties=font,fontsize=16);ax.invert_yaxis()
ax.set_xlim(0,48);ax.set_xticks([0,10,20,30,40]);ax.set_xticklabels(['0','10%','20%','30%','40%'])
for i,(a,b) in enumerate(zip(v2,v3)):
    ax.text(a+.5,i-.17,f'{a:.2f}%',va='center',fontsize=11,color='#697886')
    ax.text(b+.5,i+.17,f'{b:.2f}%',va='center',fontsize=11,color=NAVY)
ax.legend(frameon=False,loc='lower right',fontsize=13)
fig.text(.055,.066,'展示三季度前八大持仓；权重变化同时受股数、价格和组合总市值影响。',fontproperties=font,fontsize=11,color='#52616b')
fig.text(.055,.032,'来源：SEC 两季原始 13F 信息表；13f.info 逐行交叉核对。',fontproperties=font,fontsize=11,color='#52616b')
fig.savefig(OUT/'weights.png',dpi=200);plt.close(fig)
print(OUT)
