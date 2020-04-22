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

from qiskit.extensions.standard.h import HGate
from qiskit.extensions.standard.rx import RXGate
from qiskit.extensions.standard.ry import RYGate
from qiskit.extensions.standard.cz import CzGate
from qiskit.extensions.standard.cx import CnotGate
from qiskit.circuit.measure import Measure
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


class MBQCHGate(MBQCSingleGate):
    """Hadamard (bit-flip) gate."""

    def __init__(self, input_state: QuantumRegister = None):
        """Create new H gate."""
        super().__init__("h", 1, [])

        self.input_state = input_state
        if self.input_state is None:
            self._input_qr = QuantumRegister(1)
        else:
            self._input_qr = input_state

        self._qr = QuantumRegister(3)
        self._output_qr = QuantumRegister(1)

        self._cr = ClassicalRegister(4)

        self._initial_resource_state = initial_resource_state

        self._resource_state = self._init_resource()
        self._set_angle = self._set_meas_angle()
        self._measurement = self._measurement()
        self._byproduct_op_propagation = self._byproduct_op_propagation()

    def _init_resource(self):
        """ 
        Initialize the Resource state

        Returns: 
            QuantumCircuit: the QuantumCircuit object for the constructed circuit 
        """
        resource_state_circuit = QuantumCircuit(
            self._input_qr, self._qr, self._output_qr
        )
        if self.input_state is None:
            resource_state_circuit.h(self._input_qr)
        resource_state_circuit.h(self._qr)
        resource_state_circuit.h(self._output_qr)
        resource_state_circuit.cz(self._input_qr[0], self._qr[0])
        resource_state_circuit.cz(self._qr[0:2], self._qr[1:3])
        resource_state_circuit.cz(self._qr[2], self._output_qr[0])
        resource_state_circuit.barrier()

        return resource_state_circuit

    def _set_meas_angle(self):
        set_angle_circuit = QuantumCircuit(self._input_qr, self._qr)
        set_angle_circuit.ry(np.pi / 2, self._input_qr[0])
        set_angle_circuit.rx(np.pi / 2, self._qr[0])
        set_angle_circuit.rx(np.pi / 2, self._qr[1])
        set_angle_circuit.rx(np.pi / 2, self._qr[2])

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
        byproduct_op_propagation_circuit.cx(self._input_qr[0], self._output_qr[0])
        byproduct_op_propagation_circuit.cz(self._qr[0], self._output_qr[0])
        byproduct_op_propagation_circuit.cz(self._qr[1], self._output_qr[0])
        byproduct_op_propagation_circuit.cx(self._qr[1], self._output_qr[0])
        byproduct_op_propagation_circuit.cx(self._qr[2], self._output_qr[0])

        return byproduct_op_propagation_circuit

    def construct_circuit(self, input_qubit: QuantumRegister = None, measurement=False):
        """
        Construct the quantum circuit

        Returns: 
            QuantumCircuit: the QuantumCircuit object for the constructed circuit
        """
        if self._initial_resource_state is None:
            self._initial_resource_state = QuantumCircuit() + self._resource_state

        circuit = QuantumCircuit()
        circuit += self._initial_resource_state
        circuit += self._set_angle
        circuit += self._measurement
        circuit += self._byproduct_op_propagation

        if measurement:
            measurement_cr = ClassicalRegister(1, "m")
            circuit.add_register(measurement_cr)
            circuit.measure(self._qr[-1], measurement_cr)

        return circuit


# def h(self, measurement=False):

#     """
#     Example:

#         Circuit Representation:

#         .. jupyter execute::

#             from qiskit.providers.aer.mbqc.mbqc_model import MBQC

#             mbqc = MBQC()
#             mbqc.h()
#             mbqc.draw()
#     """
#     self.circuit += MBQCHGate().construct_circuit(measurement=measurement)


# MBQC.h = h
