def find_combinations(items, target, partial=[], results=set()):
    total = sum(partial)

    # 检查是否找到了一个满足条件的组合
    if total == target or abs(total - target) <= 0.5:
        combination = tuple(sorted(partial))
        if combination not in results:
            results.add(combination)
            print(f"找到组合: {combination} 总计: {sum(combination)}")
    if total > target:
        return  # 如果总和已经超过目标，则终止

    # 元素只能使用一次
    for i, item in enumerate(items):
        remaining = items[:i] + items[i+1:] # 移除已经使用过的元素
        find_combinations(remaining, target, partial + [item], results)
        
    # 元素可以多次使用
    # for item in items:
        # find_combinations(items, target, partial + [item], results)

# 示例商品价格列表
prices = [71.88, 64.9, 42.36, 34.8, 84, 93.6, 95.88, 88.2, 63.96, 90, 34.22, 21.6, 43.08, 65]

# 目标金额
target_amount = 166.53

# 寻找所有组合
find_combinations(prices, target_amount)
