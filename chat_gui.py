#! python3
# GUI for chat client
from tkinter import *
import socket, sys, threading,time,struct, tkinter.colorchooser, os, getpass
from tkinter import font,filedialog, messagebox
from PIL import Image, ImageTk
import tkinter.ttk as ttk

class ChatGui(Frame):
    """A frame for the flow of chat"""
    def __init__(self, master,host, port, name):
        Frame.__init__(self)
        self.data = [StringVar(),StringVar(),StringVar()]
        self.data[0].set(host)
        self.data[1].set(port)
        self.data[2].set(name)

        self.master.title('Chat')
        self.master.resizable(0,0)
        #self.master.protocol("WM_DELETE_WINDOW", self._delete_window)
        #self.master.attributes('-fullscreen', True)

        self.initdir='C:/Users/'+getpass.getuser()+'/Desktop'
        self.foreground="#000000"
        self.background="#FFFFFF"
        self.selectbackground='blue'
        self.selectforeground='white'
        self.font=font.Font(family='Comic Sans MS', size=11, weight='bold', slant='roman')

        self.textbox =Text(self, width =50, height =10, foreground=self.foreground, background=self.background,
                             selectforeground=self.selectforeground, selectbackground=self.selectbackground,font=self.font, wrap=WORD)
        self.textbox.grid(row=0,rowspan=100, column=0, pady=5, sticky=E)
        self.scroll =ttk.Scrollbar(self, command =self.textbox.yview)
        self.textbox.configure(yscrollcommand =self.scroll.set)
        self.scroll.grid(column=1, row=0, rowspan=100,  sticky=N+S+W, pady=5)
        #self.textbox=textbox(self, width=70, height=15, foreground=self.foreground, background=self.background, activestyle=NONE,
        #                     selectforeground=self.selectforeground, selectbackground=self.selectbackground, selectmode=EXTENDED)
        self.textbox.bind("<Button-3>", self.popup)
        self.textbox.config(state=NORMAL)
        self.textbox.insert(END, 'Хорошего дня!')
        self.textbox.yview_moveto(1.0)
        self.textbox.config(state=DISABLED)

        self.images=[]
        self.tk_images=[]
        self.imgrefs=[]
        self.full_imgs=[]
        #self.textbox.grid(row=0,rowspan=100, column=1, padx=5, pady=5)

        ######################################################
        #button = Button(self.textbox, text="Click", command=None)
        #self.textbox.window_create(INSERT, window=button)

        ######################################################

        self.help="""Right click in the chat to costumize.
Left click on pictures to save or open them in default size."""
        self.message=StringVar()
        self.e_out=Entry(self, width=49, textvariable=self.message,font=self.font, bd=3,highlightbackground=self.foreground, highlightcolor=self.selectbackground, highlightthickness=2)
        self.e_out.grid(row=101, column=0, pady=5,sticky=E)
        self.e_out.bind('<Return>', self.sendmsg)

        self.b_settings=ttk.Button(self, text="Connection Settings", command=self.settings, state=NORMAL)
        self.b_disconnect=ttk.Button(self, text="Disonnect", command=self.disconnect, state=DISABLED)
        self.b_connect=ttk.Button(self, text="Connect", command=self.connect, state=NORMAL)
        self.b_out=ttk.Button(self, text="Send message", command=self.sendmsg, state=NORMAL)
        self.b_picout=ttk.Button(self, text="Send image", command=self.img_send, state=NORMAL)
        self.b_help=ttk.Button(self, text="Help", command=lambda: messagebox.showinfo('Help', self.help), state=NORMAL)

        self.b_settings.grid(row=0, column=2, padx=10, pady=2, sticky=N+W)
        self.b_disconnect.grid(row=1, column=2, padx=10, pady=2, sticky=N+W)
        self.b_connect.grid(row=2, column=2, padx=10, pady=2, sticky =N+W)
        self.b_out.grid(row=101, column=2, padx=10, pady=5, sticky =N+W)
        self.b_picout.grid(row=101, column=2,pady=5, padx=10, sticky=N+E)
        self.b_help.grid(row=4, column=2,pady=5, padx=10, sticky=N+W)

        self.license=Label(self, text="©Hertendi Áron Levente, 2018")
        self.license.grid(row=3, column=2, padx=10, pady=5, sticky =N+W)

        self.prog_lab_sv=StringVar(self)
        self.prog_iv=IntVar(self)
        self.prog_label=Label(self, textvariable = self.prog_lab_sv)
        self.prog_label.grid(row=60, column=2)
        self.prog=ttk.Progressbar(self, orient="horizontal", length=165, mode="determinate", variable=self.prog_iv)
        self.prog.grid(row=61, column=2)

        #FONTDIRS = [os.path.join(os.environ['WINDIR'], 'Fonts')]
        #for x in FONTDIRS:
        #self.write((os.environ['WINDIR'], 'Fonts'))
        self.grid(row=0, column=0,padx=5, pady=0)
        self.connected = False
        #self.connect()

    def popup(self, event):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Background color", command= lambda: self.set_layout('b'))
        menu.add_command(label="Text color", command= lambda: self.set_layout('f'))
        menu.add_command(label="Selected text background color", command= lambda: self.set_layout('sb'))
        menu.add_command(label="Selected text color", command= lambda: self.set_layout('sf'))
        menu.add_command(label="Font", command= lambda: self.set_layout('font'))
        menu.post(event.x_root, event.y_root)

    def set_layout(self, ground):
        if ground=='f':
            self.foreground = tkinter.colorchooser.askcolor()[1]
        elif ground=='b':
            self.background= tkinter.colorchooser.askcolor()[1]
        elif ground=='sb':
            self.selectbackground= tkinter.colorchooser.askcolor()[1]
        elif ground=='sf':
            self.selectforeground= tkinter.colorchooser.askcolor()[1]
        elif ground=='font':
            SetFontTk(self,self.font)
        self.textbox.config(foreground=self.foreground, background=self.background, selectbackground=self.selectbackground, selectforeground=self.selectforeground)
    
    def set_font(self, font):
        self.font=font
        self.textbox.config(font=self.font)
        self.e_out.config(font=self.font)

    def disconnect(self):
        try:
            self.send(bytes('#fin#', 'utf-8'))
            self.write('Lekapcsolódott.')
        except Exception as e:
            pass
        self.connected=False
        self.b_settings.config(state=NORMAL)
        self.b_connect.config(state=NORMAL)
        self.b_disconnect.config(state=DISABLED)
        self.b_out.config(state=DISABLED)
        self.b_picout.config(state=DISABLED)

    def connect(self):
        self.connection=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.write("Connecting... - IPv4: {0}, Port: {1}".format(self.data[0].get(),self.data[1].get()))
        HOST, PORT=self.data[0].get(),int(self.data[1].get())
        try:
            self.connection.connect((HOST, PORT))
        except socket.error as e:
            self.write(str(e))
            self.write("Couldn't reach server.")
            self.disconnect()
            return
        self.write("Successful connection.")
        self.master.set_connection(self.connection)
        self.connection.send(bytes(self.data[2].get(), 'utf-8'))
        asd=self.connection.recv(1024).decode('utf-8')
        print(asd)
        self.data[2].set(asd)
        self.connected=True
        self.e_out.focus()
        self.b_settings.config(state=DISABLED)
        self.b_disconnect.config(state=NORMAL)
        self.b_out.config(state=NORMAL)
        self.b_picout.config(state=NORMAL)
        self.b_connect.config(state=DISABLED)
        self.th_rec=ThreadReception(self.connection, self)
        #self.th_emis=ThreadEmission(self.connection, self)
        self.th_rec.start()
        self.send(bytes('online.get', 'utf-8'))
        #self.th_emis.start()
    def prog_setter(self,x, length):
        self.prog_iv.set(x)
        self.prog_lab_sv.set("{0} %".format(int(x/length*100)))  #{:.2f}
        if (x/length)==1:
            self.prog_lab_sv.set(self.prog_lab_sv.get()+" processed!")
    def prog_getter(self):
        return self.prog_iv.get()

    def sendmsg(self, event=None):
        if self.connected:
            if len(self.message.get())>0:
                self.write(self.data[2].get()+'> '+self.message.get())
                self.send(bytes(self.message.get(), 'utf-8'))
                self.message.set('')
        else:
            self.write('Sending message unsuccessful, please connect...')


    def img_send(self):
        imgfile =  filedialog.askopenfilename(initialdir = self.initdir,title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png")))
        if imgfile!='':
            self.initdir=imgfile
            mode, size=Image.open(imgfile).mode, Image.open(imgfile).size
            self.images.append(Image.open(imgfile).tobytes())
            self.sending=self.images[-1]
            self.send(bytes("#pic#"+str(len(self.sending))+"#pic#"+str(mode)+"#pic#"+str(size[0])+"#pic#"+str(size[1]), 'utf-8'))
            self.prog['maximum']=len(self.sending)
            send_th=ThreadEmission(self.connection, self, self.sending)
            send_th.start()
            
            #self.send(sending)
            self.img_show(imgfile, mode, size[0], size[1],self.data[2].get())


    def img_show(self, imgfile, mode, size0, size1, name):
        self.write('')
        self.full_imgs.append(Image.frombytes(mode,(size0,size1),self.images[-1]))
        self.imgTk=ImageTk.PhotoImage(image=self.resized(self.full_imgs[-1]))
        self.tk_images.append(self.imgTk)
        ##### INSERTION
        self.imgrefs.append((self.textbox.image_create(END, image=self.imgTk),len(self.imgrefs), imgfile))
        self.textbox.tag_add('pic'+str(self.imgrefs[-1][1]), self.imgrefs[-1][0])
        self.textbox.config(state=NORMAL)
        self.textbox.yview_moveto(1.0)
        self.textbox.insert(END, ' ('+name+')')
        self.textbox.config(state=DISABLED)
        x=self.imgrefs[-1]
        self.textbox.tag_bind('pic'+str(self.imgrefs[-1][1]), '<Button-1>', lambda func: self.img_popup(func, x))

    def img_popup(self, event, img):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Show", command= lambda: self.img_show_full(img[1]))
        menu.add_command(label="Save", command= lambda: self.img_save(img))
        menu.post(event.x_root, event.y_root)

    def img_show_full(self, img):
        self.full_imgs[img].show()
        self.textbox.yview_moveto(1.0)
        self.textbox.mark_set(INSERT, END)

    def img_save(self,img):
        filepath= filedialog.asksaveasfilename(parent=self,initialfile=img[2], defaultextension="*.jpg", initialdir = self.initdir,title = "Choose dir",filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
        if bool(filepath):
            self.initdir=filepath
            self.full_imgs[img[1]].save(fp=filepath)
            self.write("Mentve: "+filepath)


    def resized(self, img):
        if img.width>self.textbox.winfo_width():
            multip=img.width/self.textbox.winfo_width()
            size = int(img.width/multip), int(img.height/multip)
            img=img.resize(size)
        if img.height>self.textbox.winfo_height():
            multip=img.height/self.textbox.winfo_height()
            size = int(img.width/multip), int(img.height/multip)
            img = img.resize(size)
        return img
    def write(self, text):
        self.textbox.config(state=NORMAL)
        self.textbox.insert(END, '\n'+text)
        self.textbox.yview_moveto(1.0)
        self.textbox.config(state=DISABLED)

        
    def _delete_window(self):
        try:
            self.send(bytes('#fin#', 'utf-8'))
        except Exception as e:
            pass
        finally:
            self.master.destroy()

    def settings(self):
        self.costumize=Toplevel(self)
        self.costumize.grab_set()
        labels=['IP cím: ','Port: ', 'Név: ']
        for x in range(3):
            labels[x]=Label(self.costumize, text = labels[x])
            labels[x].grid(row=x, column=0,sticky=E)
        entries=[0]*3
        entry_svar=[StringVar(self.costumize),StringVar(self.costumize),StringVar(self.costumize)]
        for x in range(3):
            entries[x]=Entry(self.costumize, textvariable=entry_svar[x])
            entry_svar[x].set(self.data[x].get())
            entries[x].grid(row=x, column=1)
        b_confirm=ttk.Button(self.costumize, command= lambda :self.save(self.costumize, entry_svar), text="OK")
        b_confirm.grid(row=1, column=3, padx=10)
        self.costumize.title('Beállítások')
        self.costumize.geometry("+%d+%d" % (self.master.winfo_rootx()+50,
                                  self.master.winfo_rooty()+50))
        self.costumize.protocol("WM_DELETE_WINDOW", self.set_destroyed)
        self.costumize.resizable(0,0)
        self.costumize.transient(self.costumize.master)
    def set_destroyed(self):
        self.costumize.destroy()
        self.write('A beállítások nem módusltak.')
    def save(self,window, settings):
        window.destroy()
        x= [i.get() for i in self.data]
        self.data=settings
        for i in range(3):
            if self.data[i].get()!=x[i]:
                self.write("Beállítása módosult: "+x[i]+" -> "+self.data[i].get())

    def send(self,msg):
        self.connection.send(bytes(chr(0),'utf-8'))
        self.connection.send(msg)
        self.connection.send(bytes(chr(0),'utf-8'))
        
class SetFontTk(Toplevel):
    """Window returning tk.font.Font()"""
    def __init__(self, master, fonts):
        Toplevel.__init__(self,master)
        self.master = master
        self.font=fonts
        self.grab_set()
        labels=['Betűtítpus: ','Méret: ', 'Stílus: ', '']
        for x in range(4):
            labels[x]=Label(self, text = labels[x])
            labels[x].grid(row=x, column=0, sticky=E)
        self.combos=[0]*4
        self.combo_opts=[font.families(), [9,10,11,12,14,16,18,20],['normal', 'bold'],['roman', 'italic']]
        self.combo_names=['family', 'size', 'weight', 'slant']
        self.entry_svar=[StringVar(self),StringVar(self),StringVar(self),StringVar(self)]
        for x in range(4):
            self.combos[x]=ttk.Combobox(self, textvariable=self.entry_svar[x], values=self.combo_opts[x])
            self.combos[x].grid(row=x, column=1)
            self.entry_svar[x].set(self.font.cget(self.combo_names[x]))
        b_confirm=ttk.Button(self, command= self.end, text="OK")
        b_confirm.grid(row=4, column=1, padx=10)
        self.title('Betűtípus')
        self.geometry("+%d+%d" % (self.master.winfo_rootx()+50,
                                  self.master.winfo_rooty()+50))
        #self.protocol("WM_DELETE_WINDOW", self.set_destroyed)
        self.resizable(0,0)
        self.transient(self.master)
    
    def end(self):
        self.font=font.Font(family=self.combos[0].get(), size=self.combos[1].get(), weight=self.combos[2].get(), slant=self.combos[3].get())
        self.master.set_font(self.font)
        self.destroy()
        

class ThreadReception(threading.Thread):
    """Thread object for receiving messages"""
    def __init__(self, conn, root):
        threading.Thread.__init__(self)
        self.conn = conn                    #ref to socket
        self.root = root
        
    def run(self):
        while True:
            # length=self.conn.recv(100).decode('utf-8')
            # if not length.startswith("#LEN#"):
            #     print(length)
            # self.conn.send(bytes("#OK#", 'utf-8'))
            # length=length.split("#LEN#")[1]
            start=self.conn.recv(1).decode('UTF-8')
            if start!=chr(0):
                print(start)
                if start=="":break
            else:
                inbox=''
                timer1=time.time()
                while True:
                    try:
                        curr=self.conn.recv(1).decode('UTF-8')
                        if curr==chr(0):
                            break
                        # if chr(0) in curr:
                        #     inbox+=curr[:curr.index(chr(0))]
                        #     curr=curr[curr.index(chr(0))+1:]
                        #     break
                        inbox+=curr
                    except Exception as e:
                        print("Log: ", curr, "\nError: ", e)
                print(time.time()-timer1)
            # elif inbox.startswith("#OK#"):
            #     self.root.master.ready=True
            if inbox.startswith("#pic#"):
                self.root.b_picout.config(state=DISABLED)
                img_data=inbox.split("#pic#")
                self.root.prog['maximum']=int(img_data[1])
                img=b''
                a=0
                while a<int(img_data[1]):
                    msgImg=self.conn.recv(4096)
                    img+=msgImg
                    a=len(img)
                    self.root.prog_setter(a, int(img_data[1]))
                self.root.images.append(img)
                self.root.img_show('new', str(img_data[2]), int(img_data[3]), int(img_data[4]), img_data[5])
                self.root.b_picout.config(state=NORMAL)
                time.sleep(2)
                self.root.prog_setter(0,1)
                #########CREATE PROGRESS WINDOW FOR EACH CLIENT TO SHOW PROGRESS
                #self.root.prval=int(inbox.split("#prog#")[1])
            elif inbox.startswith("#PLAYER#"):
                name=inbox.split("#")[-1]
                self.root.master.add_player(name)
            elif inbox.startswith("#GAME#"):
                inbox=inbox.split("#GAME#")
                for x in inbox[1:]:
                    name=x.split("#")[-1]
                    self.root.master.set_player(name, x.split("#")[0:2])
            else:
                self.root.write(inbox)
            ##### pil.image.frombytes
        self.conn.close()
        # Received a final message

class ThreadEmission(threading.Thread):
    """docstring for ThreadEmission"""
    def __init__(self, conn, root,msg):
        threading.Thread.__init__(self)
        self.conn = conn                    #ref to socket
        self.root=root
        self.msg=msg
        self.msglen=len(msg)
        
    def run(self):
        a=0
        self.root.e_out.config(state=DISABLED)
        self.root.b_out.config(state=DISABLED)
        self.root.b_picout.config(state=DISABLED)
        self.root.b_disconnect.config(state=DISABLED)
        while True:
            self.root.prog_setter(self.root.prog_getter()+self.conn.send(self.msg[a*4096:((a+1)*4096)]), self.msglen)
            if self.root.prog_getter()==len(self.msg) :break
            a+=1
        self.root.b_picout.config(state=NORMAL)
        self.root.b_out.config(state=NORMAL)
        self.root.e_out.config(state=NORMAL)
        self.root.b_disconnect.config(state=NORMAL)
        time.sleep(2)
        self.root.prog_setter(0,1)

def chat_main():
    root=ChatGui(None,'erin-PC', '64164', socket.gethostname()+'\\'+getpass.getuser())
    #root=ChatGui('aronsv.ddns.net', '45000', socket.gethostname()+'\\'+getpass.getuser())
    root.mainloop()
    
    ####WRITEFILE
if __name__ == '__main__':
    chat_main()
