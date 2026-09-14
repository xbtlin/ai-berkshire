# 本轮实时核验记录

日期：2026年9月6日。历史财务原件及其双源核验承接同日已完成的腾讯、拼多多单公司审计与七公司商业模式底稿，不复制整份旧研究。

| 项目 | 来源 | 本轮结果 |
|---|---|---|
| 腾讯9/4正规收盘442.80港元 | https://stockanalysis.com/quote/hkg/0700/history/ ; https://kr.investing.com/equities/tencent-holdings-hk-historical-data | live读取相符；来源S&P与Investing，非两个同源S&P网站 |
| PDD9/4正规收盘82.21美元 | https://stockanalysis.com/stocks/pdd/history/ ; https://chartexchange.com/symbol/nasdaq-pdd/historical/ | live读取历史表相符；顶部最后逐笔82.20与盘后82.30另列，不混用 |
| 腾讯已发行9,103,153,877股 | https://www.tencent.com/wp-content/uploads/2026/09/e_Next-Day-Disclosure-Return_20260904.pdf | web解析失败；curl实时下载成功，SHA256与同日先前取得原件一致。第1页closing balance Sep 4 |
| PDD实际普通股5,693,585,848 | https://investor.pddholdings.com/static-files/92dafbdc-3125-4f2c-a28f-3d61203efbaf | live读取第120页，日期2026-03-18；封面另有2025-12-31相同数值。不是9/4新股本 |
| PDD半年加权稀释股数、4普通股/ADS | https://investor.pddholdings.com/news-releases/news-release-details/pdd-holdings-announces-second-quarter-2026-unaudited-financial/ | live读取股数表；半年5,907百万普通股、季度5,894百万普通股；均不可代替期末已发行股数 |
| 汇率美元6.7787、港元0.86458人民币 | https://hzf.mofcom.gov.cn/article/zyfw/jrfw/jrfwywzn/jrfwwh/hlfxglzy/202609/7872.html ; https://www.moneydj.com/KMDJ/news/newsviewer.aspx?a=9a21ef2e-aa18-4653-a227-23b2f44194d2 | live搜索结果返回两个数值；商务部正文open超时。公告为9月4日官方中间价 |
| PDD不预期可预见未来分红 | 同上PDD20-F，第16、67、125页 | live读取确认；不意味着承诺永不分配，也不把未来回购写成事实 |

腾讯原件本轮下载路径为临时目录，不作为交付依赖；长期可用已保存原件为`../../腾讯/审计-20260906/20260904翌日披露.pdf`。两份SHA256相同：`1880daaf638ba97d22cc3376fe7f7e82e3067641ce59de484544d9da360bcdd2`。

官方股本优先于行情网站取整股数。精确股本没有宣称双源同等精度确认；价格和汇率经过双源数值比较，独立性不等同于逐笔行情采集链完全可知。

`audit.py`将seed42抽中的1项官方股本事实、13项模型输入/重算和1项误抽月份分开。模型复算通过不表示预测被证实；股本事实仅单源官方确认，不包装成双源。
