# This code is for making mbqc circuit for qiskit simulator
# 2020 / 3 / 25
# code origin by Yasuhiro Ohkura
#


"""
Controled-not gate.
"""
import sys
import numpy as np

from .single_gate import MBQCSingleGate

from qiskit.extensions.standard.z import ZGate
from qiskit.extensions.standard.rx import RXGate
from qiskit.extensions.standard.ry import RYGate
from qiskit.extensions.standard.cz import CzGate
from qiskit.extensions.standard.cx import CnotGate
from qiskit.circuit.measure import Measure
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


class MBQCSGate(MBQCSingleGate):
    """pi/2 phase gate."""

    def __init__(
        self, input_state: QuantumRegister = None,
    ):
        """Create new S gate."""
        super().__init__(name="s", input_state=input_state)

        self._resource_state = self._init_resource()
        self._set_angle = self._set_meas_angle()
        self._meas = self._measurement()
        self._forward_propagation = self._byproduct_op_propagation()

    def _set_meas_angle(self):
        set_angle_circuit = QuantumCircuit(self._input_qr, self._qr)
        set_angle_circuit.ry(np.pi / 2, self._input_qr[0])
        set_angle_circuit.ry(np.pi / 2, self._qr[0])
        set_angle_circuit.rx(np.pi / 2, self._qr[1])
        set_angle_circuit.ry(np.pi / 2, self._qr[2])

        return set_angle_circuit

    def _measurement(self):
        meas_circuit = QuantumCircuit(
            self._input_qr, self._qr, self._output_qr, self._cr
        )
        meas_circuit.measure(self._input_qr[0], self._cr[0])
        meas_circuit.measure(self._qr[0], self._cr[1])
        meas_circuit.measure(self._qr[1], self._cr[2])
        meas_circuit.measure(self._qr[2], self._cr[3])

        return meas_circuit

    def _byproduct_op_propagation(self):
        byproduct_op_propagation_circuit = QuantumCircuit(
            self._input_qr, self._qr, self._output_qr
        )
        byproduct_op_propagation_circuit.cx(self._qr[0], self._output_qr[0])
        byproduct_op_propagation_circuit.cx(self._qr[2], self._output_qr[0])

        byproduct_op_propagation_circuit.cz(self._input_qr[0], self._output_qr[0])
        byproduct_op_propagation_circuit.cz(self._qr[0], self._output_qr[0])
        byproduct_op_propagation_circuit.cz(self._qr[1], self._output_qr[0])
        byproduct_op_propagation_circuit.z(self._output_qr[0])

        return byproduct_op_propagation_circuit

    def construct_circuit(self, measurement=False):
        """
        Construct the quantum circuit

        Args: 
            measurement    : Boolean

        Returns: 
            QuantumCircuit : the QuantumCircuit object for the constructed circuit
        """
        self._initial_resource_state = QuantumCircuit() + self._resource_state
        circuit = QuantumCircuit()
        circuit += self._initial_resource_state
        circuit += self._set_angle
        circuit += self._meas
        circuit += self._forward_propagation

        if measurement:
            measurement_cr = ClassicalRegister(1, "output")
            circuit.add_register(measurement_cr)
            circuit.measure(self._qr[-1], measurement_cr)

        return circuit
