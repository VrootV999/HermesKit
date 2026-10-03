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
            return "Not a Supported File type"
    except FileNotFoundError: 
        print("This File does not exist")
        exit(1)

def process_binary(file: str):
    try: 
        with open(file,"rb") as file:
            binary = lief.parse(file)
    except FileNotFoundError as e:
        print("This File does not exist")
        exit(1)


def main():
    try: 
        inputs = input("Give location of file: ")
        file = filetypeanalyser(inputs)
        print(file)
        process_binary(inputs)
    except KeyboardInterrupt:
        print("\nInterrupt Detected Exitting...")
        exit(1)

if __name__ == "__main__":
    main()
