"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256

    def load(self, file_name):
        """Load a program into memory."""
        try:
            address = 0
            with open(file_name) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()
                    if command == '':
                        continue
                    instruction = int(command, 2)
                    self.ram[address] = instruction
                    address += 1
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} file not found")
            sys.exit()
                
    if len(sys.argv) < 2:
        print("Please pass in a second filename: ls8.py example/second_filename.py")
        sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            print(f"Adding {self.reg[reg_a]} and {self.reg[reg_b]} together at reg index: [{reg_a}]")
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            print(f"Multiplying {self.reg[reg_a]} by {self.reg[reg_b]} at reg index: [{reg_a}]")
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return self.reg[MAR]

    def ram_write(self, MDR, MAR):
        self.reg[MAR] = MDR

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        # store stack pointer value in register 7
        self.reg[7] = 0xF4
        running = True
        
        print("\nSpinning up the Hamster wheels...")
        while running:
            command = self.ram[self.pc]
            
            if command == LDI:
                self.ram_write(self.ram[self.pc + 2], self.ram[self.pc + 1])
                print(f"Writing Value: {self.ram[self.pc + 2]} to Reg index: [{self.ram[self.pc + 1]}]")
            
            if command == PRN:
                value = self.ram_read(self.ram[self.pc + 1])
                print(f"*Stored Value at Reg index: [{self.ram[self.pc + 1]}], is: {value}*")
            
            if command == HLT:
                print("The Hamsters are too tired to run...\U0001F634")
                running = False
            
            if command == MUL:
                self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
            
            if command == PUSH:
                # decrement stack pointer
                self.reg[7] -= 1
                
                # create stack pointer var
                sp = self.reg[7]
                # get index of register value we want (next item in ram)
                reg_index = self.ram[self.pc + 1]
                # add that value to the stack
                self.ram[sp] = self.reg[reg_index]
                # one liner code 
                # self.ram[self.reg[7]] = self.reg[self.ram[self.pc + 1]]
                print(f"Pushing Value: {self.reg[reg_index]} onto the stack at slot: {sp}!")
            
            if command == POP:
                # create stack poiner var
                sp = self.reg[7]
                # 'pop' value we want from stack
                popped_value = self.ram[sp]
                # get reg index where popped_value is to be stored (next item in ram)
                reg_index = self.ram[self.pc + 1]
                # store popped_value in register
                self.reg[reg_index] = popped_value
                # one liner code
                # self.reg[self.ram[self.pc + 1]] = self.ram[self.reg[7]]
                print(f"Popping Value: {popped_value} off the stack, into Reg index: [{reg_index}]")
                
                # increment stack pointer to 'erase' popped value
                self.reg[7] += 1
                
                print(f"Setting stack pointer +1 to slot: {self.reg[7]}!")

            self.pc += 1 + (command >> 6)
