# This code is for making mbqc circuit for qiskit simulator
# 2020 / 3 / 25
# code origin by Yasuhiro Ohkura
#

from qiskit.circuit.instruction import Instruction


class MBQCGate(Instruction):
    def __init__(self, name, num_qubits, params):
        """Create a new gate.
        
        Args:
            name (str): the Qobj name of the gate
            num_qubits (int): the number of qubits the gate acts on.
            params (list): a list of parameters.
        """
        super().__init__(name, num_qubits, 0, params)
