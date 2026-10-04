import lief

def filetypeanalyser(file: str) -> str:
    try: 
        header = ""
        with open(file,"rb") as file:
            header = str(file.read(5).hex().upper())
        if header[:8] == "7F454C46":
            return "ELF"
        elif header[:4] == "4D5A":
            return "PE"
        elif header[:8] in ["FEEDFACE", "CEFAEDFE", "FEEDFACF", "CFFAEDFE", "CAFEBABE"]:
            return "MACHO"
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
        with open(file,"rb") as f:
            binary = lief.parse(f)
        return binary
    except FileNotFoundError:
        print("This File does not exist")
    except IsADirectoryError:
        print("Input provided is a Directory not a file")
