import pandas as pd

def read_data(filename):
    NetworkData = pd.read_excel(filename, sheet_name='NetworkData')
    Line = [NetworkData.loc[i,'Unnamed: 0'] for i in NetworkData.index]
    Bus = set(list(NetworkData.FROM.unique()) + list(NetworkData.TO.unique()))
    X = {Line[i]: NetworkData.loc[i,'X'] for i in NetworkData.index}
    Capacity = {Line[i]: NetworkData.loc[i,'Capacity'] for i in NetworkData.index}

    WindGeneration = pd.read_excel(filename, sheet_name='WindGeneration')
    WindParks = pd.read_excel(filename, sheet_name='WindParks')
    T = [WindGeneration.loc[i,'Unnamed: 0'] for i in WindGeneration.index]
    W = [WindParks.loc[i,'Unnamed: 0'] for i in WindParks.index]
    W_G = {(j,WindGeneration.loc[i,'Unnamed: 0']): WindGeneration.loc[i,j] for i in WindGeneration.index for j in WindGeneration.columns[1:]}

    PVGeneration = pd.read_excel(filename, sheet_name='PVGeneration')
    PVParks = pd.read_excel(filename, sheet_name='PVParks')
    PV = [PVParks.loc[i,'Unnamed: 0'] for i in PVParks.index]
    PV_G = {(j,PVGeneration.loc[i,'Unnamed: 0']): PVGeneration.loc[i,j] for i in PVGeneration.index for j in PVGeneration.columns[1:]}

    StorageSystems = pd.read_excel(filename, sheet_name='StorageSystems')
    ESS = [StorageSystems.loc[i,'Unnamed: 0'] for i in StorageSystems.index]
    ESS_pmax = {ESS[i]: StorageSystems.loc[i,'Power'] for i in StorageSystems.index}
    ESS_energy = {ESS[i]: StorageSystems.loc[i,'Energy'] for i in StorageSystems.index}
    ESS_SOEini= {ESS[i]: StorageSystems.loc[i,'SOEini'] for i in StorageSystems.index}
    ESS_eff= {ESS[i]: StorageSystems.loc[i,'Eff'] for i in StorageSystems.index}
    ESS_loc= {ESS[i]: StorageSystems.loc[i,'Location'] for i in StorageSystems.index}

    SystemDemand = pd.read_excel(filename, sheet_name='SystemDemand')
    Loads = pd.read_excel(filename, sheet_name='Loads')
    Demand = {(j, SystemDemand.loc[i,'Unnamed: 0']): SystemDemand.loc[i,j] for i in SystemDemand.index for j in SystemDemand.columns[1:]}
    Load = [Loads.loc[i,'Unnamed: 0'] for i in Loads.index]

    Generators = pd.read_excel(filename, sheet_name='Generators')
    G = [Generators.loc[i, 'Unnamed: 0'] for i in Generators.index]
    G_pmax = {G[i]: Generators.loc[i,'Pmax'] for i in Generators.index}
    G_pmin = {G[i]: Generators.loc[i,'Pmin'] for i in Generators.index}
    G_SUC = {G[i]: Generators.loc[i,'SUC'] for i in Generators.index}
    G_SDC = {G[i]: Generators.loc[i,'SDC'] for i in Generators.index}
    G_RU = {G[i]: Generators.loc[i,'RU'] for i in Generators.index}
    G_RD = {G[i]: Generators.loc[i,'RD'] for i in Generators.index}
    G_uini = {G[i]: Generators.loc[i,'uini'] for i in Generators.index}
    G_pini = {G[i]: Generators.loc[i,'Pini'] for i in Generators.index}
    G_loc = {G[i]: Generators.loc[i,'Location'] for i in Generators.index}

    GeneratorStepSize = pd.read_excel(filename, sheet_name='GeneratorStepSize')
    G_B = [i for i in GeneratorStepSize.columns[1:]]
    G_Bpmax = {(Generators.loc[i,'Unnamed: 0'], j): GeneratorStepSize.loc[i,j] for i in GeneratorStepSize.index for j in GeneratorStepSize.columns[1:]}

    GeneratorStepCost = pd.read_excel(filename, sheet_name='GeneratorStepCost')
    G_Bcost = {(GeneratorStepCost.loc[i,'Unnamed: 0'],j): GeneratorStepCost.loc[i,j] for i in GeneratorStepCost.index for j in GeneratorStepCost.columns[1:]}


    orginal_data = [Line, Bus, X, Capacity, T, W, W_G, PV, PV_G, ESS, ESS_pmax, ESS_energy, ESS_SOEini, ESS_eff, ESS_loc, Demand, G, G_pmax, G_pmin, G_SUC,
    G_SDC, G_RU, G_RD, G_uini, G_pini, G_loc, G_B, G_Bpmax, G_Bcost, Load]

    return orginal_data