class VMError(Exception):
    """Base voicemeeterlib exception class."""


class VMCAPIError(VMError):
    """Exception raised when the C-API returns an error code"""

    def __init__(self, fn_name, code):
        self.fn_name = fn_name
        self.code = code
        super().__init__(f"{self.fn_name} returned {self.code}")
