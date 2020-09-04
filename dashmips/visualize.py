"""Memory visualizer."""
from .models import MipsProgram
from .preprocessor import preprocess
from .utils import MipsException
from struct import unpack


def visualize_memory(args):
    """Visualize the stack, heap, data of mips program."""

    def format_output(program: MipsProgram, section: str, rep_ascii: bool, rep_int: bool, rep_float: bool) -> str:
        """Create the list to be visualized."""
        escape_dict = {repr("\x00"): "\\0", repr("\n"): "\\n", repr("\t"): "\\t"}
        formatted_output = ""
        ptr = "<-- $sp/$fp" if (program.registers["$sp"] // 4) == (program.registers["$fp"] // 4) else "<-- $sp"
        added_fp = True if (program.registers["$sp"] // 4) == (program.registers["$fp"] // 4) else False
        added_sp = False

        if section == "stack":
            virtual_add = program.memory.ram["stack"]["start"] - 1
            end = program.registers["lowest_stack"]
        elif section == "heap":
            start = program.registers["end_heap"] - 1
            virtual_add = ((program.registers["end_heap"] // 4) * 4) + (0 if program.registers["end_heap"] % 4 == 0 else 4) - 1
            end = program.memory.ram["heap"]["start"]
        elif section == "data":
            virtual_add = program.memory.ram["data"]["stops"] - 1 - ((program.memory.ram["data"]["stops"]) % 4)
            end = program.memory.ram["data"]["start"]

        while virtual_add >= end:
            formatted_output += hex(virtual_add - 3) + "\t\t"

            for j in range(4):
                if section == "heap" and virtual_add - j > start:
                    formatted_output += "\t"
                elif virtual_add - j >= end:
                    formatted_output += program.memory.read08(virtual_add - j).hex().upper() + "\t"
                else:
                    formatted_output += (4 - j) * "\t"
                    break

            formatted_output += "\t"

            if rep_int:  # Int
                formatted_output += str(int.from_bytes(program.memory.read32(virtual_add - 3), byteorder="little")) + "\t"
            elif rep_float:  # Float
                byte_array = bytearray()
                for j in range(4):
                    if virtual_add - j >= end:
                        byte_array.insert(j, int.from_bytes(program.memory.read08(virtual_add - j), byteorder="little"))
                    else:
                        byte_array.insert(j, 0)
                formatted_output += str(unpack("<f", byte_array)[0]) + "\t"
            elif rep_ascii:  # Ascii
                for j in range(4):
                    if section == "heap" and virtual_add - j > start:
                        formatted_output += "\t"
                    elif virtual_add - j >= end:
                        try:
                            s = program.memory.read08(virtual_add - j).decode("utf-8")
                            formatted_output += ((escape_dict[repr(s)] if repr(s) in escape_dict else b"\x00".decode("utf-8")) if "\\" in repr(s) else s) + "\t"
                        except UnicodeDecodeError:
                            formatted_output += b"\x00".decode("utf-8") + "\t"
                    else:
                        formatted_output += (4 - j) * "\t"
                        break

            virtual_add -= 4

            # Add pointers for the stack
            if not added_sp and virtual_add - 1 < program.registers["$sp"] and section == "stack":
                formatted_output += ptr
                added_sp = True
            if not added_fp and virtual_add - 1 < program.registers["$fp"] and section == "stack":
                formatted_output += "<-- $fp"
                added_fp = True

            formatted_output += "\n"

        return formatted_output

    program = preprocess(args.FILE) if args.FILE else args.program
    message = " at assemble time" if args.FILE else " at runtime"
    header = f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}\n" + ("-" * 50) + "\n"

    output = ""

    if args.sa:
        output += "Stack" + message + "\n\n" + header

        output += format_output(program, "stack", True, False, False)
    output += "&&&& "
    if args.si:
        output += "Stack" + message + "\n\n" + header

        output += format_output(program, "stack", False, True, False)
    output += "&&&& "
    if args.sf:
        output += "Stack" + message + "\n\n" + header

        output += format_output(program, "stack", False, False, True)
    output += "&&&& "
    if args.ha:
        output += "Heap" + message + "\n\n" + header

        output += format_output(program, "heap", True, False, False)
    output += "&&&& "
    if args.hi:
        output += "Heap" + message + "\n\n" + header

        output += format_output(program, "heap", False, True, False)
    output += "&&&& "
    if args.hf:
        output += "Heap" + message + "\n\n" + header

        output += format_output(program, "heap", False, False, True)
    output += "&&&& "
    if args.da:
        output += "Data" + message + "\n\n" + header

        output += format_output(program, "data", True, False, False)
    output += "&&&& "
    if args.di:
        output += "Data" + message + "\n\n" + header

        output += format_output(program, "data", False, True, False)
    output += "&&&& "
    if args.df:
        output += "Data" + message + "\n\n" + header

        output += format_output(program, "data", False, False, True)
    output += "&&&& "
    return output
