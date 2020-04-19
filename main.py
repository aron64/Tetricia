from tkinter import *
import socket, sys, threading,time,struct, tkinter.colorchooser, os, getpass
from tkinter import font,filedialog, messagebox
from PIL import Image, ImageTk
import tkinter.ttk as ttk
from gameobjects import *
from chat_gui import *
from opponent import *
class Tetricia(Tk):
	"""The main client application"""
	def __init__(self):
		Tk.__init__(self)
		default_font = font.nametofont("TkDefaultFont")
		default_font.config(family='Comic Sans MS')
		self.screenw=self.winfo_screenwidth()
		self.screenh=self.winfo_screenheight()

		self.protocol("WM_DELETE_WINDOW", self._destroy)
		self.bind("<Escape>", self.esc)
		self.bind("<F11>", self.f11)
		self.chat=ChatGui(self,'aronsv.ddns.net', '64164', socket.gethostname()+'\\'+getpass.getuser())
		self.panel=GameDashboard(self, blocksize=self.screenh/27)
		self.panel.grid(row=0,rowspan=2 ,column=0,sticky="W")
		self.chat.grid(row=2,column=0, sticky="W")
		self.players={}
		self.title("Tetrícia")

		#self.trial_start()

	def esc(self, evt):
		"Escape fullscreen"
		self.attributes('-fullscreen', False)
	def f11(self, evt):
		"Mode fullscreen"
		self.attributes('-fullscreen', True)

	def add_player(self, name):
		"When a new player joins the server, place their dashboard"
		print("NEW:"+name)

		self.players[name]=OpponentDashboard(self,self.screenh/27*0.64)
		curr_in=len(self.players)
		if curr_in>2:
			self.players[name].grid(row=1,column=2-(curr_in%2),sticky="N", rowspan=2)
		else:
			self.players[name].grid(row=0, column=2-(curr_in%2), sticky="N")
		

	def set_player(self, name, msg):
		"Forward the action log to the corresponding panel"
		print(name,msg)
		self.players[name].log(msg)

	def update_server(self, msg):
		"Send the up-to-date information to the server"
		self.panel.netLock.acquire()
		self.ready=False
		msg=chr(0)+msg+"#"+self.chat.data[2].get()+chr(0)
		self.conn.send(bytes(msg,'utf-8'))
		self.panel.netLock.release()

	def set_connection(self, conn):
		"Set the server connection socket"
		self.conn=conn
		self.panel.online=True
		self.attributes('-fullscreen', True)

	def _destroy(self):
		"Destroy event handler"
		self.chat._delete_window()
		self.panel._destroy()
		# for x in self.players:
		# 	self.players[x]._destroy()
		self.after(5000,self.destroy)

	def opponent_control_test(self):
		"test opponent.py"
		self.player2=OpponentDashboard(20)
		self.player2.grid(row=0,column=1,sticky=N)
		self.player2.new_mino(T)
		time.sleep(0.5)
		for y in range(19,0,-1):
			self.player2.set_coords([(4,y),(5,y),(6,y),(5,y+1)])
			time.sleep(0.1)
		self.player2.lock_down()
		self.player2.set_eliminate([0])
		time.sleep(0.5)
		self.player2.set_eliminate([0])
		time.sleep(0.3)
		self.player2.set_eliminate([0])
		self.player2.set_statistics(6464,5,64)
		self.player2.grid_forget()

	def trial_start(self):
		"Quick test for opponent.py game events"
		threading.Thread(target=self.opponent_control_test).start()



if __name__ == '__main__':
	# root=Tk()
	# a=Tetricia(root,1)
	# a.grid()
	# root.mainloop()
	Tetricia().mainloop()