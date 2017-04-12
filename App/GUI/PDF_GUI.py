from Tkinter import *
from notebook import *   # window with tabs

from MSNA_GUI_frame import *
from Stanislaus_GUI_frame import *

root = Tk( ) 
root.title('Facility based PDF to CSV converter')
nb = notebook(root, TOP) # make a few diverse frames (panels), each using the NB as 'master': 

# uses the notebook's frame
f1 = Frame(nb( )) 
MSNA = MSNA_frame(f1)

f2 = Frame(nb( )) 
Stanislaus = Stanislaus_frame(f2)


nb.add_screen(f1, "MSNA") 
nb.add_screen(f2, "Stanislaus")

nb.display(f1)

root.geometry('+0+0')
root.mainloop( )
