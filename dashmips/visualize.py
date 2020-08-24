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
        added_pointer = False

        if section == "stack":
            memory = program.memory.ram["stack"]
        elif section == "heap":
            memory = program.memory.ram["heap"]
        elif section == "data":
            memory = program.memory.ram["data"]

        if section == "stack":
            virtual_add = memory["start"]
            end = program.registers["lowest_stack"] + 1
        else:
            virtual_add = memory["stops"] - 1 - ((memory["stops"]) % 4)
            end = memory["start"]

        while virtual_add >= end:
            formatted_output += hex(virtual_add - 4) + "\t\t"

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
            elif rep_ascii:
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
            if virtual_add - 1 < program.registers["$sp"] and section == "stack" and not added_pointer:
                formatted_output += "<-- $sp"
                added_pointer = True

            formatted_output += "\n"

        return formatted_output

    if args.FILE:
        try:
            program = preprocess(args.FILE)
        except MipsException as err:
            return f"Error: {args.FILE.name} failed to assemble:\n" + err.message
    else:
        program = args.program

    output = ""

    if args.sa:
        output += "Stack:\n\n" + f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}\n" + ("-" * 50) + "\n"

        output += format_output(program, "stack", True, False, False)
    output += "&&&& "
    if args.si:
        output += "Stack:\n\n" + f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}\n" + ("-" * 50) + "\n"

        output += format_output(program, "stack", False, True, False)
    output += "&&&& "
    if args.sf:
        output += "Stack:\n\n" + f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}\n" + ("-" * 50) + "\n"

        output += format_output(program, "stack", False, False, True)
    output += "&&&& "
    if args.ha:
        output += "Heap:\n\n" + f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}\n" + ("-" * 50) + "\n"

        output += format_output(program, "heap", True, False, False)
    output += "&&&& "
    if args.hi:
        output += "Heap:\n\n" + f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}\n" + ("-" * 50) + "\n"

        output += format_output(program, "heap", False, True, False)
    output += "&&&& "
    if args.hf:
        output += "Heap:\n\n" + f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}\n" + ("-" * 50) + "\n"

        output += format_output(program, "heap", False, False, True)
    output += "&&&& "
    if args.da:
        output += "Data:\n\n" + f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}\n" + ("-" * 50) + "\n"

        output += format_output(program, "data", True, False, False)
    output += "&&&& "
    if args.di:
        output += "Data:\n\n" + f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}\n" + ("-" * 50) + "\n"

        output += format_output(program, "data", False, True, False)
    output += "&&&& "
    if args.df:
        output += "Data:\n\n" + f"{'Address':15} {'03':<3} {'02':<3} {'01':<3} {'00':<7} {'Decoded Text'}\n" + ("-" * 50) + "\n"

        output += format_output(program, "data", False, False, True)
    output += "&&&& "
    return output
