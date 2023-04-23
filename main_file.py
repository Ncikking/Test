##This is the main function of deterministic model of economic dispatch.

from pyomo.environ import *
import read_data as rd
import economic_dispatch as ed

if __name__=="__main__":

    # extract data form excel document
    filename = 'data.xlsx'
    orginal_data = rd.read_data(filename)

    # create and solve the model
    model = ed.economic_dispatch(orginal_data)
    opt = SolverFactory('glpk')

    # optimal result
    results = opt.solve(model, tee=True)