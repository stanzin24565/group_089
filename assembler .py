register_dict = {
    "zero": 0,
    "ra": 1,
    "sp": 2,
    "gp": 3,
    "tp": 4,
    "t0": 5,
    "t1": 6, 
    "t2": 7, 
    "s0": 8, 
    "s1": 9,
    "a0": 10, 
    "a1": 11, 
    "a2": 12, 
    "a3": 13, 
    "a4": 14, 
    "a5": 15,
    "a6": 16, 
    "a7": 17, 
    "s2": 18, 
    "s3": 19, 
    "s4": 20, 
    "s5": 21,
    "s6": 22, 
    "s7": 23, 
    "s8": 24, 
    "s9": 25, 
    "s10": 26, 
    "s11": 27,
    "t3": 28, 
    "t4": 29, 
    "t5": 30, 
    "t6": 31

}

valid_opcode = {
    # R-Type Instructions
    "add": "0110011",
    "sub": "0110011", 
    "slt": "0110011", 
    "srl": "0110011", 
    "or": "0110011",

    # I-Type Instructions
    "lw": "0000011", 
    "addi": "0010011", 
    "jalr": "1100111",

    # S-Type Instruction
    "sw": "0100011", 

    # B-Type Instructions
    "beq": "1100011", 
    "bne": "1100011", 
    "blt": "1100011",

    # J-Type Instruction
    "jal":"-"   
}

funct3_map = {
    # R-Type Instructions
    "add": "000", 
    "sub": "000", 
    "slt": "010", 
    "srl": "101", 
    "or": "110", 
    "and": "111",

    # I-Type Instructions
    "lw": "010", 
    "addi": "000", 
    "jalr": "000", 

    # S-Type Instruction
    "sw": "010", 

    # B-Type Instructions
    "beq": "000",
    "bne": "001", 
    "blt": "100",
   
   # J-Type Instruction
    "jal":"-"
}   

funct7_map = {
             "add": "0000000",
             "sub": "0100000", 
             "srl": "0000000", 
             "or": "0000000"
}


def encode_instruction(instruction, sub_parts, label_dict, line_num):

    if instruction == "lw":
        rd, offset_rs1 = sub_parts[0], sub_parts[1]

        offset, rs1 = offset_rs1.split("(")

        rs1 = rs1.rstrip(")")
        return f"{int(offset):012b}{register_dict[rs1]:05b}{funct3_map[instruction]}{register_dict[rd]:05b}{valid_opcode[instruction]}"

    elif instruction == "sw":
        rs2, offset_rs1 = sub_parts[0], sub_parts[1]

        offset, rs1 = offset_rs1.split("(")

        rs1 = rs1.rstrip(")")
        imm = f"{int(offset):012b}"
        return f"{imm[:7]}{register_dict[rs2]:05b}{register_dict[rs1]:05b}{funct3_map[instruction]}{imm[7:]}{valid_opcode[instruction]}"

    elif instruction in ["add", "sub", "or", "srl"]:
        rd, rs1, rs2 = sub_parts

        return f"{funct7_map[instruction]}{register_dict[rs2]:05b}{register_dict[rs1]:05b}{funct3_map[instruction]}{register_dict[rd]:05b}{valid_opcode[instruction]}"
    
    elif instruction == "addi":
        rd, rs1, imm = sub_parts

        return f"{int(imm):012b}{register_dict[rs1]:05b}{funct3_map[instruction]}{register_dict[rd]:05b}{valid_opcode[instruction]}"
    
    elif instruction == "jalr":
        rd, rs1, imm = sub_parts

        imm = int(imm) & 0xFFF
        return f"{imm:012b}{register_dict[rs1]:05b}{funct3_map[instruction]}{register_dict[rd]:05b}{valid_opcode[instruction]}"
    
    elif instruction in ["beq", "blt"]:
        rs1, rs2, imm = sub_parts

        if imm in label_dict:
            imm = (label_dict[imm] - line_num) * 4  


        imm = int(imm) & 0x1FFF
        imm_bin = f"{imm:013b}"
        return f"{imm_bin[0]}{imm_bin[2:8]}{register_dict[rs2]:05b}{register_dict[rs1]:05b}{funct3_map[instruction]}{imm_bin[8:12]}{imm_bin[1]}{valid_opcode[instruction]}"
    
    return None


try:
    with open("/Users/stanzinchondol/Desktop/group_089/file .txt", 'r') as input_file:

        content = input_file.readlines()
    
    label_dict = {}
    output = []
    

    line_num = 0
    for line in content:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        if ":" in line:
            label, instruction = line.split(":")
            label_dict[label.strip()] = line_num
            
            if instruction.strip():
                line_num += 1
        else:
            line_num += 1
    

    line_num = 0
    for line in content:
        line = line.strip()

        if not line or line.startswith("#") or ":" in line:
            continue
        
        parts = line.split(" ")
        instruction = parts[0].lower()
        sub_parts = parts[1].split(",") if len(parts) > 1 else []
        
        encoded = encode_instruction(instruction, sub_parts, label_dict, line_num)

        if encoded:
            output.append(encoded)
        else:
            print(f"Error encoding instruction: {line}")
        line_num += 1

    
    with open("/Users/stanzinchondol/Desktop/assignment2 /output .txt", 'w') as output_file:
        for line in output:
            output_file.write(line + "\n")
    
    print("output saved in output.txt")

except FileNotFoundError:
    print("Input file not found.")

except Exception as e:
    print(f"Unexpected error: {e}")