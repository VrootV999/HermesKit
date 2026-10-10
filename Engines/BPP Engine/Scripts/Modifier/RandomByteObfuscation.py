from Core.binaryprocessing import process_binary
import lief
from Core.constants import SUPPORTED
import random

def binary_edit(binary: lief.PE.Binary | lief.MachO.Binary | lief.ELF.Binary,location: str):
    try:
        edited = False
        modified_count = 0
        for section in binary.sections:
            content = list(bytearray(section.content))
            if content == []:
                continue
            last_non_zero = -1
            for i in range(len(content) - 1, -1, -1):
                if content[i] != 0:
                    last_non_zero = i
                    break
            slack_start = last_non_zero + 1
            slack_length = len(content) - slack_start
            if slack_length >= 10:
                section_name = section.name.strip()
                print(f"{slack_length} in {section_name}")
                edit_offset = slack_start + random.randint(0,slack_length - 10)
                num_bytes = random.randint(5,10)
                random_bytes = [random.randint(1,255) for _ in range(num_bytes)]
                for idx, val in enumerate(random_bytes):
                    content[edit_offset + idx] = val
                section.content = content
                modified_count += 1
                edited = True
        if edited:
            binary.write(location)
            print(modified_count)
            print(f"Saved at {location}")
        else:
            print("No suitable section found")
    except Exception as e:
        # this is just for now
        print(f"Error {e}")

def random_obfuscate(location: str,outdir: str):
    try:
        binary = process_binary(location)
        if binary is None:
            print("No Binary Provided")
        for binaries in SUPPORTED.values():
            if str(type(binary))[8:-2] in binaries:
                binary_edit(binary,outdir)
        else:
            print("Unknown Binary Detected, Exitting")
    except Exception as e:
        print(f"Unknown Issue {e}")


loc = input("Location of binary: ")
outdir = input("output location: ")
random_obfuscate(loc,outdir)
