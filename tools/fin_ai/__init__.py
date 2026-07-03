"""金融 AI 数据源包（gangtise-reason，OpenAI 兼容 SSE 问答接口）。

公开 API（Task 6 填充）：
    ask(query, ...)              单次查询
    ask_multi_turn(topic)        多轮 REPL session
    quota()                      配额查询
"""

__all__ = ["ask", "ask_multi_turn", "quota"]
