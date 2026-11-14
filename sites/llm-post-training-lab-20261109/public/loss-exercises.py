#!/usr/bin/env python3
"""后训练 CPU 数学练习。Python 3.7+，无需第三方依赖。
运行：python3 loss-exercises.py
教学计算，不训练模型。试着先写自己的实现，再对照这里的参考答案。
参考：https://arxiv.org/abs/2305.18290
      https://arxiv.org/abs/1707.06347
      https://arxiv.org/abs/2402.03300
      https://huggingface.co/docs/trl/sft_trainer
"""
import math

def masked_nll(probabilities, mask):
    if len(probabilities) != len(mask) or not any(mask):
        raise ValueError('需要等长数组和至少一个有效 token')
    if not all(0 < p <= 1 for p in probabilities):
        raise ValueError('概率必须在 (0, 1]')
    return -sum(math.log(p) for p, m in zip(probabilities, mask) if m) / sum(bool(m) for m in mask)

def dpo_loss(margin, beta):
    if beta <= 0:
        raise ValueError('beta 必须大于 0')
    z = -beta * margin
    return max(z, 0) + math.log1p(math.exp(-abs(z)))

def ppo_objective(ratio, advantage, epsilon=0.2):
    if ratio < 0 or not 0 < epsilon < 1:
        raise ValueError('ratio >= 0 且 0 < epsilon < 1')
    clipped = min(1 + epsilon, max(1 - epsilon, ratio))
    return min(ratio * advantage, clipped * advantage)

def group_advantages(rewards):
    if len(rewards) < 2:
        raise ValueError('至少需要两个组内样本')
    mean = sum(rewards) / len(rewards)
    # 总体标准差：具体 Trainer 可能采用不同约定或关闭缩放。
    std = math.sqrt(sum((r - mean) ** 2 for r in rewards) / len(rewards))
    return [(r - mean) / (std + 1e-8) for r in rewards]

if __name__ == '__main__':
    assert math.isclose(dpo_loss(0, .1), math.log(2))
    assert math.isclose(dpo_loss(0, 2), math.log(2))
    assert dpo_loss(2, .2) < dpo_loss(-2, .2)
    assert math.isclose(ppo_objective(1.5, 1), 1.2)
    assert math.isclose(ppo_objective(.5, -1), -.8)
    assert math.isclose(ppo_objective(1.5, -1), -1.5)
    assert group_advantages([1, 1, 1, 1]) == [0, 0, 0, 0]
    assert group_advantages([0, 0, 0, 0]) == [0, 0, 0, 0]
    assert math.isclose(sum(group_advantages([1, 0, 0, 0])), 0, abs_tol=1e-7)
    assert math.isclose(masked_nll([.2, .8], [False, True]), -math.log(.8))
    print('数学边界检查通过。')
    print('SFT 示例:', masked_nll([.2, .8, .3, .6, .9], [False, False, True, True, True]))
    print('DPO 示例:', dpo_loss(2, .2))
    print('GRPO 示例:', group_advantages([1, 0, 0, 0]))
    print('练习：把 PPO advantage 改成负值；解释哪一侧变平。')
    print('练习：把 GRPO 奖励都加 10，为什么优势不变？')
