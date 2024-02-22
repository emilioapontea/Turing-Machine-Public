# Turing-Machine
 A class to model a Turing Machine as used in Prof. Abrahim Ladha's CS 4510 class Spring 2024 at Georgia Tech. Based on definition in Theory of Computation by Michael Sipser.

## Running the sample
`turing.py` comes pre-loaded with a basic sample Bit Flip Turing Machine. To run, simply run the command
```
python turing.py <word> -v
```
where `<word>` is a single string of $1$ and $0$. This demo will return a $\LaTeX$ formatted sequence of state configurations of the form $w_1\dots q_iw_m\dots w_n$ where each $w_i$ represents a character on the machine tape and $q_i$ represents the position and state of the tape head. `\textvisiblespace` represents the empty character on the tape alphabet, commonly replaced by `\sqcup` ($\sqcup$). To omit this output, run the command without the `-v` flag. The final output line is a boolean representing whether or not the machine ended in an accepting state.
## Constructing a Turing Machine
The `TuringMachine` class takes as input only the starting state of its state machine. This guide will walk through each individual class in `turing.py` to construct the sample Turing Machine bellow, which takes as input a sequence of $1$ and $0$ and leaves on the tape the opposite bits.

![TM for Bit Flip computation](https://github.com/emilioapontea/Turing-Machine-Public/blob/main/bit_flip.png)

### Constructing the Turing Machine States
The `TuringMachineState` class has a constructor which takes as input a `str` which is its string representation. The *BitFlip* machine has two states, $q_0$ and $q_h$. If a state is an accepting state, we pass in the optional `accepting` argument to the constructor.
```python
q_0 = TuringMachineState('q_0')
q_h = TuringMachineState('q_h', accepting=True)
```
In order to connect these states through in our Turing Machine, we must create `TuringMachineRule` objects which define transitions between the set of states. If we have some instances of `TuringMachineRule` named `rule1` and `rule` we can use the `add_rules()` function. We pass in any rules as arguments.
```python
q_0.add_rules(rule1, rule2)
```

### Turing Machine Rules
The `TuringMachineRule` constructor takes `str` arguments representing the transition $r,\to w,D$ where $r$ is a symbol which is read by the tape head, $w$ is written to the tape, and $D$ is the direction (either $L$ or $R$) which the tape head moves. We also need to specify `next`, the state to which this rule transitions. If `next` is ommited, this rule leads to an implicit rejection. **This is undefined behavior based on the Sipser definition, so take care to avoid such rules.**
For the *BitFlip* machine, we create some example rules:
```python
q_0_loop_on_0_rule = TuringMachineRule('0','1','R', next=q_0)
q_0_loop_on_1_rule = TuringMachineRule('1','0','R', next=q_0)
q_0_to_q_h_rule = TuringMachineRule('\\textvisiblespace', '\\textvisiblespace', 'L', next=q_h)

q_0.add_rules(
    q_0_loop_on_0_rule,
    q_0_loop_on_1_rule,
    q_0_to_q_h_rule
)
```

### Initializing and Running the Turing Machine
The constructor for a `TuringMachine` takes only the start state of the machine. Upon initialization, the machine stores its start state and resets its state machine. For *BitFlip* we simply say:
```python
BitFlip = TuringMachine(q_0)
```
We represent a Turing Machine tape as an (ordered) `List[str]` where each `str` represents a tape symbol. We pass in a tape of this form to the `__call__` method of the `TuringMachine` and receive the `accepts` boolean as a result. The input and output tapes also printed to the console. The optional `visualize` argument determines whether the individual state configurations are also printed (formatted in $\LaTeX$). **Every time the machine is called in this way, the state machine is reset to the defined start state.**
> Note that for cleanliness the `\textvisiblespace` characters are replaced with underscores only in the input/output sections of the console.
```python
tape = ['0','1','0']
accepts = BitFlip(tape)
```
```
input: 010
output: 101_
```
---
```python
tape = ['0','1','0']
accepts = BitFlip(tape, visualize=True)
print(accepts)
```
```
input: 1010
$q_01010$\\
$0q_0010$\\
$01q_010$\\
$010q_00$\\
$0101q_0\textvisiblespace$\\
$010q_h1\textvisiblespace$\\
output: 0101_
True
```
