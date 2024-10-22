import numpy as np

class Battery:
    def __init__(self, capacity_kWh, max_discharge_kW, voltage_nominal,
                 peukert_exponent, initial_charge_efficiency, initial_discharge_efficiency,
                 initial_soc=1.0, state_of_health=1.0, temperature_C=25, min_soc_percent=20):
        self.capacity_kWh_nominal = capacity_kWh              # Nominal capacity in kWh
        self.capacity_Wh_nominal = capacity_kWh * 1000        # Nominal capacity in Wh
        self.state_of_health = state_of_health                # Battery health (1.0 = 100% capacity)
        self.capacity_Wh_actual = self.capacity_Wh_nominal * self.state_of_health
        self.max_discharge_kW = max_discharge_kW              # Max discharge power in kW
        self.voltage_nominal = voltage_nominal                # Nominal voltage in Volts
        self.peukert_exponent = peukert_exponent              # Peukert's exponent
        self.initial_charge_efficiency = initial_charge_efficiency  # Initial charge efficiency
        self.initial_discharge_efficiency = initial_discharge_efficiency  # Initial discharge efficiency
        self.charge_efficiency = initial_charge_efficiency    # Adjusted charge efficiency
        self.discharge_efficiency = initial_discharge_efficiency  # Adjusted discharge efficiency
        self.soc = initial_soc * self.capacity_Wh_actual      # State of Charge in Wh
        self.temperature_C = temperature_C                    # Battery temperature in Celsius
        self.min_soc = min_soc_percent / 100 * self.capacity_Wh_actual  # Minimum SoC in Wh
        self.cycle_count = 0                                  # Initialize cycle count
        self.last_soc = self.soc                              # Store last SoC for cycle counting

    def get_internal_resistance(self):
        # Simplified model: internal resistance increases at low SoC
        r_min = 0.005  # Ohms at full charge
        r_max = 0.05   # Ohms at empty
        soc_percent = self.get_soc_percent() / 100
        internal_resistance = r_min + (1 - soc_percent) * (r_max - r_min)
        return internal_resistance

    def get_voltage(self):
        # More realistic voltage-SOC curve using a polynomial fit
        soc = self.get_soc_percent()
        # Polynomial coefficients for Li-ion battery (example values)
        # Voltage (V) = a*SoC^3 + b*SoC^2 + c*SoC + d
        a = -0.0001
        b = 0.01
        c = -0.1
        d = self.voltage_nominal
        voltage = a * soc**3 + b * soc**2 + c * soc + d
        return voltage

    def adjust_efficiencies_for_temperature(self):
        # Adjust efficiencies based on temperature
        temp_ref = 25  # Reference temperature in Celsius
        temp_coefficient = 0.005  # Efficiency loss per degree Celsius deviation
        temp_diff = self.temperature_C - temp_ref

        # Adjust charging efficiency
        self.charge_efficiency = self.initial_charge_efficiency - abs(temp_diff) * temp_coefficient
        self.charge_efficiency = max(0.8, min(self.charge_efficiency, self.initial_charge_efficiency))

        # Adjust discharging efficiency
        self.discharge_efficiency = self.initial_discharge_efficiency - abs(temp_diff) * temp_coefficient
        self.discharge_efficiency = max(0.8, min(self.discharge_efficiency, self.initial_discharge_efficiency))

    def discharge(self, power_demand_W, duration_h):
        self.adjust_efficiencies_for_temperature()

        # Adjust for discharge efficiency
        power_required_W = power_demand_W / self.discharge_efficiency

        # Peukert effect
        effective_capacity_Wh = self.capacity_Wh_actual / (duration_h ** (self.peukert_exponent - 1))

        # Maximum energy that can be drawn considering Peukert effect and DoD limit
        energy_available_Wh = self.soc - self.min_soc

        # Ensure we don't over-discharge
        if energy_available_Wh <= 0:
            actual_power_W = 0
            energy_drawn_Wh = 0
        else:
            # Maximum power considering battery limits
            max_power_W = self.max_discharge_kW * 1000

            # Actual power supplied
            actual_power_W = min(power_required_W, max_power_W)

            # Energy drawn
            energy_drawn_Wh = actual_power_W * duration_h

            # Ensure we don't draw more energy than available
            if energy_drawn_Wh > energy_available_Wh:
                energy_drawn_Wh = energy_available_Wh
                actual_power_W = energy_drawn_Wh / duration_h

            # Update State of Charge
            self.soc -= energy_drawn_Wh

            # Update cycle count
            self.update_cycle_count(energy_drawn_Wh)

        # Adjust actual power for discharge efficiency
        actual_power_W *= self.discharge_efficiency

        return actual_power_W  # Actual power supplied in Watts

    def charge(self, power_available_W, duration_h):
        self.adjust_efficiencies_for_temperature()

        # Adjust for charge efficiency
        power_accepted_W = power_available_W * self.charge_efficiency

        # Maximum energy that can be accepted
        energy_needed_Wh = self.capacity_Wh_actual - self.soc

        # Energy that can be added in this time step
        energy_added_Wh = power_accepted_W * duration_h

        # Ensure we don't overcharge
        if energy_added_Wh > energy_needed_Wh:
            energy_added_Wh = energy_needed_Wh
            actual_power_W = energy_added_Wh / duration_h / self.charge_efficiency
        else:
            actual_power_W = power_available_W

        # Update State of Charge
        self.soc += energy_added_Wh

        # Update cycle count
        self.update_cycle_count(-energy_added_Wh)

        return actual_power_W  # Actual power used for charging in Watts

    def update_cycle_count(self, energy_changed_Wh):
        # Calculate Depth of Discharge for this change
        delta_soc = abs(energy_changed_Wh) / self.capacity_Wh_actual

        # Accumulate partial cycles
        self.cycle_count += delta_soc / 2  # Divided by 2 because charging and discharging both count towards cycles

        # Update State of Health based on cycles
        self.update_state_of_health()

    def get_soc_percent(self):
        # Return State of Charge as a percentage
        return (self.soc / self.capacity_Wh_actual) * 100

    def update_state_of_health(self):
        # Advanced aging model based on cycle count
        # Example: Capacity fades according to a square root of cycle count
        capacity_loss = 0.2 * (self.cycle_count ** 0.5) / 100  # 0.2% per sqrt(cycle)
        self.state_of_health = max(0.8, 1.0 - capacity_loss)
        self.capacity_Wh_actual = self.capacity_Wh_nominal * self.state_of_health
