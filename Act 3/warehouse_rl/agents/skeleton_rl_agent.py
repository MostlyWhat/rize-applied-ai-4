#!/usr/bin/env python3
"""
Skeleton Optimization Agent - Template for students to implement optimization algorithms

IMPORTANT: This is NOT an RL agent - it's a template for 
students to implement their own optimization algorithms (greedy, Hungarian, etc.)

This agent currently makes terrible decisions:
- Random staffing decisions
- No layout optimization 
- Ignores order priorities
- No intelligent assignment logic

Students should replace the naive methods with proper optimization algorithms.
"""

import numpy as np
from typing import Dict, Optional
from .standardized_agents import BaselineAgent

class SkeletonOptimizationAgent(BaselineAgent):
    """
    Template for students to implement their own optimization algorithms.
    
    Students should replace the naive methods with:
    - Economic models for staffing decisions
    - Hungarian algorithm for order assignment  
    - Greedy search for layout optimization
    - Multi-objective optimization techniques
    """
    
    def __init__(self, env):
        super().__init__(env)
        self.name = "StudentOptimization"
        
        # Enable unlimited hiring for true economic optimization
        self.env._unlimited_hiring = True
        
        # Students can add their own state tracking here
        self.performance_metrics = []
        self.decision_history = []
        self.profit_history = []
        
        # Students can add algorithm parameters here
        # Example: Hungarian algorithm matrices, greedy search parameters, etc.

        # Staff Params
        self.staffing_parameters = {
            'hiring_threshold': 3,
            'firing_threshold': 1.5,
            'profit_threshold': 1000,
            'manager_threshold': 2000,
            'minimum_staff': 2,
            'trend_window': 50, # Steps to look back when measuring profit trend
            'worker_wage': 0.20, # Salary per timestep of a low wage hire
            'staffing_cooldown': 100 # Minimum steps between staffing changes so each hire/fire can take effect
        }

        self.assignment_parameters = {
            'distance_weight': 0.7,
            'value_weight': 0.3,
            'maximum_distance': self.env.warehouse_grid.width + self.env.warehouse_grid.height,
            'assignment_method': 'greedy'
        }

        # Timestep of the last hire/fire, None until the first change
        self.last_staffing_step = None

        # Students can implement adaptive parameters that change based on performance
        self.adaptive_optimization_enabled = False

        # Layout Swap Trackers
        self.layout_swap_types = []
        self.layout_metrics = []
        # Cell index -> timestep it was last swapped
        self.recent_swap_cells = {}
        # (from index, to index) -> 'frequency' or 'cooccurrence' for requested swaps
        self.swap_request_types = {}

        # Integrated Trackers
        self.integrated_metrics = []
        # (distance, value) of each order assigned since the last integrated snapshot
        self.assignment_log = []

    def reset(self):
        """Reset agent state - students should expand this"""
        self.action_history = []
        self.reward_history = []
        self.profit_history = []
        self.last_staffing_step = None

        # TODO: Reset any neural network states, replay buffers, etc.

        # Reset metrics
        self.layout_swap_types = []
        self.layout_metrics = []
        self.recent_swap_cells = {}
        self.swap_request_types = {}
        self.integrated_metrics = []
        self.assignment_log = []

    def get_action(self, observation: Dict) -> Dict:
        """
        Week 2: Integrated optimization across all decision areas
        """

        # Extract basic info from observation
        current_timestep = observation['time'][0]
        financial_state = observation['financial']  # [profit, revenue, costs, burn_rate]
        queue_info = observation['order_queue']
        employee_info = observation['employees']

        # Staffing runs first so the cooldown knows when the last hire/fire happened
        staffing_action = self._get_naive_staffing_action(financial_state, employee_info)
        if staffing_action != 0:
            self.last_staffing_step = current_timestep

        action = {
            'staffing_action': staffing_action,                                                     # Week 2 Step 1
            'layout_swap': self._get_naive_layout_action(current_timestep),                         # Week 1 (keep working)
            'order_assignments': self._get_naive_order_assignments(queue_info, employee_info)       # Week 2 Step 2
        }

        # Track layout (Week 1) and integrated performance every 100 steps
        if current_timestep % 100 == 0:
            self.track_layout_performance()
            self.track_integrated_performance()

        # TODO: Record action for optimization analysis
        self.action_history.append(action.copy())

        return action

    def _get_naive_staffing_action(self, financial_state, employee_info) -> int:
        """
        WEEK 2 STEP 1: Economic staffing optimization
        Make hiring/firing decisions based on simple business economics

        1. Analyze current demand (how many orders are waiting)
        2. Calculate workforce utilization and efficiency
        3. For each potential action (hire, fire, do nothing):
           a. Estimate benefit (additional orders completed/revenue)
           b. Calculate cost (salary expenses)
           c. Consider business constraints (current profit, trends)
        4. Select action with highest net benefit
        5. Use buffer zones to prevent rapid hire/fire cycles

        NOTES:
        1 = hire worker
        2 = fire worker
        3 = hire manager
        """

        # Extract economic and operational data
        current_profit = financial_state[0]
        revenue = financial_state[1]
        costs = financial_state[2]
        burn_rate = financial_state[3]

        num_employees = len(self.env.employees)
        queue_length = len(self.env.order_queue.orders)
        has_manager = any(employee.is_manager for employee in self.env.employees)

        # TODO: Calculate business indicators

        # TODO: - Queue pressure (how much demand vs how much capacity)
        # TODO: Calculate queue pressure (demand vs capacity)
        # HINT: queue_pressure = queue_length / max(1, num_employees)

        queue_pressure = queue_length / max(1, num_employees)

        # TODO: - Profit per employee (how efficient is our workforce)
        # TODO: Calculate profit efficiency
        # HINT: profit_per_employee = current_profit / max(1, num_employees)

        profit_per_employee = current_profit / max(1, num_employees)

        # TODO: - Recent profit trend (is business growing or shrinking?)
        # TODO: Track profit trend (if you have history)
        # HINT: Compare recent profit to older profit levels

        # The current_profit is cumulative, so the trend is its change per step over the window
        self.profit_history.append(current_profit)

        trend_window = self.staffing_parameters['trend_window']
        has_trend = len(self.profit_history) > trend_window

        if has_trend:
            recent_profit_trend = (self.profit_history[-1] - self.profit_history[-1 - trend_window]) / trend_window
        else:
            recent_profit_trend = 0.0

        # Without enough history the trend is neutral and does not block hiring
        can_afford_hire = not has_trend or recent_profit_trend > self.staffing_parameters['worker_wage']
        losing_money = has_trend and recent_profit_trend < 0

        # Cooldown: hold staffing steady until the last hire/fire has had time to show up
        # in the queue and profit, otherwise the same signal triggers a burst of changes
        cooldown = self.staffing_parameters['staffing_cooldown']
        if self.last_staffing_step is not None and self.env.current_timestep - self.last_staffing_step < cooldown:
            return 0

        # ---

        # TODO: Apply economic decision logic

        # TODO: - HIRE when: high demand + profitable + can afford wages
        # TODO: HIRING LOGIC - when does hiring make business sense?
        # TODO: Check: queue pressure > hire_threshold AND current_profit > profit_threshold

        hire_threshold = self.staffing_parameters['hiring_threshold']
        profit_threshold = self.staffing_parameters['profit_threshold']

        if queue_pressure > hire_threshold and current_profit > profit_threshold and can_afford_hire:
            return 1

        # TODO: - FIRE when: low demand + losing money + too many workers
        # TODO: FIRING LOGIC - when does firing save money without hurting capacity?
        # TODO: Check: queue pressure < fire_threshold AND num_employees > min_staff
        # TODO: Extra consideration: only fire if losing money or severe overstaffing

        fire_threshold = self.staffing_parameters['firing_threshold']
        min_staff = self.staffing_parameters['minimum_staff']

        # Also fire when losing money, since more staff is not shrinking the queue
        overstaffed = queue_pressure < fire_threshold
        if num_employees > min_staff and (overstaffed or losing_money):
            return 2

        # TODO: - HIRE MANAGER when: profitable + need layout optimization + no manager
        # TODO: Manager hiring: profit > manager_threshold AND not has_manager

        manager_threshold = self.staffing_parameters['manager_threshold']

        if current_profit > manager_threshold and not has_manager:
            return 3

        # ---

        # TODO: Implement buffer zones (different thresholds for hire vs fire)
        # TODO: Use higher threshold for hiring, lower threshold for firing
        # TODO: Use different thresholds for hiring vs firing decisions
        # TODO: This prevents flip-flopping between hiring and firing every few steps
        # HINT: hire_threshold = 3.0, fire_threshold = 1.5 creates buffer zone

        return 0  # Placeholder - implement economic logic

    def _get_naive_layout_action(self, current_timestep) -> list:
        """
        WEEK 1 STEP 1: Frequency-based layout optimization
        Move frequently accessed items closer to delivery areas
        """

        # Only optimize every 100 steps to avoid disrupting operations
        if current_timestep % 100 != 0:
            return [0, 0]

        # Skip if the manager is busy so the swap isn't wasted
        # HINT (guide): time optimization when managers can be most effectively utilized
        managers = [employee for employee in self.env.employees if employee.is_manager]
        if len(managers) == 0 or managers[0].state.name != 'IDLE':
            return [0, 0]

        # Skip if the queue isn't manageable so swaps don't disrupt busy periods
        # Checklist: layout method only optimizes when queue is manageable
        # Same ratio the top layout baselines use (layout_queue_condition_ratio)
        max_queue_per_employee = 20.0
        if len(self.env.order_queue.orders) > len(self.env.employees) * max_queue_per_employee:
            return [0, 0]

        # Get item frequency data from environment
        # HINT: Use self.env.warehouse_grid.item_access_frequency
        # HINT: Check if frequency data exists before proceeding

        grid = self.env.warehouse_grid
        item_grid = grid.item_grid
        item_frequency = grid.item_access_frequency
        hot_items_type = []
        # Where every item is stored, built once so benefit checks stay fast
        item_locations = self._get_item_locations()

        # Optimize based on hot item frequency
        if item_frequency.sum() > 0:
            # Identify "hot" items (frequently accessed)
            # HINT: Use np.percentile to find top 25% of items by frequency
            # Filter to only items that have been accessed (frequency > 0)
            active_frequencies = item_frequency[item_frequency > 0]
            # Calculate 75th percentile threshold for "hot" items
            # HINT: Use np.percentile(active_frequencies, 75)
            percentile_boundary = np.percentile(active_frequencies, 75)

            # Find all items above this threshold
            for i in range(len(item_frequency)):
                if item_frequency[i] > 0 and item_frequency[i] >= percentile_boundary:
                    hot_items_type.append(i)

            # Find delivery positions
            # HINT: Use getattr(grid, 'truck_bay_positions', [(grid.width//2, grid.height//2)])
            delivery_positions = getattr(grid, 'truck_bay_positions', [(grid.width//2, grid.height//2)])

            # Track the best swap across all hot items
            best_benefit = 0
            best_swap = None

            # For each hot item, check if it's far from delivery
            # HINT: Use grid.manhattan_distance() to calculate distances
            for (row, col), item in np.ndenumerate(item_grid):
                # Skip if -1 because none or not a hot item
                if item == -1 or item not in hot_items_type:
                    continue

                too_far = False
                distances = []
                # Row is y and col is x, positions are (x, y)
                item_position = [col, row]

                for delivery_position in delivery_positions:
                    distances.append(grid.manhattan_distance(item_position, delivery_position))

                # Skip if not the closest copy because pickers go to the closest one
                closest_copy_dist = self._closest_delivery_distance(item_locations[int(item)], delivery_positions)
                if min(distances) > closest_copy_dist:
                    continue

                # If hot item is >3 steps from delivery, find closer position
                # HINT: Look for empty spots or positions with cold items

                # Apply distance threshold (>3 steps) to decide if optimization needed
                if min(distances) > 3:
                    too_far = True

                if too_far:
                    # If optimization needed, search for closer positions
                    # HINT: Call helper method to find best swap position
                    better_position = self._find_closer_position(item_position, delivery_positions,
                                                                 hot_items_type, item_locations)

                    # Skip if none because no better position for this item
                    if better_position is None:
                        continue

                    # Benefit = frequency x distance saved minus the displaced item's penalty
                    target_position = [better_position[1] % grid.width, better_position[1] // grid.width]
                    benefit = self._estimate_swap_benefit(item_position, target_position,
                                                          delivery_positions, item_locations)

                    # Keep the [current_position_index, target_position_index] swap with the highest benefit
                    if benefit > best_benefit:
                        best_benefit = benefit
                        best_swap = better_position

            # Return the best frequency swap after checking every hot item
            if best_swap is not None and self._is_storage_swap(best_swap):
                self._record_swap_request(best_swap, 'frequency', current_timestep)
                return best_swap

        # Phase 2: If no frequency-based improvement found, try co-occurrence clustering
        if current_timestep % 200 == 0:  # Less frequent than hot-item optimization
            cooccurrence_swap = self._find_cooccurrence_swap(hot_items_type, item_locations)
            if cooccurrence_swap and self._is_storage_swap(cooccurrence_swap):
                self._record_swap_request(cooccurrence_swap, 'cooccurrence', current_timestep)
                return cooccurrence_swap

        return [0, 0]  # No beneficial swap found

    def _find_closer_position(self, current_pos, delivery_positions, hot_items_type, item_locations):
        """
        Greedy neighborhood search for better item placement.

        Algorithm: Exhaustive search of all storage positions to find
        the closer position with the highest net benefit
        (hot item's distance saved minus the displaced item's penalty).

        Returns [current_index, target_index] if beneficial swap found.
        """
        grid = self.env.warehouse_grid
        current_idx = current_pos[1] * grid.width + current_pos[0]
        current_dist = min(grid.manhattan_distance(current_pos, delivery_pos)
                           for delivery_pos in delivery_positions)

        # Skip if this shelf was swapped recently so we don't keep moving the same cells
        if self._recently_swapped(current_idx):
            return None

        best_idx = None
        best_benefit = 0

        # Exhaustive neighborhood search
        # Loop through all grid positions (nested for loops over x,y)
        for y in range(grid.height):
            for x in range(grid.width):
                # Check if position is a storage cell (grid.cell_types[y, x] == 1)
                # Skip if not a storage shelf so items never go on the floor
                if grid.cell_types[y, x] != 1:
                    continue

                # Skip if a hot item is there so we only swap with empty shelves or cold items
                # HINT: Look for empty spots or positions with cold items
                if grid.item_grid[y, x] in hot_items_type:
                    continue

                # Skip if this shelf was swapped recently so we don't undo an earlier move
                if self._recently_swapped(y * grid.width + x):
                    continue

                # Calculate distance from candidate position to delivery
                candidate_position = [x, y]
                candidate_dist = min(grid.manhattan_distance(candidate_position, delivery_pos)
                                     for delivery_pos in delivery_positions)

                # Require minimum improvement threshold (>1 step closer)
                improvement = current_dist - candidate_dist
                if improvement <= 1:
                    continue

                # Apply greedy selection: choose position with maximum net benefit
                # Pick by net benefit so the displaced item's penalty is counted too
                benefit = self._estimate_swap_benefit(current_pos, candidate_position,
                                                      delivery_positions, item_locations)

                if benefit > best_benefit:
                    best_benefit = benefit
                    # Convert 2D coordinates to 1D index for return value
                    # HINT: 1D index = y * grid.width + x
                    best_idx = y * grid.width + x

        if best_idx is None:
            return None  # No better position found

        return [current_idx, best_idx]

    def _find_cooccurrence_swap(self, hot_items_type, item_locations):
        """
        Greedy clustering algorithm for association-based spatial optimization.

        Algorithm: Scan all item pairs for clustering opportunities,
        calculate benefit for each, and greedily select highest-benefit move.

        Returns swap that maximizes benefit = co-occurrence_frequency × distance_saved
        """
        grid = self.env.warehouse_grid
        cooccurrence = grid.item_cooccurrence

        # Greedy search parameters
        min_cooccurrence = 3      # Minimum frequency threshold
        min_distance = 4          # Minimum distance threshold for clustering
        best_benefit = 0          # Track best benefit found
        best_swap = None          # Track best swap candidate
        delivery_positions = getattr(grid, 'truck_bay_positions', [(grid.width//2, grid.height//2)])

        # Greedy benefit maximization
        # Scan co-occurrence matrix (nested loops: item1, item2 where item1 < item2)
        for item1 in range(len(cooccurrence)):
            for item2 in range(item1 + 1, len(cooccurrence)):
                # Apply frequency filter (cooccurrence[item1, item2] > min_cooccurrence)
                if cooccurrence[item1, item2] <= min_cooccurrence:
                    continue

                # Get current locations from the item location map
                # Same locations as grid.find_item_locations(), built once per decision
                item1_locations = item_locations.get(item1, [])
                item2_locations = item_locations.get(item2, [])

                # Skip if one of the items is not on the grid
                if len(item1_locations) == 0 or len(item2_locations) == 0:
                    continue

                # Calculate current distance between items
                # Items can be stored in more than one spot so use the closest pair
                current_distance = None
                pair_positions = None
                for location1 in item1_locations:
                    for location2 in item2_locations:
                        distance = grid.manhattan_distance(location1, location2)
                        if current_distance is None or distance < current_distance:
                            current_distance = distance
                            pair_positions = [location1, location2]

                # Apply distance filter (current_distance > min_distance)
                if current_distance <= min_distance:
                    continue

                # Calculate benefit = cooccurrence_count × current_distance
                benefit = cooccurrence[item1, item2] * current_distance

                # Skip if not better than the best pair so far
                if benefit <= best_benefit:
                    continue

                # Cluster around the item closer to delivery so the pair ends up near the bays
                dist1 = min(grid.manhattan_distance(pair_positions[0], delivery_position)
                            for delivery_position in delivery_positions)
                dist2 = min(grid.manhattan_distance(pair_positions[1], delivery_position)
                            for delivery_position in delivery_positions)
                if dist1 <= dist2:
                    cluster_pos, moving_pos = pair_positions[0], pair_positions[1]
                else:
                    cluster_pos, moving_pos = pair_positions[1], pair_positions[0]

                # Find adjacency swap for best pair (call helper method)
                swap = self._find_adjacent_swap(cluster_pos, moving_pos, hot_items_type,
                                                cooccurrence[item1, item2], item_locations)

                # Skip if no adjacency swap so the next best pair can still be used
                if swap is None:
                    continue

                # Update best_benefit and best_swap if this benefit is higher
                best_benefit = benefit
                best_swap = swap

        return best_swap  # Return highest-benefit clustering move

    def _find_adjacent_swap(self, cluster_pos, moving_pos, hot_items_type, cooccurrence_count, item_locations):
        """
        Adjacency swap to cluster items: find the storage cell that brings the
        other item of the pair closest to the cluster item with a positive net benefit.

        benefit = co-occurrence x pair distance saved + frequency-weighted delivery
        distance saved by both swapped items (negative when items move away from delivery)

        Returns [moving_index, target_index] if a beneficial cell is found.
        """
        grid = self.env.warehouse_grid
        delivery_positions = getattr(grid, 'truck_bay_positions', [(grid.width//2, grid.height//2)])
        moving_idx = moving_pos[1] * grid.width + moving_pos[0]
        current_distance = grid.manhattan_distance(cluster_pos, moving_pos)

        # Skip if the moving item's shelf was swapped recently so we don't undo an earlier move
        if self._recently_swapped(moving_idx):
            return None

        best_idx = None
        best_benefit = 0

        for y in range(grid.height):
            for x in range(grid.width):
                # Only storage cells can hold items
                if grid.cell_types[y, x] != 1:
                    continue

                # Skip if cluster item or moving item position
                if (x == cluster_pos[0] and y == cluster_pos[1]) or (x == moving_pos[0] and y == moving_pos[1]):
                    continue

                # Skip if a hot item is there so clustering doesn't undo phase 1
                if grid.item_grid[y, x] in hot_items_type:
                    continue

                # Skip if this shelf was swapped recently so we don't undo an earlier move
                if self._recently_swapped(y * grid.width + x):
                    continue

                # Skip if the pair doesn't actually get closer
                distance_saved = current_distance - grid.manhattan_distance([x, y], cluster_pos)
                if distance_saved <= 0:
                    continue

                # Clustering gain plus the delivery change, which is the displaced item's penalty
                benefit = cooccurrence_count * distance_saved + \
                    self._estimate_swap_benefit(moving_pos, [x, y], delivery_positions, item_locations)

                # Greedy: keep the cell with the highest positive net benefit
                if benefit > best_benefit:
                    best_benefit = benefit
                    best_idx = y * grid.width + x

        if best_idx is None:
            return None  # No beneficial cell found

        return [moving_idx, best_idx]

    def _get_item_locations(self):
        """Map item type -> list of (x, y) shelves, same as grid.find_item_locations() for every item"""
        item_locations = {}
        # Row is y and col is x, positions are (x, y)
        for (row, col), item in np.ndenumerate(self.env.warehouse_grid.item_grid):
            if item != -1:
                item_locations.setdefault(int(item), []).append((col, row))
        return item_locations

    def _closest_delivery_distance(self, locations, delivery_positions):
        """Distance from the closest copy of an item to the nearest delivery point"""
        grid = self.env.warehouse_grid
        return min(grid.manhattan_distance(location, delivery_position)
                   for location in locations
                   for delivery_position in delivery_positions)

    def _estimate_swap_benefit(self, pos1, pos2, delivery_positions, item_locations):
        """
        Frequency-weighted delivery distance saved by swapping the items on two shelves.

        Counts both items (the moved one and the displaced one) and uses each
        item's closest copy because pickers go to the closest one.
        Positive = fewer steps to delivery overall, zero or negative = not worth it.
        """
        grid = self.env.warehouse_grid
        item_frequency = grid.item_access_frequency
        item1 = int(grid.item_grid[pos1[1], pos1[0]])
        item2 = int(grid.item_grid[pos2[1], pos2[0]])

        # Skip if same item because the swap changes nothing
        if item1 == item2:
            return 0

        total_saved = 0
        for item, old_pos, new_pos in [(item1, tuple(pos1), tuple(pos2)), (item2, tuple(pos2), tuple(pos1))]:
            # Skip if empty shelf
            if item == -1:
                continue

            locations = item_locations[item]
            # This copy moves to the other shelf, other copies stay put
            new_locations = [new_pos if location == old_pos else location for location in locations]

            distance_before = self._closest_delivery_distance(locations, delivery_positions)
            distance_after = self._closest_delivery_distance(new_locations, delivery_positions)
            total_saved += item_frequency[item] * (distance_before - distance_after)

        return total_saved

    def _recently_swapped(self, cell_idx):
        """True if this shelf was part of a swap in the last 500 steps"""
        swap_cooldown = 500
        return cell_idx in self.recent_swap_cells and \
            self.env.current_timestep - self.recent_swap_cells[cell_idx] < swap_cooldown

    def _is_storage_swap(self, swap):
        """True if both swap indices are different storage shelves (index = y * width + x)"""
        grid = self.env.warehouse_grid
        if swap[0] == swap[1]:
            return False
        for idx in swap:
            x, y = idx % grid.width, idx // grid.width
            if not (0 <= y < grid.height) or grid.cell_types[y, x] != 1:
                return False
        return True

    def _record_swap_request(self, swap, swap_type, current_timestep):
        """Remember the swap type and put both cells on cooldown"""
        self.layout_swap_types.append(swap_type)
        self.swap_request_types[(swap[0], swap[1])] = swap_type
        # Remember both cells so later swaps don't undo this one
        self.recent_swap_cells[swap[0]] = current_timestep
        self.recent_swap_cells[swap[1]] = current_timestep

    def track_layout_performance(self):
        """
        Performance analysis for greedy layout optimization algorithms.

        Measures:
        - Layout efficiency (frequency-weighted distances)
        - Algorithm convergence (swaps per period)
        - Optimization impact over time
        """
        if not hasattr(self, 'layout_metrics'):
            self.layout_metrics = []

        # Skip if no frequency data yet so the efficiency curve doesn't start at a fake 0
        if self.env.warehouse_grid.item_access_frequency.sum() == 0:
            return

        # Calculate current layout efficiency using weighted distance metric
        efficiency = self._calculate_layout_efficiency()

        phase1_swaps = self._count_frequency_swaps()
        phase2_swaps = self._count_cooccurrence_swaps()

        self.layout_metrics.append({
            'timestep': self.env.current_timestep,
            'efficiency': efficiency,
            # Only swaps the manager actually finished, not every request
            'total_swaps': phase1_swaps + phase2_swaps,
            'phase1_swaps': phase1_swaps,
            'phase2_swaps': phase2_swaps,
            'requested_swaps': len(self.layout_swap_types),
            # Profit per step because episodes end at different steps
            'profit_per_step': self.env.cumulative_profit / max(1, self.env.current_timestep)
        })

        # Print progress every 1000 steps
        if self.env.current_timestep % 1000 == 0:
            recent_efficiency = np.mean([m['efficiency'] for m in self.layout_metrics[-10:]])
            print(f"Layout efficiency: {recent_efficiency:.3f}")

    def _calculate_layout_efficiency(self):
        """
        Objective function evaluation for layout quality.

        Algorithm: Weighted average distance where weights = access frequency
        Lower weighted distance = higher efficiency (better layout)
        """
        # Get item frequencies and delivery positions
        grid = self.env.warehouse_grid
        item_frequency = grid.item_access_frequency
        delivery_positions = getattr(grid, 'truck_bay_positions', [(grid.width//2, grid.height//2)])

        # Farthest any cell can be from a delivery point
        max_possible_distance = grid.width + grid.height

        total_weighted_distance = 0
        total_frequency = 0
        # Where every item is stored, built once instead of one grid scan per item
        item_locations = self._get_item_locations()

        # For each item with frequency > 0:
        for item in range(len(item_frequency)):
            if item_frequency[item] <= 0:
                continue

            # - Get item location
            locations = item_locations.get(item, [])

            # Skip if item is not on the grid
            if len(locations) == 0:
                continue

            # - Calculate distance to nearest delivery
            # Use the closest copy of the item because that's the one picked
            distance = self._closest_delivery_distance(locations, delivery_positions)

            # - Weight distance by access frequency
            total_weighted_distance += item_frequency[item] * distance
            total_frequency += item_frequency[item]

        # Skip if no frequency data yet
        if total_frequency == 0:
            return 0.0

        # Return normalized efficiency score (0-1 scale)
        # HINT: efficiency = 1.0 - (weighted_avg_distance / max_possible_distance)
        weighted_avg_distance = total_weighted_distance / total_frequency
        efficiency = 1.0 - (weighted_avg_distance / max_possible_distance)

        return efficiency

    def _count_frequency_swaps(self):
        """Count completed swaps made by phase 1 (hot items to delivery)"""
        return self._count_completed_swaps('frequency')

    def _count_cooccurrence_swaps(self):
        """Count completed swaps made by phase 2 (co-occurrence clustering)"""
        return self._count_completed_swaps('cooccurrence')

    def _count_completed_swaps(self, swap_type):
        """Count swaps of this type the manager finished, so failed requests aren't counted"""
        grid = self.env.warehouse_grid
        count = 0
        for relocation in self.env.relocations_history:
            # Skip if the manager didn't finish it
            if relocation['status'] != 'completed':
                continue
            # Positions are (x, y), index = y * width + x
            from_idx = relocation['from_pos'][1] * grid.width + relocation['from_pos'][0]
            to_idx = relocation['to_pos'][1] * grid.width + relocation['to_pos'][0]
            if self.swap_request_types.get((from_idx, to_idx)) == swap_type:
                count += 1
        return count

    def track_integrated_performance(self):
        """
        Performance analysis for integrated optimization system.

        Measures:
        - Economic efficiency (profit per employee)
        - Assignment quality (distance vs value optimization)
        - Layout effectiveness (from Week 1)
        - Overall system performance
        """
        if not hasattr(self, 'integrated_metrics'):
            self.integrated_metrics = []

        # Calculate comprehensive performance metrics
        current_profit = self.env.cumulative_profit
        num_employees = len(self.env.employees)
        queue_length = len(self.env.order_queue.orders)

        # TODO: Calculate economic efficiency metrics

        # Profit made per step over the trend window, same signal staffing uses
        trend_window = self.staffing_parameters['trend_window']

        if len(self.profit_history) > trend_window:
            profit_trend = (self.profit_history[-1] - self.profit_history[-1 - trend_window]) / trend_window

        else:
            profit_trend = 0.0

        # TODO: Calculate assignment quality metrics

        # Only assignments made since the last snapshot, so each point shows recent behavior
        if len(self.assignment_log) > 0:
            avg_assignment_distance = np.mean([distance for distance, value in self.assignment_log])
            avg_assignment_value = np.mean([value for distance, value in self.assignment_log])

        else:
            avg_assignment_distance = 0.0
            avg_assignment_value = 0.0
        # Divide by the farthest possible distance so 0 = item next to worker, 1 = opposite corner
        normalized_assignment_distance = avg_assignment_distance / self.assignment_parameters['maximum_distance']
        orders_assigned = len(self.assignment_log)
        self.assignment_log = []

        # TODO: Calculate layout efficiency (from Week 1)

        # Skip if no frequency data yet, same as track_layout_performance
        if self.env.warehouse_grid.item_access_frequency.sum() > 0:
            layout_efficiency = self._calculate_layout_efficiency()

        else:
            layout_efficiency = 0.0

        # TODO: Track optimization decisions made

        # A no-op action is still a non-empty list, so check each part for a real decision
        staffing_decisions = len([a for a in self.action_history if a['staffing_action'] != 0])
        layout_decisions = len([a for a in self.action_history if a['layout_swap'] != [0, 0]])
        assignment_decisions = len([a for a in self.action_history if any(a['order_assignments'])])
        total_decisions = len([
            a for a in self.action_history
            if a['staffing_action'] != 0 or a['layout_swap'] != [0, 0] or any(a['order_assignments'])
        ])

        self.integrated_metrics.append({
            'timestep': self.env.current_timestep,
            'profit_per_employee': current_profit / max(1, num_employees),
            'queue_pressure': queue_length / max(1, num_employees),
            'profit_trend': profit_trend,
            'avg_assignment_distance': avg_assignment_distance,
            'normalized_assignment_distance': normalized_assignment_distance,
            'avg_assignment_value': avg_assignment_value,
            'orders_assigned': orders_assigned,
            'staffing_decisions': staffing_decisions,
            'layout_decisions': layout_decisions,
            'assignment_decisions': assignment_decisions,
            'total_decisions': total_decisions,
            'layout_efficiency': layout_efficiency  # From Week 1
        })

        # Print integrated progress every 1000 steps
        if self.env.current_timestep % 1000 == 0:
            recent_metrics = self.integrated_metrics[-10:]
            avg_profit_per_emp = np.mean([m['profit_per_employee'] for m in recent_metrics])
            avg_queue_pressure = np.mean([m['queue_pressure'] for m in recent_metrics])
            avg_distance = np.mean([m['avg_assignment_distance'] for m in recent_metrics])
            print(f"Integrated Performance: ${avg_profit_per_emp:.0f}/employee, Queue pressure: {avg_queue_pressure:.2f}, "
                  f"Assignment distance: {avg_distance:.1f}")

    def _get_naive_order_assignments(self, queue_info, employee_info) -> list:
        """
        WEEK 2 STEP 2: Worker-to-order matching optimization
        Optimally match idle workers to pending orders

        WORKER-TO-ORDER-MATCHING():
        1. Identify available workers (idle, not managers)
        2. Identify pending orders (up to action space limit)
        3. For each worker-order pair:
           a. Calculate distance cost (how far worker must walk to items)
           b. Calculate value benefit (how much money this order is worth)
           c. Calculate urgency factor (how soon order must be completed)
           d. Compute combined assignment score
        4. Apply assignment algorithm (choose best matches)
        5. Return optimal worker-order assignments
        """

        assignments = [0] * 20  # Initialize with no assignments

        # TODO: Find idle workers (not managers, currently available)
        # HINT: Check employee_info for active workers with idle state

        idle_workers = self._get_idle_workers(employee_info)

        # TODO: Get pending orders (limit to action space size)
        # HINT: Use self.env.order_queue.orders[:20]

        # Claimed orders stay in the queue until delivered, so keep the queue index
        # because assignments[i] maps to self.env.order_queue.orders[i]
        pending_orders = []
        for order_index, order in enumerate(self.env.order_queue.orders[:len(assignments)]):
            # Skip if already claimed so we don't waste a worker on it
            if order.status != 'pending':
                continue
            pending_orders.append((order_index, order))

        # TODO: If no workers or orders available, return empty assignments

        if len(idle_workers) == 0 or len(pending_orders) == 0:
            return assignments

        # ---

        # TODO: Calculate assignment scores for all worker-order pairs
        # TODO: For each worker-order combination:

        distance_weight = self.assignment_parameters['distance_weight']
        value_weight = self.assignment_parameters['value_weight']
        max_order_value = max(order.value for order_index, order in pending_orders)
        # Clear item locations from the last step because swaps move items
        self.item_location_cache = {}

        scored_pairs = []
        for worker_number, worker_position in idle_workers:
            for order_index, order in pending_orders:

                # TODO: - Calculate distance to order items
                # TODO: 1. Distance score = 1 / (1 + min_distance_to_items)

                min_distance = self._calculate_order_distance(worker_position, order)
                distance_score = 1 / (1 + min_distance)

                # TODO: - Calculate order value benefit
                # TODO: 2. Value score = order_value / max_order_value

                value_score = order.value / max(1, max_order_value)

                # TODO: - Compute combined assignment score
                # TODO: 3. Combined score = distance_weight × distance_score + value_weight × value_score
                # HINT: Higher score = better assignment

                score = distance_weight * distance_score + value_weight * value_score
                scored_pairs.append((score, worker_number, order_index, min_distance, order.value))

        # ---

        # TODO: Apply assignment algorithm (choose best matches)
        # TODO: Ensure each worker and order assigned at most once

        # TODO: Sort all worker-order pairs by assignment score (highest first)
        # TODO: Choose best available combinations one at a time
        # TODO: Track assigned workers and orders to avoid double-assignment
        # HINT: Use sets to track what's already assigned

        # Only greedy is built, stop early so a typo in the method doesn't silently run greedy
        assignment_method = self.assignment_parameters['assignment_method']
        if assignment_method != 'greedy':
            raise ValueError(f"Unknown assignment_method: {assignment_method}")

        scored_pairs.sort(key=lambda pair: pair[0], reverse=True)
        assigned_workers = set()
        assigned_orders = set()

        for score, worker_number, order_index, min_distance, order_value in scored_pairs:
            # Skip if worker or order already used so nobody gets double assigned
            if worker_number in assigned_workers or order_index in assigned_orders:
                continue

            assignments[order_index] = worker_number
            assigned_workers.add(worker_number)
            assigned_orders.add(order_index)
            # Keep for track_integrated_performance's assignment quality
            self.assignment_log.append((min_distance, order_value))

            # Stop once every worker or every order is used
            if len(assigned_workers) == len(idle_workers) or len(assigned_orders) == len(pending_orders):
                break

        return assignments

    def _calculate_order_distance(self, worker_pos, order):
        """
        Calculate minimum distance from worker to any item needed for this order.

        Algorithm: Find closest item location for each item type in order,
        return minimum distance across all required items.
        """
        grid = self.env.warehouse_grid
        min_distance = float('inf')

        # TODO: For each item type in order.items:
        # TODO: - Find item locations using grid.find_item_locations()
        # TODO: - Calculate distance from worker_pos to each location
        # TODO: - Track minimum distance found

        for item in order.items:
            item = int(item)
            # Scan the grid once per item type each step, not once per worker-order pair
            if item not in self.item_location_cache:
                self.item_location_cache[item] = grid.find_item_locations(item)

            for location in self.item_location_cache[item]:
                distance = grid.manhattan_distance(worker_pos, location)
                if distance < min_distance:
                    min_distance = distance

        return min_distance if min_distance != float('inf') else 0

    def _get_idle_workers(self, employee_info):
        """
        Identify workers available for order assignment.

        Returns list of (worker_index, worker_position) for available workers.
        worker_index is 1-based because 0 means no assignment in the action.
        """
        idle_workers = []

        # TODO: Loop through employee_info array
        # TODO: Check if employee is active, idle, and not a manager
        # TODO: Extract position and add to idle_workers list
        # HINT: employee_info format: [x, y, state, has_order, items_collected, is_manager]

        for row_index, row in enumerate(employee_info):
            x, y, state, has_order, items_collected, is_manager = row

            # Skip if row is empty so unused rows don't count as idle workers
            if x == 0 and y == 0:
                continue

            # Skip if busy (state 0 = idle) or already holding an order
            if state != 0 or has_order != 0:
                continue

            # Skip if manager so only workers get orders
            if is_manager == 1:
                continue

            idle_workers.append((row_index + 1, (int(x), int(y))))

        return idle_workers

    def record_reward(self, reward: float):
        """
        WEEK 3 STEP 1: Reward tracking and learning - students should expand this
        
        TODO WEEK 3 STEP 1: Students should implement:
        - Proper reward tracking
        - Performance analysis
        - Adaptive parameter adjustment
        - Multi-objective optimization
        """
        self.reward_history.append(reward)
        
        # Skeleton optimization - doesn't actually learn anything useful
        if len(self.reward_history) > 10:
            # "Update" weights randomly (this doesn't actually improve performance)
            if reward > 0:
                self.staffing_weights += np.random.randn(4) * 0.01
                self.layout_weights += np.random.randn(3) * 0.01
    
    def should_update_policy(self) -> bool:
        """
        WEEK 3 STEP 2: Policy updates and adaptation - students should improve this
        
        TODO WEEK 3 STEP 2: Students should implement proper update schedules
        """
        return len(self.action_history) % 50 == 0  # Arbitrary update frequency
    
    def get_performance_metrics(self) -> Dict:
        """
        Get agent performance metrics for analysis
        Students can use this to debug their improvements
        """
        if not self.reward_history:
            return {"avg_reward": 0, "total_actions": 0}
        
        return {
            "avg_reward": np.mean(self.reward_history[-100:]),  # Last 100 rewards
            "total_actions": len(self.action_history),
            "exploration_rate": self.exploration_rate,
            "recent_performance": np.mean(self.reward_history[-10:]) if len(self.reward_history) >= 10 else 0
        }


def create_skeleton_optimization_agent(env) -> SkeletonOptimizationAgent:
    """Factory function to create skeleton Optimization agent"""
    return SkeletonOptimizationAgent(env)


# TODO: Students should implement these advanced components:

class StudentOptimizationAgent(SkeletonOptimizationAgent):
    """
    Template for students to implement their improved Optimization agent
    
    Suggested improvements:
    1. Replace random staffing with demand-based hiring
    2. Implement proper layout optimization using item frequencies
    3. Add distance-based order assignment
    4. Implement basic Q-optimization or policy gradients
    5. Add proper exploration vs exploitation balance
    """
    
    def __init__(self, env):
        super().__init__(env)
        self.name = "StudentOptimization"
        
        # TODO: Students implement these
        # self.q_table = {}
        # self.policy_network = SimpleNeuralNetwork()
        # self.experience_buffer = []
        # self.target_network = None
        
    def _get_improved_staffing_action(self, financial_state, employee_info, queue_info):
        """
        WEEK 2 STEP 1: Students implement intelligent staffing:
        - Hire when queue is growing
        - Fire when queue is empty for extended periods
        - Consider profit margins before hiring
        - Balance managers vs workers
        """
        pass
    
    def _get_improved_layout_action(self, observation):
        """
        WEEK 1 STEP 1: Students implement smart layout optimization:
        - Move frequently accessed items closer to delivery
        - Group items that are often ordered together
        - Only optimize when queue is manageable
        - Track swap effectiveness
        """
        pass
    
    def _get_improved_order_assignments(self, queue_info, employee_info):
        """
        WEEK 2 STEP 2: Students implement efficient order assignment:
        - Assign orders to closest available employees
        - Prioritize high-value or urgent orders
        - Consider employee current locations
        - Balance workload across employees
        """
        pass
    
    def learn_from_experience(self, state, action, reward, next_state, done):
        """
        WEEK 3 STEP 3: Students implement multi-objective optimization:
        - Performance trend analysis
        - Adaptive parameter tuning
        - Multi-objective trade-off handling
        - Robust optimization techniques
        """
        pass