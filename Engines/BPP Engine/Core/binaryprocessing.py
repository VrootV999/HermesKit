import lief

def filetypeanalyser(file: str) -> str:
    try: 
        header = ""
        with open(file,"rb") as file:
            header = str(file.read(5).hex().upper())
        print(header[8:11])
        if header[:8] == "7F454C46":
            return "ELF"
        elif header[:4] == "4D5A":
            return "PE"
        elif header[:8] in ["FEEDFACE", "CEFAEDFE", "FEEDFACF", "CFFAEDFE", "CAFEBABE"]:
            if header[8:10] == "07":
                return "MACHOx86"
            elif header[8:10] == "0C":
                return "MACHOarmv8"
        else: 
            print("Not a Supported File type")
            return ""
    except FileNotFoundError: 
        print("This File does not exist")
        return ""
    except IsADirectoryError:
        print("Input provided is a Directory not a file")
        return ""

def process_binary(file: str):
    try:
        binary_type = filetypeanalyser(file)
        if binary_type in ["MACHOx86","MACHOarmv8"]:
            config = lief.MachO.ParserConfig()
            config.parse_dyld_bindings = False
            config.parse_dyld_exports = False
            config.parse_dyld_rebases = False
            binary = lief.MachO.parse(file,config)
        else:
            binary = lief.parse(file)
        if isinstance(binary, lief.MachO.FatBinary):
            binary = binary.at(0)
        for section in binary.sections:
            print(section.name)
        return binary
    except FileNotFoundError:
        print("This File does not exist")
    except IsADirectoryError:
        print("Input provided is a Directory not a file")

