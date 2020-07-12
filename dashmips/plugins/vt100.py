"""VT100 Simulator using MMIO."""
try:
    import tkinter as tk
except ImportError:
    # We expect the user to know they have a version of python without tkinter
    pass  # So we do nothing
from typing import Any

from . import Plugin

VGA_COLORS = {
    0b0000: "black",
    0b0001: "blue",
    0b0010: "green",
    0b0011: "cyan",
    0b0100: "red",
    0b0101: "magenta",
    0b0110: "brown",
    0b0111: "gray",
    0b1000: "Dark Gray",
    0b1001: "Blue",
    0b1010: "Green",
    0b1011: "Cyan",
    0b1100: "Red",
    0b1101: "Magenta",
    0b1110: "Yellow",
    0b1111: "White",
}

TAGS = {f"{c1}_{c2}": {"bg": c1.lower(), "fg": c2.lower()} for c1 in VGA_COLORS.values() for c2 in VGA_COLORS.values()}


class VT100(Plugin):
    """VT100 GUI MMIO Simulator."""

    # ANSI Escape Sequences
    # https://www.csie.ntu.edu.tw/~r92094/c++/VT100.html
    # VGA Color Bytes
    # http://wiki.osdev.org/Text_UI#Colours

    # 80 Columns by 25 Rows represented by 2 bytes each
    HEIGHT = 25
    WIDTH = 80
    SIZE = (80 * 25) * 2
    BASE_ADDR = 0x2060  # 8288

    def __init__(self):
        """Construct VT100."""
        super(VT100, self).__init__(name="VT100")
        self.root = tk.Tk()
        self.root.title("VT100")

        self.content = tk.Variable(self.root, b"", "content")
        self.content.trace_add("write", self.pull)

        self.quit_request = tk.BooleanVar(self.root, False, "quit_request")
        self.quit_request.trace_add("write", self.close)

        self.vt = tk.Text(self.root, state="disabled", width=80, height=25)
        self.vt.configure({"fg": "white", "bg": "black", "font": ("Courier", 12, "normal")})
        self.vt.pack()

        self.add_tags()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.screen: bytes = b"\x0F " * VT100.SIZE

    def start(self):
        """Run simulator FUNCTION BLOCKS."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass

    def add_tags(self):
        """Add Color Tags to vt widget."""
        bold = ("Courier", 12, "bold")
        normal = ("Courier", 12, "normal")
        for tagname, color in TAGS.items():
            self.vt.tag_configure(
                tagname, foreground=color["fg"], background=color["bg"], font=(bold if any(c.isupper() for c in tagname) else normal),
            )

    @staticmethod
    def get_tagname(num: int) -> str:
        """Get Tag name based on vga byte."""
        bgcolor = VGA_COLORS[(num & 0b1111_0000) >> 4]
        fgcolor = VGA_COLORS[(num & 0b0000_1111) >> 0]
        return f"{bgcolor}_{fgcolor}"

    @staticmethod
    def get_index(idx: int) -> str:
        """From index into byte array return tk.Text position string."""
        return f"{(idx // VT100.WIDTH) + 1}.{idx % VT100.WIDTH}"

    def close(self, *a: Any):
        """Close the VT100 Window."""
        self.root.quit()

    def request_close(self):
        """Request to close the VT100 Window."""
        self.quit_request.set(True)

    def pull(self, *changes: Any):
        """Pull Updated Screen."""
        vga_memory: bytes = self.content.get()

        if not len(vga_memory) % 2 == 0 or not len(vga_memory) <= VT100.SIZE:
            # Sequence incomplete
            return

        self.vt["state"] = "normal"
        self.vt.delete("1.0", tk.END)
        vga = zip(vga_memory[::2], vga_memory[1::2].decode("ascii"))
        for i, (color, char) in enumerate(vga):
            tag = VT100.get_tagname(color)
            pos = VT100.get_index(i)
            self.vt.insert(pos, char, (tag))

        self.vt["state"] = "disabled"

    def push(self, memory: bytearray):
        """Push a new memory text layout."""
        mmio = bytes(memory[VT100.BASE_ADDR : VT100.BASE_ADDR + VT100.SIZE])
        if mmio == self.screen:
            return
        self.content.set(mmio)
