1. What improvements did your model make in the baselining test results?

    The model did not make any significant improvements over the baseline results as it only produced \$9.65 more than the baseline model, which in terms of noise of the uncertainty is not far off. The updated model still performs on par with the unedited model, with both ending up in last place at 8th out of 8 agents. Between runs there was not much changes as the new model will still be bankrupt at around a few dollars past -\$1000. The issue I found after troubleshooting was that the system hired so much people to around 50 people that their cost was higher than the profit. This caused a bankruptcy before the layout optimization became significant and helpful, as the bankrupt happens at around step 100 to 400 out of 3000. But by capping the headcount to only 20, the agent was able to make more than \$10,000 in some tests. The layout did not impact the hiring, but the random is actively and significantly impacting the results in such a negative way that the only option I see is to update the hiring logic and that should see better results. When tested with and without the cap, the efficiency measured and tracked still went up over 5% without the cap and over 20% with the cap on. The CI was also in almost the same range but the error bars are just slightly off, but this is not really meaningful as both bankrupt past \$1000, so just by a small amount. The completion rate meanwhile is in the same range and share most of the error bars. The other models like aggressive_swap and fixed_std, outperformed my model by a lot and reaching \$20,000 consistently at the top, those are fixed models that controls all the parts involved. Which until I make sure every single part of my system work together coherently, there is no shot at competing with the others where only one part is perfected. I cannot just bring a car with a good engine but poor wheel and drive system, it just cannot compete.

2. What changes did you make to the layout optimizing algorithm?

    The layout optimizing algorithm was modified as per the instructions to be comprised of 2 phases. The first phase is a greedy frequency-based swapping algorithm that looks at the top 25% of items based on their type and frequency of orders that are more than 3 steps from the delivery station. This is run once every 100 steps to search around every shelf and ranks the result with the one that would provide the most benefit based on the formula (benefit = frequency of hot item * distance saved + frequency of the item displaced * the distance changed). The second phase is more of a fallback that runs once every 200 steps if the first phase were to fail at finding good matches, as phase 1 has priority. The co-occurrence system looks at pairs of items that are often ordered together by clustering them together and minimizing the distance needed to complete an order. So it looks at every pair of item and ranks on which pair would be more beneficial next to each other. After some extensive testing and monitoring the swaps, there were some flaws that persisted. One major fix was to not allow a hot item from far out to be swapped by a closer one, because both are hot items, the initial system would switch them around seeing that the benefit was higher. Another flaw was that the phase 2 system would do a similar thing and bring a hot item closed to the station out, essentially reversing what phase 1 did. I have also done a test where I allowed hot items to swap with other hot items and that reduced the efficiency compared to the blocking and only allowing with non-hot items. With those main changes, the efficiency did go up for a bit until there were too many employees.

3. What future opportunities for improvement do you see with your model?

  As mentioned prior, the fix will be the staffing, the layout is advanced enough that the thing holding it back the most is the hiring management. The warehouse model comprises of two main parts, the layout and hiring. I would like to modify the hiring and staffing system to be more in line with the actual demand for packages, so I want to design a metric that evaluates the current demand vs the current ability to fulfil orders. But also to check if we need to hire managers vs actual employee to keep the costs low. A manager is more expensive compared to an employee and the model must run for longer in order to see the profits later on, so I want to make sure that it is worth it to hire a manager when needed. Even with the fix, phase 2 sometimes still pushes a hot item far out, so I need to find a fix even though it rarely activates compared to phase 1. But I also want to look into adjusting the threshold to be more dynamic, so instead of the top 25%, the system can look at the actual demand and see if maybe it needs to only adjust the top 10% as it might account for 50% of the demand.

Results

BASELINE RESULTS
1. intelligent_queue | Profit: $20973.59 ± $2280.05 | Completion:  42.1% ±  2.7%
2. fixed_std       | Profit: $20769.57 ± $810.21 | Completion:  37.5% ±  1.4%
3. aggressive_swap | Profit: $20762.96 ± $668.67 | Completion:  36.8% ±  1.4%
4. distance_based  | Profit: $ 6062.98 ± $2110.19 | Completion:  32.0% ±  2.2%
5. intelligent_hiring | Profit: $ 4641.40 ± $2217.39 | Completion:  30.8% ±  2.2%
6. greedy_std      | Profit: $ 2706.11 ± $1606.25 | Completion:  28.8% ±  2.1%
7. random_std      | Profit: $ 1768.91 ± $1452.19 | Completion:  28.1% ±  2.3%
8. skeleton_optimization | Profit: $-1014.20 ± $  3.98 | Completion:  32.4% ±  6.5%

UPDATED RESULTS
1. aggressive_swap | Profit: $20248.14 ± $814.74 | Completion:  36.3% ±  0.9%
2. fixed_std       | Profit: $19975.66 ± $730.79 | Completion:  37.6% ±  2.7%
3. random_std      | Profit: $19416.49 ± $2802.48 | Completion:  41.3% ±  3.3%
4. intelligent_queue | Profit: $17852.45 ± $1706.24 | Completion:  39.9% ±  2.2%
5. intelligent_hiring | Profit: $ 6280.61 ± $1805.57 | Completion:  33.0% ±  1.6%
6. distance_based  | Profit: $ 4276.39 ± $1785.89 | Completion:  31.6% ±  1.7%
7. greedy_std      | Profit: $ 1952.52 ± $1210.70 | Completion:  27.3% ±  1.4%
8. skeleton_optimization | Profit: $-1004.55 ± $  2.33 | Completion:  30.7% ±  6.7%
