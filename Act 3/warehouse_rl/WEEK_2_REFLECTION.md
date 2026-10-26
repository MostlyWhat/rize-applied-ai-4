1. What improvements did your model make in the baselining test results?

    Last week, the baseline results showed my model in last place. This week had more improvements to address the issues found last week, which moved the model from 8th place in the previous week to 1st this week. This was a jump from a -\$1,000 deficit to a \$26,000 profit, and also a jump from 30.7% completion to 58.7%. Compared to aggressive_swap, which was the previous week's winner, it manages to maintain a similar consistent performance of around \$20,000 with under \$1,000 of uncertainty. Yet the confidence intervals did not overlap with my agent, showing that the performance improvement was significant. This means that out of all the tests, it was not just random chance that my model made it to first, but it was due to the improvements. This is mainly because the over-hiring problem from last week was resolved, so the agent can now hire based on the demand requirements and profitability calculations.

2. What changes did you make to the staffing and package pickup optimizing algorithms? Describe their strategies in plain english.

    The issue of staffing and hiring was resolved this week with the implementation of strategic staffing, based on seeing how much the current crew can benefit from a new employee. The benefit is calculated from various factors, but mostly from whether a new hire will reduce the pressure and allow for more profit. The staffing system works by checking how many orders exist per worker, and hires if there are more than 3 orders for every worker. It also checks that the profit is above \$1,000, which is the profit threshold, and that the profit is currently growing faster than a worker's wage of \$0.20 per step to keep profitability. The firing system works when there are fewer than 1.5 orders per worker or when profit goes down, to keep profitability, but it will keep a minimum of 2 workers. This is a trade-off because each worker costs \$0.20 per step, so more workers ship orders faster but take away from the profit. The manager hiring system then hires a manager if profit is above \$2,000, so that the manager can help with rearranging the shelves. Moreover, the most significant system implemented was the cooldown system, because it can take time for a hire or fire to have an impact on the queue and profit. By waiting 100 steps after each change, the system does not hire out of control before the impact is seen. Then another system was added on top of that to assign workers to their orders based on distance and value, with 70% going to the distance and 30% going to the value of the order. This is done to ensure that the work assigned is worth the time and distance for that worker. The system works by finding free workers first, comparing them to the orders, and seeing which order is closer and pays well. The best pair is assigned first, and the rest of the workers are assigned to the other orders. So the system has to decide which pair provides the most benefit, for example, whether a far away order that pays a lot is better than another order that is closer to the worker.

3. How do your newly optimized set of algorithms compliment one another (IE. How does a better manager hiring strategy impact your layout optimization algorithm?)

    It starts with the staff, who create the profits and ship the orders. With enough profit, a manager can be hired to help with the rearrangement of items to create a more efficient layout. The more efficient layout allows for more profit because the hot items are closer to the delivery bay, which leads to shorter trips and more orders completed. This can be seen with my agent completing 58.7% of orders compared to 37.6% for the 2nd place agent. Now that the orders are fulfilled much quicker and more efficiently, more profit can be made. Then some of the profit is put into hiring more staff. So both the hiring and layout systems are in a positive feedback loop that helps each other, until it reaches a point where the layout is optimized so well that barely any swaps happen. After that, the hiring becomes more meaningful and continues to hire more staff as needed, so the profit continues to rise. But if profit drops, then the staffing system fires workers to keep profitability.

RESULTS

BASELINE RESULTS
1. aggressive_swap | Profit: $20248.14 ± $814.74 | Completion:  36.3% ±  0.9%
2. fixed_std       | Profit: $19975.66 ± $730.79 | Completion:  37.6% ±  2.7%
3. random_std      | Profit: $19416.49 ± $2802.48 | Completion:  41.3% ±  3.3%
4. intelligent_queue | Profit: $17852.45 ± $1706.24 | Completion:  39.9% ±  2.2%
5. intelligent_hiring | Profit: $ 6280.61 ± $1805.57 | Completion:  33.0% ±  1.6%
6. distance_based  | Profit: $ 4276.39 ± $1785.89 | Completion:  31.6% ±  1.7%
7. greedy_std      | Profit: $ 1952.52 ± $1210.70 | Completion:  27.3% ±  1.4%
8. skeleton_optimization | Profit: $-1004.55 ± $  2.33 | Completion:  30.7% ±  6.7%

UPDATED RESULTS
1. skeleton_optimization | Profit: $25712.49 ± $2011.14 | Completion:  58.7% ±  3.4%
2. aggressive_swap | Profit: $20953.79 ± $650.75 | Completion:  37.6% ±  1.7%
3. fixed_std       | Profit: $20361.87 ± $790.19 | Completion:  35.7% ±  2.0%
4. intelligent_queue | Profit: $19903.09 ± $3005.72 | Completion:  43.5% ±  2.3%
5. random_std      | Profit: $ 4522.97 ± $5983.29 | Completion:  29.3% ±  5.3%
6. distance_based  | Profit: $ 3754.44 ± $3510.49 | Completion:  31.2% ±  3.5%
7. greedy_std      | Profit: $ 3212.63 ± $1724.71 | Completion:  28.4% ±  2.1%
8. intelligent_hiring | Profit: $ 2406.88 ± $2439.19 | Completion:  29.4% ±  3.3%
