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
		#Default background color
		self.bg="black"

		#The main canvas and the map of the game
		self.can = Canvas(self, width=10*blocksize, height=20*blocksize, bg=self.bg)
		self.GM = [[0]*40 for x in range(10)] #GameMatrix
		
		#The hold canvas
		self.hold_can = Canvas(self, width=6*blocksize, height=4*blocksize, bg=self.bg)

		#Canvas of the next pieces
		self.queue_can = Canvas(self, width=6*blocksize, height=20*blocksize, bg=self.bg)

		self.hold_can.grid(row=0, column=0, padx=5, pady=5, sticky=N)
		self.can.grid(row=0, column=1, pady=5, rowspan=5)
		self.queue_can.grid(row=0, column=2, columnspan=5, padx=5, pady=5, sticky = N)

	def soft_drop(self):
		"Soft drop event on Arrow Down pressed"
		pass

	def hard_drop(self):
		"Hard drop event on Space pressed"
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
		### Generation phase code ###
		###
		###

		self.falling_phase()

	def falling_phase(self):
		"During falling, the player can rotate, move sideways, soft drop, hard drop or hold the Tetromino"
		pass


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
#Speed : (0.8 - ((level - 1) * 0.007))**(level - 1)
if __name__ == '__main__':
	root=Tk()
	fr=GameDashboard(root)
	fr.pack()
	root.title("Tetrícia")
	root.mainloop()