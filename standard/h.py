# This code is for making mbqc circuit for qiskit simulator
# 2020 / 3 / 25
# code origin by Yasuhiro Ohkura
#


"""
Controled-not gate.
"""
from .gate import MBQCGate
from ..mbqc_model import MBQC
from qiskit.extensions.standard.x import HGate
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


class MBQCHGate(MBQCGate):
    """Pauli X (bit-flip) gate."""

    def __init__(self):
        """Create new X gate."""
        super().__init__("x", 1, [])

        self.qr = QuantumRegister(5)
        self.cr = ClassicalRegister(5)
        self.circuit = QuantumCircuit(self.qr, self.cr)

    def resource(self):
        self.circuit.h(self.qr)
        self.circuit.cz(self.qr[0:4], self.qr[1:5])

    def set_meas_angle(self):
        self.circuit.h(self.qr[0])

        self.circuit.h(self.qr[1])
        self.circuit.t(self.qr[1])

        self.circuit.h(self.qr[2])
        self.circuit.t(self.qr[2])

        self.circuit.h(self.qr[3])
        self.circuit.t(self.qr[3])

    def feed_forward_measurement(self):
        self.circuit.measure(self.qr[0])
        self.cirucuit.cx(self.qr[0], self.qr[1])

        self.circuit.measure(self.qr[1])
        self.cirucuit.cx(self.qr[1], self.qr[2])

        self.circuit.measure(self.qr[2])
        self.cirucuit.cx(self.qr[2], self.qr[3])

        self.circuit.measure(self.qr[3])
        self.cirucuit.cx(self.qr[3], self.qr[4])


def h(self, qubit, *, q=None):

    """
    Example:

        Circuit Representation:

        .. jupyter execute::

            from qiskit.providers.aer.mbqc.mbqc_model import MBQC

            mbqc = MBQC()
            mbqc.h(0)
            mbqc.draw()
    """

    return self.circuit.append(HGate, [qubit], [])


MBQC.h = h