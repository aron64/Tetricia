from gameobjects import *
class OpponentDashboard(GameEngine,Frame):
	"""docstring for OpponentDashboard"""
	def __init__(self, master,blocksize):
		Frame.__init__(self)
		#threading.Thread.__init__(self)
		#Default background color
		self.boss=self
		self.master=master
		self.bg="black"
		self.blocksize=blocksize
		#The main canvas and the map of the game
		self.can = Canvas(self, width=10*blocksize, height=20*blocksize+5, bg=self.bg)
		self.can.create_line(0,0,10*blocksize, 0, fill="white")
		self.can.yview_scroll(22, 'units')
		self.change_lock=threading.Lock()
		#The hold canvas
		self.hold_can = Canvas(self, width=6*blocksize, height=4*blocksize, bg=self.bg)

		#Canvas of the next pieces
		self.queue_can = Canvas(self, width=6*blocksize, height=20*blocksize+5, bg=self.bg)
		self.queue_can.create_rectangle(0,0,7*blocksize,100, fill="cyan")
		#self.bag=Bag(self.queue_can, blocksize)

		#Widget placements
		self.hold_can.grid(row=0, column=0,columnspan=2, padx=5, pady=5, sticky=N)
		self.can.grid(row=0, column=2, pady=5, rowspan=5)
		self.queue_can.grid(row=0, column=3, rowspan=5, padx=5, pady=5, sticky = N)

		#Font
		self.font=font.Font(family='Comic Sans MS', size=12, weight='bold', slant='roman')
		#Labels:
		self.label_frame=Frame(self)
		self.label_frame.grid(row=4, column=0)
		Label(self.label_frame,text="Points: ",font=self.font).grid(row=1, column=0, sticky="SW")
		Label(self.label_frame,text="Level: ",font=self.font).grid(row=2, column=0, sticky="SW")
		Label(self.label_frame,text="Lines cleared: ",font=self.font).grid(row=3, column=0, sticky="SW")
		self.l_points=Label(self.label_frame,text="0",font=self.font)
		self.l_levels=Label(self.label_frame,text="1",font=self.font)
		self.l_lines=Label(self.label_frame,text="0",font=self.font)

		self.l_points.grid(row=1, column=1, sticky="SW")
		self.l_levels.grid(row=2, column=1, sticky="SW")
		self.l_lines.grid(row=3, column=1, sticky="SW")

		self.GM = [[0]*40 for x in range(10)]
		self.OGM = [[0]*40 for x in range(10)]
		self.active = None
		self.actions=[]

		self.online=False #Because of inheritance
		
		self.commands = {"COORDS":self.set_coords,
						 "ELIM":self.set_eliminate,
						 "NEW": self.new_mino,
						 "STAT":self.set_statistics,
						 "LOCK":self.lock_down,
						 "HOLD":self.hold,
						 "OVER":self.over,
						 "ATTACK": self.attacked,
						 "LIFT": self.lift}

	def attacked(self, num):
		"The player, not opponent received a line attack"
		num=int(num)
		self.master.panel.gameThread.receive_attacks(num)

	def lift(self, gap="0"):				#XD
		"This opponent received a line attack"
		gap=int(gap)
		bs=self.blocksize
		for x in range(10):
			for y in range(40):
				if self.OGM[x][y]!=0:
					self.can.move(self.OGM[x][y], 0, -self.blocksize)
		for x in range(10):
			del self.GM[x][39]
			del self.OGM[x][39]
			if x == gap:
				self.GM[x][0:0]=[0]
				self.OGM[x][0:0]=[0]
				continue
			self.GM[x][0:0]=['B']
			self.OGM[x][0:0]=[self.can.create_rectangle(2+(bs*x),(19)*bs,2+bs+(bs*x), (20)*bs, fill="darkgray", outline="gray")]

		
	def hold(self):
		"The player held his Tetromino"

		if self.ghost:
			for i in self.ghost:
				self.can.delete(i)

		for x,y in self.active['coords']:
				self.GM[x][y]=0
		for i in self.active['objects']:
			self.can.delete(i)

		self.place_hold(self.active['type'])

	def run(self):
		self.change_lock.acquire()
		for item in self.actions:
			action=item[0]
			forward=item[1]
			if forward!='0':
				self.commands[action](forward)
			else:
				self.commands[action]()
		self.actions=[]
		self.change_lock.release()

	def log(self,msg):
		"Action log receiving function. Runs the action on the panel."
		# action=msg[0]
		# forward=msg[1]
		self.change_lock.acquire()
		self.actions.append(msg)
		self.change_lock.release()
		# if forward!='0':
		# 	self.commands[action](forward)
		# else:
		# 	self.commands[action]()

	def over(self):
		exit()

	def new_mino(self, mino):
		"Function to receive the type and coords of the new mino"
		bs=self.blocksize
		self.active=eval(mino).generate()
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

	def set_coords(self, coords):
		"Function to receive the opponent's matrix"
		coords=eval(coords)
		bs=self.blocksize
		for x,y in self.active['coords']:
			self.GM[x][y]=0
		self.active['coords']=coords
		for x,y in self.active['coords']:
			self.GM[x][y]='A'
		for i in range(4):
			x,y=self.active['coords'][i]
			self.can.coords(self.active['objects'][i],2+(bs*x),-(y-19)*bs,2+bs+(bs*x), -(y-20)*bs)

		self.ghost_adjust()

	#self.lock_down gets called by server, then eliminate

	def set_eliminate(self, lines):
		lines=eval(lines)
		self.eliminate=lines
		self.clear_marked_lines()

	def set_statistics(self, stats):
		stats=eval(stats)
		self.l_points.config(text=stats[0])
		self.l_levels.config(text=stats[1])
		self.l_lines.config(text=stats[2])

	def _destroy(self):
		pass#raise AbandonException()

#a=OpponentDashboard(1)
#a.start()