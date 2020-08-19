"""Memory visualizer."""
from .models import MipsProgram
from .preprocessor import preprocess
from struct import unpack


def visualize_memory(args):
    """Visualize the stack, heap, data of mips program."""

    def format_output(program: MipsProgram, section: str, rep_int: bool, rep_float: bool) -> str:
        """Create the list to be visualized."""
        escape_dict = {repr("\x00"): "\\0", repr("\n"): "\\n", repr("\t"): "\\t"}
        formatted_output = ""

        if section == "stack":
            memory = program.memory.ram["stack"]
        elif section == "heap":
            memory = program.memory.ram["heap"]
        elif section == "data":
            memory = program.memory.ram["data"]

        if section == "stack":
            virtual_add = memory["start"] - 1
            end = program.registers["lowest_stack"] + 1
        else:
            virtual_add = memory["stops"] - 2
            end = memory["start"]

        while virtual_add >= end:
            formatted_output += hex(virtual_add - 3) + "\t\t"

            for j in range(4):
                if virtual_add - j >= end:
                    formatted_output += program.memory.read08(virtual_add - j).hex().upper() + "\t"
                else:
                    formatted_output += (4 - j) * "\t"
                    break

            formatted_output += "\t"

            if rep_int:
                formatted_output += str(int.from_bytes(program.memory.read32(virtual_add - 3), byteorder="little")) + "\t"
            elif rep_float:
                byte_array = bytearray()
                for j in range(4):
                    if virtual_add - j >= end:
                        byte_array.insert(j, int.from_bytes(program.memory.read08(virtual_add - j), byteorder="little"))
                    else:
                        byte_array.insert(j, 0)
                formatted_output += str(unpack("<f", byte_array)[0]) + "\t"
            else:
                for j in range(4):
                    if virtual_add - j >= end:
                        try:
                            s = program.memory.read08(virtual_add - j).decode("utf-8")
                            formatted_output += ((escape_dict[repr(s)] if repr(s) in escape_dict else b"\x00".decode("utf-8")) if "\\" in repr(s) else s) + "\t"
                        except UnicodeDecodeError:
                            formatted_output += b"\x00".decode("utf-8") + "\t"
                    else:
                        formatted_output += (4 - j) * "\t"
                        break

            virtual_add -= 4
            if virtual_add < program.registers["$sp"] and section == "stack":
                formatted_output += "<--"

            formatted_output += "\n"

        return formatted_output

    program = preprocess(args.FILE)
    if args.s:
        print("Stack:")
        print()
        print(f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}")
        print("-" * (49))

        memory = format_output(program, "stack", args.i, args.f)

        print(memory, end="")
    if args.h:
        print("Heap:")
        print()
        print(f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}")
        print("-" * (49))

        memory = format_output(program, "heap", args.i, args.f)

        print(memory, end="")
    if args.d:
        print("Data:")
        print()
        print(f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}")
        print("-" * (49))

        memory = format_output(program, "data", args.i, args.f)

        print(memory, end="")
    return 0
