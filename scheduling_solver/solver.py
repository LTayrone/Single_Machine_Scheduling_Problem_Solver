import gurobipy as gp
from gurobipy import GRB
from scheduling_solver.data_reader import ler_instancia


def solve_scheduling_problem(file):
    n, processing_times, precedence_constraints, setup_times = ler_instancia(file)

    # Adicionar uma linha e uma coluna de zeros para o job dummy
    setup_times = [[0] * (n + 1)] + [[0] + row for row in setup_times]
    processing_times = [0] + processing_times

    # Atualizar o número de trabalhos para incluir o dummy
    n = n + 1

    # Criação do modelo
    model = gp.Model("Single_Machine_Scheduling")

    # Defina o limite de tempo para 3600 segundos (1 hora)
    #model.setParam('TimeLimit', 3600)

    # Variáveis de decisão
    x = model.addVars([(i, j) for i in range(n) for j in range(n) if i != j], vtype=GRB.BINARY, name="x")
    c = model.addVars(range(n), vtype=GRB.CONTINUOUS, name="c")
    b = model.addVars(range(n), vtype=GRB.CONTINUOUS, name="b")
    C_max = model.addVar(vtype=GRB.CONTINUOUS, name="C_max")

    # Função objetivo
    model.setObjective(C_max, GRB.MINIMIZE)

    # Restrições de precedência
    for j in range(n):
        model.addConstr(C_max >= c[j], f"Cmax_greater_c_{j}")

    # Cada trabalho deve ser seguido por um trabalho
    for i in range(n):
        model.addConstr(gp.quicksum(x[i, j] for j in range(n) if i != j) == 1, f"One_successor_{i}")

    # Cada trabalho deve ter um predecessor
    for j in range(n):
        model.addConstr(gp.quicksum(x[i, j] for i in range(n) if i != j) == 1, f"One_predecessor_{j}")

    # Relação entre tempos de início e tempos de conclusão com tempos de setup e atrasos de precedência
    M = 10000  # Um grande número
    for i in range(n):
        for j in range(n):
            if i != j:
                model.addConstr(b[j] >= c[i] + setup_times[i][j] - M * (1 - x[i, j]), f"Start_time_relation_{i}_{j}")

    # Restrições de precedência
    for (i, j, dij) in precedence_constraints:
        model.addConstr(b[j] >= c[i] + dij, f"Precedence_{i}_{j}")

    # Relação entre tempo de conclusão e tempo de início
    for j in range(1, n):  # Começa de 1 para ignorar o dummy
        model.addConstr(c[j] == b[j] + processing_times[j], f"Completion_time_{j}")

    # Resolver o modelo
    model.optimize()

    result = {}
    if model.status == GRB.Status.OPTIMAL:
        result['C_max'] = C_max.X
        result['order'] = [(i, j) for i in range(n) for j in range(n) if i != j and x[i, j].X > 0.5]
        result['times'] = [(j, b[j].X, c[j].X) for j in range(n)]
    elif model.status == GRB.Status.INFEASIBLE:
        result['infeasible'] = True

    return result