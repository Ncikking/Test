from pyomo.environ import *

def economic_dispatch(orginal_data):

    #Data extract
    Line = orginal_data[0]
    Bus =  orginal_data[1]
    X = orginal_data[2]
    Capacity = orginal_data[3]

    T = orginal_data[4]

    W = orginal_data[5]
    W_G = orginal_data[6]

    PV = orginal_data[7]
    PV_G = orginal_data[8]

    ESS = orginal_data[9]
    ESS_pmax = orginal_data[10]
    ESS_energy = orginal_data[11]
    ESS_SOEini = orginal_data[12]
    ESS_eff = orginal_data[13]
    #ESS_loc = orginal_data[14]

    Demand = orginal_data[15]

    G = orginal_data[16]
    G_pmax = orginal_data[17]
    G_pmin = orginal_data[18]
    G_SUC = orginal_data[19]
    G_SDC = orginal_data[20]
    G_RU = orginal_data[21]
    G_RD = orginal_data[22]
    G_uini = orginal_data[23]
    G_pini = orginal_data[24]
    G_loc = orginal_data[25]
    G_B = orginal_data[26]
    G_Bpmax = orginal_data[27]
    G_Bcost = orginal_data[28]
    Load = orginal_data[29]

  ##define the pyomo model
    model = ConcreteModel()

    ##Define Set
    #model.N = Set(ordered=True, initialize=Bus)
    model.L = Set(ordered=True, initialize=Line)
    model.T = Set(ordered=True, initialize=T)
    model.G = Set(ordered=True, initialize=G)
    model.G_B = Set(ordered=True, initialize=G_B)
    #model.G_loc = Set(ordered=True, initialize=G_loc)
    model.W = Set(ordered=True, initialize=W)
    model.PV = Set(ordered=True, initialize=PV)
    model.ESS = Set(ordered=True, initialize=ESS)
    #model.ESS_loc = Set(ordered=True, initialize=ESS_loc)
    model.Load = Set(ordered=True, initialize=Load)

  ##Generator parameter
    model.G_pmin = Param(model.G, initialize=G_pmin, mutable=True)
    model.G_pmax = Param(model.G, initialize=G_pmax, mutable=True)
    model.G_SUC = Param(model.G, initialize=G_SUC, mutable=True)
    model.G_SDC = Param(model.G, initialize=G_SDC, mutable=True)
    model.G_RU = Param(model.G, initialize=G_RU, mutable= True)
    model.G_RD = Param(model.G, initialize=G_RD, mutable=True)
    model.G_uini = Param(model.G, initialize=G_uini, mutable=True)
    model.G_pini = Param(model.G, initialize=G_pini, mutable=True)
    model.G_Bpmax = Param(model.G, model.G_B, initialize=G_Bpmax, mutable=True)
    model.G_Bcost = Param(model.G, model.G_B, initialize=G_Bcost, mutable=True)

  ##Energy Storage parameter
    model.ESS_pmax = Param(model.ESS, initialize=ESS_pmax, mutable=True)
    model.ESS_energy = Param(model.ESS, initialize=ESS_energy, mutable=True)
    model.ESS_SOEini = Param(model.ESS, initialize=ESS_SOEini, mutable=True)
    model.ESS_eff = Param(model.ESS, initialize=ESS_eff, mutable=True)

  ##PV parameter
    model.PV_G = Param(model.PV, model.T, initialize=PV_G, mutable=True)

  ##Wind parameter
    model.W_G = Param(model.W, model.T, initialize=W_G, mutable=True)

  ##Demand parameter
    model.Demand = Param(model.Load, model.T, initialize=Demand, mutable=True)

  ##Line parameter
    model.X = Param(model.L, initialize=X, mutable=True)
    model.Capacity = Param(model.L, initialize=Capacity, mutable=True)


  ##Decision variables: Generators
    model.G_p = Var(model.G, model.T, within=NonNegativeReals)
    model.G_pb = Var(model.G, model.G_B, model.T, within=NonNegativeReals)
    model.G_u = Var(model.G, model.T, within=Binary)
    model.CSU = Var(model.G, model.T, within=NonNegativeReals)
    model.CSD = Var(model.G, model.T, within=NonNegativeReals)

  ##Decision variables: ESS
    model.ESS_SOE = Var(model.ESS, model.T, within=NonNegativeReals)
    model.ESS_pch = Var(model.ESS, model.T, within=NonNegativeReals)
    model.ESS_pdis = Var(model.ESS, model.T, within=NonNegativeReals)
    model.ESS_u = Var(model.ESS, model.T, within=Binary)

  ##Decision variables: Network
    #model.flow = Var(model.L, model.T, initialize=Reals)
    #model.theta = Var(model.N, model.T, initialize=Reals)


  ##Objective function
    def Objective_TSC(model):
        return sum(sum(sum(model.G_Bcost[i,j]*model.G_pb[i,j,t] for j in model.G_B) + model.CSU[i,t] + model.CSD[i,t]\
                       for i in model.G) for t in model.T)
    model.obj = Objective(rule=Objective_TSC)

  ##Constraints: Generators
    def Powerblock1(model, i,t):
        return model.G_p[i,t] == sum(model.G_pb[i,j,t] for j in model.G_B)
    model.ConPowerblock_1 = Constraint(model.G, model.T, rule=Powerblock1)

    def Powerblock2(model, i,j,t):
        return model.G_pb[i,j,t] <= model.G_Bpmax[i,j]
    model.ConPowerblock_2 = Constraint(model.G, model.G_B, model.T, rule=Powerblock2)

    def Powermin(model, i,t):
        return model.G_p[i,t] >= model.G_pmin[i]*model.G_u[i,t]
    model.ConPowermin = Constraint(model.G, model.T, rule=Powermin)

    def Powermax(model, i,t):
        return model.G_p[i,t] <= model.G_pmax[i]*model.G_u[i,t]
    model.Conpowermax = Constraint(model.G, model.T, rule=Powermax)

    def Rampup(model, i,t):
        if model.T.ord(t) == 1:
            return model.G_p[i, t] - model.G_pini[i] <= model.G_RU[i]
        else:
            return model.G_p[i,t] - model.G_p[i,model.T.prev(t)] <= model.G_RU[i]
    model.ConRampup = Constraint(model.G, model.T, rule=Rampup)

    def Rampdown(model, i,t):
        if model.T.ord(t) == 1:
            return model.G_pini[i] - model.G_p[i,t] <= model.G_RD[i]
        else:
            return model.G_p[i,model.T.prev(t)] - model.G_p[i,t] <= model.G_RD[i]
    model.ConRampdown = Constraint(model.G, model.T, rule=Rampdown)

    def Shutdown(model, i,t):
        if model.T.ord(t) == 1:
            return model.CSD[i,t] >= model.G_SDC[i]*(model.G_uini[i]-model.G_u[i,t])
        else:
            return model.CSD[i,t] >= model.G_SDC[i]*(model.G_u[i,model.T.prev(t)]-model.G_u[i,t])
    model.ConShutdown = Constraint(model.G, model.T, rule=Shutdown)

    def Startup(model, i,t):
        if model.T.ord(t) == 1:
            return model.CSU[i, t] >= model.G_SUC[i] * (model.G_u[i, t]-model.G_uini[i])
        else:
            return model.CSU[i, t] >= model.G_SUC[i] * (model.G_u[i, t]-model.G_u[i,model.T.prev(t)])
    model.ConStartup = Constraint(model.G, model.T, rule=Startup)

##Constraints: Energy storage systems
    def ESS_SOEupdate(model, s,t):
        if model.T.ord(t) == 1:
            return model.ESS_SOE[s,t] == model.ESS_SOEini[s] + model.ESS_eff[s]*model.ESS_pch[s,t] - model.ESS_pdis[s,t]/model.ESS_eff[s]
        else:
            return model.ESS_SOE[s,t] == model.ESS_SOE[s,model.T.prev(t)] + model.ESS_eff[s]*model.ESS_pch[s,t] - model.ESS_pdis[s,t]/model.ESS_eff[s]
    model.ConESS_SOEupdate = Constraint(model.ESS, model.T, rule=ESS_SOEupdate)

    def ESS_limit(model, s,t):
        return model.ESS_SOE[s,t] <= model.ESS_energy[s]
    model.ConESS_limit = Constraint(model.ESS, model.T, rule=ESS_limit)

    def ESScharging(model, s,t):
        return model.ESS_pch[s,t] <= model.ESS_pmax[s]*model.ESS_u[s,t]
    model.Concharging = Constraint(model.ESS, model.T, rule=ESScharging)

    def ESSdischarging(model, s,t):
        return model.ESS_pdis[s,t] <= model.ESS_pmax[s] * (1 - model.ESS_u[s,t])
    model.Condischarging = Constraint(model.ESS, model.T, rule=ESSdischarging)

   ##Constraints: Power balance
    def balance(model, t):
        return sum(model.G_p[i,t] for i in model.G) +sum(model.ESS_pdis[s,t] for s in model.ESS) +sum(model.PV_G[k,t] for k in model.PV) \
               + sum(model.W_G[q,t] for q in model.W) == sum(model.Demand[j,t] for j in model.Load) +sum(model.ESS_pch[s,t] for s in model.ESS)
    model.Conbalance = Constraint(model.T, rule=balance)

    return model