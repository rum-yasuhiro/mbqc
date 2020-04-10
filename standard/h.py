# This code is for making mbqc circuit for qiskit simulator
# 2020 / 3 / 25
# code origin by Yasuhiro Ohkura
#


"""
Controled-not gate.
"""
from .gate import MBQCGate
from ..mbqc_model import MBQC

from qiskit.extensions.standard.h import HGate
from qiskit.extensions.standard.t import TGate
from qiskit.extensions.standard.cz import CzGate
from qiskit.circuit.measure import Measure
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


class MBQCHGate(MBQCGate):
    """Hadamard (bit-flip) gate."""

    def __init__(self, initial_resource_state=None):
        """Create new H gate."""
        super().__init__("h", 1, [])

        self._qr = QuantumRegister(5)
        self._cr = ClassicalRegister(4)

        self._initial_resource_state = initial_resource_state

        self._resource_state = self._init_resource()
        self._set_angle = self._set_meas_angle()
        self._feed_forward_measurement = self._feed_forward_measurement()

    def _init_resource(self):
        """ 
        Initialize the Resource state

        Returns: 
            QuantumCircuit: the QuantumCircuit object for the constructed circuit 
        """
        resource_state_circuit = QuantumCircuit(self._qr)
        resource_state_circuit.h(self._qr)
        resource_state_circuit.cz(self._qr[0:4], self._qr[1:5])

        return resource_state_circuit

    def _set_meas_angle(self):
        set_angle_circuit = QuantumCircuit(self._qr)
        set_angle_circuit.h(self._qr[0])

        set_angle_circuit.h(self._qr[1])
        set_angle_circuit.t(self._qr[1])

        set_angle_circuit.h(self._qr[2])
        set_angle_circuit.t(self._qr[2])

        set_angle_circuit.h(self._qr[3])
        set_angle_circuit.t(self._qr[3])

        return set_angle_circuit

    def _feed_forward_measurement(self):
        meas_circuit = QuantumCircuit(self._qr, self._cr)
        meas_circuit.measure(self._qr[0], self._cr[0])
        self.cirucuit.cx(self._qr[0], self._qr[1])

        meas_circuit.measure(self._qr[1], self._cr[1])
        self.cirucuit.cx(self._qr[1], self._qr[2])

        meas_circuit.measure(self._qr[2], self._cr[2])
        self.cirucuit.cx(self._qr[2], self._qr[3])

        meas_circuit.measure(self._qr[3], self._cr[3])
        self.cirucuit.cx(self._qr[3], self._qr[4])

        return meas_circuit

    def construct_circuit(self, measurement=False):
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
        circuit += self._feed_forward_measurement

        if measurement:
            measurement_cr = ClassicalRegister(1, "m")
            circuit.add_register(measurement_cr)
            circuit.measure(self._qr[-1], measurement_cr)

        return circuit


def h(self, measurement=False):

    """
    Example:

        Circuit Representation:

        .. jupyter execute::

            from qiskit.providers.aer.mbqc.mbqc_model import MBQC

            mbqc = MBQC()
            mbqc.h(0)
            mbqc.draw()
    """
    self.circuit += MBQCHGate.construct_circuit(measurement)
    return self.circuit


MBQC.h = h
