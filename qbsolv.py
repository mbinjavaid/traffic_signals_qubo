import dwave_qbsolv as QBSolv
import time
from dwave.system.samplers import DWaveSampler
from dwave.system import LeapHybridSampler

# from dwave_qbsolv import QBSolv
# from dwave.system.composites import EmbeddingComposite
# from dwave.system.samplers import DWaveSampler
# from dwave.system.composites import FixedEmbeddingComposite
# from minorminer import find_embedding
# import dimod
from hybrid.reference.kerberos import KerberosSampler
# from dwave.cloud import Client


# from Q_proper import Q
# from itertools import repeat


qc_time_list = []

def Q_dict(Q):
    """This function changes the Q from matrix form to Dict form usable by QBSolv"""

    keys = []
    QDist_list = []

    for i in range(len(Q[0])):
        for j in range(len(Q[0])):
            if Q[i][j] != 0:
                keys.append((i, j))
                QDist_list.append(Q[i][j])

    Qdict = {keys[i]: QDist_list[i] for i in range(len(keys))}

    return Qdict


def QBSolve_quantum_solution(Q, times_list, token, annealing_time, print_energy=False):
    """This function use QC to get solution dictionary"""

    Qdict = Q_dict(Q)
    # print("QDICT: ", Qdict)
    # endpoint = 'https://cloud.dwavesys.com/sapi'

    # bqm = dimod.BinaryQuadraticModel.from_qubo(Qdict)

    # print("BQM: ", bqm)

    print("ACCESSING QUANTUM COMPUTER . . . . .")
    print("Anneal time: ", annealing_time)
    sampler = LeapHybridSampler(token=token)

    start = time.clock()

    # try:

    response = sampler.sample_qubo(Qdict, qpu_params={'annealing_time': annealing_time})

    timing_dict = response.info
    # print("\n\n\n\nTIMING INFO: ", timing_dict)

    qc_time = timing_dict["qpu_access_time"]

    qc_time_list.append(qc_time)
    print("\n\n\n\n\nQC TIMES UHUHUHUHUHHUHU", qc_time_list)

    end = time.clock()

    # print("INFO: ", response.info)
    print("RESPONSE: ", response)

    # except ValueError:
    #     print("\n\nEXCEPTION FOUND ...............\n")
    #     # response = QBSolv.QBSolv().sample_qubo(Qdict, solver=sampler)
    #     response = QBSolv.QBSolv().sample_qubo(Qdict)

    # print("RESPONSE: ", response)

    print("energies=" + str(list(response.data_vectors['energy'])))
    print("num_occurence=" + str(list(response.data_vectors['num_occurrences'])))

    if print_energy:
        print("energies=" + str(list(response.data_vectors['energy'])))

    time_taken = end - start

    times_list.append(time_taken)

    print("Time taken by QPU: ", time_taken)

    qb_solution = list(response.samples())

    qb_solution_list = list(qb_solution[0].values())

    return qb_solution_list


def QBSolve_classical_solution(Q, times_list, print_energy=False):
    """This function use classical QBSolve to get solution dictionary"""

    Qdict = Q_dict(Q)

    start = time.clock()

    response = QBSolv.QBSolv().sample_qubo(Qdict)

    # print("ENERGY: ", str(list(response.data_vectors['energy'])))
    # print("RESPONSE: ", response)

    qb_solution = list(response.samples())

    if print_energy:
        print("energies=" + str(list(response.data_vectors['energy'])))

    end = time.clock()

    time_taken = end - start

    # print("Time taken by classical QBSolv: ", time_taken)

    times_list.append(time_taken)

    qb_solution_list = list(qb_solution[0].values())

    return qb_solution_list


def solution_slicer(qb_solution_list):

    sliced_sol = [qb_solution_list[x:x + 6] for x in range(0, len(qb_solution_list), 6)]

    # print("Sliced solution: ", sliced_sol)

    return sliced_sol
