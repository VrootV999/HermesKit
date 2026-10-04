import lief
from Core.binaryprocessing import process_binary

def mask_sections(binary: lief.PE.Binary | lief.MachO.Binary | lief.ELF.Binary):
    print("Masking Section Name")
def custom_section(binary: lief.PE.Binary | lief.MachO.Binary | lief.ELF.Binary):
    print("Adding Custom Sections")
def merge_sections(binary: lief.PE.Binary | lief.MachO.Binary | lief.ELF.Binary):
    print("Merging Various Sections")
def align_sections(binary: lief.PE.Binary | lief.MachO.Binary | lief.ELF.Binary):
    print("Aligning Sections Properly")
def get_imp_data(binary: lief.PE.Binary | lief.MachO.Binary | lief.ELF.Binary):
    print("Getting Required Data from the binary")

def main():
    binary_input = input("File Name: ")
    outdir_input = input("Output file Name: ")
    binary = process_binary(binary_input)
    mask_sections(binary)
    custom_section(binary)
    merge_sections(binary)
if __name__ == '__main__':
    main()

