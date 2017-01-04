import random
#import os
import tkinter as tk

class AdventureGame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, 
                          master, 
                          width=1000,
                          height=200)

        self.master.title('Daycare Game')
        self.pack_propagate(0)
        self.pack()
        self.greeting_var = tk.StringVar()
        self.greeting_var.set('N')

        # Question for user input
        self.question_var = tk.StringVar()
        self.question_var.set('go where?')
        self.question = tk.Label(self, textvariable=self.question_var)
        
         # The nextaction for where to go
        self.nextaction_var = tk.StringVar()
        self.nextaction = tk.Entry(self,
                                  textvariable=self.nextaction_var)
        self.nextaction_var.set('N')

        # Status of last action
        self.status_var = tk.StringVar()
        self.status_var.set('status')
        self.status = tk.Label(self, textvariable=self.status_var)

        # The go button
        #self.go_button = tk.Button(self,
                                   #text='Go',
                                   #command=self.game_action)
        self.master.bind('<Return>', self.game_action)
        self.go_button = tk.Button(self,
                                   text='Go')
        self.go_button.bind('<Return>', self.game_action)

        # Put the controls on the form
        self.go_button.pack(fill=tk.X, side=tk.BOTTOM)
        self.question.pack(fill=tk.X, side=tk.TOP)
        self.nextaction.pack(fill=tk.X, side=tk.TOP)
        self.status.pack(fill=tk.X, side=tk.TOP)
                
        self.init_game()
                   
    def print_status(self, text):
        self.status_var.set(text)
        print('%s' % text)

    def print_question(self, text):
        self.question_var.set(text)
        print('%s' % text)
        
    def msg(self, room):
        if room['msg'] == '':
            return "You have entered the " +room['name'] + ' ' + room['description'] + '.'
        else:
            return room['msg']
            
    def get_choice(self, room, dir):
        if dir=='N':
            choice = 0
        elif dir=='E':
            choice = 1
        elif dir=='S':
            choice = 2
        elif dir=='W':
            choice = 3
        else:
            return -1
            
        if room['directions'][choice] == 0:
            return 4
        else:
            return choice
            
    def init_game(self):
        self.dirs = (0,0,0,0)
    
        self.entrance = {'name':'Entrance Way','directions':self.dirs,'msg':'','description':''}
        self.classroom = {'name':'Classroom','directions':self.dirs,'msg':'','description':'where the kids can learn and expand their mental facilities'} 
        self.hallway = {'name':'Hallway','directions':self.dirs,'msg':'','description':''}
        self.kitchen = {'name':'Kitchen','directions':self.dirs,'msg':'','description':'where the staff make the kids\' lunch and food'}
        self.cafeteria = {'name':'Cafeteria','directions':self.dirs,'msg':'','description':'where the kids eat their snack and lunch'}
        self.tech_room = {'name':'Tech Room','directions':self.dirs,'msg':'','description':'where the kids can learn how to type or play during freetime'}
        self.nap_room = {'name':'Nap Room','directions':self.dirs,'msg':'','description':'where the kids sleep'}
        self.closet1 = {'name':'Closet 1','directions':self.dirs,'msg':'','description':'where cleaning supplies are kept'}
        self.closet2 = {'name':'Closet 2','directions':self.dirs,'msg':'','description':'where kitchen supplies are kept'}
        self.playground = {'name':'Playground','directions':self.dirs,'msg':'','description':'where the kids play'}
    
        #(N,E,S,W)
        self.classroom['directions'] = (self.entrance,self.cafeteria,self.tech_room,0)
        self.tech_room['directions'] = (self.classroom,0,0,0)
        self.hallway['directions'] = (self.cafeteria,self.kitchen,self.nap_room,self.playground)
        self.cafeteria['directions'] = (0,self.closet1,self.hallway,self.classroom)
        self.entrance['directions'] = (0,0,self.classroom,0)
        self.kitchen['directions'] = (self.closet2,0,0,self.hallway)
        self.nap_room['directions'] = (self.hallway,0,0,0)
        self.closet1['directions'] = (0,0,0,self.cafeteria)
        self.closet2['directions'] = (0,0,self.kitchen,0)
        self.playground['directions'] = (0,self.hallway,0,0)
        
        self.rooms = [self.classroom,self.tech_room,self.hallway,self.cafeteria,self.entrance,self.kitchen,self.nap_room,self.closet1,self.closet2,self.playground]
        self.room_with_kid = random.choice(self.rooms)
        self.kid_found = False
        self.stuck = True
        self.room = self.entrance
        self.print_status('Welcome to Tender Moments Daycare. Try to find your kid and leave.')
        self.print_question("Please enter N,E,S, or W? ")
        print('Kid location: %s' % self.room_with_kid['name'])
        
    def game_status(self):
        #while True:
            if self.kid_found and self.room['name'] == 'Entrance Way':
                self.print_status('You\'ve found your kid and found the way out. ')
                self.print_question('You can now leave. Congrats!')
                return;
            elif not self.kid_found and self.room['name'] == self.room_with_kid['name']:
                self.kid_found = True
                self.print_status(self.msg(self.room) + ' There\'s your kid but his best ' +
                      'friend\'s mom is near! Get out before she wants ' +
                      'to talk to you!')
                self.room['msg'] = ('You found you way back to the ' + self.room['name'] +
                               '! You got your kid. Get out before your kid\'s ' +
                               'best friend\'s mom finds you!')
            else:
                self.print_status(self.msg(self.room))
                self.room['msg'] = 'You are back in the ' + self.room['name']
             
    def game_action(self, event):
        #self.stuck = True
        #while stuck:
        #if self.stuck:            
        dir = self.nextaction_var.get()
        print('%s' % dir)
        #input("Which direction do you want to go: N,E,S, or W? ")
        choice = self.get_choice(self.room, dir)
        if choice == -1:
            self.print_status("Please enter N,E,S, or W? ")
            self.print_question("Which direction do you want to go: N,E,S, or W? ")
            return;
        elif choice == 4:
            self.print_status('You cannot go in that direction.')
            self.print_question("Which direction do you want to go: N,E,S, or W? ")
            return;
        else:
            self.room = self.room['directions'][choice]
        self.game_status()

    def run(self):
            self.mainloop()

# Launch the game GUI
app = AdventureGame(tk.Tk())
app.run()
