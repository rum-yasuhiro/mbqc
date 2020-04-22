# This code is for making mbqc circuit for qiskit simulator
# 2020 / 3 / 10
# code origin by Yasuhiro Ohkura
#

from typing import List
import logging
import sys
import warnings
import itertools
import numpy as np

from qiskit.extensions.standard.h import HGate
from qiskit.extensions.standard.cz import CzGate

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

## Gates
sys.path.append("./")
from standard.h import MBQCHGate


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# logger.debug(sys.path)

# 抽象基底クラス(ABC)を用いるかどうかは、今後の開発状況によって決める。 2020 / 3 / 11


class MBQC:
    """
    The transpiler for measurement based quantum computation ( mbqc )
    """

    def __init__(
        self, circuit: QuantumCircuit = None, connection_list: List = None
    ) -> None:
        """
        Args:
            circuit: the quantum circuit you want to convert to MBQC model
            connection_list: the list of pairs of connecting qubits for resource state


        """
        # input circuit
        if circuit is not None:
            self.input_circuit = circuit
        else:
            self.input_circuit = QuantumCircuit()

        self.circuit = QuantumCircuit()

        # cluster state propaty
        if connection_list is None and circuit is not None:
            self.connection_list = []
            # define cluster state
            # row*column matrix cluster state ( 4*8 = 32 by default )
            __row = 4
            __column = 8

            _row_connection = []  # qubit connection ( row ) for cluster state
            for i in range(__row):
                for j in range(__column - 1):
                    head = __column * i + j
                    tale = __column * i + j + 1
                    _row_connection.append([head, tale])

            # qubit connection ( column ) for cluster state
            _column_connection = []
            for i in range(__row - 1):
                for j in range(__column):
                    head = __column * i + j
                    tale = __column * (i + 1) + j
                    _column_connection.append([head, tale])

            self.connection_list.extend(_row_connection)
            self.connection_list.extend(_column_connection)

            # number of qubits which constructs the cluster state
            self._resource_qubits = QuantumRegister(__row * __column, "clst")

            # mbqc circuit
            self._resource = self._prep_resource()
            # self._measurement = self._feed_forward_measurement(self.circuit)

        elif connection_list is not None and circuit is not None:
            self.connection_list = connection_list
            # get the maximum number in the connection_list as # of resource qubits
            num_q = max(sum(connection_list, ())) + 1
            self._resource_qubits = QuantumRegister(num_q, "clst")

            # mbqc circuit
            self._resource = self._prep_resource()
            # self._measurement = self._feed_forward_measurement(self.circuit)

        else:
            pass

    ## 特に入力がない場合の、リソース状態をどのように扱うがが決まってない 2020 / 04 / 17

    def _construct_circuit(self):
        qc = QuantumCircuit()

        # prepare cluster state
        qc += self._resource
        # qc += self._measurement

        return qc

    def _prep_resource(self) -> QuantumCircuit:
        """
        topologyのcluster stateを実装するかは今後決める 2020 / 3 / 11
        """

        qc = QuantumCircuit(self._resource_qubits)
        qc.h(self._resource_qubits)
        for i, j in self.connection_list:
            qc.cz(self._resource_qubits[i], self._resource_qubits[j])
        return qc

    # def _feed_forward_measurement(self, quantum_circuit: QuantumCircuit):
    #     """
    #     Args:
    #         qubit_label: The qubit number which is measured

    #         x_angle: x axis measurement angle (float)
    #         z_angle: z axis measurement angle (float)

    #         x_axis: boolean for X byproduct operator
    #         z_axis: boolean for Z byproduct operator
    #     """
    #     qc = QuantumCircuit()
    #     meas_dict_list = circuit_to_mbqc(quantum_circuit)

    #     for _meas_set in meas_dict_list:
    #         _meas_qubit = _meas_set.get("qubit_label")

    #     return qc

    def draw(
        self,
        output=None,
        scale=0.7,
        filename=None,
        style=None,
        interactive=False,
        line_length=None,
        plot_barriers=True,
        reverse_bits=False,
        justify=None,
        vertical_compression="medium",
        idle_wires=True,
        with_layout=True,
        fold=None,
        ax=None,
        initial_state=False,
    ):
        # pylint: disable=cyclic-import
        from qiskit.visualization import circuit_drawer

        if isinstance(output, (int, float, np.number)):
            warnings.warn(
                "Setting 'scale' as the first argument is deprecated. "
                "Use scale=%s instead." % output,
                DeprecationWarning,
            )
            scale = output
            output = None

        return circuit_drawer(
            self.circuit,
            scale=scale,
            filename=filename,
            style=style,
            output=output,
            interactive=interactive,
            line_length=line_length,
            plot_barriers=plot_barriers,
            reverse_bits=reverse_bits,
            justify=justify,
            vertical_compression=vertical_compression,
            idle_wires=idle_wires,
            with_layout=with_layout,
            fold=fold,
            ax=ax,
            # initial_state=initial_state,
        )

    # Gates
    def h(self, input_qubit: QuantumRegister = None, measurement=False):

        """
        Example:

            Circuit Representation:

            .. jupyter execute::

                from qiskit.providers.aer.mbqc.mbqc_model import MBQC

                mbqc = MBQC()
                mbqc.h()
                mbqc.draw()
        """
        self.circuit += MBQCHGate(input_state=input_qubit).construct_circuit(
            measurement=measurement
        )
