import tkinter as tk
from tkinter import ttk
import threading
import time
from datetime import datetime
import numpy as np
import ToolController as UNIC

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def Keithley_bias_graph(ax, ax2, canvas, sense_array, bias_array, time_array):
    ax.clear()
    ax2.clear()
    
    ax.plot(time_array, sense_array, "o", label='Voltage (V)', color='blue')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (V)', color='blue')
    ax.tick_params(axis='y', labelcolor='blue')
    
    ax2.plot(time_array, bias_array, "o", label='Bias Current (A)', color='red')
    ax2.set_ylabel('Bias Current (A)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    ax.grid(True)
    
    ax.set_title('Keithley Bias Graph')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    canvas.draw_idle()


def LS_temp_graph(ax, canvas, time_array, temp_array):
    ax.clear()
    ax.plot(time_array, temp_array, marker='o', color='tab:blue')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Temperature (K)', color='tab:blue')
    ax.tick_params(axis='y', labelcolor='tab:blue')
    ax.grid(True)
    ax.set_title('Lakeshore Channel A Temperature')
    canvas.draw_idle()