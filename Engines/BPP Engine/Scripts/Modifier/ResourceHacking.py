from io import BufferedReader
import lief
from Core.binaryprocessing import filetypeanalyser, process_binary
from Core.constants import ParseError, UnknownBinary

def ResourceHider(payload: str,
                  binary: str,
                  newbin: str,
                  encrypt: bool=False,
                  enclvl: int=5,
                  ):
    print("Hiding Payload in the binary")
    # load payload
    payload1 = process_binary(payload,True)
    if payload is None:
        raise ParseError(payload)

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
        # add the payload to the binary
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
