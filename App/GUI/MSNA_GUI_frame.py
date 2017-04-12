# GUI frame for the MSNA_PDFscript.py

from Tkinter import *
import tkFileDialog, tkMessageBox
import sys, os
from scipy.io.wavfile import read
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../Scripts/'))
import MSNA_PDFscript

class MSNA_frame:
  
	def __init__(self, parent):  
		 
		self.parent = parent        
		self.initUI()

	def initUI(self):

		choose_label = "Input file (.PDF MSNA):"
		Label(self.parent, text=choose_label).grid(row=0, column=0, sticky=W, padx=5, pady=(10,2))
 
		#TEXTBOX TO PRINT PATH OF THE PDF FILE
		self.filelocation = Entry(self.parent)
		self.filelocation.focus_set()
		self.filelocation["width"] = 25
		self.filelocation.grid(row=1,column=0, sticky=W, padx=10)
		self.filelocation.delete(0, END)
		self.filelocation.insert(0, '../Files/MSNA/')

		#BUTTON TO BROWSE PDF FILE
		self.open_file = Button(self.parent, text="Browse...", command=self.browse_file)
		self.open_file.grid(row=1, column=0, sticky=W, padx=(220, 6)) #put it beside the filelocation textbox
 
		#BUTTON TO PREVIEW PDF FILE
#		self.preview = Button(self.parent, text=">", command=lambda:UF.wavplay(self.filelocation.get()), bg="gray30", fg="white")
#		self.preview.grid(row=1, column=0, sticky=W, padx=(306,6))

		#BUTTON TO COMPUTE EVERYTHING
		self.compute = Button(self.parent, text="Compute", command=self.compute_model, bg="dark red", fg="white")
		self.compute.grid(row=6, column=0, padx=5, pady=(10,15), sticky=W)

		# define options for opening file
		self.file_opt = options = {}
		options['defaultextension'] = '.PDF'
		options['filetypes'] = [('All files', '.*'), ('PDF files', '.PDF')]
		options['initialdir'] = '../Files/MSNA/'
		options['title'] = 'Open a file .PDF for MSNA'
 
	def browse_file(self):
		
		self.filename = tkFileDialog.askopenfilename(**self.file_opt)
 
		#set the text of the self.filelocation
		self.filelocation.delete(0, END)
		self.filelocation.insert(0,self.filename)

	def compute_model(self):
		
		try:
			inputFile = self.filelocation.get()
			
			MSNA_PDFscript.main(inputFile)

		except ValueError as errorMessage:
			tkMessageBox.showerror("Input values error",errorMessage)
			
