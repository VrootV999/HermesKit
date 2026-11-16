from io import BufferedReader
import lief
from Core.binaryprocessing import filetypeanalyser, process_binary
from Core.constants import ImproperArguement, ParseError, UnknownBinary

def enc1():
    print("")
def enc2():
    print("")

def ResourceHider(payload: str,
                  binary: str,
                  newbin: str,
                  encrypt: bool=False,
                  enclvl: int=0,
                  ):
    print("Hiding Payload in the binary")
    # load payload
    payload1 = process_binary(payload,True)
    if payload is None:
        raise ParseError(payload)

    if enclvl > 2:
        raise ImproperArguement("Improper Encryption Value Provided","Between 0-2", str(enclvl) )

    # load target
    target = process_binary(binary)
    if target is None:
        raise ParseError(binary)

    # get the resource
    # use rsrc if its PE
    if filetypeanalyser(binary) == "PE":
        # read the resourcs available
        rsrc = target.resources
        print(rsrc)
        # Encrypt the payload if its mentioned based on its level
        if encrypt:
            if enclvl == 1:
                enc1()
            elif enclvl == 2:
                enc2()
            # add the payload in the rsrc
            # call the assembly code generator
            # add the assembly code for loading the payload
        # Done without Encryption
        else:
            # add the payload in the rsrc
            # call the assembly code generator
            # add the assembly code for loading the payload
        # save the binary in different location
    # For MACHO and and ELF
    else: 
        print("")
        # check if the target binary already uses this tactic
        # create a custom section
        # add the payload to the binary
        # call the assembly code generator
        # add the assembly code for loading the payload
        # save the binary in different location


ResourceHider("test","sigcheck.exe","test2")
