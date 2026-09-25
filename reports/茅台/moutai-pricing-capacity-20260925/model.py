#!/usr/bin/env python3
"""Conditional 2026E-to-2036 model; all prospective inputs are assumptions."""
from decimal import Decimal as D, getcontext
import json
from pathlib import Path
getcontext().prec = 36

def forecast(volume, growth='0.05', series_volume=55000, series_asp='65', margin='0.49'):
    asp = D(312) * (1 + D(growth)) ** 10
    revenue = (D(volume)*asp + D(series_volume)*D(series_asp))/10000 + D('0.63')
    return dict(moutai_volume_tonnes=volume, moutai_asp_wan=asp, series_volume_tonnes=series_volume,
                series_asp_wan=D(series_asp), attributable_margin=D(margin), revenue_yi=revenue,
                attributable_profit_yi=revenue*D(margin))

central=forecast(68000)
old=D('1095.9487')
price_only=forecast(52000,series_volume=40000)['attributable_profit_yi']
volume_step=forecast(68000,series_volume=40000)['attributable_profit_yi']
capacity=D('56271.99')+19800
out={
 'period':'2026E to 2036; 10 compounding periods',
 'price_factor':D('1.05')**10,
 'mature_base_liquor_supply_proxy_tonnes':capacity,
 'central_sales_to_supply_proxy':D(68000)/capacity,
 'volume_sensitivity':{str(v):forecast(v) for v in [48000,52000,60000,63000,65000,68000,70000,72000]},
 'price_sensitivity':{g:forecast(68000,growth=g) for g in ['0.02','0.03','0.05']},
 'margin_sensitivity':{m:forecast(68000,margin=m) for m in ['0.45','0.49','0.52']},
 'bridge':{'previous':old,'price_only':price_only,'moutai_volume_step':volume_step,'series_volume_step':central['attributable_profit_yi'],
           'price_delta':price_only-old,'moutai_volume_delta':volume_step-price_only,'series_volume_delta':central['attributable_profit_yi']-volume_step},
 'both_categories_5pct':forecast(68000,series_asp=str(D('53.5')*D('1.05')**10)),
 'central_profit_cagr_from_2026E':(central['attributable_profit_yi']/D('821.8704'))**D('.1')-1,
 'central_profit_in_2026_money_at_2pct_inflation':central['attributable_profit_yi']/D('1.02')**10,
 'volume_growth_from_2026E':D(68000)/48000-1,
 'volume_cagr_from_2026E':(D(68000)/48000)**D('.1')-1,
 'moutai_revenue_multiple_from_2026E':D(68000)/48000*D('1.05')**10,
 'required_share_multiple_if_category_volume_falls_20pct':D(68000)/48000/D('.8'),
 'luxury_ten_year_cagr':{k:(D(end)/D(start))**D('.1')-1 for k,start,end in [
   ('Birkin25_USD','9400','13500'),('Birkin25_EUR','5900','9600'),
   ('Birkin30_USD','10900','14900'),('Birkin30_EUR','7000','10600')]}}
assert central['attributable_profit_yi'].quantize(D('.01'))==D('1868.86')
assert price_only.quantize(D('.01'))==D('1422.64')
assert out['bridge']['price_delta']+out['bridge']['moutai_volume_delta']+out['bridge']['series_volume_delta']==central['attributable_profit_yi']-old
Path(__file__).with_name('model-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2,default=str))
