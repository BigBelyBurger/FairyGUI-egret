import tkinter as tk
from tkinter import Entry, ttk
import threading
import time
from datetime import datetime
import numpy as np

import ToolController as UNIC
import FAIRY_GRAPHER as FAIRY_G

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

##########################################################################################################################################################################
#
#           FUNCTIONS
#
##########################################################################################################################################################################

#   CREATE A LABEL
def LabelMaker(text, row, column, root, padx, pady):
    label = ttk.Label(root, text=text)
    label.grid(row=row, column=column, padx=padx, pady=pady)
    return label

#   CREATE AN ENTRY
def EntryMaker(text, row, column, root, function, state, padx, pady, columnspan = 1):
    entry = ttk.Entry(root, textvariable=text, state = state)
    entry.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan, sticky="ew")
    entry.bind("<Return>", function)
    return entry

#   CREATE A BUTTON
def ButtonMaker(text, row, column, root, function, style = None):
    button = ttk.Button(root, text=text, command=function, style=style)
    button.grid(row=row, column=column, padx=5, pady=5)
    return button

#   CREATE A COMBOBOX
def ComboMaker(options,text, row, column, root, function, state="readonly"):
    combo = ttk.Combobox(root, textvariable=text, values=options, state=state)
    combo.grid(row=row, column=column, padx=5, pady=5)
    combo.bind("<<ComboboxSelected>>", function)
    return combo

#   CREATE A CHECKBUTTON
def CheckButtonMaker(text, variable, row, column, root, function):
    checkbutton = ttk.Checkbutton(root, text=text, variable=variable, command=function)
    checkbutton.grid(row=row, column=column, padx=5, pady=5)
    return checkbutton

#   CLOSE THE WINDOW
def close_window():
    global inst
    try:
        UNIC.writer(inst, "OUTP OFF")
        inst.close()
    except Exception as e:
        print(e)
    root.destroy()

##########################################################################################################################################################################
#
#           GUI MAKER
#
##########################################################################################################################################################################

root = tk.Tk()
root.title("Instrument / Script Controller")
root.geometry("950x700")
root.geometry("+0+0")

##########################################################################################################################################################################
#
#           VARIABLES
#
##########################################################################################################################################################################

#region

inst = None
TestMode = True

#   IP SETTINGS
IP = tk.StringVar(value = "169.254.88.3")
PORT = tk.StringVar(value = "")
CodeReply = tk.StringVar(value = "")
ErrorReply = tk.StringVar(value = "")

#   SAVE LOCATION
save_location_var = tk.StringVar(value = "/TestData/")
save_file_var = tk.StringVar(value = "RAS_test.txt")

#  KEITHLEY VARIABLES
Keithley_output_var = tk.BooleanVar(value = False)
KeithleyMode_var = tk.StringVar(value = "")
Keithley_biasmode_var = tk.StringVar(value = "Current")
Keithley_bias_var = tk.DoubleVar(value = 0.0)
Keithley_bias_var_BIS = tk.DoubleVar(value = 0.0)
Keithley_compliance_var = tk.DoubleVar(value = 20.0)
Keithley_biasrange_var = tk.DoubleVar(value = 0.0)
Keithley_sense_var = tk.DoubleVar(value = 0.0)
Keithley_senserange_var = tk.DoubleVar(value = 0.0)
Keithley_four_wire_var = tk.BooleanVar(value = False)
Keithley_sense_loop_running_var = tk.BooleanVar(value = False)
Keithley_sense_loop_stop_var = tk.BooleanVar(value = False)

Keithley_start_time = 0.0
Keithley_time_array = np.array([])
Keithley_bias_array = np.array([])
Keithley_sense_array = np.array([])

#   KEITHLEY IV VARIABLES
iv_textfile_var = tk.StringVar(value = "IV_Curve_2.1k_fast")
Keithley_iv_var = tk.BooleanVar(value = False)
Keithley_bias_var_IV = tk.DoubleVar(value = 17e-3)
Keithley_step_var_IV = tk.DoubleVar(value = 1e-4)
Keithley_wait_time_var_IV = tk.DoubleVar(value = 0.01)
Keithley_intermediate_value_var_IV = tk.DoubleVar(value = 0.0)
Keithley_intermediate_step_var_IV = tk.DoubleVar(value = 0.0)
Keithley_IV_single_branch_var = tk.BooleanVar(value = False)

#RAS VARIABLES
ras_bias_voltage_var_A = tk.DoubleVar(value=0.0)
ras_max_current_var_A = tk.DoubleVar(value=0.0)
ras_actual_voltage_var_A = tk.DoubleVar(value=0.0)
ras_actual_current_var_A = tk.DoubleVar(value=0.0)
ras_actual_power_var_A = tk.DoubleVar(value=0.0)
ras_output_state_var_A = tk.BooleanVar(value=False)
ras_start_time_var_A = tk.DoubleVar(value=0.0)
ras_thread_running_var_A = tk.BooleanVar(value=False)
ras_thread_stop_var_A = tk.BooleanVar(value=False)

ras_time_array_A = np.array([])
ras_voltage_array_A = np.array([])
ras_current_array_A = np.array([])

ras_bias_voltage_var_B = tk.DoubleVar(value=0.0)
ras_max_current_var_B = tk.DoubleVar(value=0.0)
ras_actual_voltage_var_B = tk.DoubleVar(value=0.0)
ras_actual_current_var_B = tk.DoubleVar(value=0.0)
ras_actual_power_var_B = tk.DoubleVar(value=0.0)
ras_output_state_var_B = tk.BooleanVar(value=False)
ras_start_time_var_B = tk.DoubleVar(value=0.0)
ras_thread_running_var_B = tk.BooleanVar(value=False)
ras_thread_stop_var_B = tk.BooleanVar(value=False)

ras_time_array_B = np.array([])
ras_voltage_array_B = np.array([])
ras_current_array_B = np.array([])

ras_bias_voltage_var_C = tk.DoubleVar(value=0.0)
ras_max_current_var_C = tk.DoubleVar(value=0.0)
ras_actual_voltage_var_C = tk.DoubleVar(value=0.0)
ras_actual_current_var_C = tk.DoubleVar(value=0.0)
ras_actual_power_var_C = tk.DoubleVar(value=0.0)
ras_output_state_var_C = tk.BooleanVar(value=False)
ras_start_time_var_C = tk.DoubleVar(value=0.0)
ras_thread_running_var_C = tk.BooleanVar(value=False)
ras_thread_stop_var_C = tk.BooleanVar(value=False)

ras_time_array_C = np.array([])
ras_voltage_array_C = np.array([])
ras_current_array_C = np.array([])

#LAKESHORE VARIABLES
LS_curve_number_var = tk.IntVar(value=0)
LS_Curve_Unit_var = tk.StringVar(value="Ohm/K")
LS_Curve_Coefficient_var = tk.StringVar(value="positive")
LS_Curve_location_var = tk.StringVar(value="")
LS_Curve_limit_var = tk.DoubleVar(value=0.0)
LS_Curve_name_var = tk.StringVar(value="")
LS_curve_serialnumber_var = tk.StringVar(value="")
LS_chA_output_var = tk.BooleanVar(value = False)
LS_chB_output_var = tk.BooleanVar(value = False)
LS_chC_output_var = tk.BooleanVar(value = False)
LS_chD_output_var = tk.BooleanVar(value = False)
#endregion

##########################################################################################################################################################################
#
#           NECESSARY FUNCTIONS
#
##########################################################################################################################################################################

#region
def next_higher(array, value):
    higher_values = [x for x in array if x > value]

    if not higher_values:
        return 1

    return min(higher_values)

def next_higher_iv(array, value):
    higher_values = [x for x in array if x > value]

    if not higher_values:
        return None

    return min(higher_values)

def next_lower(array, value):
    lower_values = [x for x in array if x < value]

    if not lower_values:
        return None

    return max(lower_values)

def CheckError(Result, Error, message):
    if Result == False:
            #ERROR
            CodeReply_Entry.config(style="CodeReplyError.TEntry")
            CodeReply.set(message)
            ErrorReply_Entry.config(style="CodeReplyError.TEntry")
            ErrorReply.set(Error)
            UNIC.Obliviate(inst)

def now_to_number():
    return datetime.now().timestamp()
#endregion

##########################################################################################################################################################################
#
#           CONNECTION GUI
#
##########################################################################################################################################################################

#region
# Define styles for Entry widgets
style = ttk.Style()
style.configure("CodeReplyError.TEntry", foreground="red")
style.configure("CodeReplyNormal.TEntry", foreground="black")
style.configure("OutputOff.TButton", foreground="red")
style.configure("OutputOn.TButton", foreground="green")

LabelMaker("IP Address", 10, 10, root, 0, 0)
Ip_Entry = EntryMaker(IP, 11, 10, root, 
                        lambda event: IP_Changed(),
                        state = "normal", 
                        padx=0, pady=0, columnspan = 1)

LabelMaker("Port", 10, 11, root, 0, 0)
Port_Entry = EntryMaker(PORT, 11, 11, root, 
                        lambda event: PORT_Changed(),
                        state = "normal", 
                        padx=0, pady=0, columnspan = 1)

Ip_Button = ButtonMaker("Connect", 11, 12, root, lambda: IP_Connect())

CodeReply_Entry = EntryMaker(CodeReply, 100, 10, root, 
                        lambda event: None,
                        state = "readonly", 
                        padx=0, pady=0, columnspan = 3)

ErrorReply_Entry = EntryMaker(ErrorReply, 101, 10, root,
                        lambda event: None,
                        state = "readonly",
                        padx=0, pady=0, columnspan = 3)

SaveLocation_label = LabelMaker("Save location", 102, 10, root, 0, 0)
SaveLocation_entry = EntryMaker(save_location_var, 103, 10, root,
                        lambda event: Save_Location_Changed(),
                        state = "normal",
                        padx=0, pady=0, columnspan = 3)

SaveFile_label = LabelMaker("Save file name", 104, 10, root, 0, 0)
SaveFile_entry = EntryMaker(save_file_var, 105, 10, root,
                        lambda event: Save_Location_Changed(),
                        state = "normal",
                        padx=0, pady=0, columnspan = 3)
#endregion

##########################################################################################################################################################################
#
#           CONNECTION GUI FUNCTIONS
#
###########################################################################################################################################################################

#region
def IP_Changed():
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("IP changed to: " + str(IP))

def PORT_Changed():
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("PORT changed to: " + str(PORT))

def IP_Connect():
    global inst
    if TestMode == False:
        response, inst = UNIC.DeviceChecker(IP, SOCKET=PORT)
        print(response)
    else: 
        response = "LSCI"
        inst = "lsci"

    if "Incorrect" not in response:
        if TestMode == False:
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Connected to ip: TCPIP0::" + IP + "::" + PORT + "::SOCKET")
        else:
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Test mode: Connected to " + response)
        if "KEITHLEY" in response or "YOKOGAWA" in response:
            frames[0].grid(row=20, column=10, columnspan=2, sticky="ew", padx=10, pady=10)
        elif "LSCI" in response:
            frames[1].grid(row=20, column=10, columnspan=2, sticky="ew", padx=10, pady=10)
        elif "ROHDE" in response:
            frames[2].grid(row=20, column=10, columnspan=2, sticky="ew", padx=10, pady=10)
        elif IP.get() == "169.254.88.31":
            frames[3].grid(row=20, column=10, columnspan=2, sticky="ew", padx=10, pady=10)
    else:
        CodeReply_Entry.config(style="CodeReplyError.TEntry")
        CodeReply.set("Could not connect to : TCPIP0::" + IP + "::" + PORT + "::SOCKET")

def Save_Location_Changed():
    pass

#endregion

##########################################################################################################################################################################
#
#           KEITHLEY
#
###########################################################################################################################################################################

#region
keithley_frame = ttk.LabelFrame(root, text="KEITHLEY 2450 SourceMeter", padding=(10, 10))

ComboMaker(["Continuous Bias", "IV Curve"], KeithleyMode_var, 10, 0, keithley_frame, lambda event: Keithley_Mode_Changed())

#
#           BIAS FRAME
#
keithley_bias_frame = ttk.LabelFrame(keithley_frame, text="Continuous Bias")

#   SWITCH ON/OFF
Keithley_biasoutput_button = ButtonMaker("OFF", 
                                         0, 0, 
                                         keithley_bias_frame, 
                                         lambda: Keithley_Bias_Output_Switch(),
                                         style = "OutputOff.TButton")

#   CHANGE BIAS MODE
LabelMaker("Bias mode", 5, 0, keithley_bias_frame, 0, 0)
Keithley_bias_mode_combo = ComboMaker(["Voltage", "Current"], 
                                      Keithley_biasmode_var, 5, 1, 
                                      keithley_bias_frame, 
                                      lambda event: Keithley_Bias_Mode_Changed())

#   CHANGE BIAS VALUE
LabelMaker("Bias", 10, 0, keithley_bias_frame, 0, 0)
Keithley_bias_entry = EntryMaker(Keithley_bias_var, 
                                10, 1, 
                                keithley_bias_frame, 
                                lambda event: Keithley_Bias_Changed(),
                                state = "normal", 
                                padx=0, pady=0, columnspan = 1)

#   CHANGE COMPLIANCE VALUE
LabelMaker("Compliance (V)", 11, 0, keithley_bias_frame, 0, 0)
Keithley_compliance_entry = EntryMaker(Keithley_compliance_var,
                                        11, 1, 
                                        keithley_bias_frame, 
                                        lambda event: Keithley_Compliance_Changed(),
                                        state = "normal",
                                        padx=0, pady=0, columnspan = 1)

ttk.Separator(keithley_bias_frame, orient='horizontal').grid(row=15, column=0, columnspan=3, sticky="ew", pady=10)

#   BIAS VALUE (READ ONLY)
Bias_value_label = LabelMaker("Bias value", 20, 0, keithley_bias_frame, 0, 0)
Bias_value_entry = EntryMaker(Keithley_bias_var_BIS,
                                20, 1,
                                keithley_bias_frame,
                                lambda event: None,
                                state = "readonly",
                                padx=0, pady=0, columnspan = 1)

#   BIAS RANGE (READ ONLY)
Bias_range_label = LabelMaker("Bias  range", 21, 0, keithley_bias_frame, 0, 0)
Bias_range_entry = EntryMaker(Keithley_biasrange_var,
                                21, 1,
                                keithley_bias_frame,
                                lambda event: None,
                                state = "readonly",
                                padx=0, pady=0, columnspan = 1)

#   SENSE VALUE (READ ONLY)
Sense_value_label = LabelMaker("Sense value", 22, 0, keithley_bias_frame, 0, 0)
Sense_value_entry = EntryMaker(Keithley_sense_var,
                                22, 1,
                                keithley_bias_frame,
                                lambda event: None,
                                state = "readonly",
                                padx=0, pady=0, columnspan = 1)

#   SENSE RANGE (READ ONLY)
Sense_range_label = LabelMaker("Sense range", 23, 0, keithley_bias_frame, 0, 0)
Sense_range_entry = EntryMaker(Keithley_senserange_var,
                                23, 1,
                                keithley_bias_frame,
                                lambda event: None,
                                state = "readonly",
                                padx=0, pady=0, columnspan = 1)

ttk.Separator(keithley_bias_frame, orient='horizontal').grid(row=30, column=0, columnspan=3, sticky="ew", pady=10)

four_wire_label = LabelMaker("Four wire ?", 31, 0, keithley_bias_frame, 0, 0)
four_wire_box = CheckButtonMaker("", Keithley_four_wire_var, 31, 1, 
                                keithley_bias_frame, 
                                lambda: Keithley_FourWire_Changed("None"))

#
#           GRAPH STARTER
#

#           KEITHLEY GRAPH MAKER
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax2 = ax.twinx()
#           MODIFY THE LOOK OF THE GRAPH
#ax.plot(time_array, sense_array, label='Voltage (V)', color='blue')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (V)', color='blue')
ax.tick_params(axis='y', labelcolor='blue')

#ax2.plot(time_array, bias_array, label='Bias Current (A)', color='red')
ax2.set_ylabel('Bias Current (A)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

ax.set_title('Keithley Bias Graph')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

#           CREATE THE CANVAS
canvas = FigureCanvasTkAgg(fig, master=keithley_bias_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=10, columnspan=3, rowspan=100, padx=10, pady=10)

#
#           IV FRAME
#

keithley_iv_frame = ttk.LabelFrame(keithley_frame, text="IV Curve")

IV_output_button = ButtonMaker("Start IV Curve",
                                0, 0,
                                keithley_iv_frame,
                                lambda: Keithley_IV_Curve_Start(),
                                style = "OutputOff.TButton")

IV_textfile_label = LabelMaker("Text file name", 10, 0, keithley_iv_frame, 0, 0)
IV_textfile_entry = EntryMaker(iv_textfile_var, 
                                10, 1,
                                keithley_iv_frame,
                                lambda event: Keithley_IV_Curve_Textfile_Name_Changed(),
                                state = "normal",
                                padx=0, pady=0, columnspan = 1)

IV_max_bias_label = LabelMaker("Max Bias", 11, 0, keithley_iv_frame, 0, 0)
IV_max_bias_entry = EntryMaker(Keithley_bias_var_IV,
                                11, 1,
                                keithley_iv_frame,
                                lambda event: Keithley_IV_Curve_Max_Bias_Changed(),
                                state = "normal",
                                padx=0, pady=0, columnspan = 1)

IV_step_label = LabelMaker("Bias Step", 12, 0, keithley_iv_frame, 0, 0)
IV_step_entry = EntryMaker(Keithley_step_var_IV,
                                12, 1,
                                keithley_iv_frame,
                                lambda event: Keithley_IV_Curve_Step_Changed(),
                                state = "normal",
                                padx=0, pady=0, columnspan = 1)

IV_wait_time_label = LabelMaker("Wait time (s)", 13, 0, keithley_iv_frame, 0, 0)
IV_wait_time_entry = EntryMaker(Keithley_wait_time_var_IV,
                                13, 1,
                                keithley_iv_frame,
                                lambda event: Keithley_IV_Curve_Wait_Time_Changed(),
                                state = "normal",
                                padx=0, pady=0, columnspan = 1)

IV_intermediate_level_label = LabelMaker("Intermediate level", 14, 0, keithley_iv_frame, 0, 0)
IV_intermediate_level_entry = EntryMaker(Keithley_intermediate_value_var_IV,
                                14, 1,
                                keithley_iv_frame,
                                lambda event: Keithley_IV_Curve_Intermediate_Level_Changed(),
                                state = "normal",
                                padx=0, pady=0, columnspan = 1)

IV_intermediate_step_label = LabelMaker("Intermediate step", 15, 0, keithley_iv_frame, 0, 0)
IV_intermediate_step_entry = EntryMaker(Keithley_intermediate_step_var_IV,
                                15, 1,
                                keithley_iv_frame,
                                lambda event: Keithley_IV_Curve_Intermediate_Step_Changed(),
                                state = "normal",
                                padx=0, pady=0, columnspan = 1)

IV_single_branch_check_button = CheckButtonMaker("Single branch?", 
                                Keithley_IV_single_branch_var, 
                                16, 0, 
                                keithley_iv_frame, 
                                lambda: Keithley_IV_Curve_Single_Branch_Changed())

#           IV GRAPH MAKER
iv_fig = Figure(figsize=(3, 2), dpi=100)
iv_ax = iv_fig.add_subplot(111)
#           MODIFY THE LOOK OF THE GRAPH
iv_ax.set_xlabel("Current")
iv_ax.set_ylabel("Voltage")
iv_ax.set_title("Live graph")
#           CREATE THE CANVAS
iv_canvas = FigureCanvasTkAgg(iv_fig, master=keithley_iv_frame)
iv_canvas_widget = iv_canvas.get_tk_widget()
iv_canvas_widget.grid(row=0, column=10, columnspan=3, rowspan=100, padx=10, pady=10)

#endregion

##########################################################################################################################################################################
#
#           KEITHLEY FUNCTIONS CONTINUOUS BIAS
#
###########################################################################################################################################################################

#region
Keithley_Labels = [Bias_value_label, Bias_range_label, Sense_value_label, Sense_range_label]
CurrRangeValues= [ 1e-9, 10e-9, 100e-9, 1e-6, 10e-6, 100e-6, 1e-3, 10e-3, 100e-3, 1]
VoltRangeValues = [0.02, 0.2, 2, 20, 200]

def Keithley_Mode_Changed():
    keithley_bias_frame.grid_forget()
    keithley_iv_frame.grid_forget()

    if KeithleyMode_var.get() == "Continuous Bias":
        keithley_bias_frame.grid(row=20, column=0, columnspan=10, sticky="ew", padx=10, pady=10)
        CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
        CodeReply.set("Mode changed to: " + KeithleyMode_var.get())
    elif KeithleyMode_var.get() == "IV Curve":
        keithley_iv_frame.grid(row=20, column=0, columnspan=10, sticky="ew", padx=10, pady=10)
        CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
        CodeReply.set("Mode changed to: " + KeithleyMode_var.get())

def Keithley_Bias_Output_Switch():
    State = Keithley_output_var.get()
    if State == False:
        Keithley_output_var.set(True)
        if TestMode == False:
            Result, Error = UNIC.Write_And_Check("OUTP ON", "OUTP?", inst, "1")
            if Result == False:
                Keithley_output_var.set(False)
                CheckError(Result, Error, "Failed to turn on output")
                return
        start_read_sense_loop()
        Keithley_biasoutput_button.config(text="ON", style="OutputOn.TButton")
        CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
        CodeReply.set("Output turned ON")
    elif State == True:
        Keithley_output_var.set(False)
        if TestMode == False:
            Result, Error = UNIC.Write_And_Check("OUTP OFF", "OUTP?", inst, "0")
            if Result == False:
                Keithley_output_var.set(True)
                CheckError(Result, Error, "Failed to turn off output")
                return
        stop_read_sense_loop()
        Keithley_biasoutput_button.config(text="OFF", style="OutputOff.TButton")
        CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
        CodeReply.set("Output turned OFF")

def Keithley_Bias_Mode_Changed():
    #Get the correct variables for the mode selected
    BiasMode = Keithley_biasmode_var.get()
    Unit = "V" if BiasMode == "Voltage" else "A"
    UnitOpposit = "A" if BiasMode == "Voltage" else "V"
    if BiasMode == "Voltage":        
        BiasMode = "VOLT"
        SenseMode = "CURR"

    elif BiasMode == "Current":      
        BiasMode = "CURR"
        SenseMode = "VOLT"

    #Modify the mode and check if it is correct, if not return
    if TestMode == False:
        #Modify and check the source mode
        Result, Error = UNIC.Write_And_Check("SOUR:FUNC:MODE " + BiasMode, "SOUR:FUNC:MODE?", inst, BiasMode)
        if Result == False:
            CheckError(Result, Error, "Failed to change bias mode to: " + BiasMode)
            return
        #Modify and check the sense mode
        Result, Error = UNIC.Write_And_Check('SENS:FUNC ' + f'"{SenseMode}"', "SENS:FUNC?", inst, f'"{SenseMode}:DC"')
        if Result == False:
            CheckError(Result, Error, "Failed to change sense mode to: " + SenseMode)
            return
    else:
        Result = True
        Error = "0, No error"

    #Update the GUI
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("Bias mode changed to: " + BiasMode)
    ErrorReply_Entry.config(style="CodeReplyNormal.TEntry")
    ErrorReply.set(Error)
    Keithley_Labels[0].config(text=f"Bias Value ({Unit}):")
    Keithley_Labels[1].config(text=f"Bias Range ({Unit}):")
    Keithley_Labels[2].config(text=SenseMode + f" Value ({UnitOpposit}):")
    Keithley_Labels[3].config(text=SenseMode + f" Range ({UnitOpposit}):")
    #Check and modify the bias and sense range
    if TestMode == False:
        Keithley_biasrange_var.set(UNIC.Query_And_Check("SOUR:" + BiasMode + ":RANG?", inst)[0])
        Keithley_senserange_var.set(UNIC.Query_And_Check("SENS:" + SenseMode + ":RANG?", inst)[0])
    else:
        Keithley_biasrange_var.set(10.0)
        Keithley_senserange_var.set(10.0)

def Keithley_Bias_Changed():
    #Get the correct variables for the mode selected
    BiasMode = Keithley_biasmode_var.get()
    Bias = Keithley_bias_var.get()

    #Set the variables correctly for the mode selected
    if BiasMode == "Voltage":
        BiasMode = "VOLT"
        SenseMode = "CURR"
    elif BiasMode == "Current":
        BiasMode = "CURR"
        SenseMode = "VOLT"

    if TestMode == False:
        #Modify and check the ranges for the bias wanted entered
        if BiasMode == "VOLT":
            Result, Error = UNIC.Write_And_Check(f"SOUR:{BiasMode}:RANG {float(next_higher(VoltRangeValues, abs(1.1*float(Bias))))}", f"SOUR:{BiasMode}:RANG?", inst, float(next_higher(VoltRangeValues, abs(1.1*float(Bias)))))
            if Result == False:
                CheckError(Result, Error, "Failed to change bias range to: " + str(float(next_higher(VoltRangeValues, abs(1.1*float(Bias))))))
                return
        elif BiasMode == "CURR":
            Result, Error = UNIC.Write_And_Check(f"SOUR:{BiasMode}:RANG {float(next_higher(CurrRangeValues, abs(1.1*float(Bias))))}", f"SOUR:{BiasMode}:RANG?", inst, float(next_higher(CurrRangeValues, abs(1.1*float(Bias)))))
            if Result == False:
                CheckError(Result, Error, "Failed to change bias range to: " + str(float(next_higher(CurrRangeValues, abs(1.1*float(Bias))))))
                return
        Keithley_biasrange_var.set(UNIC.Query_And_Check("SOUR:" + BiasMode + ":RANG?", inst)[0])
        Keithley_senserange_var.set(UNIC.Query_And_Check("SENS:" + SenseMode + ":RANG?", inst)[0])

        #Change the basis and check if it is correct
        Result, Error = UNIC.Write_And_Check(f"SOUR:{BiasMode} {Bias}", f"SOUR:{BiasMode}?", inst, Bias)
        if Result == False:
            CheckError(Result, Error, "Failed to change bias to: " + Bias)
            return
    else:
        if BiasMode == "CURR":
            Keithley_biasrange_var.set(float(next_higher(CurrRangeValues, abs(1.1*float(Bias)))))
        else:
            Keithley_biasrange_var.set(float(next_higher(VoltRangeValues, abs(1.1*float(Bias)))))
    #All good if you got here
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("Bias changed to: " + str(Bias))
    ErrorReply_Entry.config(style="CodeReplyNormal.TEntry")
    ErrorReply.set(Error)

def Keithley_Compliance_Changed():
    Compliance = Keithley_compliance_var.get()
    BiasMode = Keithley_biasmode_var.get()
    if BiasMode == "Voltage":
        BiasMode = "VOLT"
        SenseMode = "CURR"
    elif BiasMode == "Current":
        BiasMode = "CURR"
        SenseMode = "VOLT"

    #Modify and check the compliance depending on the bias mode selected
    if TestMode == False:
        if BiasMode == "CURR":
            Result, Error = UNIC.Write_And_Check(f"SOUR:{BiasMode}:VLIM {Compliance}", f"SENS:{BiasMode}:VLIM?", inst, Compliance)
            if Result == False:
                CheckError(Result, Error, "Failed to change compliance to: " + str(Compliance))
                return
            Keithley_compliance_var.set(UNIC.Query_And_Check(f"SENS:{BiasMode}:VLIM?", inst)[0])
        elif BiasMode == "VOLT":
            Result, Error = UNIC.Write_And_Check(f"SOUR:{BiasMode}:ILIM {Compliance}", f"SENS:{BiasMode}:ILIM?", inst, Compliance)
            if Result == False:
                CheckError(Result, Error, "Failed to change compliance to: " + str(Compliance))
                return
            Keithley_compliance_var.set(UNIC.Query_And_Check(f"SENS:{BiasMode}:ILIM?", inst)[0])
    else:
        Result = True
        Error = "0, No error"

    #All good if you got here, Update the GUI
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("Compliance changed to: " + str(Compliance))
    ErrorReply_Entry.config(style="CodeReplyNormal.TEntry")
    ErrorReply.set(Error)

def Keithley_FourWire_Changed(event):
    if TestMode == False:
        if Keithley_four_wire_var.get() == True:
            Result, Error = UNIC.Write_And_Check("SYST:RSEN ON", "SYST:RSEN?", inst, "1")
            if Result == False:
                CheckError(Result, Error, "Failed to turn on four wire sensing")
                return
        else:
            Result, Error = UNIC.Write_And_Check("SYST:RSEN OFF", "SYST:RSEN?", inst, "0")
            if Result == False:
                CheckError(Result, Error, "Failed to turn off four wire sensing")
                return
    else:
        Result = True
        Error = "0, No error"
        
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("Four wire sensing changed to: " + str(Keithley_four_wire_var.get()))
    ErrorReply_Entry.config(style="CodeReplyNormal.TEntry")
    ErrorReply.set(Error)
#endregion

##########################################################################################################################################################################
#
#           KEITHLEY LOOPS CONTINUOUS BIAS
#
###########################################################################################################################################################################

#region
def start_read_sense_loop():
    global Keithley_start_time
    
    if Keithley_sense_loop_running_var.get() == False:
        Keithley_start_time = now_to_number()
        Keithley_sense_loop_stop_var.set(False)
        sense_thread = threading.Thread(target=read_sense_loop)
        sense_thread.start()

def stop_read_sense_loop():
    if Keithley_sense_loop_running_var.get() == True:
        Keithley_sense_loop_stop_var.set(True)
        if TestMode == False:
            Result, Error = UNIC.Write_And_Check("OUTP OFF", "OUTP?", inst, "0")
    print("Loop stopped")


def read_sense_loop():
    global Keithley_time_array
    global Keithley_bias_array
    global Keithley_sense_array

    BiasMode = "CURR" if Keithley_biasmode_var.get() == "Current" else "VOLT"

    Keithley_sense_loop_running_var.set(True)
    Keithley_sense_loop_stop_var.set(False)
    while Keithley_sense_loop_running_var.get():
        if TestMode == False:
            #Read the actual bias value and update the GUI
            if BiasMode == "VOLT":
                SenseMode = "CURR"
            elif BiasMode == "CURR":
                SenseMode = "VOLT"
            sense_value, Error = UNIC.Query_And_Check(f"MEAS?", inst)
            Keithley_sense_var.set(sense_value)
            bias_value, Error = UNIC.Query_And_Check(f"SOUR:{BiasMode}?", inst)
            Keithley_bias_var.set(bias_value)

            #Perform the necessarry checks during the loop and if something is wrong, stop the loop and return
            if Keithley_output_var.get() == False:
                Keithley_sense_loop_running_var.set(False)
                break
            Keithley_biasrange_var.set(UNIC.Query_And_Check("SOUR:" + BiasMode + ":RANG?", inst)[0])
            Keithley_senserange_var.set(UNIC.Query_And_Check("SENS:" + SenseMode + ":RANG?", inst)[0])

            if BiasMode == "VOLT":
                Result, Error = UNIC.Query_And_Check(f"SOUR:{BiasMode}:ILIM:TRIP?", inst)
                if Result == "1":
                    CheckError(False, Error, "Compliance reached")
                    stop_read_sense_loop()
                    break
            elif BiasMode == "CURR":
                Result, Error = UNIC.Query_And_Check(f"SOUR:{BiasMode}:VLIM:TRIP?", inst)
                if Result == "1":
                    CheckError(False, Error, "Compliance reached")
                    stop_read_sense_loop()
                    break
        else:
            #Just for testing
            Keithley_sense_var.set(1.234)
        
        #Check if the loop has stopped during the process
        if Keithley_sense_loop_stop_var.get() == True:
            Keithley_sense_loop_running_var.set(False)
            break

        Keithley_time_var = now_to_number()
        Keithley_time_array = np.append(Keithley_time_array, Keithley_time_var - Keithley_start_time)
        print(Keithley_time_var - Keithley_start_time)
        Keithley_bias_array = np.append(Keithley_bias_array, Keithley_bias_var.get())
        Keithley_sense_array = np.append(Keithley_sense_array, Keithley_sense_var.get())

        FAIRY_G.Keithley_bias_graph(ax, ax2, canvas, Keithley_sense_array, Keithley_bias_array, Keithley_time_array)

        #Update the files
        with open(save_location_var.get() + save_file_var.get(), "a") as f:
            f.write(f"{Keithley_sense_var.get()}, {Keithley_bias_var.get()}, {datetime.now()}\n")
        time.sleep(0.01)
    Keithley_sense_loop_running_var.set(False)
#endregion

##########################################################################################################################################################################
#
#           KEITHLEY FUNCTIONS IV CURVE
#
###########################################################################################################################################################################

#region

def Keithley_IV_Curve_Start():
    pass

def Keithley_IV_Curve_Textfile_Name_Changed():
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("Textfile name changed to: " + str(iv_textfile_var.get()))

def Keithley_IV_Curve_Max_Bias_Changed():
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("Max bias changed to: " + str(Keithley_bias_var_IV.get()))

def Keithley_IV_Curve_Step_Changed():
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("Step changed to: " + str(Keithley_step_var_IV.get()))

def Keithley_IV_Curve_Wait_Time_Changed():
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("Wait time changed to: " + str(Keithley_wait_time_var_IV.get()))

def Keithley_IV_Curve_Intermediate_Level_Changed():
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("Intermediate level changed to: " + str(Keithley_intermediate_value_var_IV.get()))

def Keithley_IV_Curve_Intermediate_Step_Changed():
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("Intermediate step changed to: " + str(Keithley_intermediate_step_var_IV.get()))

def Keithley_IV_Curve_Single_Branch_Changed():
    CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
    CodeReply.set("Single branch changed to: " + str(Keithley_IV_single_branch_var.get()))

#endregion

##########################################################################################################################################################################
#
#           KEITHLEY LOOPS IV CURVE 
#
###########################################################################################################################################################################

#region

#endregion

##########################################################################################################################################################################
#
#           ROHDE AND SCHWARZ
#
###########################################################################################################################################################################

#region
ras_frame = ttk.LabelFrame(root, text="ROHDE AND SCHWARZ", padding=(10, 10))

ras_frame_A = ttk.LabelFrame(ras_frame, text= "Ch A", padding = (10, 10))
ras_frame_A.grid(row=20, column=10, columnspan=2, sticky="ew", padx=10, pady=10)

ras_output_button_A = ButtonMaker("Output OFF", 
                                0, 0, 
                                ras_frame_A, 
                                lambda: ras_output_switch("A"), 
                                style = "OutputOff.TButton")

LabelMaker("Bias voltage", 10, 0, ras_frame_A, 0, 0)
ras_bias_voltage_entry = EntryMaker(ras_bias_voltage_var_A,
                                    10, 1,
                                    ras_frame_A, 
                                    lambda event: ras_bias_voltage_changed("A"),
                                    state = "normal",
                                    padx=0, pady=0)

LabelMaker("Maximum Current", 11, 0, ras_frame_A, 0, 0)
ras_max_current_entry = EntryMaker(ras_max_current_var_A,
                                    11, 1,
                                    ras_frame_A,
                                    lambda event: ras_max_current_changed("A"),
                                    state = "normal",
                                    padx=0, pady=0)

ttk.Separator(ras_frame_A, orient='horizontal').grid(row=15, column=0, columnspan=3, sticky="ew", pady=10)

LabelMaker("Actual Voltage", 20, 0, ras_frame_A, 0, 0)
ras_actual_voltage_entry = EntryMaker(ras_actual_voltage_var_A,
                                    20, 1,
                                    ras_frame_A,
                                    lambda event: None,
                                    state = "readonly",
                                    padx=0, pady=0)

LabelMaker("Actual Current", 21, 0, ras_frame_A, 0, 0)
ras_actual_current_entry = EntryMaker(ras_actual_current_var_A,
                                    21, 1,
                                    ras_frame_A,
                                    lambda event: None,
                                    state = "readonly",
                                    padx=0, pady=0)

LabelMaker("Actual Power", 22, 0, ras_frame_A, 0, 0)
ras_actual_power_entry = EntryMaker(ras_actual_power_var_A,
                                    22, 1,
                                    ras_frame_A,
                                    lambda event: None,
                                    state = "readonly",
                                    padx=0, pady=0)

ras_frame_B = ttk.LabelFrame(ras_frame, text= "Ch B", padding = (10, 10))
ras_frame_B.grid(row=20, column=20, columnspan=2, sticky="ew", padx=10, pady=10)

ras_output_button_B = ButtonMaker("Output OFF", 
                                0, 0, 
                                ras_frame_B, 
                                lambda: ras_output_switch("B"), 
                                style = "OutputOff.TButton")

LabelMaker("Bias voltage", 10, 0, ras_frame_B, 0, 0)
ras_bias_voltage_entry = EntryMaker(ras_bias_voltage_var_B,
                                    10, 1,
                                    ras_frame_B, 
                                    lambda event: ras_bias_voltage_changed("B"),
                                    state = "normal",
                                    padx=0, pady=0)

LabelMaker("Maximum Current", 11, 0, ras_frame_B, 0, 0)
ras_max_current_entry = EntryMaker(ras_max_current_var_B,
                                    11, 1,
                                    ras_frame_B,
                                    lambda event: ras_max_current_changed("B"),
                                    state = "normal",
                                    padx=0, pady=0)

ttk.Separator(ras_frame_B, orient='horizontal').grid(row=15, column=0, columnspan=3, sticky="ew", pady=10)

LabelMaker("Actual Voltage", 20, 0, ras_frame_B, 0, 0)
ras_actual_voltage_entry = EntryMaker(ras_actual_voltage_var_B,
                                    20, 1,
                                    ras_frame_B,
                                    lambda event: None,
                                    state = "readonly",
                                    padx=0, pady=0)

LabelMaker("Actual Current", 21, 0, ras_frame_B, 0, 0)
ras_actual_current_entry = EntryMaker(ras_actual_current_var_B,
                                    21, 1,
                                    ras_frame_B,
                                    lambda event: None,
                                    state = "readonly",
                                    padx=0, pady=0)

LabelMaker("Actual Power", 22, 0, ras_frame_B, 0, 0)
ras_actual_power_entry = EntryMaker(ras_actual_power_var_B,
                                    22, 1,
                                    ras_frame_B,
                                    lambda event: None,
                                    state = "readonly",
                                    padx=0, pady=0)

ras_frame_C = ttk.LabelFrame(ras_frame, text= "Ch C", padding = (10, 10))
ras_frame_C.grid(row=20, column=10, columnspan=2, sticky="ew", padx=10, pady=10)

ras_output_button_C = None

#endregion

##########################################################################################################################################################################
#
#           ROHDE AND SCHWARZ FUNCTIONS
#
###########################################################################################################################################################################

#region
def ras_output_switch(channel):
    if channel == "A":
        num = "1"
    elif channel == "B":
        num = "2"
    elif channel == "C":
        num = "3"

    if channel == "A":
        if ras_output_state_var_A.get() == False:
            ras_output_state_var_A.set(True)
            ras_output_button_A.config(text="Output ON", style="OutputOn.TButton")
            ras_start_read_sense_loop(channel)
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Output turned ON for channel " + channel)
        else:
            ras_output_state_var_A.set(False)
            ras_output_button_A.config(text="Output OFF", style="OutputOff.TButton")
            ras_stop_read_sense_loop(channel)
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Output turned OFF for channel " + channel)
    elif channel == "B":
        if ras_output_state_var_B.get() == False:
            ras_output_state_var_B.set(True)
            ras_output_button_B.config(text="Output ON", style="OutputOn.TButton")
            ras_start_read_sense_loop(channel)
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Output turned ON for channel " + channel)
        else:
            ras_output_state_var_B.set(False)
            ras_output_button_B.config(text="Output OFF", style="OutputOff.TButton")
            ras_stop_read_sense_loop(channel)
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Output turned OFF for channel " + channel)
    elif channel == "C":
        if ras_output_state_var_C.get() == False:
            ras_output_state_var_C.set(True)
            ras_output_button_C.config(text="Output ON", style="OutputOn.TButton")
            ras_start_read_sense_loop(channel)
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Output turned ON for channel " + channel)
        else:
            ras_output_state_var_C.set(False)
            ras_output_button_C.config(text="Output OFF", style="OutputOff.TButton")
            ras_stop_read_sense_loop(channel)
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Output turned OFF for channel " + channel)

def ras_bias_voltage_changed(channel):
    if channel == "A":
        num = "1"
    elif channel == "B":
        num = "2"
    elif channel == "C":
        num = "3"
    #Selects the correct channel to start the next part, should be done each time a commands is sent to the tool
    if TestMode == False:
        UNIC.writer(inst, f"INST OUT{num}")

        if channel == "A":
            response, error = UNIC.Write_And_Check(f"SOUR:VOLT {ras_bias_voltage_var_A.get()}", f"SOUR:VOLT?", inst, ras_bias_voltage_var_A.get())
        elif channel == "B":
            response, error = UNIC.Write_And_Check(f"SOUR:VOLT {ras_bias_voltage_var_B.get()}", f"SOUR:VOLT?", inst, ras_bias_voltage_var_B.get())
        elif channel == "C":
            response, error = UNIC.Write_And_Check(f"SOUR:VOLT {ras_bias_voltage_var_C.get()}", f"SOUR:VOLT?", inst, ras_bias_voltage_var_C.get())
        CheckError(response, error, "Failed to change bias voltage for channel " + channel)
    else:
        response, error = True, "0, No error"

    if response == True:
        if channel == "A":
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Bias voltage for channel " + channel + " changed to: " + str(ras_bias_voltage_var_A.get()))
        elif channel == "B":
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Bias voltage for channel " + channel + " changed to: " + str(ras_bias_voltage_var_B.get()))
        elif channel == "C":
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Bias voltage for channel " + channel + " changed to: " + str(ras_bias_voltage_var_C.get()))
    else:
        CodeReply_Entry.config(style="CodeReplyError.TEntry")
        if channel == "A":
            CodeReply.set("Failed to change bias voltage for channel " + channel + " to: " + str(ras_bias_voltage_var_A.get()))
        elif channel == "B":
            CodeReply.set("Failed to change bias voltage for channel " + channel + " to: " + str(ras_bias_voltage_var_B.get()))
        elif channel == "C":
            CodeReply.set("Failed to change bias voltage for channel " + channel + " to: " + str(ras_bias_voltage_var_C.get()))
        ras_output_state_var_C.set(False)
        UNIC.writer(inst, f"OUTP:GEN 0")

def ras_max_current_changed(channel):
    if channel == "A":
        num = "1"
    elif channel == "B":
        num = "2"
    elif channel == "C":
        num = "3"
    #Selects the correct channel to start the next part, should be done each time a commands is sent to the tool
    if TestMode == False:
        UNIC.writer(inst, f"INST OUT{num}")

        if channel == "A":
            response, error = UNIC.Write_And_Check(f"SOUR:CURR {ras_max_current_var_A.get()}", f"SOUR:CURR?", inst, ras_max_current_var_A.get())
        elif channel == "B":
            response, error = UNIC.Write_And_Check(f"SOUR:CURR {ras_max_current_var_B.get()}", f"SOUR:CURR?", inst, ras_max_current_var_B.get())
        elif channel == "C":
            response, error = UNIC.Write_And_Check(f"SOUR:CURR {ras_max_current_var_C.get()}", f"SOUR:CURR?", inst, ras_max_current_var_C.get())
        CheckError(response, error, "Failed to change max current for channel " + channel)
    else:
        response, error = True, "0, No error"

    if response == True:
        CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
        if channel == "A":
            CodeReply.set("Max current for channel " + channel + " changed to: " + str(ras_max_current_var_A.get()))
        elif channel == "B":
            CodeReply.set("Max current for channel " + channel + " changed to: " + str(ras_max_current_var_B.get()))
        elif channel == "C":
            CodeReply.set("Max current for channel " + channel + " changed to: " + str(ras_max_current_var_C.get()))
    else:
        CodeReply_Entry.config(style="CodeReplyError.TEntry")
        if channel == "A":
            CodeReply.set("Failed to change max current for channel " + channel + " to: " + str(ras_max_current_var_A.get()))
        elif channel == "B":
            CodeReply.set("Failed to change max current for channel " + channel + " to: " + str(ras_max_current_var_B.get()))
        elif channel == "C":
            CodeReply.set("Failed to change max current for channel " + channel + " to: " + str(ras_max_current_var_C.get()))
        ras_output_state_var_A.set(False)
        UNIC.writer(inst, f"OUTP:GEN 0")
#endregion

##########################################################################################################################################################################
#
#           ROHDE AND SCHWARZ LOPPS
#
###########################################################################################################################################################################

#region
def ras_start_read_sense_loop(channel):
    global ras_start_time

    if channel == "A":
        if ras_thread_running_var_A.get() == False:
            ras_thread_running_var_A.set(True)  
            ras_start_time = now_to_number()
            ras_thread_A = threading.Thread(target=ras_read_sense_loop, args=(channel,))
            ras_thread_A.start()
    elif channel == "B":
        if ras_thread_running_var_B.get() == False:
            ras_thread_running_var_B.set(True)  
            ras_start_time = now_to_number()
            ras_thread_B = threading.Thread(target=ras_read_sense_loop, args=(channel,))
            ras_thread_B.start()
    elif channel == "C":
        if ras_thread_running_var_C.get() == False:
            ras_thread_running_var_C.set(True)  
            ras_start_time = now_to_number()
            ras_thread_C = threading.Thread(target=ras_read_sense_loop, args=(channel,))
            ras_thread_C.start()


def ras_stop_read_sense_loop(channel):
    if channel == "A":
        ras_thread_stop_var_A.set(True)
    elif channel == "B":
        ras_thread_stop_var_B.set(True)
    elif channel == "C":
        ras_thread_stop_var_C.set(True)

def ras_read_sense_loop(channel):
    global ras_time_array_A
    global ras_voltage_array_A
    global ras_current_array_A
    global ras_time_array_B
    global ras_voltage_array_B
    global ras_current_array_B
    global ras_time_array_C
    global ras_voltage_array_C
    global ras_current_array_C

    if channel == "A":
        while ras_thread_running_var_A.get():
            if TestMode == False:
                UNIC.writer(inst, "INST OUT1")
                voltage, error = UNIC.Query_And_Check("MEAS:VOLT?", inst)
                current, error = UNIC.Query_And_Check("MEAS:CURR?", inst)
                power, error = UNIC.Query_And_Check("MEAS:POW?", inst)

                ras_actual_voltage_var_A.set(voltage)
                ras_actual_current_var_A.set(current)
                ras_actual_power_var_A.set(power)

                if ras_output_state_var_A.get() == False:
                    ras_thread_running_var_A.set(False)
                    break

            else:
                ras_actual_voltage_var_A.set(1.234)
                ras_actual_current_var_A.set(0.1234)
                ras_actual_power_var_A.set(0.1516)

            if ras_thread_stop_var_A.get() == True:
                ras_thread_running_var_A.set(False)
                ras_thread_stop_var_A.set(False)
                if TestMode == False:
                    response, error = UNIC.writer(inst, "INST OUT1", "OUTP:GEN?")
                    response, error = UNIC.Write_And_Check("OUTP:STATE 0", "OUTP:STATE?", inst, "0")
                break

            ras_time_var = now_to_number()
            ras_time_array_A = np.append(ras_time_array_A, ras_time_var - ras_start_time)
            ras_voltage_array_A = np.append(ras_voltage_array_A, ras_actual_voltage_var_A.get())
            ras_current_array_A = np.append(ras_current_array_A, ras_actual_current_var_A.get())

            #Save the data
            with open(save_location_var.get() + "ChA_" + save_file_var.get(), "a") as f:
                f.write(f"{ras_actual_voltage_var_A.get()}, {ras_actual_current_var_A.get()}, {ras_actual_power_var_A.get()}, {datetime.now()}\n")

            time.sleep(0.01)
        ras_thread_running_var_A.set(False)

#endregion

##########################################################################################################################################################################
#
#           SR400
#
###########################################################################################################################################################################

#region
sr400_frame = ttk.LabelFrame(root, text="SR400 Photon Counter", padding=(10, 10))
#endregion

##########################################################################################################################################################################
#
#           LAKESHORE
#
###########################################################################################################################################################################

#region
lakeshore_frame = ttk.LabelFrame(root, text="LAKESHORE Temperature Controller", padding=(10, 10))

#CRDG tells you the temp reading for a single channel "CRDG? 1" for the first channel, etc...
#CRVDEL to delete a curve
#CRVHDR <curve>,<name>,<SN>,<format>,<limit value>,<coefficient>[term] Edit the header for a curve
#DIOCUR <input> 0 for 10uA bias on the diode
#HTRSET? request the heater status for 1 or 2
#INCRV input curve, sets the curve that input a b c or d will use
#INTYPE <input>,<sensor type>,<autorange>,<range>,<compensation>,<units>, input is 0 or 1 for 2.5V or 10V, 
#   sensor type is 0 for disabled, 1 for diode, 2 for platinum rtd, 3 for ntc rtd, 4 for thermocouple, 5 for capacitance
#   autorange is 0 for off, 1 for on
#   range depends on the actual diode, see manual
#   compensation is 0 for off, 1 for current reversal
#   unit is 1 for K, 2 for C, 3 for Sensor
#OUTMODE 1-4 for heater, 1-4 for channel, power up 0 for off, 1 for on
#PID <output>, <P>, <I>, <D>
#SETP <output>, <setpoint>, sets the actual temp setpoint for the output channel selected

Curve_frame_LS = ttk.LabelFrame(lakeshore_frame, text="Curve handling", padding=(10, 10))
Curve_frame_LS.grid(row=0, column=0, padx=10, pady=10)

LabelMaker("Curve Header parameters", 0, 0, Curve_frame_LS, 0, 0)
LabelMaker("Curve number", 5, 0, Curve_frame_LS, 0, 0)
LS_curve_number_entry = EntryMaker(LS_curve_number_var,
                                    5, 1,
                                    Curve_frame_LS,
                                    lambda event: Curve_Number_Changed(),
                                    state = "normal",
                                    padx=0, pady=0)

LabelMaker("Between 21-59", 5, 2, Curve_frame_LS, 0, 0)

ttk.Separator(Curve_frame_LS, orient='horizontal').grid(row=10, column=0, columnspan=20, sticky="ew", pady=10)

LabelMaker("-- name", 11, 0, Curve_frame_LS, 0, 0)
LS_Curve_name_Entry = EntryMaker(LS_Curve_name_var,
                                 11, 1,
                                 Curve_frame_LS,
                                 lambda event: LS_Curve_name_changed(),
                                 state = "normal",
                                 padx = 0, pady=0)

LabelMaker("-- Serial Number", 12, 0, Curve_frame_LS, 0, 0)
LS_Curve_serialnumber_Entry = EntryMaker(LS_curve_serialnumber_var, 
                                         12, 1,
                                         Curve_frame_LS,
                                         lambda event: LS_Curve_serialnumber_changed(),
                                         state = "normal",
                                         padx = 0, pady = 0)

LabelMaker("-- Unit format", 13, 0, Curve_frame_LS, 0, 0)
LS_Unit_Combobox = ComboMaker(["mV/K", "V/K", "Ohm/K", "log(Ohm)/K"],
                                LS_Curve_Unit_var,
                                13, 1,
                                Curve_frame_LS,
                                lambda event: Changed_LS_Curve_Unit(),
                                state="readonly")

LabelMaker("-- limit", 14, 0, Curve_frame_LS, 0, 0)
LS_Curve_limit_Entry = EntryMaker(LS_Curve_limit_var,
                                  14, 1, 
                                  Curve_frame_LS,
                                  lambda event: LS_Curve_limit_changed(),
                                  state= "normal",
                                  padx = 0, pady = 0)

LabelMaker("-- Coefficient", 15, 0, Curve_frame_LS, 0, 0)
LS_Coefficient_Combobox = ComboMaker(["negative", "positive"],
                                        LS_Curve_Coefficient_var,
                                        15, 1,
                                        Curve_frame_LS,
                                        lambda event: Changed_LS_Curve_Coefficient(),
                                        state="readonly")

ttk.Separator(Curve_frame_LS, orient='horizontal').grid(row=20, column=0, columnspan=20, sticky="ew", pady=10)

LabelMaker("Select a curve to add", 30, 0, Curve_frame_LS, 0, 0)
Curve_location_Entry = EntryMaker(LS_Curve_location_var,
                                  30, 1,
                                  Curve_frame_LS,
                                  lambda event: LS_curve_location_changed(),
                                  state = "normal",
                                  padx=0 , pady=0,
                                  columnspan = 3)

LS_Add_curve_button = ButtonMaker("Add curve",
                                  31, 1,
                                  Curve_frame_LS,
                                  lambda: Add_LS_Curve(),
                                  style="OutputOff.TButton")

LS_Channel_frames = ttk.LabelFrame(lakeshore_frame, text = "Channels", padding = (10, 10))
LS_Channel_frames.grid(row = 10, column = 0, padx = 10, pady = 10)

LabelMaker("Active channels", row = 10, column = 0, root = LS_Channel_frames, padx=0, pady=0)
LS_ChannelA_Switch_Check = CheckButtonMaker("A", LS_chA_output_var,
                                            20, 1,
                                            LS_Channel_frames,
                                            lambda event: LS_Switched_channel_A())

LS_cha = ttk.LabelFrame(lakeshore_frame, text="Channel A", padding=(10, 10))
LS_cha.grid(row=10, column=1, padx=10, pady=10)



LS_chb = ttk.LabelFrame(lakeshore_frame, text="Channel B", padding=(10, 10))
LS_chb.grid(row=10, column=2, padx=10, pady=10)

LS_chc = ttk.LabelFrame(lakeshore_frame, text="Channel C", padding=(10, 10))
LS_chc.grid(row=10, column=3, padx=10, pady=10)

LS_chd = ttk.LabelFrame(lakeshore_frame, text="Channel D", padding=(10, 10))
LS_chd.grid(row=10, column=4, padx=10, pady=10)


#endregion

##########################################################################################################################################################################
#
#           LAKESHORE FUNCTIONS
#
###########################################################################################################################################################################

#region
def Curve_Number_Changed():
    if LS_curve_number_var.get() < 21 or LS_curve_number_var.get() > 59:
        CodeReply_Entry.config(style="CodeReplyError.TEntry")
        CodeReply.set("Curve number must be between 21 and 59")
    else:
        CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
        CodeReply.set("Curve number changed to: " + str(LS_curve_number_var.get()))

        if TestMode == False:
            Result, Error = UNIC.Query_And_Check("CRVHDR?", inst)
            Params = Result.split(",")
        else:
            Params = ["test curve", 1729, "Ohm/K", 300, "positive"]
        #Modify the fields below to fit the header of the curve selected
        LS_Curve_Unit_var.set(Params[2])
        LS_Curve_Coefficient_var .set(Params[4])
        LS_Curve_limit_var.set(Params[3])
        LS_Curve_name_var.set(Params[0])
        LS_curve_serialnumber_var.set(Params[1])

def Changed_LS_Curve_Unit():
    if LS_curve_number_var.get() > 20 and LS_curve_number_var.get() < 60:
        #Modify the header in the tool for the curve selected   
        if TestMode == False:
            Result, Error = UNIC.Write_And_Check(f"CRVHDR {LS_curve_number_var.get()},{LS_Curve_name_var.get()},{LS_curve_serialnumber_var.get()},{LS_Curve_Unit_var.get()},{LS_Curve_limit_var.get()}",
                                "CRVHDR?",
                                inst,
                                f"{LS_Curve_name_var.get()},{LS_curve_serialnumber_var.get()},{LS_Curve_Unit_var.get()},{LS_Curve_limit_var.get()}")
            CheckError(Result, Error, "Failed to change the header correctly, please check the values entered !")
        else:
            Result, Error = True, "0, No error"
        if Result:
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Curve unit changed to: " + str(LS_Curve_Unit_var.get()))
    else:
        CodeReply_Entry.config(style="CodeReplyError.TEntry")
        CodeReply.set("Please selected a curve first")

def LS_Curve_limit_changed():
    if LS_Curve_limit_var.get() < 0 or LS_Curve_limit_var.get() > 1000:
        CodeReply_Entry.config(style="CodeReplyError.TEntry")
        CodeReply.set("Curve limit must be between 0 and 1000 K")
    else:
        if LS_curve_number_var.get() > 20 and LS_curve_number_var.get() < 60:
            #Modify the header in the tool for the curve selected
            if TestMode == False:
                Result, Error = UNIC.Write_And_Check(f"CRVHDR {LS_curve_number_var.get()},{LS_Curve_name_var.get()},{LS_curve_serialnumber_var.get()},{LS_Curve_Unit_var.get()},{LS_Curve_limit_var.get()}",
                                    "CRVHDR?",
                                    inst,
                                    f"{LS_Curve_name_var.get()},{LS_curve_serialnumber_var.get()},{LS_Curve_Unit_var.get()},{LS_Curve_limit_var.get()}")
                CheckError(Result, Error, "Failed to change the header correctly, please check the values entered !")
            else:
                Result, Error = True, "0, No error"
            if Result:
                CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
                CodeReply.set("Change the curve limit to " + str(LS_Curve_limit_var.get()))
        else:
            CodeReply_Entry.config(style="CodeReplyError.TEntry")
            CodeReply.set("Please selected a curve first")

def LS_Curve_name_changed():
    #Modify the header in the tool for the curve selected
    if LS_curve_number_var.get() > 20 and LS_curve_number_var.get() < 60:
        if TestMode == False:
            Result, Error = UNIC.Write_And_Check(f"CRVHDR {LS_curve_number_var.get()},{LS_Curve_name_var.get()},{LS_curve_serialnumber_var.get()},{LS_Curve_Unit_var.get()},{LS_Curve_limit_var.get()}",
                                "CRVHDR?",
                                inst,
                                f"{LS_Curve_name_var.get()},{LS_curve_serialnumber_var.get()},{LS_Curve_Unit_var.get()},{LS_Curve_limit_var.get()}")
            CheckError(Result, Error, "Failed to change the header correctly, please check the values entered !")
        else:
            Result, Error = True, "0, No error"
        if Result:
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Changed the curve name to " + str(LS_Curve_name_var.get()))
    else:
        CodeReply_Entry.config(style="CodeReplyError.TEntry")
        CodeReply.set("Please selected a curve first")

def LS_Curve_serialnumber_changed():
    if LS_curve_number_var.get() > 20 and LS_curve_number_var.get() < 60:
        if TestMode == False:
            Result, Error = UNIC.Write_And_Check(f"CRVHDR {LS_curve_number_var.get()},{LS_Curve_name_var.get()},{LS_curve_serialnumber_var.get()},{LS_Curve_Unit_var.get()},{LS_Curve_limit_var.get()}",
                                "CRVHDR?",
                                inst,
                                f"{LS_Curve_name_var.get()},{LS_curve_serialnumber_var.get()},{LS_Curve_Unit_var.get()},{LS_Curve_limit_var.get()}")
            CheckError(Result, Error, "Failed to change the header correctly, please check the values entered !")
        else:
            Result, Error = True, "0, No error"
        if Result:
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Changed the curve's serial number to " + str(LS_curve_serialnumber_var.get()))
    else:
        CodeReply_Entry.config(style="CodeReplyError.TEntry")
        CodeReply.set("Please selected a curve first")

def Changed_LS_Curve_Coefficient():
    if LS_curve_number_var.get() > 20 and LS_curve_number_var.get() < 60:
        if TestMode == False:
            Result, Error = UNIC.Write_And_Check(f"CRVHDR {LS_curve_number_var.get()},{LS_Curve_name_var.get()},{LS_curve_serialnumber_var.get()},{LS_Curve_Unit_var.get()},{LS_Curve_limit_var.get()}",
                                "CRVHDR?",
                                inst,
                                f"{LS_Curve_name_var.get()},{LS_curve_serialnumber_var.get()},{LS_Curve_Unit_var.get()},{LS_Curve_limit_var.get()}")
            CheckError(Result, Error, "Failed to change the header correctly, please check the values entered !")
        else:
            Result, Error = True, "0, No error"
        if Result:
            CodeReply_Entry.config(style="CodeReplyNormal.TEntry")
            CodeReply.set("Changed the curve's coefficient to " + str(LS_Curve_Coefficient_var.get()))
    else:
        CodeReply_Entry.config(style="CodeReplyError.TEntry")
        CodeReply.set("Please selected a curve first")

def Add_LS_Curve():
    #Should delete the curvefirst before actually creating it just in case something fucks up
    #Should also use the parameters above for the headers, even if they aren't correct, at least it's something
    #And maybe use a random value or standard value for the first time that is then changed by the user
    pass

def LS_curve_location_changed():
    #please check here if the file actually exists and if it is what the code expects to add it right after or not
    pass

def LS_Switched_channel_A():
    pass

#endregion

##########################################################################################################################################################################
#
#           CODE END
#
###########################################################################################################################################################################

frames = [keithley_frame, lakeshore_frame, ras_frame, sr400_frame]

root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()