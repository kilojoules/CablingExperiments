import numpy as np
import networkx as nx
from scipy.interpolate import griddata
from windIO.utils.yml_utils import validate_yaml, Loader, load_yaml
import os
import yaml
import xarray as xr

def load_data():
    # Custom constructor for netCDF data
    def includeBathymetryNetCDF(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        dataset = xr.open_dataset(filename)
        bathymetry_data = {variable: list(dataset[variable].values.reshape(-1))
                           for variable in dataset.variables}
        return bathymetry_data

    Loader.includeBathymetryNetCDF = includeBathymetryNetCDF
    Loader.add_constructor('!includeBathymetryNetCDF', Loader.includeBathymetryNetCDF)

    # Load YAML files
    with open('../Reference_Site_Draft/IEA37_Borssele_Regular_System.yaml', 'r') as f:
        regular_system = yaml.load(f, Loader)

    with open('../Reference_Site_Draft/IEA37_Borssele_irregular_System.yaml', 'r') as f:
        irregular_system = yaml.load(f, Loader)

    # Extract site and wind farm data
    b = regular_system['site']
    regular = regular_system['wind_farm']
    irregular = irregular_system['wind_farm']

    regx = regular['layouts']['initial_layout']['coordinates']['x']
    regy = regular['layouts']['initial_layout']['coordinates']['y']
    irrgx = irregular['layouts']['initial_layout']['coordinates']['x']
    irrgy = irregular['layouts']['initial_layout']['coordinates']['y']

    # Parameters
    X = regx
    Y = regy
    substation_pos = [497620.7, 5730622.0]
    cable_costs = [206, 287, 406]  # Costs per distance for each cable type
    turbines_per_cable = [3, 5, 7]

    return X, Y, substation_pos, cable_costs, turbines_per_cable

# Example usage
#X, Y, substation_pos, cable_costs, turbines_per_cable = load_data()

