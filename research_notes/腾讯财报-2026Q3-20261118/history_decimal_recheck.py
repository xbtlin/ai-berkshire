from pathlib import Path
import ast,json
from decimal import Decimal as D,localcontext
base=Path(__file__).resolve().parent
data=json.loads((base/'history_calculations.json').read_text())
def evaluate(node):
 if isinstance(node,ast.Expression):return evaluate(node.body)
 if isinstance(node,ast.Num):return D(str(node.n))
 if hasattr(ast,'Constant') and isinstance(node,ast.Constant):return D(str(node.value))
 if isinstance(node,ast.UnaryOp):
  val=evaluate(node.operand)
  return -val if isinstance(node.op,ast.USub) else val
 if isinstance(node,ast.BinOp):
  a=evaluate(node.left);b=evaluate(node.right)
  if isinstance(node.op,ast.Add):return a+b
  if isinstance(node.op,ast.Sub):return a-b
  if isinstance(node.op,ast.Mult):return a*b
  if isinstance(node.op,ast.Div):return a/b
 raise ValueError(node)
with localcontext() as ctx:
 ctx.prec=40
 for k,v in data.items():v['decimal_exact_result']=str(evaluate(ast.parse(v['expression'],mode='eval')))
(base/'history_calculations.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
(base/'history_decimal_recheck.py').write_text(Path('/tmp/tencent_history_decimal.py').read_text().replace("base=Path(__file__).resolve().parent","base=Path(__file__).resolve().parent"))
print('Decimal rechecked',len(data),'calculations')
