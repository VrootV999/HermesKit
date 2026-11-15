import lief

def filetypeanalyser(file: str) -> str|None:
    checks = {
        "PE": lief.is_pe,
        "ELF": lief.is_elf,
        "MachO": lief.is_macho,
        "ART": lief.is_art,
        "DEX": lief.is_dex,
        "VDEX": lief.is_vdex,
        "OAT": lief.is_oat
    }

    for name, detector in checks.items():
        if detector(file):
            return name
    return None

def process_binary(file: str,specific: bool=False):
    if specific:
        f = open(file,"rb")
        return f
    binary_type = filetypeanalyser(file)
    binary = lief.parse(file)
    if isinstance(binary, lief.MachO.FatBinary):
        binary = binary.at(0)
    for section in binary.sections:
        print(section.name)
    return binary
