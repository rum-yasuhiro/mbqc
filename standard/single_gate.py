# This code is for making mbqc circuit for qiskit simulator
# 2020 / 3 / 25
# code origin by Yasuhiro Ohkura
#

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

from qiskit.extensions.standard.h import HGate
from qiskit.extensions.standard.cz import CzGate


class MBQCSingleGate:
    def __init__(self, name, input_state=None):
        """Create a new gate.
        
        Args:
            name (str): the Qobj name of the gate
            num_qubits (int): the number of qubits the gate acts on.
            params (list): a list of parameters.
        """
        self.input_state = input_state
        if self.input_state is None:
            self._input_qr = QuantumRegister(1)
        else:
            self._input_qr = input_state

        self._qr = QuantumRegister(3)
        self._output_qr = QuantumRegister(1)

        self._cr = ClassicalRegister(4)

    def _init_resource(self):
        """ 
        Initialize the Resource state

        Returns: 
            QuantumCircuit: the QuantumCircuit object for the constructed circuit 
        """
        resource_state_circuit = QuantumCircuit(
            self._input_qr, self._qr, self._output_qr
        )

        resource_state_circuit.h(self._qr)
        resource_state_circuit.h(self._output_qr)
        resource_state_circuit.cz(self._input_qr[0], self._qr[0])
        resource_state_circuit.cz(self._qr[0:2], self._qr[1:3])
        resource_state_circuit.cz(self._qr[2], self._output_qr[0])
        resource_state_circuit.barrier()

        return resource_state_circuit
