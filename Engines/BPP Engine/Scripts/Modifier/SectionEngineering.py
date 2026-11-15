from io import BufferedWriter
import lief
import random
from Core.binaryprocessing import ProcessBinary
from Core.constants import SECTIONS, SAFE_SECTIONS, SUPPORTED, macho_segments, macho_sections

def mask_sections(
    binary: lief.PE.Binary | lief.ELF.Binary | lief.MachO.Binary | BufferedWriter,
    location: str,
    target: str | None = None,
    new: str | None = None,
    evth: bool | None = False
):
    if not evth:
        if target is not None:
            print(f"Target {target}")
            if not binary.has_section(target):
                print("No Target detected")
            section = binary.get_section(target)
            if section is None:
                print(f"Invalid Section {target}")
            else:
                if new is not None:
                    print(f"Masking Section {target} to {new}")
                    section.name = new
                else:
                    name = random.choice(list(random.choice(SAFE_SECTIONS)))
                    print(f"Masking {target} to {name}")
                    section.name =  name
        else:
            print("Masking Section Name")
            for section in binary.sections:
                if section.name in SECTIONS:
                    print(f"Maskable Section Detected: {section.name} @ {section.virtual_address}")
                    random_name = random.choice(list(random.choice(SAFE_SECTIONS)))
                    section.name = random_name
                    print(f"Masked it with: {random_name}")
    else:
        for section in binary.sections:
            section.name = random.choice(list(random.choice(SAFE_SECTIONS)))
    binary.write(location)
    print(f"saved as {location}")
    return 

def custom_section(
        binary: lief.PE.Binary | lief.MachO.Binary | lief.ELF.Binary,
        location: str | None,
        name: str | None,
        data: bytearray | None,
):
    bin_type = str(type(binary))[8:-2]
    for binaries in SUPPORTED.values():
        if bin_type in binaries:
            print("Adding Custom Sections")
            item = binaries[0].split(".")[-2]
            section_name = name if name is not None else random.choice(list(random.choice(SAFE_SECTIONS)))
            custom = getattr(lief,item).Section(name)
            custom.content = data if data is not None else [0xCC] * 0x100
        else: 
            continue
    if bin_type.split(".")[-2] == "ELF":
        binary.add(custom,loaded=True)
    else:
        binary.add_section(custom)
    binary.write(location)

def binary_bloater(
    # binary: lief.PE.Binary | lief.MachO.Binary | lief.ELF.Binary,
    binary: str,
    location: str,
    size: int | None,
):
    try:
        print("Bloating Binary")
        b = ProcessBinary(binary).process_binary()
        with open(location,"wb") as f:
            if size is not None:
                f.write(b.read() + urandom(size * 1024 * 1024))
            else:
                f.write(b.read() + urandom(12 * 1024 * 1024))
    finally:
        b.close()
