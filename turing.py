import sys
from typing import List, Tuple

class TuringMachineRule:
    def __init__(self, *args: str, next: 'TuringMachineState' = None) -> None:
        self.read, self.write, self.move = args
        self.next = next

    def __str__(self) -> str:
        return f"{self.read} \\to {self.write}, {self.move}"

class TuringMachineState:
    def __init__(self, name: str, accepting: bool = False) -> None:
        self.name = name
        self.rules = {}
        self.accepting = accepting

    def __str__(self) -> str:
        print = ""
        if self.rules:
            for rule in self.rules:
                print += rule.__str__() + " : "
        return f"State {self.name} with rules: {print}\n"

    def add_rule(self, rule: TuringMachineRule) -> None:
        self.rules[rule.read] = (rule.write, rule.move, rule.next)

    def add_rules(self, *rules: TuringMachineRule) -> None:
        for rule in rules:
            self.add_rule(rule)

    @property
    def halts(self) -> bool:
        return self.accepting

    def __call__(self, read_symbol: str) -> Tuple[str, str, 'TuringMachineState']:
        """
        A Turing Machine State evaluates an input symbol from the tape head and returns a tuple
        (write_symbol, move_direction, next_state) so the Turing Machine will write write_symbol to the tape,
        move the tape head in the move_direction direction, and transition to next_state.
        If no rule exists matching the read_symbol, the Turing Machine will implicitly reject and thus return None.
        """
        return self.rules.get(read_symbol, (read_symbol, None, None))

class TuringMachine:
    """
    A class to model a Turing Machine as used in Prof. Abrahim Ladha's CS 4510 class Spring 2024 at Georgia Tech
    Based on definition in Theory of Computation by Michael Sipser
    Note: Some simplification have been made to ignore the restrictions of the input and tape alphabets as well
    as the set of states Q. This class assumes the states and rules form a valid Turing Machine.
    """
    def __init__(self, q_0: TuringMachineState) -> None:
        self.q_0 = q_0
        self.__reset__()

    def __reset__(self) -> None:
        self.curr = self.q_0
        self.tape_idx = 0

    def __call__(self, input: List[str], visualize: bool = False) -> bool:
        """
        A Turing Machine takes as input a pre-filled tape of symbols, in this case represented by a string.
        If the Turing Machine has a halting state, then it will return a string representation of the tape
        after its computation halts. A Turing Machine will also halt if it has reached a rejecting state through
        implicit rejection.
        This implementation does not verify validity or halting conditions, so be warned that some Turing Machines
        may not halt.
        Update: No longer returns tape but instead whether or not the Turing Machine accepted the input.
        """
        self.__reset__()
        self.tape = []
        for symbol in input:
            self.tape.append(symbol)
        self.print_tape('input')
        while (self.curr and not self.curr.halts):
            if visualize:
                print(f"${self}$\\\\")
            write_symbol, move_direction, next_state = self.curr(self.read)
            self.write(write_symbol)
            self.move(move_direction)
            self.curr = next_state
        if visualize and self.curr and self.curr.halts:
            print(f"${self}$\\\\")
        self.print_tape('output')
        return self.curr is not None and self.curr.halts

    @property
    def read(self) -> str:
        return self.tape[self.tape_idx]

    def write(self, write_symbol: str) -> None:
        self.tape[self.tape_idx] = write_symbol

    def move(self, move_direction: str) -> None:
        if (move_direction == 'L'):
            if (self.tape_idx > 0):
                self.tape_idx -= 1
        elif (move_direction == 'R'):
            self.tape_idx += 1
            if (self.tape_idx >= len(self.tape)):
                self.tape.append('\\textvisiblespace')

    def __str__(self) -> str:
        """
        The string representation of a Turing Machine during a given state. In the format taught in class:
        aq_0bb means the tape contains symbols [a, b, b], the tape head is at index 1 (0-indexed), and
        the machine is in state q_0.
        """
        s = ""
        for i, symbol in enumerate(self.tape):
            if i == self.tape_idx:
                s += self.curr.name
            s += symbol
        return s

    def print_tape(self, label: str = None) -> None:
        s = ""
        for symbol in self.tape:
            if symbol == '\\textvisiblespace':
                s += '_'
            else:
                s += symbol
        if label:
            print(f"{label}: {s}")
        else:
            print(s)

"""
A sample instance of this Turing Machine class.
A simple Turing Machine which takes as input a sequence of bits and leaves on the tape
those bits flipped.
"""
if __name__ == '__main__':
    if len(sys.argv) != 3 and len(sys.argv) != 2:
        print("Usage: python turing.py <word> [visualize (optional)]")
        sys.exit(1)

    word = sys.argv[1]
    input_tape = list(word)

    q_0 = TuringMachineState('q_0')
    q_H = TuringMachineState('q_H', accepting=True)

    q_0.add_rules(
        TuringMachineRule('0', '1', 'R', next=q_0),
        TuringMachineRule('1', '0', 'R', next=q_0),
        TuringMachineRule('\\textvisiblespace', '\\textvisiblespace', 'L', next=q_H)
    )

    T = TuringMachine(q_0)

    accepts = T(input_tape, visualize=len(sys.argv) == 3)
    print(f"{accepts}")