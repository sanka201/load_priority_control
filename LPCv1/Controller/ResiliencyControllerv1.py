import pulp

class BatteryOptimizer:
    def __init__(self, n_hours, battery_capacity, initial_soc, max_loads, weights,vip):
        """
        Initialize the optimizer with the necessary parameters.

        Parameters:
        - n_hours (int): Number of hours to optimize over in each step.
        - battery_capacity (float): Total capacity of the battery.
        - initial_soc (float): Initial SOC of the battery.
        - max_loads (dict): Maximum possible loads for each group.
        - weights (dict): Weights for each load group in the objective function.
        """
        self.n_hours = n_hours
        self.battery_capacity = battery_capacity
        self.initial_soc = initial_soc
        self.max_loads = max_loads
        self.weights = weights
        self.M = battery_capacity  # Big M value
        self.vip=vip
        result=self.vip.rpc.call('storageAgentagent-0.1_1','config_battery1',100,10,1,20).get(timeout=20)
        # Initialize SOC and other variables
        self.current_soc = initial_soc
        self.results = None

    def optimize(self):
        """
        Perform the battery optimization with gradual shedding.

        Parameters:
        - actual_consumption_data (list of dicts): Actual consumption data per hour.

        Returns:
        - list: Results containing SOC and power supplied to each load group at each time step.
        """
        time_step = 0


        #while self.current_soc > 0.5 * self.battery_capacity:
        # Create the LP problem for the current time step
        prob = pulp.LpProblem(f"Battery_Optimization_Time_{time_step}", pulp.LpMaximize)
        
        # Decision Variables
        P_critical = {}
        P_medium = {}
        P_low = {}
        SOC = {}
        Binary_Medium = {}
        Binary_Low = {}

        # Initialize SOC at time 0 for this optimization step
        SOC[0] = self.current_soc
        print("Current SOC Before>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",self.vip.rpc.call('storageAgentagent-0.1_1','get_batter1_SOC').get(timeout=20))
        for t in range(1, self.n_hours + 1):
            # Power supplied to each load group at time t
            P_critical[t] = pulp.LpVariable(f'P_critical_{t}', lowBound=0, upBound=self.max_loads['critical'])
            P_medium[t] = pulp.LpVariable(f'P_medium_{t}', lowBound=0, upBound=self.max_loads['medium'])
            P_low[t] = pulp.LpVariable(f'P_low_{t}', lowBound=0, upBound=self.max_loads['low'])

            # SOC variable at time t
            SOC[t] = pulp.LpVariable(f'SOC_{t}', lowBound=0, upBound=self.battery_capacity)

            # Binary variables for SOC thresholds
            Binary_Medium[t] = pulp.LpVariable(f'Binary_Medium_{t}', cat='Binary')
            Binary_Low[t] = pulp.LpVariable(f'Binary_Low_{t}', cat='Binary')

            # SOC balance equation
            total_power = P_critical[t] + P_medium[t] + P_low[t]
            prob += SOC[t] == SOC[t-1] - total_power, f"SOC_balance_{t}"

            # Discharge rate constraints
            prob += total_power <= 0.2 * self.battery_capacity, f"Total_Discharge_Max_{t}"

            # SOC thresholds for each group
            SOC_threshold_upper_low = 0.8 * self.battery_capacity  # SOC above which low loads get full power
            SOC_threshold_lower_low = 0.7 * self.battery_capacity  # SOC below which low loads are fully shed

            SOC_threshold_upper_medium = 0.75 * self.battery_capacity
            SOC_threshold_lower_medium = 0.65 * self.battery_capacity

            # Critical load is always supplied fully unless SOC is critically low
            prob += P_critical[t] == self.max_loads['critical'], f"P_Critical_{t}"

            # Constraints linking SOC and Binary Variables
            prob += SOC[t] >= SOC_threshold_lower_medium - self.M * (1 - Binary_Medium[t]), f"SOC_Medium_Binary_Lower_{t}"
            prob += SOC[t] <= SOC_threshold_upper_medium + self.M * Binary_Medium[t], f"SOC_Medium_Binary_Upper_{t}"

            prob += SOC[t] >= SOC_threshold_lower_low - self.M * (1 - Binary_Low[t]), f"SOC_Low_Binary_Lower_{t}"
            prob += SOC[t] <= SOC_threshold_upper_low + self.M * Binary_Low[t], f"SOC_Low_Binary_Upper_{t}"

            # Correct calculation of slope and intercept for P_medium[t]
            slope_medium = self.max_loads['medium'] / (SOC_threshold_upper_medium - SOC_threshold_lower_medium)
            intercept_medium = -slope_medium * SOC_threshold_lower_medium

            prob += P_medium[t] >= 0, f"P_Medium_Lower_{t}"
            prob += P_medium[t] <= self.max_loads['medium'] * Binary_Medium[t], f"P_Medium_Upper_{t}"
            prob += P_medium[t] <= slope_medium * SOC[t] + intercept_medium + self.M * (1 - Binary_Medium[t]), f"P_Medium_SOC_{t}"

            # Similarly for P_low[t]
            slope_low = self.max_loads['low'] / (SOC_threshold_upper_low - SOC_threshold_lower_low)
            intercept_low = -slope_low * SOC_threshold_lower_low

            prob += P_low[t] >= 0, f"P_Low_Lower_{t}"
            prob += P_low[t] <= self.max_loads['low'] * Binary_Low[t], f"P_Low_Upper_{t}"
            prob += P_low[t] <= slope_low * SOC[t] + intercept_low + self.M * (1 - Binary_Low[t]), f"P_Low_SOC_{t}"

            # Priority constraints
            prob += P_low[t] <= P_medium[t], f"Priority_Low_{t}"

        # Objective function: maximize weighted sum of supplied loads
        total_weighted_load = pulp.lpSum([
            self.weights['critical'] * P_critical[t] +
            self.weights['medium'] * P_medium[t] +
            self.weights['low'] * P_low[t]
            for t in range(1, self.n_hours + 1)
        ])
        prob += total_weighted_load, "Total_Weighted_Load"

        # Solve the problem
        prob.solve()

        # Check if the problem is feasible
        if pulp.LpStatus[prob.status] != 'Optimal':
            print(f"Problem is infeasible at time step {time_step}")
         #   break

        # Retrieve optimized power supplied for the first hour
        P_critical_value = pulp.value(P_critical[1])
        P_medium_value = pulp.value(P_medium[1])
        P_low_value = pulp.value(P_low[1])
        self.current_soc = self.vip.rpc.call('storageAgentagent-0.1_1','get_batter1_SOC').get(timeout=20)# max(0, self.current_soc - total_consumption)
        print("Current SOC After>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",self.current_soc)

        # Record results
        # self.results.append({
        #     'Time_Step': time_step,
        #     'Optimization_Status': pulp.LpStatus[prob.status],
        #     'P_critical_Optimized': P_critical_value,
        #     'P_medium_Optimized': P_medium_value,
        #     'P_low_Optimized': P_low_value,
        #     'Actual_Consumption_Critical': consumption_critical,
        #     'Actual_Consumption_Medium': consumption_medium,
        #     'Actual_Consumption_Low': consumption_low,
        #     'SOC': self.current_soc
        # })
        
        self.results={
            'Time_Step': time_step,
            'Optimization_Status': pulp.LpStatus[prob.status],
            'P_critical_Optimized': P_critical_value,
            'P_medium_Optimized': P_medium_value,
            'P_low_Optimized': P_low_value,
            'SOC': self.current_soc
        }


        # Check if SOC has reached the minimum threshold
        #if self.current_soc <= 0.5 * self.battery_capacity:
            #break

        time_step += 1

        return self.results

# Example usage:
if __name__ == "__main__":
    n_hours = 1  # Number of hours to optimize ahead in each step
    battery_capacity = 100  # Total battery capacity in kWh
    initial_soc = 100       # Initial SOC in kWh

    # Maximum possible loads for each priority group in kW
    max_loads = {
        'critical': 2.5,
        'medium': 2,
        'low': 3
    }

    # Weights for the objective function
    weights = {
        'critical': 100,
        'medium': 10,
        'low': 1
    }

    # Actual consumption data per hour
    actual_consumption_data = [
        {'critical': 1, 'medium': 1, 'low': 2},
        {'critical': 2, 'medium': 1, 'low': 0},  # Low priority load shed
        {'critical': 2.5, 'medium': 0, 'low': 0},  # Medium and low priority loads shed
        # Add more data if needed
    ]

    # Create an optimizer instance
    optimizer = BatteryOptimizer(n_hours, battery_capacity, initial_soc, max_loads, weights,1)
    
    for i in range(5):
        # Perform optimization
        print("time 444444444444444444444444444444444444")
        results = optimizer.optimize()

        # Print the results
        for res in results:
            print(f"Time Step: {res['Time_Step']}")
            print(f"Optimization Status: {res['Optimization_Status']}")
            print(f"Optimized Power for Critical Loads: {res['P_critical_Optimized']} kW")
            print(f"Optimized Power for Medium Loads: {res['P_medium_Optimized']} kW")
            print(f"Optimized Power for Low Loads: {res['P_low_Optimized']} kW")
            print(f"Actual Consumption for Critical Loads: {res['Actual_Consumption_Critical']} kW")
            print(f"Actual Consumption for Medium Loads: {res['Actual_Consumption_Medium']} kW")
            print(f"Actual Consumption for Low Loads: {res['Actual_Consumption_Low']} kW")
            print(f"SOC: {res['SOC']} kWh")
            print("-" * 50)
