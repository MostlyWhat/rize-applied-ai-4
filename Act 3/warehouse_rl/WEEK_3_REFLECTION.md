1. What are the pareto maximal points for this simulation? What do those points mean, in plain english?

    There were 5 pareto maximal points in the simulation below. Each point represents how a different wage can impact both the profit and service. When comparing the profit to the service, increasing profits reduces the service quality and increasing service quality decreases the profit margin. A pareto maximal point is a wage where no other wage beats it on both profit and service. In this case, moving between the points either increases the profit but reduces the service, or the other way around. These 5 points form the pareto frontier, which is the best possible mix of profit and service. Any other wage is an objectively worse choice, because there is a point on the frontier that is better on at least one goal and not worse on the other. The two extremes are \$0.30, which has the highest profit on the frontier, and \$3.50, which has the highest service. With both, \$0.30 trades service quality for the highest profit and \$3.50 trades profit for the highest service. I was also surprised to see the program report \$0.15 as the sweet spot, yet \$0.30 doubled both the profit and service quality, so \$0.15 should not be the sweet spot, and it is not pareto optimal. Similarly, \$0.40 was worse than \$0.30 on both profit and service. \$4.00, the highest wage, gives a lower service of 53.5% than \$0.30 at 54.4%, which means that the highest wage does not always result in a higher service quality. Lastly, \$3.00 and \$3.50 are both pareto points, but they have negative profit, or a deficit, so these points are not practical for a business to run. It is also worth noting that each wage was only run for 5 episodes, so the results have some noise and the frontier could shift slightly with more runs.

    - \$0.30: \$17,937 profit, 54.4% service
    - \$1.20: \$8,075 profit, 56.8% service
    - \$1.40: \$7,879 profit, 62.6% service
    - \$3.00: -\$675 profit, 63.8% service
    - \$3.50: -\$1,008 profit, 64.4% service

2. Based on the data, what salary would you recommend the company pays warehouse workers (salary per step) and why? Include the impact you think your choice would have on the business.

    Based on the data, I would recommend \$0.30 per step, as it has the highest profit of \$17,937 and a 54.4% service quality. The wages below that cause the workers to be slow, so the service quality drops to only 25% to 37% and the profit also decreases. Above that, the wages start costing so much that the extra productivity cannot keep up, so the service quality increases but the profit decreases. For example, going from \$0.30 to \$1.40 raises the service by about 8 points, but the profit falls by about 56%, and above \$2.00 the company starts losing money. At \$0.30, the company makes the most profit and ships slightly more than half of the orders. This is very good in terms of efficiency for both the profit and service. But about half of the customers might be unsatisfied with their order, leading to bad reviews and potentially hurting the company's future. A low wage can also make it harder to keep workers, and if they quit, the company has to pay to hire and train new ones, which takes away from the profit. If the company prefers better service and can accept lower profit, then \$1.40 is the second-best option. This is a pareto optimal solution and is the highest service solution before running into a deficit. Therefore, for higher profit, I would recommend \$0.30 per step, but to improve customer and worker retention in the future, \$1.40 per step is also recommended.

3. What conditions would lead you to prioritize profitability over service, or vice versa? Is there any condition under which you would recommend maximizing either service or profitability?

    I would prioritize profitability over service if the business is in desperate need of cash, customers care more about price than service, demand is very volatile and the company needs to keep cash for the slow periods, or when there is little competition. But I would prioritize service over profitability if there is high competition, customers care more about service than price, the priority is to improve the reputation, or the focus is on customer retention. I care about both, but in the long term it matters much more to focus on the customer retention side of good service quality, because good service means returning customers and constant revenue. However, I would consider maximizing profit for a short term if the company is in need of a cash injection or in a crisis that requires more funds. But for maximizing service, I would only maximize it as long as it does not lead the company into a deficit, as you cannot maintain a company that is going under, unless it is for a specific few customers that would prefer a higher quality to maintain the relationship. I cannot pick one as it is highly dependent on the situation, but I would prefer to keep both the service and profit good, like at \$0.30 per step. Overall, the best choice is to pick the pareto point that fits the company's current goal instead of going to either extreme.

Script Output

Starting Multi-Objective Warehouse Optimization Demo...
🎯 Multi-Objective Optimization Demo
=====================================
Running 5 episodes per configuration...
Testing 20 different wage levels...
Objectives: Profit Maximization vs Service Quality
💰 Wage-based productivity tradeoffs:
   • Blue points: Low wages, slow workers, low cost
   • Red points: High wages, fast workers, high cost
   • Pareto frontier shows optimal tradeoff curve

Wage_$0.15... Done! .
  Avg Profit: $9087.7, Service Rate: 25.1%
Wage_$0.20... Done! .
  Avg Profit: $9758.0, Service Rate: 27.1%
Wage_$0.25... Done! .
  Avg Profit: $13486.2, Service Rate: 37.3%
Wage_$0.30... Done! .
  Avg Profit: $17937.1, Service Rate: 54.4%
Wage_$0.40... Done! .
  Avg Profit: $14248.8, Service Rate: 47.5%
Wage_$0.50... Done! .
  Avg Profit: $9975.4, Service Rate: 49.9%
Wage_$0.60... Done! .
  Avg Profit: $12704.4, Service Rate: 52.5%
Wage_$0.70... Done! .
  Avg Profit: $10876.9, Service Rate: 47.0%
Wage_$0.80... Done! .
  Avg Profit: $13035.4, Service Rate: 53.9%
Wage_$0.90... Done! .
  Avg Profit: $10377.0, Service Rate: 51.9%
Wage_$1.00... Done! .
  Avg Profit: $10078.9, Service Rate: 52.1%
Wage_$1.20... Done! .
  Avg Profit: $8075.3, Service Rate: 56.8%
Wage_$1.40... Done! .
  Avg Profit: $7878.5, Service Rate: 62.6%
Wage_$1.60... Done! .
  Avg Profit: $5599.0, Service Rate: 60.3%
Wage_$1.80... Done! .
  Avg Profit: $3560.4, Service Rate: 56.4%
Wage_$2.00... Done! .
  Avg Profit: $76.2, Service Rate: 58.6%
Wage_$2.50... Done! .
  Avg Profit: $-418.6, Service Rate: 62.6%
Wage_$3.00... Done! .
  Avg Profit: $-675.3, Service Rate: 63.8%
Wage_$3.50... Done! .
  Avg Profit: $-1008.4, Service Rate: 64.4%
Wage_$4.00... Done! .
  Avg Profit: $-1011.1, Service Rate: 53.5%

======================================================================
DETAILED WAGE-PRODUCTIVITY ANALYSIS
======================================================================
Wage Level   Profit       Service      Efficiency     
----------------------------------------------------------------------
$0.15        $    9088      25.1%          60.6
$0.20        $    9758      27.1%          48.8
$0.25        $   13486      37.3%          53.9
$0.30        $   17937      54.4%          59.8
$0.40        $   14249      47.5%          35.6
$0.50        $    9975      49.9%          20.0
$0.60        $   12704      52.5%          21.2
$0.70        $   10877      47.0%          15.5
$0.80        $   13035      53.9%          16.3
$0.90        $   10377      51.9%          11.5
$1.00        $   10079      52.1%          10.1
$1.20        $    8075      56.8%           6.7
$1.40        $    7879      62.6%           5.6
$1.60        $    5599      60.3%           3.5
$1.80        $    3560      56.4%           2.0
$2.00        $      76      58.6%           0.0
$2.50        $    -419      62.6%          -0.2
$3.00        $    -675      63.8%          -0.2
$3.50        $   -1008      64.4%          -0.3
$4.00        $   -1011      53.5%          -0.3

======================================================================
KEY INSIGHTS:
======================================================================
🏆 Highest Profit: $0.30 wage
   Profit: $17937, Service: 54.4%

⭐ Best Service: $3.50 wage
   Profit: $-1008, Service: 64.4%

💡 Most Efficient: $0.15 wage
   Profit: $9088, Service: 25.1%
   Efficiency: 60.6 profit per wage dollar

🎯 Sweet Spot: $0.15 wage level
   Optimal balance of productivity and cost

📊 Modern wage-productivity visualization saved as 'wage_productivity_scatterplot.png'

✅ Wage-productivity optimization demo completed!
The scatterplot shows how different wage levels affect performance.

Key takeaways:
• Blue points (low wages): Cheaper workers but slower service
• Red points (high wages): Expensive workers but faster service
• Gold star shows the optimal wage level for maximum profit
• Color gradient reveals the wage-productivity relationship
• There's often a 'sweet spot' where moderate wages maximize efficiency