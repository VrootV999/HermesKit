from io import BufferedWriter
import lief
import random
from Core.binaryprocessing import filetypeanalyser, process_binary
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
    # if not isinstance(binary,BufferedWriter):
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
    
def merge_sections(
        binary: lief.PE.Binary | lief.MachO.Binary | lief.ELF.Binary
):
    print("Merging Various Sections")

def align_sections(
        binary: lief.PE.Binary | lief.MachO.Binary | lief.ELF.Binary
):
    print("Aligning Sections Properly")

def get_imp_data(
        binary: lief.PE.Binary | lief.MachO.Binary | lief.ELF.Binary
):
    print("Getting Required Data from the binary")

def main():
    binary_input = input("File Name: ").strip()
    if not binary_input:
        print("No file given")
        return
    binary = process_binary(binary_input)
    if binary is None:
        return
    # if isinstance(binary, BufferedWriter):


    print("\nOperations:")
    print("  1) mask all sections")
    print("  2) mask a specific section")
    print("  3) add a custom section")
    choice = input("Choice (1/2/3) [1]: ").strip() or "1"

    out_path = input("Output file name [masked.bin]: ").strip() or "masked.bin"

    try:
        if choice == "1":
            mask_sections(binary, out_path,evth=True)
        elif choice == "2":
            target = input("Target section name: ").strip()
            if not target:
                print("Target section required")
                return
            new = input("New name (blank = random): ").strip() or None
            mask_sections(binary, out_path, target=target, new=new)
        elif choice == "3":
            name = input("Custom section name [custom]: ").strip() or "custom"
            data = input("Data (blank = 0xCC * 0x100): ").strip()
            payload = bytearray(data.encode()) if data else None
            custom_section(binary, out_path, name, payload)
        else:
            mask_sections(binary, out_path)
    except Exception as exc:  # keep manual testing alive even when a feature is broken
        import traceback
        print(f"\n[ERROR] {type(exc).__name__}: {exc}")
        traceback.print_exc()
        return

    import os
    if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
        print(f"\n[FAIL] no output written at {out_path}")
        return
    reparsed = lief.parse(out_path)
    if reparsed is None:
        print(f"\n[FAIL] {out_path} exists but refuses to parse")
        return
    same = type(reparsed).__name__ == type(binary).__name__
    print(
        f"\n[OK] {out_path}: {type(reparsed).__name__}, {len(reparsed.sections)} sections, "
        f"same type as input: {same}"
    )
if __name__ == '__main__':
    main()
