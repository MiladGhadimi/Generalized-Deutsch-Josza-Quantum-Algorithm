Generalized Deutsch–Jozsa algorithm implementation in Qiskit.

This module provides:
- A helper to build an oracle U_f for a classical function f : {0,1}^n -> {0,1}
- A function to build the full Deutsch–Jozsa / GDJ circuit
- A convenience function to run the circuit and interpret the result
"""

from typing import Callable, Dict

from qiskit import QuantumCircuit, Aer, execute


def build_oracle_from_function(f: Callable[[int], int], n: int) -> QuantumCircuit:
    """
    Build a quantum oracle U_f implementing a classical Boolean function
    f : {0,1}^n -> {0,1}, given as f(x) with x in [0, 2^n).

    The oracle acts on n + 1 qubits (n input qubits + 1 ancilla):
        U_f |x>|y> = |x>|y ⊕ f(x)|

    Args:
        f: Python function taking an integer x (0 <= x < 2^n) and returning 0 or 1.
        n: Number of input qubits.

    Returns:
        QuantumCircuit implementing U_f on n + 1 qubits.
    """
    qc = QuantumCircuit(n + 1)

    # For each basis state |x>, if f(x) = 1, flip the ancilla conditioned on |x>
    for x in range(2 ** n):
        if f(x) % 2 == 1:
            # Encode the pattern x on the first n qubits by flipping qubits where bit = 0
            # (so that the multi-controlled X triggers exactly on |x>)
            for i in range(n):
                if ((x >> i) & 1) == 0:
                    qc.x(i)

            # Multi-controlled X from the n input qubits onto the ancilla (last qubit)
            qc.mcx(list(range(n)), n)

            # Uncompute the encoding of x
            for i in range(n):
                if ((x >> i) & 1) == 0:
                    qc.x(i)

    return qc


def deutsch_jozsa_circuit(oracle: QuantumCircuit) -> QuantumCircuit:
    """
    Construct the full Deutsch–Jozsa (or generalized Deutsch–Jozsa) circuit for a given oracle.

    The oracle must be defined on n + 1 qubits (n inputs + 1 ancilla).

    Circuit layout:
    - Initialize ancilla in |1>
    - Apply H to all qubits
    - Apply oracle U_f
    - Apply H to the n input qubits again
    - Measure the n input qubits

    If f is constant, the measurement result should be 0...0 with probability 1.
    If f is balanced, some bit will be 1 with non-zero probability.

    Args:
        oracle: QuantumCircuit implementing U_f on n + 1 qubits.

    Returns:
        QuantumCircuit ready to run, with classical bits attached for the n input qubits.
    """
    n_plus_1 = oracle.num_qubits
    n = n_plus_1 - 1

    qc = QuantumCircuit(n_plus_1, n)

    # Initialize ancilla in |1>
    qc.x(n)

    # Apply Hadamards to all qubits
    for q in range(n_plus_1):
        qc.h(q)

    # Insert the oracle
    qc.compose(oracle, range(n_plus_1), inplace=True)

    # Apply Hadamards to the input register again
    for q in range(n):
        qc.h(q)

    # Measure only the n input qubits
    qc.measure(range(n), range(n))

    return qc


def run_deutsch_jozsa(
    f: Callable[[int], int],
    n: int,
    shots: int = 1024,
    backend_name: str = "qasm_simulator",
) -> Dict[str, int]:
    """
    Convenience function: build the oracle from a classical f, create the DJ circuit,
    execute it on a simulator, and return the measurement counts.

    Args:
        f: Classical Boolean function f(x) -> 0 or 1, with x in [0, 2^n).
        n: Number of input qubits.
        shots: Number of shots for the simulation.
        backend_name: Name of the Qiskit backend to use (default is "qasm_simulator").

    Returns:
        A dictionary mapping bitstrings (e.g. "000", "101", ...) to counts.
    """
    # Build oracle and DJ circuit
    oracle = build_oracle_from_function(f, n)
    dj_circuit = deutsch_jozsa_circuit(oracle)

    # Run on simulator
    backend = Aer.get_backend(backend_name)
    job = execute(dj_circuit, backend=backend, shots=shots)
    result = job.result()
    counts = result.get_counts()

    return counts


if __name__ == "__main__":
    # Example usage

    # Number of input qubits
    n_qubits = 3

    # Example 1: constant function f(x) = 0
    def f_constant(x: int) -> int:
        return 0

    counts_const = run_deutsch_jozsa(f_constant, n_qubits)
    print("Constant function counts:", counts_const)

    # Example 2: balanced function f(x) = parity of x (sum of bits mod 2)
    def f_balanced(x: int) -> int:
        # Count number of 1 bits in x and take mod 2
        return bin(x).count("1") % 2

    counts_bal = run_deutsch_jozsa(f_balanced, n_qubits)
    print("Balanced function counts:", counts_bal)
