RISC-V Instruction Encoder (Assembler Component)
----Overview-----

This project implements a basic RISC-V instruction encoder in Python.
It converts supported RISC-V assembly instructions into their corresponding 32-bit binary machine code.

The encoder handles multiple instruction formats (R, I, S, B, J types), resolves register names, processes immediates, and supports label-based branching.

This code is part of a custom assembler / simulator pipeline.

----Supported Instruction Set----
R-Type Instructions

add

sub

slt

srl

or
I-Type Instructions

lw

addi

jalr

S-Type Instructions

sw

B-Type Instructions

beq

bne

blt

J-Type Instructions

jal

----Key Features----

 Register name to register number mapping (x0–x31)

 Opcode, funct3, and funct7 encoding

 Label resolution for branch instructions

 Immediate value handling with proper bit masking

 Outputs 32-bit binary instructions (one per line)

---- File Structure------
.
├── assembler.py        # Main encoder logic
├── input.txt           # Input RISC-V assembly file
├── output.txt          # Generated machine code
└── README.md

-------How to Run------
1️ Prepare Input File

Create an assembly file (input.txt) with valid RISC-V instructions.

Example:

add x1,x2,x3
addi x4,x1,10
loop: beq x1,x2,loop

2️Update File Paths (Important)

In the Python script, update file paths to your system:

with open("input.txt", "r") as input_file:


and

with open("output.txt", "w") as output_file:

3️ Run the Program
python3 assembler.py

4️ Output

Machine code is written to output.txt

Each line contains a 32-bit binary instruction

Example output:

00000000001100010000000010110011
00000000101000001000001010010011

---- Encoding Logic (Brief)---

Registers are mapped using register_dict

Opcodes are selected via valid_opcode

Instruction formats are identified dynamically

Labels are converted to PC-relative offsets for branches

Immediate values are masked and split per RISC-V spec

----Assumptions & Limitations----

Input must be syntactically correct

Limited subset of RISC-V instructions supported

No pseudo-instruction expansion

Error handling is minimal (educational focus)

-----Learning Outcomes-----

Understanding RISC-V instruction formats

Binary encoding of assembly instructions

PC-relative branching and label resolution

Low-level architecture and ISA design
