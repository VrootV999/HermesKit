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

# def process_binary2(file: str):
#     try: 
#         parse_config = lief.PE.ParserConfig()
#         parse_config.parse_signature = False
#         pe = lief.PE.parse(file,parse_config)
#         with open(file,"rb") as f:


def main():
    try: 
        inputs = input("Give location of file: ")
        # file = filetypeanalyser(inputs)
        # print(file)
        process_binary(inputs)
    except KeyboardInterrupt:
        print("\nInterrupt Detected Exitting...")
        exit(1)

if __name__ == "__main__":
    main()
