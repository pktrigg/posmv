import tkinter as tk

LARGE_FONT = ("Verdana", 12)

class SeaofBTCapp(tk.Tk):

	def __init__(self, *args, **kwargs):
		
		tk.Tk.__init__(self, *args, **kwargs)

		
		menu = tk.Menu(self.master)
		self.master.config(menu=menu)
		file = tk.Menu(menu)
		file.add_command(label='Exit', command=self.client_exit)
		menu.add_cascade(label='File', menu=file)


		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight =1)
		container.grid_columnconfigure(0, weight =1)

		self.frames = {}

		frame = StartPage(container, self)

		self.frames[StartPage] = frame

		frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="hellow world", font=LARGE_FONT)
		label.pack(pady=10, padx=10)

app = SeaofBTCapp()
app.mainloop()