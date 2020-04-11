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
from random import randrange,choice
import threading,time

class I:
	"""I - Tetromino behaviour description"""
	def generate():
		return {'coords': [(x,20) for x in range(3,7)], 'rot': 'N', 'color':'lightblue'}
		
		

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

		#Widget placements
		self.hold_can.grid(row=0, column=0, padx=5, pady=5, sticky=N)
		self.can.grid(row=0, column=1, pady=5, rowspan=5)
		self.queue_can.grid(row=0, column=2, columnspan=5, padx=5, pady=5, sticky = N)


		#Bindings
		self.master.bind("<Down>", self.arrow_down)

		#Button for test
		self.startButton = Button(self, text="PLAY", command=self.start_new_game)
		self.startButton.grid(row=0)

	def start_new_game(self):
		self.gameThread=GameEngine(self, self.can, self.blocksize, self.level)
		self.gameThread.start()

	def arrow_down(self, event):
		if self.ingame and not self.paused:
			self.gameThread.soft_drop()


class GameEngine(threading.Thread):
	"""docstring for GameEngine"""
	def __init__(self, boss, can, blocksize, level):
		threading.Thread.__init__(self)
		self.boss = boss
		self.can = can
		self.blocksize = blocksize
		self.level = level

		#Game Phase tracker
		self.phase="Inactive"

		#Timing the soft drop
		self.last_soft_drop=0

		#Game speed
		self.speed=(0.8 - ((self.level - 1) * 0.007))**(self.level - 1)

		#Game Matrix
		#A: Active Tetromino
		self.GM = [[0]*40 for x in range(10)]

		#The way it works
		self.minos={'I':I}

		#Initialize the active Tetromino's namespace
		self.active=None
		print("YES")

	def run(self):
		self.boss.ingame=True
		self.generation_phase()


	def soft_drop(self):
		"Soft drop event on Arrow Down pressed"
		print("Soft drop")
		now=time.time()
		if now-self.last_soft_drop<(self.speed/20):
			return
		else:
			if not self.touching_surface():
				self.last_soft_drop=now
				self.down_one_row()

	def hard_drop(self):
		"Hard drop event on Space pressed"
		pass

	def rotate_cw(self):
		"Clockwise rotation event listener"
		pass
	def rotate_ccw(self):
		"Counter-clockwise rotation event listener"
		pass

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

		#Set the phase
		self.phase = "Generate"
		### Choose the Tetromino - probably should make it pseudo-random?
		bs=self.blocksize
		### Choosing the tetromino - "bag" should be implemented
		self.active=choice(list(self.minos.values())).generate()
		if self.block_out(self.active['coords']):
			self.game_over()
			return

		self.active['objects']=[]
		for x,y in self.active['coords']:
			self.GM[x][y]='A'
			self.active['objects'].append(self.can.create_rectangle(0+(bs*x),-bs,bs+(bs*x), 0, fill="blue"))
		print(self.active)
		self.falling_phase()

	def falling_phase(self):
		"During falling, the player can rotate, move sideways, soft drop, hard drop or hold the Tetromino"
		if self.touching_surface():
			print("HERE111")
			self.lock_phase()
			return
		else:
			print("HERE")
			self.down_one_row()
	
		print("HERE1")
		time.sleep(self.speed)
		self.falling_phase()

	def down_one_row(self):
		
		#Backend
		#Refreshing both the self.active and the main matrix
		new_coords=[]
		for x,y in self.active['coords']:
			new_coords.append((x,y-1))
			self.GM[x][y]=0
		self.active['coords']=new_coords[:]
		for x,y in new_coords:
			self.GM[x][y]='A'

		#Visual
		for block in self.active['objects']:
			self.can.move(block, 0, 30)

	def lock_phase(self):
		"During lock phase the player still rotate or move according to Extendended Placement Lockdown\nLock after: 0.5s\nAction limit: 15 actions"
		pass

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
		pass
		
if __name__ == '__main__':
	root=Tk()
	fr=GameDashboard(root)
	fr.pack()
	root.title("Tetrícia")
	root.mainloop()