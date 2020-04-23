#########################
# Hertendi Áron Levente #
#                       #
#   #       #        #  #
#   ###    ###     ###  #
#                       #
#       Tetrícia        #
#                       #
#########################
"""
Tetrícia

Some function descriptions are fully or partially taken from the 2009 Tetris Guideline:
https://www.dropbox.com/s/g55gwls0h2muqzn/tetris_guideline_docs_2009.zip?dl=0
https://tetris.fandom.com/wiki/Tetris_Guideline
"""


from tkinter import *
import tkinter.ttk as ttk
from random import shuffle, randrange
import threading, time
from pynput.keyboard import Key, Listener
from chat_gui import *

class I:
	"""I - Tetromino behaviour description"""
	def generate():
		return {'type': I, 'coords': [(x,20) for x in range(3,7)], 'rot': 'N', 'color':'#00ffff', 'name':'I'}
	Defaults={'W':[(4,3),(4,4),(4,5),(4,6)],
			  'N':[(3,5),(4,5),(5,5),(6,5)],
			  'E':[(5,3),(5,4),(5,5),(5,6)],
			  'S':[(3,4),(4,4),(5,4),(6,4)]}
	Points={'W':[(4,5),(4,5),(4,5),(4,3),(4,6)],
			'N':[(4,5),(3,5),(6,5),(3,5),(6,5)],
			'E':[(4,5),(5,5),(5,5),(5,6),(5,3)],
			'S':[(4,5),(6,5),(3,5),(6,4),(3,4)],}

class T:
	"""T - Tetromino behaviour description"""
	def generate():
		return {'type': T, 'coords': [(x,20) for x in range(3,6)]+[(4,21)], 'rot': 'N', 'color':'#800080', 'name':'T'}
	Defaults={'W':[(4,3),(4,4),(4,5),(3,4)],
			  'N':[(3,4),(4,4),(5,4),(4,5)],
			  'E':[(4,5),(4,4),(4,3),(5,4)],
			  'S':[(5,4),(4,4),(3,4),(4,3)]}
	Points={'W':[(4,4),(3,4),(3,3),(4,6),(3,6)],
			'N':[(4,4),(4,4),(4,4),(4,4),(4,4)],
			'E':[(4,4),(5,4),(5,3),(4,6),(5,6)],
			'S':[(4,4),(4,4),(4,4),(4,4),(4,4)]}
class L:
	"""L - Tetromino behaviour description"""
	def generate():
		return {'type': L, 'coords': [(x,20) for x in range(3,6)]+[(5,21)], 'rot': 'N', 'color':'#ffa500', 'name':'L'}
	Defaults={'W':[(4,3),(4,4),(4,5),(3,5)],
			  'N':[(3,4),(4,4),(5,4),(5,5)],
			  'E':[(4,5),(4,4),(4,3),(5,3)],
			  'S':[(5,4),(4,4),(3,4),(3,3)]}
	Points={'W':[(4,4),(3,4),(3,3),(4,6),(3,6)],
			'N':[(4,4),(4,4),(4,4),(4,4),(4,4)],
			'E':[(4,4),(5,4),(5,3),(4,6),(5,6)],
			'S':[(4,4),(4,4),(4,4),(4,4),(4,4)]}

class J:
	"""J - Tetromino behaviour description"""
	def generate():
		return {'type': J, 'coords': [(x,20) for x in range(3,6)]+[(3,21)], 'rot': 'N', 'color':'#0000ff', 'name':'J'}
	Defaults={'W':[(4,3),(4,4),(4,5),(3,3)],
			  'N':[(3,4),(4,4),(5,4),(3,5)],
			  'E':[(4,5),(4,4),(4,3),(5,5)],
			  'S':[(5,4),(4,4),(3,4),(5,3)]}
	Points={'W':[(4,4),(3,4),(3,3),(4,6),(3,6)],
			'N':[(4,4),(4,4),(4,4),(4,4),(4,4)],
			'E':[(4,4),(5,4),(5,3),(4,6),(5,6)],
			'S':[(4,4),(4,4),(4,4),(4,4),(4,4)]}

class S:
	"""S - Tetromino behaviour description"""
	def generate():
		return {'type': S, 'coords': [(3,20),(4,20), (4,21),(5,21)], 'rot': 'N', 'color':'#00ff00', 'name':'S'}
	Defaults={'W':[(4,3),(4,4),(3,4),(3,5)],
			  'N':[(3,4),(4,4),(4,5),(5,5)],
			  'E':[(4,5),(4,4),(5,4),(5,3)],
			  'S':[(5,4),(4,4),(4,3),(3,3)]}
	Points={'W':[(4,4),(3,4),(3,3),(4,6),(3,6)],
			'N':[(4,4),(4,4),(4,4),(4,4),(4,4)],
			'E':[(4,4),(5,4),(5,3),(4,6),(5,6)],
			'S':[(4,4),(4,4),(4,4),(4,4),(4,4)]}
class Z:
	"""Z - Tetromino behaviour description"""
	def generate():
		return {'type': Z, 'coords': [(4,20),(5,20), (3,21),(4,21)], 'rot': 'N', 'color':'#ff0000', 'name':'Z'}
	Defaults={'W':[(4,4),(4,5),(3,3),(3,4)],
			  'N':[(4,4),(5,4),(3,5),(4,5)],
			  'E':[(4,4),(4,3),(5,5),(5,4)],
			  'S':[(4,4),(3,4),(5,3),(4,3)]}
	Points={'W':[(4,4),(3,4),(3,3),(4,6),(3,6)],
			'N':[(4,4),(4,4),(4,4),(4,4),(4,4)],
			'E':[(4,4),(5,4),(5,3),(4,6),(5,6)],
			'S':[(4,4),(4,4),(4,4),(4,4),(4,4)]}
		
class O:
	"""O - Tetromino behaviour description"""
	def generate():
		return {'type': O, 'coords': [(4,20),(5,20), (4,21),(5,21)], 'rot': 'N', 'color':'#ffff00', 'name':'O'}
	Defaults={'W':[(4,4),(5,4),(4,5),(5,5)],
			  'N':[(4,4),(5,4),(4,5),(5,5)],
			  'E':[(4,4),(5,4),(4,5),(5,5)],
			  'S':[(4,4),(5,4),(4,5),(5,5)]}
	Points={'W':[(4,4),(4,4),(4,4),(4,4),(4,4)],
			'N':[(4,4),(4,4),(4,4),(4,4),(4,4)],
			'E':[(4,4),(4,4),(4,4),(4,4),(4,4)],
			'S':[(4,4),(4,4),(4,4),(4,4),(4,4)]}



class GameDashboard(Frame):
	"""
Definition of the frame containing all the information the player needs for the gameplay, except other player's boards.

init(master, blocksize=30, level=1)
    master is the parent of the frame
    blocksize is the size of the x*x block of which each Tetromino is built of, scales the canvas
    level is the initial game difficulcity (speed and scoring multiplier)

"""
	def __init__(self, master, mixer,sounds, blocksize=30, level=1):
		Frame.__init__(self)
		##Blocksize in pixels
		self.blocksize = blocksize
		self.mixer=mixer
		##The level to start the game on
		self.level=level
		self.sounds=sounds

		##Different lock object for gameplay and network interferences
		self.netLock = threading.Lock()
		##Different lock object for gameplay and network interferences
		self.gameLock = threading.Lock()

		##Is the player in the game right now?
		self.ingame = False
		self.paused = False
		self.online=False

		self.gameThread=None
		
		##Default background color
		self.bg="black"

		##The main canvas and the map of the game
		self.can = Canvas(self, width=10*blocksize, height=20*blocksize+5, bg=self.bg)
		self.can.create_line(0,0,10*blocksize, 0, fill="white")
		self.can.yview_scroll(22, 'units')

		##The hold canvas
		self.hold_can = Canvas(self, width=6*blocksize, height=4*blocksize, bg=self.bg)

		##Canvas of the Queue
		self.queue_can = Canvas(self, width=6*blocksize, height=20*blocksize+5, bg=self.bg)
		self.queue_can.create_rectangle(0,0,7*blocksize,blocksize*3.33, fill="cyan")
		self.bag=Bag(self.queue_can, blocksize)

		#Widget placements
		self.hold_can.grid(row=0, column=0,columnspan=2, padx=5, pady=5, sticky=N)
		self.can.grid(row=0, column=2, pady=5, rowspan=5)
		self.queue_can.grid(row=0, column=3, rowspan=5, padx=5, pady=5, sticky = N)

		#Font
		self.font=font.Font(family='Comic Sans MS', size=12, weight='bold', slant='roman')

		##Frame containing our labels
		self.label_frame=Frame(self)
		self.label_frame.grid(row=4, column=0)
		
		Label(self.label_frame,text="Incoming Lines: \n\n",font=self.font).grid(row=0, column=0, sticky="NW")
		self.l_attacks=Label(self.label_frame,text="0",font=self.font, fg="red")
		self.l_attacks.grid(row=0, column=1, sticky="NW")

		Label(self.label_frame,text="Points: ",font=self.font).grid(row=3, column=0, sticky="SW")
		Label(self.label_frame,text="Level: ",font=self.font).grid(row=4, column=0, sticky="SW")
		Label(self.label_frame,text="Lines cleared: ",font=self.font).grid(row=5, column=0, sticky="SW")
		self.l_points=Label(self.label_frame,text="0",font=self.font)
		self.l_levels=Label(self.label_frame,text="0",font=self.font)
		self.l_lines=Label(self.label_frame,text="0",font=self.font)

		self.l_points.grid(row=3, column=1, sticky="SW")
		self.l_levels.grid(row=4, column=1, sticky="SW")
		self.l_lines.grid(row=5, column=1, sticky="SW")

		#Bindings
		#self.bind("<Destroy>", self._destroy)
		#self.master.protocol("WM_DELETE_WINDOW", self._destroy)
		self.master.bind("<space>", self.button_space)
		self.master.bind("c", self.button_c)
		self.master.bind("<Shift_L>", self.button_shift_l)

		#Sound


		self.bgvar=IntVar()
		self.bgvar.set(1)
		self.chmusic=ttk.Checkbutton(self,text="Music", command=self.swmusic,variable=self.bgvar, state=ACTIVE)
		self.chmusic.grid(row=1, column=0)
		self.bgmusic=StringVar()
		try:
			with open("music.prefs", 'r') as f:
				self.bgmusic.set(f.read())
		except:
			self.bgmusic.set("bg3")
			with open("music.prefs", 'w') as f:self.bgmusic.get()
		Label(self,text="Music volume", font=self.font).grid(row=2, column=0,sticky="S")
		self.vol = ttk.Scale(self, from_=0, to=100, orient=HORIZONTAL,command=self.set_vol)
		self.vol.grid(row=3,column=0,sticky=N)
		self.vol.set(100)
		self.choosemusic=ttk.Button(self, text="Chose",command=self.choose_music)
		self.choosemusic.grid(row=2, column=0,sticky=N)
		##Play button to start playing
		self.startButton = ttk.Button(self, text="\nPLAY\n", command=self.start_new_game, width=int(0.85*blocksize))
		self.startButton.grid(row=0, column=0,padx=8, sticky="S")
	
	def set_vol(self,evt):
		"""Set the volume of all music"""
		self.mixer.Channel(0).set_volume(float(evt)/100)
	def choose_music(self):
		"""Toplevel window to costumize connection settings"""
		self.can.focus_set()
		self.costumize=Toplevel(self)
		self.costumize.grab_set()
		b_confirm=ttk.Button(self.costumize, command= lambda :self.close_choose(), text="OK")
		b_confirm.grid(row=0, column=3, rowspan=2,padx=10)

		Radiobutton(self.costumize, text="Ievan Polkka", variable=self.bgmusic, value="bg1").grid(row=0)
		Radiobutton(self.costumize, text="Коробейники", variable=self.bgmusic, value="bg2").grid(row=2)
		Radiobutton(self.costumize, text="Коробейники piano", variable=self.bgmusic, value="bg3").grid(row=3)
		Radiobutton(self.costumize, text="Platinum Disco", variable=self.bgmusic, value="bg4").grid(row=4)
		Radiobutton(self.costumize, text="Ao no kanata", variable=self.bgmusic, value="bg").grid(row=5)
		self.costumize.title('Music settings')
		self.costumize.geometry("+%d+%d" % (self.master.winfo_rootx()+50,
											self.master.winfo_rooty()+50))
		self.costumize.protocol("WM_DELETE_WINDOW", self.close_choose)
		self.costumize.resizable(0,0)
		self.costumize.transient(self.costumize.master)

	def close_choose(self):
		"""Called upon closing the music selecting dialog"""
		self.costumize.destroy()
		self.swmusic()
		with open("music.prefs", 'w') as f:
			f.write(self.bgmusic.get())

	def swmusic(self):
		"""Toggle the background/endgame music"""
		self.can.focus_set()
		if 'selected' in self.chmusic.state() and self.ingame:
			self.mixer.Channel(0).play(self.sounds[self.bgmusic.get()],loops=-1)
		else:
			self.mixer.Channel(0).stop()
			
	def _destroy(self):
		"""Window closed event handler"""
		if self.ingame:
			self.gameThread.call_quit()

	def start_new_game(self):
		"""Start a solo game"""
		self.can.focus_set()
		if not self.ingame:
			self.set_levels(self.level)
			self.can.delete(ALL)
			self.can.create_line(0,0,10*self.blocksize, 0, fill="white")
			self.queue_can.delete(ALL)
			self.queue_can.create_rectangle(0,0,7*self.blocksize,self.blocksize*3.33, fill="cyan")
			self.hold_can.delete(ALL)
			self.ingame=True
			self.swmusic()
			self.bag.start()
			self.gameThread=GameEngine(self, self.can, self.blocksize, self.level,self.bag, self.mixer,self.sounds,self.online)
			self.gameThread.start()

	def button_space(self, event):
		"""keyboard.space Event handler"""
		if self.ingame and not self.paused:
			self.gameThread.call_hard_drop()
	def button_c(self, event):
		"""keyboard.c Event handler"""
		if self.ingame and not self.paused:
			self.gameThread.call_hold()
	def button_shift_l(self, event):
		"""keyboard.l_shift Event handler"""
		if self.ingame and not self.paused:
			self.gameThread.call_hold()

	def set_points(self,points):
		"""Update the corresponding stats tracking label"""
		self.l_points.config(text="%d"%points)

	def set_levels(self,level):
		"""Update the corresponding stats tracking label"""
		self.l_levels.config(text="%d"%level)
	def set_lines(self,lines):
		"""Update the corresponding stats tracking label"""
		self.l_lines.config(text="%d"%lines)
	def set_attacks(self,lines):
		"""Update the corresponding stats tracking label"""
		self.l_attacks.config(text="%d"%lines)

		
class GameEngine(threading.Thread):
	"""The main gameplay's Thread"""
	def __init__(self, boss, can, blocksize, level,bag, mixer,sounds,online=False):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.mixer=mixer
		self.sounds=sounds

		self.boss = boss
		self.can = can
		self.blocksize = blocksize
		self.bag=bag
		self.online=online
		self.soft_drop_flag=False
		#Game Phase tracker
		self.phase="Inactive"
		#Window closed?
		self.abandon=False

		#Hold slot
		self.hold_slot=None
		#Game Matrix
		#A: Active Tetromino
		#B: Block
		#OGM: Object Game Matrix
		self.GM = [[0]*40 for x in range(10)]
		self.OGM=[[0]*40 for x in range(10)]

		#Initialize the active Tetromino's namespace
		self.active=None
		#The ghost piece
		self.ghost=None

		self.bonuses=["Single","Double","Triple","Tetris","Mini T-Spin","Mini T-Spin Single","T-Spin","T-Spin Single","T-Spin Double","T-Spin Triple"]
		self.multiplier=[100,300,500,800,100,200,400,800,1200,1600]
		self.attacks=[0,1,2,4,0,0,0,2,4,6]
		if self.online:
			self.players=len(self.boss.master.players)
			if self.players>1:
				self.attacks=[0,0,1,2,0,0,0,1,2,5]
		
		self.score={}
		self._gameScore=0
		self._lineScore=0
		self._levelScore=level
		self._newAttacks=0
		self.gameScore=0
		self.levelScore=level
		self.lineScore=0
		self.newAttacks=0

		self.B2B=False
		
		# When any single button is then released, the Tetrimino should again move in the direction still held,
		# with the Auto-Repeat delay of roughly 0.3 seconds applied once more.
		self.auto_repeat_delay=0.21
		self.auto_repeat_speed=0.03

		# The method to repeat
		self.to_repeat=None
		
		# Can we be repeating yet?
		self.timer_repeat=0
		# secondary timer for the repeat phase
		self.last_repeat=0

		# Keyboard listening
		self.up_released=True
		self.ctrl_l_released=True
		self.pressed=False
		self.held={}

		self.kb_listen=Listener(on_press=self.on_press, on_release=self.on_release)
		self.kb_listen.start()

		#Line attacks
		self.gap_position=randrange(0,10)
		self.lift_count=0

		#Online victory
		self.win=False

	@property
	def gameScore(self):
		"""I'm the 'gameScore' property."""
		return self._gameScore

	@gameScore.setter
	def gameScore(self, value):
		"""I'm the setter of 'gameScore' property."""
		self._gameScore = value
		self.boss.set_points(self._gameScore)
	
	@property
	def lineScore(self):
		"""I'm the 'lineScore' property."""
		return self._lineScore

	@lineScore.setter
	def lineScore(self, value):
		"""I'm the setter of 'lineScore' property."""
		self._lineScore = value
		self.boss.set_lines(self._lineScore)
	
	@property
	def levelScore(self):
		"""I'm the 'levelScore' property."""
		return self._levelScore

	@levelScore.setter
	def levelScore(self, value):
		"""I'm the setter of 'levelScore' property."""
		self._levelScore = value
		self.boss.set_levels(self._levelScore)
	@property
	def newAttacks(self):
		"""I'm the 'newAttacks' property."""
		return self._newAttacks

	@newAttacks.setter
	def newAttacks(self, value):
		"""I'm the setter of 'newAttacks' property."""
		self._newAttacks = value
		self.boss.set_attacks(self._newAttacks)


	def on_press(self, key):
		"""pynput event handler"""
		if self.pressed==key:
			return True
		elif key==Key.up and self.up_released==False:
			return True
		elif key==Key.ctrl_l and self.ctrl_l_released==False:
			return True
		else:
			#Don't want to gain the lock unnecessarily
			if key not in (Key.left, Key.right, Key.up, Key.ctrl_l, Key.down):return True

			self.boss.gameLock.acquire()
			if key==Key.left:
				self.pressed=key
				self.reset_auto_repeat_cooldowns()
				self.held[key]=True
				self.to_repeat=self.move_left
			elif key==Key.right:
				self.pressed=key
				self.reset_auto_repeat_cooldowns()
				self.held[key]=True
				self.to_repeat=self.move_right
			elif key==Key.up:
				self.up_released=False
				self.call_rotate_cw()
			elif key==Key.ctrl_l:
				self.ctrl_l_released=False
				self.call_rotate_ccw()
			elif key==Key.down:
				self.mixer.Channel(1).play(self.sounds["move"])
				if not self.call_soft_drop():
					self.call_soft_drop()
			self.boss.gameLock.release()

	def on_release(self,key):
		"""pynput event handler"""
		if self.pressed==key:
			self.boss.gameLock.acquire()
			self.pressed=False
			self.reset_auto_repeat_cooldowns()
			self.held[key]=False
			self.boss.gameLock.release()
			# Check if another key was held through a press-release
			for key in self.held:
				if self.held[key]:
					self.on_press(key)
					break
		elif key in self.held:
			self.held[key]=False
		elif key==Key.up:
			self.up_released=True
		elif key==Key.ctrl_l:
			self.ctrl_l_released=True
		elif key==Key.down:
			self.call_soft_drop(False)

	def reset_auto_repeat_cooldowns(self):
		"""Set timers to 0 when an action just occured"""
		self.last_repeat=0
		self.timer_repeat=0


	def call_quit(self):
		"""Call this to shut down the Engine Thread"""
		self.abandon=True
	def won(self):
		"""Call this when the player won"""
		self.win=True

	def run(self):
		"""Run, run, run, run-runrunrunruuuuuuun!"""
		try:
			while True:
				self.boss.ingame=True
				self.phase = "generation"
				if self.generation_phase():
					self.phase="falling"
					locked=False
					while not locked:
						if self.phase=="falling":
							locked=self.falling_phase()
							if not locked:
								self.phase="locking"
						elif self.phase=="locking":
							locked=self.lock_phase()
							if not locked:
								self.phase="falling"
						else:
						# if self.phase="pattern":
						# 	self.pattern_phase()
							raise "This should've never occur!"
					self.phase="pattern"
					self.pattern_phase()
					self.eliminate_phase()
				else:
					break
		except AbandonException:
			print("Player abandoned.")
		except GameOverException:
			print("The game was over.")
			if self.online:
				while self.boss.master.playing:
					self.check_opponents()
				print("Exiting thread")
		except Exception as e:
			print(e)

	def call_hold(self):
		"""Set flag to hold the piece"""
		if self.phase not in ("falling", "locking"):
			return
		if self.hold==None:
			self.hold=True
	def call_soft_drop(self, logical=True):
		"""Set flag for a Soft Drop"""
		self.soft_drop_flag=logical
		return self.soft_drop_flag

	def soft_drop(self):
		"""Method which excecutes a soft drop whenever off cooldown."""
		#self.soft_drop_flag=False
		now=time.time()
		if now-self.last_linedrop<(self.speed/20):
			return
		else:
			if not self.touching_surface():
				self.gameScore+=1
				self.last_linedrop=now
				self.linedrop()
				self.send_coords()
				self.send_stats()


	def call_hard_drop(self):
		"""Set flag for a Hard Drop"""

		if self.phase not in ("falling", "locking"):
			return
		self.hard_drop_flag=True

	def hard_drop(self):
		"""Method which excecutes a Hard Drop"""
		#How much is it possible to drop?
		distance=self.distance_from_surface()
		if distance>0:
			self.spin_last=False
		[self.linedrop() for x in range(distance)]
		self.gameScore+=distance*2
		self.send_coords()
		self.lock_down()
		self.hard_drop_flag=False

	def distance_from_surface(self):
		"""Finds the lowest distance between an open surface and the active Tetromino"""
		#How much is it possible to drop?
		min_d=40
		for x,y in self.active['coords']:
			y0=0
			if min_d>y-y0:
				min_d=y-y0

			for y0 in range(0,y):
				if self.GM[x][y0]=='B':
					if min_d>y-y0-1:
						min_d=y-y0-1
		return min_d

	def get_quarter(self, original, direction):
		"""Original quarter: NSWE: 1 char\nDirection: Left=-1, Right=+1"""
		qrtrs=['E', 'N', 'W', 'S']
		return qrtrs[(qrtrs.index(original)+direction)%4]

	def call_rotate_cw(self):
		"""Set flag for a Clockwise Rotation"""
		if self.phase not in ("falling", "locking"):
			return
		self.rotate_cw_flag=True

	def call_rotate_ccw(self):
		"""Set flag for a Clockwise Rotation"""
		if self.phase not in ("falling", "locking"):
			return
		self.rotate_ccw_flag=True

	def rotate(self, counter_clockwise=False):
		"""Clockwise rotation event = RIGHT"""
		#Reset flag
		if counter_clockwise:
			self.rotate_ccw_flag=False
			direction=1
		else:
			self.rotate_cw_flag=False
			direction=-1
		bs=self.blocksize

		src=self.active['rot']
		dest=self.get_quarter(src,direction)

		new_coords=self.SRS(src, dest, self.active['coords'], self.GM,self.active['type'])
		if new_coords==None:
			return False
		#Rotation succeeded
		if self.mixer:
			self.mixer.Channel(2).play(self.sounds["rotate"])
		self.last_action=time.time()
		self.active['rot']=dest

		for x,y in self.active['coords']:
			self.GM[x][y]=0
		self.active['coords']=new_coords[:]
		for x,y in new_coords:
			self.GM[x][y]='A'

		#Visual
		#Replace the objects
		for i in range(4):
			x,y=self.active['coords'][i]
			self.can.coords(self.active['objects'][i], 2+(bs*x),-(y-19)*bs,2+bs+(bs*x), -(y-20)*bs)
		#Adjust ghost
		self.ghost_adjust()
		return True



	def SRS(self,from_, to_, coords, matrix, Tetromino):
		"""Super Rotation System - coordinate calculor"""
		for P in range(5):
			#return I.west(P,I.Points['N'][P])
			#new_coords=I.west(P,I.Points['N'][P])

			p=Tetromino.Points[to_][P]
			dest=Tetromino.Points[from_][P]
			shift=(dest[0]-p[0],dest[1]-p[1])

			new_coords=[]
			for x,y in Tetromino.Defaults[to_]:
				new_coords.append((x+shift[0], y+shift[1]))

			#The difference between the old and the new coordinates
			map_shift=[(new_coords[x][0]-Tetromino.Defaults[from_][x][0], new_coords[x][1]-Tetromino.Defaults[from_][x][1]) for x in range(4)]

			#The real new coordinates
			map_coords=[(coords[x][0]+map_shift[x][0], coords[x][1]+map_shift[x][1]) for x in range(4)]
			#Test these
			failed=False
			for x,y in map_coords:
				if x<0 or y<0 or x>9 or y>40 or matrix[x][y]=='B':
					failed=True
					break

			if failed:continue
			return map_coords

	def move_right(self):
		"""Attemps to move the Tetromino one block right. Returns True if successful and False if not."""
		for x,y in self.active['coords']:
			if x==9:return False
			if self.GM[x+1][y]=='B':return False

		self.last_action=time.time()
		self.spin_last=False
		#Backend
		#Writing into both the self.active and the main matrix
		new_coords=[]
		for x,y in self.active['coords']:
			new_coords.append((x+1,y))
			self.GM[x][y]=0
		self.active['coords']=new_coords[:]
		for x,y in new_coords:
			self.GM[x][y]='A'

		#Visual
		for block in self.active['objects']:
			self.can.move(block, self.blocksize, 0)
		if self.mixer:
			self.mixer.Channel(1).play(self.sounds["move"])
		self.ghost_adjust()
		return True

	def move_left(self):
		"""Attemps to move the Tetromino one block left. Returns True if successful and False if not."""

		for x,y in self.active['coords']:
			if x==0:return False
			if self.GM[x-1][y]=='B':return False

		self.last_action=time.time()
		self.spin_last=False
		#Backend
		#Writing into both the self.active and the main matrix
		new_coords=[]
		for x,y in self.active['coords']:
			new_coords.append((x-1,y))
			self.GM[x][y]=0
		self.active['coords']=new_coords[:]
		for x,y in new_coords:
			self.GM[x][y]='A'

		#Visual
		for block in self.active['objects']:
			self.can.move(block, -self.blocksize, 0)
		if self.mixer:
			self.mixer.Channel(1).play(self.sounds["move"])
		self.ghost_adjust()
		return True

	def ghost_adjust(self):
		"""This method adjusts the ghost piece to the new position. Each turn or horizontal move action should call this."""
		distance=self.distance_from_surface()
		bs=self.blocksize
		i=0
		for x,y in self.active['coords']:
			self.can.coords(self.ghost[i],2+(bs*x),-(y-19-distance)*bs,2+bs+(bs*x), -(y-20-distance)*bs)
			i+=1

	def generation_phase(self, from_hold=False):
		"""
The generation time of a Tetrimino is 0.2 seconds after the Lock Down of the previous Tetrimino.
This slight delay happens as soon as the Completion Phase is finished.
Generation time may change depending on the handling of the target platform.

As soon as a Tetrimino is generated, three things immediately happen:
1) the Tetrimino drops one row if no existing Block is in its path,
2) the Tetrimino enters the Falling Phase where the player is able to move and rotate it, and
3) the Ghost Piece (if turned on) appears below, North Facing.
If an existing Block is in the Tetrimino’s path, the Tetrimino does not drop one row immediately,
however, a few pixels of the generated Tetrimino are shown (hardware permitting)
to help the player manipulate it above the Skyline.
		"""
		if self.win:
			self.eliminate=[x for x in range(40)]
			self.eliminate_phase()
			self.send_won()
			self.boss.ingame=False
			if self.online:
				self.boss.master.chat.write("You won!\nScore: %s"%self.gameScore)
			else:
				messagebox.showinfo("You won!","Score: %s"%self.gameScore)
			raise GameOverException()
		if self.newAttacks>0:
			for x in range(self.newAttacks):
				self.lift()
				time.sleep(0.05)
		self.newAttacks=0
		bs=self.blocksize
		#Game speed
		self.speed=(0.8 - ((self.levelScore - 1) * 0.007))**(self.levelScore - 1)
		#Score in each turn will be logged in a dictionary
		self.score={}
		#Lowest line tracker
		self.lowest_line_reached=21

		#Reset Flags
		#Did a hard drop occur?
		self.hard_drop_flag=False
		#Soft drop?
		#Rotate?
		self.rotate_cw_flag=False
		self.rotate_ccw_flag=False
		#Lines to eliminate
		self.eliminate=[]

		#Action counter in locking phasee
		self.counter=0

		#Timing the soft drop
		self.last_linedrop=0

		#Timing of the last action (move/rotate, NOT drop)
		self.last_action=time.time()

		#Did it lock down after a spin?
		self.spin_last=False

		if self.ghost:
			for i in self.ghost:
				self.can.delete(i)
		#Can the player Hold this round
		#Hold
		#None: Last piece was taken from bag
		#True: The flag was set to True, to make the Engine call generation_phase again.
		#False: The last piece was taken from the Hold, so the player cannot swap again. (The flag wont be set to true in this case in the call)
		if from_hold:
			for x,y in self.active['coords']:
				self.GM[x][y]=0
			for i in self.active['objects']:
				self.can.delete(i)
			held=self.active['type']
			if self.hold_slot==None:				
				self.active=self.bag.next().generate()
			else:
				self.active=self.hold_slot.generate()

			self.hold_slot=held
			self.hold=False
			self.place_hold(self.hold_slot)
			self.send_hold()
		else:
		#   Pick up the next tetromino from the Next Queue
			self.hold=None
			self.active=self.bag.next().generate()

		if self.block_out(self.active['coords']):
			self.game_over()

		self.active['objects']=[]
		for x,y in self.active['coords']:
			self.GM[x][y]='A'
			self.active['objects'].append(self.can.create_rectangle(2+(bs*x),-(y-19)*bs,2+bs+(bs*x), -(y-20)*bs, fill=self.active['color']))

		distance=self.distance_from_surface()
		self.ghost=[]
		for x,y in self.active['coords']:
			self.ghost.append(self.can.create_rectangle(2+(bs*x),-(y-19-distance)*bs,2+bs+(bs*x), -(y-20-distance)*bs, outline=self.active['color']))
		
		for i in self.active['objects']:
			self.can.tag_raise(i)

		#Update the server
		self.send_mino()
		return 1

	def place_hold(self, tetromino):
		"Places the tetromino to the hold canvas"
		self.boss.hold_can.delete(ALL)
		curr=tetromino.generate()
		bs=self.blocksize*0.85
		dx=-(bs*(5/3))
		dy=0
		if curr['type']==O:
			dx=-(bs*2)
		elif curr['type']==I:
			dx=-(bs*2)
			dy=-bs*0.5
		[self.boss.hold_can.create_rectangle(dx+(bs*(x+0.5)),dy+(bs*3.5)-(y-19)*bs,dx+bs+(bs*(x+0.5)), dy+(bs*3.5)-(y-20)*bs, fill=curr['color']) for x,y in curr['coords']]


	def falling_phase(self):
		"During falling, the player can rotate, move sideways, soft drop, hard drop or hold the Tetromino"
		
		while self.phase=="falling":
			self.check_opponents()
			#coordinates
			c1=self.active['coords'].copy()

			if self.abandon:raise AbandonException()
			if self.boss.paused: continue
			if self.hold:
				self.generation_phase(True)
			#Hard Drop?
			if self.hard_drop_flag:
				self.hard_drop()
				return True

			#Atop Surface?
			if self.touching_surface():
				#return to main cycle
				return False
			now=time.time()
			if now-self.last_linedrop>=self.speed:
				self.last_linedrop=now
				self.linedrop()
				self.send_coords()
				continue

			#Soft Drop?
			if self.soft_drop_flag:
				self.soft_drop()
			if self.rotate_cw_flag:
				act=self.rotate()
				if act:self.spin_last=True
			elif self.rotate_ccw_flag:
				act=self.rotate(True)
				if act:self.spin_last=True

			self.boss.gameLock.acquire()
			if self.pressed:
				now=time.time()
				if self.timer_repeat==0:
					self.timer_repeat=now
					self.to_repeat()
				elif self.last_repeat==0:
					if now-self.timer_repeat>=self.auto_repeat_delay:
						self.last_repeat=now
						self.to_repeat()
				elif now-self.last_repeat>=self.auto_repeat_speed:
					self.last_repeat=now
					self.to_repeat()
			self.boss.gameLock.release()

			#Send to server if the coordinates have changed
			if self.active['coords']!=c1:
				self.send_coords()

			

		raise "Only the run() method should set the phase flag"


	def linedrop(self):
		"Let the tetromino fall down one line. WARNING: This function does not check circumstances."
		#Backend
		#Writing into both the self.active and the main matrix
		self.spin_last=False
		new_coords=[]
		for x,y in self.active['coords']:
			new_coords.append((x,y-1))
			self.GM[x][y]=0
		self.active['coords']=new_coords[:]
		for x,y in new_coords:
			self.GM[x][y]='A'
			if y<self.lowest_line_reached:
				self.lowest_line_reached=y
				self.counter=0

		#Visual
		for block in self.active['objects']:
			self.can.move(block, 0, self.blocksize)

	def lock_phase(self):
		"During lock phase the player still rotate or move according to Extendended Placement Lockdown\nLock after: 0.5s\nAction limit: 15 actions"
		
		self.last_action=time.time()
		while self.phase=="locking":
			self.check_opponents()
			c1=self.active['coords'].copy()
			if self.abandon:raise AbandonException()
			if self.boss.paused: continue
			if self.hold:
				self.generation_phase(True)
				return False
			#Still Atop Surface?
			if not self.touching_surface():
				#return to main cycle
				self.spin_last=False
				return False

			if self.counter==15:
				self.lock_down()
				return True
			#Hard Drop?
			if self.hard_drop_flag:
				self.hard_drop()
				return True


			#Soft Drop?
			#Once the surface is reached, Soft Drop should not auto-repeat, rather just wait out the 0.5 sec to lock down.
			#rotation?
			if self.rotate_cw_flag:
				act=self.rotate()
				if act:
					self.counter+=1
					self.spin_last=True
			elif self.rotate_ccw_flag:
				act=self.rotate(True)
				if act:
					self.counter+=1
					self.spin_last=True
			elif self.pressed:
				do=False
				now=time.time()
				if self.timer_repeat==0:
					self.timer_repeat=now
					do=True
				elif self.last_repeat==0:
					if now-self.timer_repeat>=self.auto_repeat_delay:
						self.last_repeat=now
						do=True
				elif now-self.last_repeat>=self.auto_repeat_speed:
					self.last_repeat=now
					do=True
				if do:
					act=self.to_repeat()
					if act:
						self.counter+=1
						self.spin_last=False

			if self.active['coords']!=c1:
				self.send_coords()

			if time.time()-self.last_action>=0.5:
				self.lock_down()
				return True



	def lock_down(self):
		"Sets the Tetromino to the permanent state, deletes the ghost piece"
		for x,y in self.active['coords']:
			self.GM[x][y]='B'
			self.OGM[x][y]=self.active['objects'][self.active['coords'].index((x,y))]
		for x in self.ghost:
			self.can.delete(x)
		if self.mixer:
			self.mixer.Channel(4).play(self.sounds["lock"])
		self.send_lock()

	def pattern_phase(self):
		"""
In this phase, the engine looks for patterns made from Locked Down Blocks in the Matrix. Once a pattern has been matched, it can trigger any number of Tetris variant-related effects.
The classic pattern is the Line Clear pattern.
This pattern is matched when one or more rows of 10 horizontally aligned Matrix cells are occupied by Blocks.
The matching Blocks are then marked for removal on a hit list.
Blocks on the hit list are cleared from the Matrix at a later time in the Eliminate Phase.
This phase takes up no apparent game time.
"""
		#Check for Lock Out
		lockout=True
		for x,y in self.active['coords']:
			if y<=20:
				lockout=False
				break

		if lockout:
			self.game_over()

		tspin=False
		mini_tspin=False
		#recognize T-Spins
		if self.active['type']==T and self.spin_last:

			center=self.active['coords'][1]
			leg=self.active['coords'][3]
			diff=(leg[0]-center[0], leg[1]-center[1])
			aleg=(center[0]-diff[0], center[1]-diff[1])
			ab=[(leg[0]-diff[1], leg[1]-diff[0]), (leg[0]+diff[1],leg[1]+diff[0])]
			cd=[(aleg[0]-diff[1], aleg[1]-diff[0]), (aleg[0]+diff[1],aleg[1]+diff[0])]
			bs=self.blocksize

			
			ab_count=self.surfaces(ab)
			cd_count=self.surfaces(cd)
			
			if ab_count==2 and cd_count>=1:
				tspin=True
			if cd_count==2 and ab_count==1:
				mini_tspin=True

		#Find and mark lines for elimination
		lines=0
		clear=['B']*10
		for y in range(40):
			line=[self.GM[x][y] for x in range(10)]
			if line==clear:
				lines+=1
				self.eliminate.append(y)
		

		#Bonuses are name of lineclears, tspins, or both with tspin name in front
		bonus=""
		if mini_tspin:
			bonus+="Mini T-Spin"
		elif tspin:
			bonus+="T-Spin"
		if lines>0 and len(bonus)>0:
			bonus+=" "
		if lines>0:
			bonus+=self.bonuses[lines-1]

			#Increase the level if another 10 lines has been cleared
			if self.levelScore<15:
				before=self.lineScore//10
				self.lineScore+=lines
				after=self.lineScore//10
				if after>before:self.levelScore+=1
		

		#Back-To-Back recognition
		apply_b2b=False
		if bonus in ("Tetris", "T-Spin Single",  "T-Spin Double", "T-Spin Triple", "Mini T-Spin Single"):
			if self.B2B:
				self.send_bonus("Back-To-Back "+bonus+"!")
				apply_b2b=True
			else:
				self.send_bonus(bonus+"!")
				self.B2B=True
		elif bonus not in ("Mini T-Spin", "T-Spin"):
			self.B2B=False

		points=0
		attack=0
		if len(bonus)>0:
			points=self.multiplier[self.bonuses.index(bonus)]
			attack=self.attacks[self.bonuses.index(bonus)]
		if apply_b2b:
			points*=1.5
			attack+=1

		self.gameScore+=points

		if self.newAttacks>=attack:
			self.newAttacks-=attack
			attack=0
		elif self.newAttacks<attack:
			attack-=self.newAttacks
			self.newAttacks=0
		if attack>0:
			self.send_attack(attack)


	def surfaces(self, list_):
		"Determines how many coordinates is Surface"
		counter=0
		for x,y in list_:
			if y==-1 or x==-1 or x==10:
				counter+=1
			elif self.GM[x][y]=='B':
				counter+=1
		return counter

	def eliminate_phase(self):
		"""
Involves animation. Note that I did the scoring in the pattern phase.

Any Minos marked for removal, i.e., on the hit list, are cleared from the Matrix in this phase.
If this results in one or more complete 10-cell rows in the Matrix becoming unoccupied by Minos,
then all Minos above that row(s) collapse, or fall by the number of complete rows cleared from the Matrix.
Points are awarded to the player according to the Tetris Scoring System,[...].
"""
		self.send_elim()
		self.send_stats()
		self.clear_marked_lines()

	def clear_marked_lines(self):
		"Clears any line marked by having it's id in the sorted list self.eliminate"
		if self.eliminate==[]:
			return
		elim=self.eliminate.copy()
		for i in range(len(elim)):
			y=elim[i]
			for x in range(10):
				del self.GM[x][y]
				self.GM[x].append(0)
			for j in range(len(elim)):
				elim[j]-=1
		#threading.Thread(target=self.clear_line_animation).start()
		#time.sleep(0.0001)
		if self.mixer:
			self.mixer.Channel(3).play(self.sounds["clear"])
		self.clear_line_animation()

	def clear_line_animation(self):
		"Method, removes the marked blocks visually. Note: This should take up no gametime, but the fact it does, only awards multiple line clears by a brief pause, which can be helpful at high levels."
		elim=self.eliminate.copy()
		rgb_fact=0
		while rgb_fact<255:
			for x in range(10):
				for y in elim:
					self.can.itemconfig(self.OGM[x][y], fill ="#%02x%02x%02x" % (rgb_fact,rgb_fact,rgb_fact))
			rgb_fact+=16
			time.sleep(0.005)

		for i in range(len(elim)):
			y=elim[i]
			for x in range(10):
				self.can.delete(self.OGM[x][y])
				self.OGM[x][y]=0
				for y1 in range(y+1,40):
					if self.OGM[x][y1]:
						self.OGM[x][y1-1]=self.OGM[x][y1]
						self.can.move(self.OGM[x][y1], 0, self.blocksize)
						self.OGM[x][y1]=0
				time.sleep(0.01)
			for j in range(len(elim)):
				elim[j]-=1

	def block_out(self, coords):
		"Game Over Condition - Is it possible to place the new Tetromino?"
		for x,y in coords:
			if self.GM[x][y]!=0:
				return True
		return False

	def touching_surface(self):
		"Is the Tetromino directily on a surface?"
		for x,y in self.active['coords']:

			#Is it on the ground?
			if y==0:return True

			#Is it on top of another [B]lock?
			if self.GM[x][y-1]=='B':
				return True

	def game_over(self):
		self.boss.ingame=False
		self.send_over()
		if self.mixer:
			self.mixer.Channel(0).play(self.sounds["over"], fade_ms=8000)
		#self.eliminate=[x for x in range(40)]
		coords=[[(0,38),(0,37),(0,36),(1,39),(2,39),(3,39),(2,37),(3,37),(3,36),(1,35),(2,35),(3,35)],
				[(6,35),(6,36),(6,37),(6,38),(7,37),(7,39),(8,37),(8,39),(9,35),(9,36),(9,37),(9,38),],
				[(0,30),(0,31),(0,32),(0,33),(0,34),(1,33), (2,32),(3,33),(4,30),(4,31),(4,32),(4,33),(4,34),],
				[(6,33),(6,32),(6,31),(7,34),(7,32),(7,30),(8,34),(8,32),(8,30),(9,34),(9,30),],
				[(0,28),(0,27),(0,26),(1,29),(2,29),(3,29),(4,28),(4,27),(4,26),(1,25),(2,25),(3,25),],
				[(6,28),(6,27),(6,26),(9,28),(9,27),(9,26),(7,25),(8,25),],
				[(0,23),(0,22),(0,21),(1,24),(2,24),(3,24),(1,22),(2,22),(1,20),(2,20),(3,20),],
				[(6,24),(6,23),(6,22),(6,21),(6,20),(7,24),(8,24),(9,24),(9,23),(7,22),(8,22),(9,22),(8,21),(9,20)]
		]
		self.eliminate=[y for y in range(21)]
		self.clear_line_animation()
		bs=self.blocksize
		clr=["red", "red", "orange", "orange", "purple", "purple", "blue", "blue"]
		for i in range(len(coords)):
			for x,y in coords[i]:
				self.OGM[x][y]=self.can.create_rectangle(2+(bs*x),-(y-19)*bs,2+bs+(bs*x), -(y-20)*bs, fill=clr[i])
		self.eliminate=[y for y in range(20)]
		self.clear_line_animation()
		time.sleep(4)
		if self.online:
			self.boss.master.chat.write("Game over!\nYour score: %s"%self.gameScore)
		else:
			messagebox.showinfo("Game over!","Score: %s"%self.gameScore)
		raise GameOverException()

	def receive_attacks(self,amount):
		self.newAttacks+=amount
	def lift(self):
		"Manages receiving counter attacks"
		#The game may be over here
		self.check_topout()
		bs=self.blocksize
		#New gap position after every 8 garbage line
		if self.lift_count%8==0:
			new = randrange(0,10)
			while new==self.gap_position:
				new = randrange(0,10)
			self.gap_position=new
		self.lift_count+=1
		for x in range(10):
			for y in range(40):
				if self.OGM[x][y]!=0:
					self.can.move(self.OGM[x][y], 0, -self.blocksize)
		for x in range(10):
			del self.GM[x][39]
			del self.OGM[x][39]
			if x == self.gap_position:
				self.GM[x][0:0]=[0]
				self.OGM[x][0:0]=[0]
				continue
			self.GM[x][0:0]=['B']
			self.OGM[x][0:0]=[self.can.create_rectangle(2+(bs*x),(19)*bs,2+bs+(bs*x), (20)*bs, fill="darkgray", outline="gray")]
		self.send_lift(self.gap_position)


	def check_opponents(self):
		"""Check it all"""
		if not self.online:return
		for i in self.boss.master.players:
			self.boss.master.players[i].run()

	def check_topout(self):
		"""Only gets checked before a lift, ends the game if there's a tetromino part found in the 40th line"""
		for x in range(10):
			if self.GM[x][39]=='B':
				self.game_over()

	def send_coords(self):
		"""Format the string such that it can be evaluated later and forward it"""
		if not self.online:return
		str1="["
		for x,y in self.active['coords']:
			str1+="("+str(x)+","+str(y)+"),"
		str1+="]"
		self.boss.master.update_server("#GAME#COORDS#"+str1)
	def send_mino(self):
		"""Format the string such that it can be evaluated later and forward it"""
		if not self.online:return
		self.boss.master.update_server("#GAME#NEW#"+self.active['name'])
	def send_lock(self):
		"""Format the string such that it can be evaluated later and forward it"""
		if not self.online:return
		self.boss.master.update_server("#GAME#LOCK#0")
	def send_hold(self):
		"""Format the string such that it can be evaluated later and forward it"""
		if not self.online:return
		self.boss.master.update_server("#GAME#HOLD#0")
	def send_over(self):
		"""Format the string such that it can be evaluated later and forward it"""
		if not self.online:return
		self.boss.master.update_server("#GAME#OVER#0")
	def send_elim(self):
		"""Format the string such that it can be evaluated later and forward it"""
		if not self.online:return
		str1="["
		for y in self.eliminate:
			str1+=str(y)+','
		str1+="]"
		self.boss.master.update_server("#GAME#ELIM#"+str1)
	def send_stats(self):
		"""Format the string such that it can be evaluated later and forward it"""
		if not self.online:return
		self.boss.master.update_server("#GAME#STAT#[%d,%d,%d]"%(self.gameScore, self.levelScore, self.lineScore))
	

	def send_attack(self, lines):
		"""Format the string such that it can be evaluated later and forward it"""
		if not self.online:return
		self.boss.master.update_server("#GAME#ATTACK#%d"%(lines))
	def send_lift(self, gap):
		"""Format the string such that it can be evaluated later and forward it"""
		if not self.online:return
		self.boss.master.update_server("#GAME#LIFT#%d"%(gap))
	def send_won(self):
		"""Format the string such that it can be evaluated later and forward it"""
		if not self.online:return
		self.boss.master.update_server("#GAME#WON#0")
	def send_bonus(self, bonus):
		"""Format the string such that it can be announced later and forward it"""
		if not self.online:return
		self.boss.master.update_server("#GAME#ANNOUNCE#%s"%bonus)
		self.boss.master.chat.write("You had a "+bonus)
class Bag:
	"""
Tetris uses a “bag” system to determine the sequence of Tetriminos that appear during game play.
This system allows for equal distribution among the seven Tetriminos.
"""
	def __init__(self, queue_can,blocksize):
		self.minos=[T, I, J, L, S, Z, O]
		self.queue_can=queue_can
		self.next_queue=[]
		self.bag=[]
		##tkinter graphical objects
		self.objects=[]
		##Original blocksize
		self.orig_box=blocksize
		self.blocksize=blocksize*(8/10)

	def start(self):
		"""Initialize the first Bag and Next Queue"""
		self.bag=self.minos.copy()
		shuffle(self.bag)
		self.next_queue=self.bag[:6]
		for i in self.next_queue:
			self.queue_forward(i, False)
		del self.bag[:6]
		
	def next(self):
		"""Return the next tetromino for the Game Engine, and step the que forward"""
		ret=self.next_queue[0]
		del self.next_queue[0]
		self.next_queue.append(self.bag[0])
		del self.bag[0]
		if len(self.bag)==0:
			self.bag=self.minos.copy()
			shuffle(self.bag)
		self.queue_forward(self.next_queue[-1])
		return ret

	def queue_forward(self, mino, delete=True):
		"""Delete (optionally) the top tetromino, Move each Tetromino up by one in the que, and place the next to the end of queue\nqueue_forward(mino, delete=True)\nmino:Tetromino-type ref\ndelete: delete the top piece"""
		if delete:
			for i in self.objects[0]:
				self.queue_can.delete(i)
			del self.objects[0]
		for i in self.objects:
			for j in i:
				self.queue_can.move(j, 0, -self.orig_box*3.33)
		bs=self.blocksize
		curr=mino.generate()
		dx=self.orig_box*1.33
		self.objects.append([self.queue_can.create_rectangle(-dx+(bs*(x+1)),self.orig_box*19-(y-19)*bs,-dx+bs+(bs*(x+1)), self.orig_box*19-(y-20)*bs, fill=curr['color']) for x,y in curr['coords']])


class AbandonException(Exception):
	"""Exception occurs when the player quits during an ongoing (either paused or unpaused) game. This serves the purpose of closing down threads."""
	pass
class GameOverException(Exception):
	"""Exception occurs when the game is over. This serves the purpose of closing down threads."""
	pass


if __name__ == '__main__':
	from pygame import mixer # Load the required library
	import os
	os.system('cls')
	root=Tk()
	mixer.pre_init(44100, 16, 2, 4096) 
	mixer.init()
	sounds={"lock":mixer.Sound("effects/lock.ogg"),
					 "rotate":mixer.Sound("effects/rotate.ogg"),
					 "move":mixer.Sound("effects/move.ogg"),
					 "clear":mixer.Sound("effects/lineclear.ogg"),
					 "over":mixer.Sound("music/gameover.ogg"),
					 "bg":mixer.Sound("music/bg.OGG"),
					 "bg1":mixer.Sound("music/bg1.OGG"),
					 "bg2":mixer.Sound("music/bg2.OGG"),
					 "bg3":mixer.Sound("music/bg3.OGG"),
					 "bg4":mixer.Sound("music/bg4.OGG")
		}
	fr=GameDashboard(root, mixer=mixer, sounds=sounds)
	fr.grid(row=0, column=0)
	root.title("Tetrícia")
	root.resizable(0,0)
	root.mainloop()