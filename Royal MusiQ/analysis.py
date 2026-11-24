import numpy as np,pandas as pd,matplotlib.pyplot as plt
from pathlib import Path
P=Path(__file__).parent
rows=[('Royal MusiQ','Unknown',2300973,386277,'23 Nov','StreamClout'),('Zee Nxumalo','18–24',2342151,1972908,'23 Nov','StreamClout'),('CowBoii','18–24',528927,485203,'21 Nov','artist.tools'),('Uncle Waffles','25–29',1485890,1651068,'22 Nov','StreamClout'),('Young Stunna','25–29',2993138,2038392,'23 Nov approx.','StreamClout'),('Focalistic','30–34',2969017,1702321,'23 Nov','StreamClout'),('Kabza De Small','30–34',4052829,8482380,'18 Nov','StreamClout'),('Xduppy','Unclassified',2299558,593168,'21 Nov approx.','StreamClout'),('LeeMcKrazy','Unclassified',1797148,1122172,'23 Nov','StreamClout')]
df=pd.DataFrame(rows,columns=['artist','age_band','listeners','followers','snapshot_2026','provider']);df['ratio']=df.followers/df.listeners;df.to_csv(P/'peer_data.csv',index=False)
peer=df.iloc[1:7].copy();roy=df.iloc[0]; X=np.log10(peer[['listeners','followers']].to_numpy()); z=np.log10([roy.listeners,roy.followers]); sd=X.std(axis=0,ddof=1); groups=peer.age_band.unique(); dist={}; means={}
for g in groups:
 a=peer[peer.age_band==g]; means[g]=a[['listeners','followers']].mean().to_numpy(); dist[g]=np.linalg.norm((np.log10(a[['listeners','followers']]).mean().to_numpy()-z)/sd)
print('means',means,'distance',dist,'ratio',roy.ratio, 'reach distances', {g:abs(np.log10(peer[peer.age_band==g].listeners).mean()-z[0])/sd[0] for g in groups}); print('arithmetic reach closest', {g:abs(means[g][0]-roy.listeners) for g in groups})
# charts
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#222222','axes.titleweight':'bold','figure.facecolor':'white','axes.facecolor':'white'})
blue='#163d63'; muted='#96afc4'; gold='#a77325'
def save(fig,name): fig.tight_layout();fig.savefig(P/(name+'.png'),dpi=190,bbox_inches='tight',pad_inches=.10);plt.close(fig)
def hbar(field,name,label):
 d=df.sort_values(field); fig,ax=plt.subplots(figsize=(7.1,3.0)); v=d[field]/1e6; ax.barh(d.artist,v,color=[blue if a=='Royal MusiQ' else muted for a in d.artist]); ax.set_xlabel(label); ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True);ax.set_xlim(0,max(v)*1.18);[ax.text(x+.025,i,f'{x:.2f}',va='center',fontsize=8) for i,x in enumerate(v)];save(fig,name)
hbar('listeners','reach','Monthly listeners (millions)'); hbar('followers','followers','Spotify followers (millions)')
fig,ax=plt.subplots(figsize=(7.1,2.6)); a=np.arange(3); ax.bar(a-.17,[means[g][0]/1e6 for g in groups],.34,label='Mean listeners',color=blue);ax.bar(a+.17,[means[g][1]/1e6 for g in groups],.34,label='Mean followers',color=muted);ax.axhline(roy.listeners/1e6,color=gold,linestyle='--',label='Royal listeners');ax.axhline(roy.followers/1e6,color=gold,linestyle=':',label='Royal followers');ax.set_xticks(a,groups);ax.set_ylabel('Millions');ax.legend(ncol=2,fontsize=8,loc='upper left');save(fig,'cohort')
fig,ax=plt.subplots(figsize=(7.1,2.5));ax.bar(groups,list(dist.values()),color=[blue if v==min(dist.values()) else muted for v in dist.values()]);ax.set_ylabel('Standardised distance');[ax.text(i,v+.03,f'{v:.2f}',ha='center') for i,v in enumerate(dist.values())];ax.set_ylim(0,max(dist.values())*1.18);save(fig,'distance')
# historical and forecasts, holdout last two weeks, 3 training points
v=np.array([2343443,2311273,2288927,2292754,2300973],float); x=np.arange(5); h=np.arange(1,13); slope,intercept=np.polyfit(x,v,1); pred={'Naive':np.full(12,v[-1]),'3-week mean':np.full(12,v[-3:].mean()),'OLS trend':intercept+slope*(4+h)}
train=v[:3]; test=v[3:]; ts,ti=np.polyfit(np.arange(3),train,1); hold={'Naive':np.full(2,train[-1]),'3-week mean':np.full(2,train.mean()),'OLS trend':ti+ts*np.arange(3,5)};mae={k:np.mean(abs(p-test)) for k,p in hold.items()};print('forecast', {k:[p[3],p[11]] for k,p in pred.items()},'mae',mae,'mean',v.mean(),'sd',v.std(ddof=1),'slope',slope)
fig,ax=plt.subplots(figsize=(7.1,2.65));ax.plot(x,v/1e6,'o-',color=blue,label='Observed');ax.set_xticks(x,['26 Oct','2 Nov','9 Nov','16 Nov','23 Nov']);ax.set_ylabel('Monthly listeners (M)');ax.grid(alpha=.2);save(fig,'history')
fig,ax=plt.subplots(figsize=(7.1,2.75));ax.plot(x,v/1e6,'o-',color=blue,label='Observed');colors=['#477b99','#a77325','#858585'];forbidden=None
for (k,p),c in zip(pred.items(),colors):ax.plot(np.r_[4,4+h],np.r_[v[-1],p]/1e6,'--',label=k,color=c)
ax.axvline(4,color='#aaa',lw=.8);ax.set_xticks([0,4,8,12,16],['26 Oct','23 Nov','+4 wk','+8 wk','+12 wk']);ax.set_ylabel('Monthly listeners (M)');ax.legend(ncol=2,fontsize=8);ax.grid(alpha=.2);save(fig,'forecast')
# tiktok visible first 23 records (rounded thousands)
posts=[('15 Nov',474,71),('11 Nov',734,145),('10 Nov',761,228),('8 Nov',491,49),('24 Oct',1600,321),('undated',943,123),('28 Sep',798,152),('26 Sep',662,115),('26 Sep',473,100),('22 Sep',750,101),('12 Sep',2000,442),('10 Sep',2300,492),('5 Sep',643,83),('5 Sep',2000,474),('2 Sep',1200,208),('31 Aug',631,81),('30 Aug',947,157),('30 Aug',994,216),('30 Aug',302,40),('29 Aug',965,200),('29 Aug',342,40),('29 Aug',1200,293),('27 Aug',394,61)]
post=pd.DataFrame(posts,columns=['date','views_k','likes_k']);post.to_csv(P/'tiktok_sample.csv',index=False);print('TT',post.views_k.mean(),post.views_k.median(),post.likes_k.mean(),post.likes_k.sum()/post.views_k.sum(),post.corr(numeric_only=True).iloc[0,1],(post.views_k>=1000).sum())
fig,ax=plt.subplots(figsize=(7.1,2.65));ax.scatter(post.views_k,post.likes_k,c=blue,alpha=.78);ax.set_xlabel('Views (thousands)');ax.set_ylabel('Likes (thousands)');ax.grid(alpha=.2);save(fig,'tiktok')
fig,ax=plt.subplots(figsize=(7.1,2.65));city=['Johannesburg','Pretoria','Durban','Cape Town','Lagos'];cityv=np.array([472995,257830,168524,136621,96636]);ax.barh(city[::-1],cityv[::-1]/1000,color=muted);ax.set_xlabel('Monthly listeners (thousands)');ax.set_xlim(0,540);[ax.text(v/1000+5,i,f'{v/1000:.0f}',va='center',fontsize=8) for i,v in enumerate(cityv[::-1])];save(fig,'cities')
fig,ax=plt.subplots(figsize=(7.1,2.5));plat=['TikTok','Instagram','Spotify','YouTube*'];pv=np.array([695463,389600,386277,90400]);ax.bar(plat,pv/1000,color=[blue,muted,muted,muted]);ax.set_ylabel('Followers/subscribers (000s)');[ax.text(i,v/1000+12,f'{v/1000:.1f}',ha='center',fontsize=9) for i,v in enumerate(pv)];ax.set_ylim(0,800);save(fig,'social')
# asset stress model exposure 100% vs reusable base; explicitly hypothetical
m=np.arange(13);fig,ax=plt.subplots(figsize=(7.1,2.7));
for floor,c in [(0,'#858585'),(.25,muted),(.50,blue)]:ax.plot(m,100*(floor+(1-floor)*.85**m),label=f'{floor:.0%} durable floor',color=c,lw=2)
ax.set_xlabel('Months after initial shock');ax.set_ylabel('Indexed attention (start = 100)');ax.legend(fontsize=8);ax.grid(alpha=.2);save(fig,'asset')
pd.DataFrame({'week':['2026-10-26','2026-11-02','2026-11-09','2026-11-16','2026-11-23'],'listeners':v.astype(int)}).to_csv(P/'weekly_listeners.csv',index=False)
# cross-platform comparator (different capture dates, channel scope noted in paper)
social=pd.DataFrame({'artist':['Royal MusiQ','Zee Nxumalo','Focalistic'],'instagram':[389600,1400000,2800000],'tiktok':[695463,3600000,8600],'youtube':[90400,423000,569000]});social.to_csv(P/'social_comparison.csv',index=False)
fig,ax=plt.subplots(figsize=(7.1,2.65));i=np.arange(3);w=.23
for j,(col,c) in enumerate(zip(['instagram','tiktok','youtube'],[blue,muted,gold])):ax.bar(i+(j-1)*w,social[col]/1e6,w,label=col.title(),color=c)
ax.set_xticks(i,social.artist);ax.set_ylabel('Accounts (millions)');ax.legend(ncol=3,fontsize=8);ax.grid(axis='y',alpha=.2);save(fig,'social_peer')
ben=np.array([2447567,2385407,2328773,2279649,2259649]);pd.DataFrame({'week':['2026-10-26','2026-11-02','2026-11-09','2026-11-16','2026-11-23'],'royal':v.astype(int),'benzoo':ben}).to_csv(P/'royal_benzoo.csv',index=False)
fig,ax=plt.subplots(figsize=(7.1,2.65));ax.plot(x,v/1e6,'o-',color=blue,label='Royal MusiQ');ax.plot(x,ben/1e6,'s-',color=gold,label='Benzoo');ax.set_xticks(x,['26 Oct','2 Nov','9 Nov','16 Nov','23 Nov']);ax.set_ylabel('Monthly listeners (M)');ax.legend(fontsize=8);ax.grid(alpha=.2);save(fig,'benzoo')
