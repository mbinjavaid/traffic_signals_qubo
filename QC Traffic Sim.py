from main import Main
import tkinter
# from tkinter import ttk
import sys
import threading

def Run():

    token = str(api_entry.get())

    annealing_time = int(anneal_entry.get())

    tkinter.Label(window, text="Simulation Running . . . . . . Please wait. Feel free to minimize this window and check back later.").grid(row=5)
    tkinter.Label(window, text="If any error message appears in the Command Prompt window, please note the error for us and close this program.").grid(row=6)

    Main(token, annealing_time)

    tkinter.Label(window, text="Simulation Successfully Completed! Please email us the Output folder "
                                 "generated inside the program folder. Thank you!").grid(row=7)
    window.quit()



def on_closing():
    # print("wowoow")
    sys.exit()


def button_press():

    thread = threading.Thread(target=Run)

    # make test_loop terminate when the user exits the window
    thread.daemon = True

    thread.start()

window = tkinter.Tk()

window.geometry("800x200")

window.resizable(False, False)

window.title("Traffic Flow Simulation for D-Wave's QC")

window.protocol("WM_DELETE_WINDOW", on_closing)


tkinter.Label(window, text = "D-Wave API token: ").grid(row = 0)
api_entry = tkinter.Entry(window, width = 30)
api_entry.grid(row = 0, column = 1)

anneal_entry = tkinter.Entry(window, width = 30)
anneal_entry.grid(row = 1, column = 1)

tkinter.Label(window, text = "Enter anneal time (20, 30, 40, 50, 60, .....)").grid(row=1)
tkinter.Label(window, text = "After clicking Run, please wait for the simulation to run its course (it may take a while).").grid(row=2)
tkinter.Label(window, text = "Please do not close this window before the simulation completes.").grid(row=3)
tkinter.Label(window, text = "When the simulation is complete, please email us the OUTPUT folder generated in the program folder. Thank you!").grid(row=4)


button = tkinter.Button(window, text="Run!", command=button_press, width=20).grid(row=2, column=1)


window.mainloop()