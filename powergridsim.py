import simpy
import random

class Supplier(object):
    ''' Defines a supplier of power for the grid
        tn = Type Number
        Types : Coal, Natural Gas, Nuclear, Hydroelctric, Wind, Solar, Geothermal
     '''
    def __init__(self, tn, wattage):
        # Type of power supply from fixed options
        # Individual type is defined by tn
        self.types = ['coal', 'naturalgas', 'nuclear', 'hydro', 'wind', 'solar', 'geothermal']
        self.type = self.types[tn]
   
        # Maximum power output variables
        # Units - Wattage - MWh
        #       - Running Cost - $/MWh
        #       - 
        self.wattage = wattage

        # Metrics for optimization
        if self.type == "coal":
            self.running_cost = random.randint(128.9, 196.3) * wattage
            self.co2_output = self.running_cost-128.9/67.4 * 
        elif self.type == "naturalgas":
            self.running_cost = random.randint(52.4, 129.8) * wattage
        elif self.type == "nuclear":
            self.running_cost = random.randint(95.9, 104.3) * wattage
        elif self.type == "hydro":
            self.running_cost = random.randint(57.4, 69.8) * wattage
        elif self.type == "wind":
            self.running_cost = random.randint(43.4, 212.9) * wattage
        elif self.type == "solar":
            self.running_cost = random.randint(58.3, 212.9) * wattage
        elif self.type == "geothermal":
            self.running_cost = random.randint(42.8, 53.4) * wattage
        self.startup_cost = 0
        self.renewable = False

        # Time to start
        self.startuptime = 0
        self.pausetime = 0
        self.unpausetime = 0
    
    def generate(self):
        pass
    
class Conductor(object):
    def __init__(self):
            pass
