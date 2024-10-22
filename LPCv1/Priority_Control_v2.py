class StackPriorityStrategy(PriorityControlStrategy):
    def __init__(self):
        self.priority_groups = {}
        self.non_communicable_devices = []

    def update_priorities(self, devices):
        self.priority_groups = {}
        self.non_communicable_devices = []
        for device in devices:
            if not device.connected or device.flagged:
                self.non_communicable_devices.append(device)
            else:
                if device.priority not in self.priority_groups:
                    self.priority_groups[device.priority] = []
                self.priority_groups[device.priority].append(device)

        for priority in self.priority_groups:
            # Sort devices within the same priority by their power consumption (ascending)
            self.priority_groups[priority].sort(key=lambda x: x.get_power_consumption())

    def execute(self, facade: IOTDeviceFacade, threshold: int):
        total_consumption = sum(device.get_power_consumption() for device in facade.devices.values() if device.status == 'on')
        
        if total_consumption > threshold:
            print("Threshold exceeded. Turning off devices...")
            for priority in sorted(self.priority_groups.keys(), reverse=True):
                stack = self.priority_groups[priority]
                while total_consumption > threshold and stack:
                    device = stack.pop(0)
                    if device.status == 'on':
                        facade.turn_off(device.id)
                        total_consumption -= device.get_power_consumption()

        elif total_consumption < threshold:
            print("Below threshold. Turning on devices...")
            for priority in sorted(self.priority_groups.keys()):
                stack = self.priority_groups[priority]
                for device in stack:
                    if total_consumption < threshold and device.status == 'off':
                        facade.turn_on(device.id)
                        total_consumption += device.get_power_consumption()
