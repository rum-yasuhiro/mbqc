# This code is for making mbqc circuit for qiskit simulator
# 2020 / 3 / 10
# code origin by Yasuhiro Ohkura
#


from typing import List

from qiskit import QuantumCircuit


"""
convert quantum circuit model to mbqc model


quantum circuit -> unitary(angles) -> measurement angle

"""


def circuit_to_mbqc(qc) -> List:
    """

    Args:
        qc (Quantum circuit): the input circuit.

    return:
        cluster_topology    : coupling map of input qubit
        measurement_list    : The list of information set of measurement: dict
            
            [{meas_set_dict1}, {meas_set_dict2}, ...]

            meas_set_dict = {
                qubit_label         : int,
                theta_angle         : float,
                phi_angle           : float,
                lambda_angle        : float,
                byproduct_cancel    : [s, Gate] ## s: result of measurement ( s = 0, 1 )
            }
    """
    _decomp_instruction(qc)

    topology = []
    mbqc_instruction_list = []

    return topology, mbqc_instruction_list


# @staticmethod
def _decomp_instruction(qc):
    """
    Args: 
        qc (Quantum circuit)    :  input circuit

    return: 
        
    """

    return

