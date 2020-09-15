"""CPU functionality."""

import sys

HLT = 0b00000001
MUL = 0b10100010
ADD = 0b10100000
LDI = 0b10000010
PRN = 0b01000111
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 0xF4
        self.running = False
        self.fl = 0b00000000
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value

    # def HLT(self):
    #     self.running = False
    #     self.pc += 1

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            with open(file_name) as file:
                for line in file:
                    split_file = line.split("#")[0]
                    comm = split_file.strip()
                    if comm == "":
                        continue
                    instruction = int(comm, 2)
                    self.ram[address] = instruction
                    address += 1
                # print(self.ram[:30])
        except FileNotFoundError:
            print(f"{sys.argv[0]} {sys.argv[1]} file not found")
            sys.exit()

    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""

    #     if op == "ADD":
    #         self.reg[reg_a] += self.reg[reg_b]
    #     # elif op == "SUB": etc
    #     if op == "AND":
    #         if reg_a == 1 and reg_b == 1:
    #             return True
    #         else:
    #             return False
    #     if op == "MUL":
    #         self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
    #         # self.reg[reg_a] += self.reg[reg_b]
    #     else:
    #         raise Exception("Unsupported ALU operation")

    def handle_HLT(self):
        self.running = False

    def handle_LDI(self):
        op_a = self.ram_read(self.pc+1)
        op_b = self.ram_read(self.pc+2)
        self.reg[op_a] = op_b
        self.pc += 3

    def handle_MUL(self):
        op_a = self.ram_read(self.pc+1)
        op_b = self.ram_read(self.pc+2)
        self.reg[op_a] = self.reg[op_a]*self.reg[op_b]
        self.pc += 3

    def handle_ADD(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.reg[op_a] += self.reg[op_b]
        self.pc += 3

    def handle_PRN(self):
        reg_num = self.ram_read(self.pc+1)
        print(self.reg[reg_num])
        self.pc += 2

    def handle_PUSH(self):
        # decrement stack pointer
        self.reg[7] -= 1
        reg_num = self.ram_read(self.pc+1)
        val = self.reg[reg_num]
        stack_pointer = self.reg[7]
        self.ram[stack_pointer] = val
        self.pc += 2

    def handle_POP(self):
        # Get value from top of stack
        stack_pointer = self.reg[7]
        val = self.ram[stack_pointer]
        # Get register number and store value there
        reg_num = self.ram_read(self.pc+1)

        self.reg[reg_num] = val
        # Increment stack pointer
        self.reg[7] += 1
        # Increment program counter
        self.pc += 2

    def handle_CALL(self):

        # store return address on the stack
        # decrement the stack pointer
        self.reg[7] -= 1
        # push return address to stack so we know where to come back to
        self.ram[self.reg[7]] = self.pc + 2
        # call the subroutine + grab next instruction
        given_reg = self.ram[self.pc+1]
        # set the pc to the register value to move to this spot in memory
        self.pc = self.reg[given_reg]

    def handle_RET(self):
        stack_pointer = self.reg[7]
        self.pc = self.ram[stack_pointer]
        self.reg[7] += 1

    def handle_CMP(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        if self.reg[op_a] == self.reg[op_b]:
            self.fl = 0b00000001  # equal flag
        if self.reg[op_a] > self.reg[op_b]:
            self.fl = 0b00000010  # greater than flag
        if self.reg[op_a] < self.reg[op_b]:
            self.fl = 0b00000100  # less than flag
        self.pc += 3

    def handle_JMP(self):
        # set register variable to next spot in file
        reg = self.ram_read(self.pc + 1)
        add = self.reg[reg]
        self.pc = add  # set program counter to given register

    def handle_JEQ(self):
        reg = self.ram_read(self.pc + 1)
        add = self.reg[reg]
        if self.fl == 0b00000001:  # equal flag
            self.pc = add  # jump to address stored in register
        else:
            self.pc += 2  # jump to spots ahead

    def handle_JNE(self):
        reg = self.ram_read(self.pc+1)
        add = self.reg[reg]
        if self.fl != 0b00000001:
            self.pc = add
        else:
            self.pc += 2

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        self.running = True
        while self.running:

            ir = self.ram_read(self.pc)
            if ir in self.branchtable:
                fun = self.branchtable[ir]
                fun()
            else:
                print(f"Unknown Instruction: {ir}")
                sys.exit()