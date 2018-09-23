"""Syscall Class."""


class Syscall:
    """Syscall Class, callable."""

    def __init__(self, function, number):
        """Create Syscall."""
        self.function = function
        self.name = self.function.__name__
        self.number = number

    def __call__(self, program):
        """Callable Instruction."""
        return self.function(program)

    def __repr__(self):
        """Return Representation string."""
        return f"Syscall({self.number}, {self.name})"
