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
        #       - Running Cost - $
        #       - Cost per Watt - $/MWh
        #       - CO2 - kgCO2eq/MWh
        self.wattage = wattage

        # Metrics for optimization
        # co2 stats
        # "IPCC Working Group III – Mitigation of Climate Change, Annex III: Technology - specific cost and performance parameters" (PDF). IPCC. 2014. p. 10. Retrieved 2014-08-01.
        # cpw stats
        # US Energy Information Administration, Levelized cost and levelized avoided cost of new generation resources in the Annual Energy Outlook 2015, 14 April 2015
        # cpw = Cost per MWatt
        # co2 = grams of Carbon Dioxide Equivalent per MWatt / Enviromental impact
        if self.type == "coal":
            low_cpw = 128.9
            high_cpw = 196.3
            low_co2 = 740
            high_co2 = 910
            self.cost_per_watt = random.uniform(low_cpw, high_cpw)
            self.running_cost = self.cost_per_watt * wattage
            self.co2_output = ((((self.cost_per_watt-low_cpw)/(high_cpw-low_cpw)) * (low_co2-high_co2) ) + high_co2)
        elif self.type == "naturalgas":
            low_cpw = 52.4
            high_cpw = 129.8
            low_co2 = 410
            high_co2 = 650
            self.cost_per_watt = random.uniform(low_cpw, high_cpw)
            self.running_cost = self.cost_per_watt * wattage
            self.co2_output = ((((self.cost_per_watt-low_cpw)/(high_cpw-low_cpw)) * (low_co2-high_co2) ) + high_co2)
        elif self.type == "nuclear":
            low_cpw = 52.4
            high_cpw = 129.8
            low_co2 = 3.7
            high_co2 = 25
            self.cost_per_watt =  random.uniform(95.9, 104.3)
            self.running_cost = self.cost_per_watt * wattage
            self.co2_output = ((((self.cost_per_watt-low_cpw)/(high_cpw-low_cpw)) * (low_co2-high_co2) ) + high_co2)
        elif self.type == "hydro":
            low_cpw = 52.4
            high_cpw = 129.8
            low_co2 = 1
            high_co2 = 50
            self.cost_per_watt = random.uniform(57.4, 69.8)
            self.running_cost = self.cost_per_watt * wattage
            self.co2_output = ((((self.cost_per_watt-low_cpw)/(high_cpw-low_cpw)) * (low_co2-high_co2) ) + high_co2)
        elif self.type == "wind":
            low_cpw = 52.4
            high_cpw = 129.8
            low_co2 = 8
            high_co2 = 35
            self.cost_per_watt = random.uniform(43.4, 212.9)
            self.running_cost = self.cost_per_watt * wattage
            self.co2_output = ((((self.cost_per_watt-low_cpw)/(high_cpw-low_cpw)) * (low_co2-high_co2) ) + high_co2)
        elif self.type == "solar":
            low_cpw = 52.4
            high_cpw = 129.8
            low_co2 = 18
            high_co2 = 180
            self.cost_per_watt = random.uniform(58.3, 212.9)
            self.running_cost = self.cost_per_watt * wattage
            self.co2_output = ((((self.cost_per_watt-low_cpw)/(high_cpw-low_cpw)) * (low_co2-high_co2) ) + high_co2)
        elif self.type == "geothermal":
            low_cpw = 52.4
            high_cpw = 129.8
            low_co2 = 6
            high_co2 = 79
            self.cost_per_watt = random.uniform(42.8, 53.4)
            self.running_cost = self.cost_per_watt * wattage
            self.co2_output = ((((self.cost_per_watt-low_cpw)/(high_cpw-low_cpw)) * (low_co2-high_co2) ) + high_co2)
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