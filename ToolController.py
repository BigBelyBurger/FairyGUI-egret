import pyvisa
import numpy as np
import time

#############################################################################################################
#                                                                                                           #
#                    FUNCTION TO CHECK IF THE INSTRUMENT IS WORKING                                         #
#                                                                                                           #
#############################################################################################################

def DeviceChecker(IP, PORT=None, SOCKET=None):
	try:
		rm = pyvisa.ResourceManager("@py")
		if SOCKET == "5025" or SOCKET == "7777":
			inst = rm.open_resource(f"TCPIP0::{IP}::{SOCKET}::SOCKET")
			inst.read_termination = '\n'
			inst.write_termination = '\n'
			inst.timeout = 5000  # ms
		else:
			inst = rm.open_resource(f'TCPIP::{IP}::INSTR')
		inst.read_termination = '\n'
		inst.write_termination = '\n'
		inst.timeout = 5000
		inst.write("*CLS")
		answer = inst.query("*IDN?")
		return answer, inst
	except Exception as e: return e, e
	
def writer(inst, command):
	inst.write(command)

def query(inst, command):
	answer = inst.query(command)
	return answer

def reader(inst):
	answer = inst.read()
	return answer

def Write_And_Check(wc, rc, inst, value):
    writer(inst, wc)
    time.sleep(0.01)
    response = query(inst, rc)
    error = query(inst, "SYST:ERR?")
    try:
        if float(response) == float(value):
            return True, error
        else:
            return False, error
    except:
        if response == value:
            return True, error
        else:
            return False, error

def Query_And_Check(qc, inst):
    response = query(inst, qc)
    error = query(inst, "SYST:ERR?")
    return response, error

def Obliviate(inst):
    writer(inst, "*CLS")

def Save_Location_Changed(save_location_var, Entry, EntryText, ErrorEntry, ErrorEntryText):
    Entry.config(style="CodeReplyNormal.TEntry")
    EntryText.set("Save location changed to: " + save_location_var.get())