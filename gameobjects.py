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

Some function definitions are fully or partially taken from the 2009 Tetris Guideline:
https://www.dropbox.com/s/g55gwls0h2muqzn/tetris_guideline_docs_2009.zip?dl=0
https://tetris.fandom.com/wiki/Tetris_Guideline
"""


from tkinter import *
from random import randrange,shuffle
import threading,time
from pynput.keyboard import Key, Listener

class I:
	"""I - Tetromino behaviour description"""
	def generate():
		return {'type': I, 'coords': [(x,20) for x in range(3,7)], 'rot': 'N', 'color':'#00ffff'}

class T:
	"""T - Tetromino behaviour description"""
	def generate():
		return {'type': T, 'coords': [(x,20) for x in range(4,7)]+[(5,21)], 'rot': 'N', 'color':'#800080'}

class L:
	"""L - Tetromino behaviour description"""
	def generate():
		return {'type': L, 'coords': [(x,20) for x in range(4,7)]+[(6,21)], 'rot': 'N', 'color':'#ffa500'}

class J:
	"""J - Tetromino behaviour description"""
	def generate():
		return {'type': J, 'coords': [(x,20) for x in range(4,7)]+[(4,21)], 'rot': 'N', 'color':'#0000ff'}

class S:
	"""S - Tetromino behaviour description"""
	def generate():
		return {'type': S, 'coords': [(4,20),(5,20), (5,21),(6,21)], 'rot': 'N', 'color':'#00ff00'}

class Z:
	"""Z - Tetromino behaviour description"""
	def generate():
		return {'type': Z, 'coords': [(5,20),(6,20), (4,21),(5,21)], 'rot': 'N', 'color':'#ff0000'}
		
class O:
	"""O - Tetromino behaviour description"""
	def generate():
		return {'type': O, 'coords': [(5,20),(6,20), (5,21),(6,21)], 'rot': 'N', 'color':'#ffff00'}
		

class GameDashboard(Frame):
	"""
Definition of the frame containing all the information the player needs for the gameplay, except other player's boards.

init(master, blocksize=30, level=1)
    master is the parent of the frame
    blocksize is the size of the x*x block of which each Tetromino is built of, scales the canvas
    level is the initial game difficulcity (speed and scoring multiplier)

"""
	def __init__(self, master, blocksize=30, level=1):
		Frame.__init__(self)
		self.blocksize = blocksize
		self.level=level

		#Different lock object for gameplay and network interferences
		self.netLock = threading.Lock()
		self.gameLock = threading.Lock()

		#Is the player in the game right now?
		self.ingame = False
		self.paused = False

		self.gameThread=None

		#Default background color
		self.bg="black"

		#The main canvas and the map of the game
		self.can = Canvas(self, width=10*blocksize, height=20*blocksize, bg=self.bg)
		
		#The hold canvas
		self.hold_can = Canvas(self, width=6*blocksize, height=4*blocksize, bg=self.bg)

		#Canvas of the next pieces
		self.queue_can = Canvas(self, width=6*blocksize, height=20*blocksize, bg=self.bg)
		self.queue_can.create_rectangle(0,0,7*blocksize,100, fill="cyan")
		self.bag=Bag(self.queue_can, blocksize)

		#Widget placements
		self.hold_can.grid(row=0, column=0, padx=5, pady=5, sticky=N)
		self.can.grid(row=0, column=1, pady=5, rowspan=5)
		self.queue_can.grid(row=0, column=2, columnspan=5, padx=5, pady=5, sticky = N)


		#Bindings
		#self.bind("<Destroy>", self._destroy)
		self.master.protocol("WM_DELETE_WINDOW", self._destroy)
		self.master.bind("<Down>", self.arrow_down)
		# self.master.bind("<Right>", self.arrow_right)
		# self.master.bind("<Left>", self.arrow_left)
		self.master.bind("<space>", self.button_space)

		#Button for test
		self.startButton = Button(self, text="PLAY", command=self.start_new_game)
		self.startButton.grid(row=0)

	def _destroy(self):
		if self.ingame:
			self.gameThread.call_quit()
		self.master.after(200,self.master.destroy)

	def start_new_game(self):
		if not self.ingame:
			self.ingame=True
			self.bag.start()
			self.gameThread=GameEngine(self, self.can, self.blocksize, self.level,self.bag)
			self.gameThread.start()

	def arrow_down(self, event):
		if self.ingame and not self.paused:
			self.gameThread.call_soft_drop()

	def arrow_right(self, event):
		if self.ingame and not self.paused:
			self.gameThread.call_move_right()

	def arrow_left(self, event):
		if self.ingame and not self.paused:
			self.gameThread.call_move_left()

	def button_space(self, event):
		if self.ingame and not self.paused:
			self.gameThread.call_hard_drop()

class GameEngine(threading.Thread):
	"""docstring for GameEngine"""
	def __init__(self, boss, can, blocksize, level,bag, left=Key.left, right=Key.right):
		threading.Thread.__init__(self)
		self.boss = boss
		self.can = can
		self.blocksize = blocksize
		self.level = level
		self.bag=bag

		#Button bindings
		self.left=left
		self.right=right

		#Game Phase tracker
		self.phase="Inactive"

		#Window closed?
		self.abandon=False

		#Game Matrix
		#A: Active Tetromino
		#B: Block
		#E: Marked for elimination
		self.GM = [[0]*40 for x in range(10)]

		#Initialize the active Tetromino's namespace
		self.active=None
		#The ghost piece
		self.ghost=None

		self.bonuses=["Single","Double","Triple","Tetris","Mini T-Spin","Mini T-Spin Single","T-Spin","T-Spin Single","T-Spin Double","T-Spin Triple","Back-to-Back Bonus","Soft Drop","Hard Drop"]
		self.multiplier=[100,300,500,800,100,200,400,800,1200,1600, 0.5, 1,2]
		self.score={}
		self.gameScore=0

		
		# When any single button is then released, the Tetrimino should again move in the direction still held,
		# with the Auto-Repeat delay of roughly 0.3 seconds applied once more.
		self.auto_repeat_delay=0.3
		self.auto_repeat_speed=0.04

		# The method to repeat
		self.to_repeat=None
		
		# Can we be repeating yet?
		self.timer_repeat=0
		# secondary timer for the repeat phase
		self.last_repeat=0

		# Keyboard listening
		self.pressed=False
		self.held={}

		self.kb_listen=Listener(on_press=self.on_press, on_release=self.on_release)
		self.kb_listen.start()

	def on_press(self, key):
		if self.pressed==key:
			return True
		else:
			if key==Key.left:
				self.pressed=key
				self.to_repeat=self.move_left
				self.held[key]=True
			elif key==Key.right:
				self.pressed=key
				self.held[key]=True
				self.to_repeat=self.move_right


	def on_release(self,key):
		if self.pressed==key:
			self.pressed=False
			self.last_repeat=0
			self.timer_repeat=0
			self.held[key]=False

		# Check if another key was held through a press-release
		for key in self.held:
			if self.held[key]:
				self.on_press(key)
				break


	def call_quit(self):
		self.abandon=True

	def run(self):
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
					print("Locked!")
				else:
					print("OVER")
					break
		except AbandonException:
			print("Player abandoned.")
		except GameOverException:
			print("The game was over.")
		except Exception as e:
			print(e)


	def call_soft_drop(self):
		"Set flag for a Soft Drop"
		if self.phase not in ("falling", "locking"):
			return
		self.soft_drop_flag=True

	def soft_drop(self):
		self.soft_drop_flag=False
		now=time.time()
		if now-self.last_linedrop<(self.speed/20):
			return
		else:
			if not self.touching_surface():
				self.last_linedrop=now
				self.linedrop()

	def call_hard_drop(self):
		"Set flag for a Hard Drop"

		if self.phase not in ("falling", "locking"):
			return
		self.hard_drop_flag=True

	def hard_drop(self):
		#How much is it possible to drop?
		distance=self.distance_from_surface()

		[self.linedrop() for x in range(distance)]
		self.score['Hard Drop']=distance
		self.lock_down()
		self.hard_drop_flag=False

	def distance_from_surface(self):
		"Finds the lowest distance between an open surface and the active Tetromino"
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

	def rotate_cw(self):
		"Clockwise rotation event listener"
		pass
	def rotate_ccw(self):
		"Counter-clockwise rotation event listener"
		pass

	def call_move_right(self):
		"Set flag for moving the Tetromino to the right direction"
		if self.phase not in ("falling", "locking"):
			return
		self.move_right_flag=True

	def move_right(self):
		"Attemps to move the Tetromino one block right. Returns True if successful and False if not."
		self.move_right_flag=False
		for x,y in self.active['coords']:
			if x==9:return False
			if self.GM[x+1][y]=='B':return False

		self.last_action=time.time()
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
		self.ghost_adjust()
		return True

	def call_move_left(self):
		"Set flag for moving the Tetromino to the left direction"

		if self.phase not in ("falling", "locking"):
			return
		self.move_left_flag=True

	def move_left(self):
		"Attemps to move the Tetromino one block left. Returns True if successful and False if not."
		self.move_left_flag=False
		for x,y in self.active['coords']:
			if x==0:return False
			if self.GM[x-1][y]=='B':return False

		self.last_action=time.time()
		
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
		self.ghost_adjust()
		return True

	def ghost_adjust(self):
		distance=self.distance_from_surface()
		bs=self.blocksize
		i=0
		for x,y in self.active['coords']:
			self.can.coords(self.ghost[i],2+(bs*x),-(y-19-distance)*bs,2+bs+(bs*x), -(y-20-distance)*bs)
			i+=1

	def generation_phase(self):
		"""
Note: Pixels shown above the skyline (Point 3 below) currently not planned. - dev

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

		bs=self.blocksize

		#Game speed
		self.speed=(0.8 - ((self.level - 1) * 0.007))**(self.level - 1)
		#Score in each turn will be logged in a dictionary
		self.score={}
		#Lowest line tracker
		self.lowest_line_reached=21

		#### Flags ####
		#Did a hard drop occur?
		self.hard_drop_flag=False
		#Soft drop?
		self.soft_drop_flag=False
		#Move?
		self.move_left_flag=False
		self.move_right_flag=False

		#Action counter in locking phasee
		self.counter=0

		#Timing the soft drop
		self.last_linedrop=0

		#Timing of the last action (move/rotate, NOT drop)
		self.last_action=time.time()

		### Pick up the next tetromino from the Next Queue
		self.active=self.bag.next().generate()

		if self.block_out(self.active['coords']):
			self.game_over()
			return

		self.active['objects']=[]
		for x,y in self.active['coords']:
			self.GM[x][y]='A'
			self.active['objects'].append(self.can.create_rectangle(2+(bs*x),-(y-19)*bs,2+bs+(bs*x), -(y-20)*bs, fill=self.active['color']))
		print(self.active)
		distance=self.distance_from_surface()
		self.ghost=[]
		for x,y in self.active['coords']:
			self.ghost.append(self.can.create_rectangle(2+(bs*x),-(y-19-distance)*bs,2+bs+(bs*x), -(y-20-distance)*bs, outline=self.active['color']))
		#self.ghost={'coords':[self.active['coords'][x][0], self.active['coords'][x][1]-distance_from_surface]}
		return 1

	def falling_phase(self):
		"During falling, the player can rotate, move sideways, soft drop, hard drop or hold the Tetromino"

		while self.phase=="falling":
			if self.abandon:raise AbandonException()
			if self.boss.paused: continue

			#Hard Drop?
			if self.hard_drop_flag:
				self.hard_drop()
				return True

			#Atop Surface?
			if self.touching_surface():
				#return to main cycle
				return False
			#Soft Drop?
			if self.soft_drop_flag:
				self.soft_drop()
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

			else:
				now=time.time()
				if now-self.last_linedrop>=self.speed:
					self.last_linedrop=now
					self.linedrop()

		raise "Only the run() method should set the phase flag"


	def linedrop(self):
		"Let the tetromino fall down one line. WARNING: This function does not check circumstances."
		#Backend
		#Writing into both the self.active and the main matrix
		new_coords=[]
		for x,y in self.active['coords']:
			new_coords.append((x,y-1))
			self.GM[x][y]=0
		self.active['coords']=new_coords[:]
		for x,y in new_coords:
			self.GM[x][y]='A'

		#Visual
		for block in self.active['objects']:
			self.can.move(block, 0, self.blocksize)

	def lock_phase(self):
		"During lock phase the player still rotate or move according to Extendended Placement Lockdown\nLock after: 0.5s\nAction limit: 15 actions"
		
		self.last_action=time.time()
		while self.phase=="locking":##time.time()-timer<0.5:
			if self.abandon:raise AbandonException()
			if self.boss.paused: continue

			if self.counter==15:
				self.lock_down()
				print("FORCED DOWN")
				return True
			#Hard Drop?
			if self.hard_drop_flag:
				self.hard_drop()
				return True

			#Atop Surface?
			if not self.touching_surface():
				#return to main cycle
				return False

			#Soft Drop?
			#Once the surface is reached, Soft Drop should not auto-repeat, rather just wait out the 0.5 sec to lock down.

			if self.pressed:
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
					if act:self.counter+=1

			else:
				if time.time()-self.last_action>=0.5:
					self.lock_down()
					return True


	def lock_down(self):
		for x,y in self.active['coords']:
			self.GM[x][y]='B'
		for x in self.ghost:
			self.can.delete(x)

	def pattern_phase(self):
		"""
In this phase, the engine looks for patterns made from Locked Down Blocks in the Matrix. Once a pattern has been matched, it can trigger any number of Tetris variant-related effects.
The classic pattern is the Line Clear pattern.
This pattern is matched when one or more rows of 10 horizontally aligned Matrix cells are occupied by Blocks.
The matching Blocks are then marked for removal on a hit list.
Blocks on the hit list are cleared from the Matrix at a later time in the Eliminate Phase.
This phase takes up no apparent game time.
"""
		pass

	def eliminate_phase(self):
		"""
Involves animation.

Any Minos marked for removal, i.e., on the hit list, are cleared from the Matrix in this phase.
If this results in one or more complete 10-cell rows in the Matrix becoming unoccupied by Minos,
then all Minos above that row(s) collapse, or fall by the number of complete rows cleared from the Matrix.
Points are awarded to the player according to the Tetris Scoring System, as seen in the Scoring section.
"""
		pass

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
		raise GameOverException()

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
		self.objects=[]
		self.blocksize=blocksize*(8/10)

	def start(self):
		"Initialize the first Bag and Next Queue"
		self.bag=self.minos.copy()
		shuffle(self.bag)
		self.next_queue=self.bag[:6]
		for i in self.next_queue:
			self.queue_forward(i, False)
		del self.bag[:6]
		
	def next(self):
		"Return the next tetromino for the Game Engine, and step the que forward"
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
		"Delete (optionally) the top tetromino, Move each Tetromino up by one in the que, and place the next to the end of queue\nqueue_forward(mino, delete=True)\nmino:Tetromino-type ref\ndelete: delete the top piece"
		if delete:
			for i in self.objects[0]:
				self.queue_can.delete(i)
		for i in self.objects:
			for j in i:
				self.queue_can.move(j, 0, -100)
		bs=self.blocksize
		curr=mino.generate()
		self.objects.append([self.queue_can.create_rectangle(-40+(bs*x),570-(y-19)*bs,-40+bs+(bs*x), 570-(y-20)*bs, fill=curr['color']) for x,y in curr['coords']])


class AbandonException(Exception):
	"""Exception occurs when the player quits during an ongoing (either paused or unpaused) game. This serves the purpose of closing down threads."""
	pass
class GameOverException(Exception):
	"""Exception occurs when the game is over. This serves the purpose of closing down threads."""
	pass

if __name__ == '__main__':
	root=Tk()
	fr=GameDashboard(root)
	fr.pack()
	root.title("Tetrícia")
	root.mainloop()


#TODO
#The bag is doing some crazy shit
#SRS