import re


SUPPORTED = {
        "PE": ["lief._lief.PE.Binary","lief.PE.Binary"],
        "ELF": ["lief._lief.ELF.Binary","lief.ELF.Binary"],
        "MachO": ["lief._lief.MachO.Binary","lief.MachO.Binary"]
}
SECTIONS = [
        ["UPX0","UPX1","UPX2"],
        ["MPRESS1","MPRESS2"],
        ["ASPack",".themida","Themida"],
]
SAFE_SECTIONS = [
    {
        ".text": "CNT_CODE,MEM_EXECUTE,MEM_READ",
        ".data": "CNT_INITIALIZED_DATA,MEM_READ,MEM_WRITE",
        ".rdata": "CNT_INITIALIZED_DATA,MEM_READ",
        ".bss": "CNT_UNINITIALIZED_DATA,MEM_READ,MEM_WRITE",
        ".rsrc": "CNT_INITIALIZED_DATA,MEM_READ",
        ".reloc": "CNT_INITIALIZED_DATA,MEM_READ",
        ".idata": "CNT_INITIALIZED_DATA,MEM_READ",
        ".edata": "CNT_INITIALIZED_DATA,MEM_READ",
        ".tls": "CNT_INITIALIZED_DATA,MEM_READ,MEM_WRITE",
        ".pdata": "CNT_INITIALIZED_DATA,MEM_READ"
    },
    {
        ".typelink": "CNT_INITIALIZED_DATA,MEM_READ",
        ".itablink": "CNT_INITIALIZED_DATA,MEM_READ",
        ".go.buildinfo": "CNT_INITIALIZED_DATA,MEM_READ",
        "CODE": "CNT_CODE,MEM_EXECUTE,MEM_READ",
        "DATA": "CNT_INITIALIZED_DATA,MEM_READ,MEM_WRITE",
        "BSS": "CNT_UNINITIALIZED_DATA,MEM_READ,MEM_WRITE"
    }
]
macho_segments = {"__TEXT","__DATA","__DATA_CONST","__LINKEDIT","__OBJC","__AUTH","__AUTH_CONST","__PAGEZERO","__DWARF", "__LLVM","__RESTRICT","__INFO_FILTER","__CTF","__UNICODE",}

macho_sections = {"__text","__stubs","__stub_helper","__cstring","__const","__data","__bss","__common","__literal4","__literal8","__literal16","__objc_classlist","__objc_catlist","__objc_methname","__objc_methtype","__objc_selrefs","__objc_classrefs","__objc_const","__objc_data","__cfstring","__mod_init_func","__mod_term_func","__unwind_info","__eh_frame","__got","__la_symbol_ptr","__nl_symbol_ptr","__compact_unwind",}

class BinaryErrors(Exception):
    pass

class UnknownBinary(BinaryErrors):
    """Raised if the Binary format is not supported."""
    def __init__(self, message: str, bname: str, btype: str) -> None:
        self.message = message
        self.bname = bname.replace("\\", "/").split("/")[-1]
        self.btype = btype
        super().__init__(message)
    def __str__(self):
        return f"{self.message} {self.bname}:{self.btype}"

class NoSuitableSection(BinaryErrors):
    """Raised if there's no Suitable Sections available in the binary"""
    def __init__(self, message, bname, btype) -> None:
        self.message = message
        self.bname = bname
        self.btype = btype
        super().__init__(message)
    def __str__(self):
        return f"{self.message} {self.bname}:{self.btype}"

class ParseError(BinaryErrors):
    """Raised if a File can't be parsed"""
    def __init__(self,binary: str):
        self.bname = binary
        super().__init__(binary)
    def __str__(self):
        return f"Unable to parse {self.bname}"

class ImproperArguement(BinaryErrors):
    """Raised if Improper argument is provided"""
    def __init__(self,context: str,req: str,val: str) -> None:
        self.context = context
        self.req = req
        self.val = val
        super().__init__(context)
    def __str__(self):
        return f"{self.context} Required Value:{self.req} Recieved:{self.val}"
