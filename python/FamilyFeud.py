from cgitb import text
from fileinput import close
import tkinter as tk
import tkinter.ttk as ttk
import json
from functools import partial
from playsound import playsound
import os

#(!)Add ability to make X's show up

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # To Get A Relative File Path On Any OS(Windows, Mac, Linux)

class AnswerBox(ttk.Frame):
    ansFrms = []
    ansLbls = []
    numLbls = []
    ansRevealed = [False] * 8
    prev_font = 0

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.round_over = False

        self.parent = parent
        self.style = parent.style
        self.style.configure('AnswerBox1.TLabel',background='#07125B',foreground='white',font=('Arial',35))
        self.style.configure('AnswerBox2.TLabel',background='#1A36DC',foreground='white',font=('Arial',35))
        self.style.configure('AnswerBox3.TLabel',background='#1A36DC',foreground='white',font=('Arial',35))

        self.bind('<Configure>',self.resize)
        
        self.columnconfigure(0, weight=1)
        self.questionLbl = ttk.Label(self,text='Question',anchor='center',relief='ridge',style='AnswerBox3.TLabel')
        self.questionLbl.grid(row=0,sticky='nsew')

        self.Board = ttk.Frame(self)
        self.Board.grid(sticky='nsew')

        for col in range(2):
            self.Board.columnconfigure(col,weight=1, uniform="fred")
            for row in range(2,6):
                self.Board.rowconfigure(row, weight=1, uniform="fred")
                i = row+col*4-2

                #Creating frame for answer
                self.ansFrms.append(ttk.Frame(self.Board,relief='sunken',borderwidth=5,style='Frame1.TFrame'))
                #Adjusting how the frame resizes when the window is changed
                self.ansFrms[i].grid(padx=(10,10),pady=(10,10),row=row,column=col,sticky='nswe')
                self.ansFrms[i].rowconfigure(0, weight=1)
                self.ansFrms[i].columnconfigure(0,weight=3)
                self.ansFrms[i].columnconfigure(1,weight=0)

                #Creating label for answer to be displayed
                self.ansLbls.append(ttk.Label(self.ansFrms[i],text="Answer", style='AnswerBox1.TLabel'))
                self.ansLbls[i].grid(row=0,column=0)
                self.ansLbls[i].grid_remove()

                #Creating label for number displayed and points
                self.numLbls.append(ttk.Label(self.ansFrms[i],text=str(i+1),anchor='center',style='AnswerBox2.TLabel'))
                self.numLbls[i].grid(row=0,column=0,sticky="nsew")

    #Reveals answer of index given or unreveals answer if the answer was already revealed
    def revealAns(self, index):

        try:
            self.questionSet['answers']
        except:
            return 0

        #Checks if given answer index is out of range of answers on the board.
        if len(self.questionSet['answers']) <= index:
            return 0
        
        #Checks if answer is revealed
        #If self.ansRevealed[index] is False the answer is hidden and needs to be revealed
        if self.ansRevealed[index] == False:

            #Adjusts the collumn weights for the answer index so that where the answer is is larger than the box for the points
            #Note that the uniform = 'fred' is there so that the cells stay the same ratio
            self.ansFrms[index].columnconfigure(0,weight=2, uniform = 'fred')
            self.ansFrms[index].columnconfigure(1,weight=1, uniform = 'fred')

            self.ansLbls[index].grid() #Adds label with answer text to the frame one the board. The label already has the answer text stored in it

            #Changes the text of the number label to the amount of points this answer is worth
            #And changes the relief to look more inline with what family fued looks like
            self.numLbls[index].config(text=str(self.questionSet['answers'][index]['points']),relief='raised')
            self.numLbls[index].grid(row=0,column=1) #Changes the grid position of the number label

            self.ansRevealed[index] = True #Changes this index to true so that next time it will know this answer is revealed

            points = self.questionSet['answers'][index]['points'] #Adds points to point variable so it can be returned to be added to the score
        else: #This is the case that the answer was already revealed
            #Removed the answer label from the frame
            self.ansLbls[index].grid_remove()

            #Reconfigures the column weights back to have only one weighted column
            self.ansFrms[index].columnconfigure(0,weight=3, uniform = '')
            self.ansFrms[index].columnconfigure(1,weight=0, uniform = '')

            #Sets number label back to its board number and flat relief then moves it back to the weighted column
            self.numLbls[index].config(text=str(index+1),relief='flat')
            self.numLbls[index].grid(row=0,column=0)

            self.ansRevealed[index] = False #Changes this index to false so that next time it will know this answer is not revealed

            points = -self.questionSet['answers'][index]['points'] #Adds the points to variable but negative so they will be subtracted from the current score
        #This checks if the round is over 
        #If it is the points should not be changed since at the end of a round all answers are shown
        if not(self.round_over):
            return points
        else:
            return 0

    #Loads a question set into the board and resets board to start position
    #questionSet should be a dictionary with the same layout as from the questions.json file
    def loadQuestionSet(self, questionSet):
        self.questionLbl.config(text=questionSet['question'])
        self.questionSet = questionSet

        self.resetBoard()

        for i in range(8):
            if len(questionSet['answers']) > i:
                self.ansLbls[i].config(text=questionSet['answers'][i]['answer'])
            else:
                self.numLbls[i].config(text='')
        self.resize(None)

    #Clears board of any revealed answers and sets the board up to play again
    def resetBoard(self):
        for i in range(8):
            self.ansLbls[i].grid_remove()

            self.ansFrms[i].columnconfigure(0,weight=3, uniform = '')
            self.ansFrms[i].columnconfigure(1,weight=0, uniform = '')

            self.numLbls[i].config(text=str(i+1),relief='flat')
            self.numLbls[i].grid(row=0,column=0)

        self.ansRevealed = [False] * 8
        self.round_over = False
    
    def endRound(self):
        self.round_over = True

    def resize(self, event):

        #Math for determining min sizes given ethier a width or height of the window. Not perfect and could use tweaking
        width_size=int((self.winfo_width())/12)
        height_size=int((self.parent.parent.winfo_height()-self.parent.score_board.winfo_height())/15)

        if width_size<height_size:
            size = width_size
        else:
            size=height_size

        if self.prev_font==size:
            pass

        self.style.configure('AnswerBox1.TLabel',font=('Arial',int(size*0.6)))
        self.style.configure('AnswerBox2.TLabel',font=('Arial',int(size)))

        try:
            n = 0.01
            questionLen = len(self.questionSet['question'])
            q_width_size=int((self.winfo_width()/questionLen)*1.3)

            if q_width_size<height_size:
                self.style.configure('AnswerBox3.TLabel',font=('Arial',q_width_size))
            else:
                self.style.configure('AnswerBox3.TLabel',font=('Arial',size))

            #self.style.configure('AnswerBox2.TLabel',font=('Arial',int(size*(1/(n*questionLen-n+1)))))
            #print(int(size*(1/(n*questionLen-n+1))))
        except:
            self.style.configure('AnswerBox2.TLabel',font=('Arial',int(size)))
        self.prev_font = size

    def getAnswers(self):
        answers = []
        for answer in self.questionSet['answers']:
            answers.append(answer['answer'])
        return answers

class ScoreBoard(ttk.Frame):
    prev_font = 0
    current_score = 0
    team_one_score = 0
    team_two_score = 0

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.style = parent.style
        self.style.configure('ScoreBoard1.TLabel',background='#1A36DC',foreground='white',font=('Arial',25))
        self.style.configure('ScoreBoard2.TLabel',background='#1A36DC',foreground='white',font=('Arial',25))
        self.bind('<Configure>',self.resize)

        self.columnconfigure((0,1,2,3,4),weight=1, uniform='fred')
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=2)
        #self.columnconfigure((1,2,3),weight=1)

        self.team_one_name_label = ttk.Label(self, text='Team One', style='ScoreBoard1.TLabel',anchor='center',relief='sunken',borderwidth=5)
        self.team_one_score_label = ttk.Label(self, text='0', style='ScoreBoard2.TLabel',anchor='center',relief='sunken',borderwidth=5)
        self.team_one_name_label.grid(row=0,column=0, sticky = 'nsew')
        self.team_one_score_label.grid(row=1,column=0, sticky = 'nsew')

        self.current_score_text_label = ttk.Label(self, text='Current Score', style='ScoreBoard1.TLabel',anchor='center',relief='sunken',borderwidth=5)
        self.current_score_label = ttk.Label(self, text='0', style='ScoreBoard2.TLabel',anchor='center',relief='sunken',borderwidth=5)
        self.current_score_text_label.grid(row=0,column=2, sticky = 'nsew')
        self.current_score_label.grid(row=1,column=2, sticky = 'nsew')

        self.team_two_name_label = ttk.Label(self, text='Team Two', style='ScoreBoard1.TLabel',anchor='center',relief='sunken',borderwidth=5)
        self.team_two_score_label = ttk.Label(self, text='0', style='ScoreBoard2.TLabel',anchor='center',relief='sunken',borderwidth=5)
        self.team_two_name_label.grid(row=0,column=4, sticky = 'nsew')
        self.team_two_score_label.grid(row=1,column=4, sticky = 'nsew')

    def increaseCurrentScore(self, num):
        self.current_score += num
        self.current_score_label.config(text=str(self.current_score))

    def teamScoreAdd(self, team):
        if team == 1:
            self.team_one_score += self.current_score
            self.team_one_score_label.config(text=str(self.team_one_score))
        else:
            self.team_two_score += self.current_score
            self.team_two_score_label.config(text=str(self.team_two_score))
        self.current_score = 0
        self.current_score_label.config(text='0')
    
    def updateName(self, team, name):
        if team == 1:
            self.team_one_name_label.config(text=name)
        else:
            self.team_two_name_label.config(text=name)

    def resize(self, event):

        width_size=int((event.width)/30)
        height_size=int((self.parent.parent.winfo_height()-40)/18)
        if width_size<height_size:
            size = width_size
        else:
            size=height_size
        if self.prev_font==size:
            pass
        
        self.style.configure('ScoreBoard1.TLabel',font=('Arial',int(size*0.6)))
        self.style.configure('ScoreBoard2.TLabel',font=('Arial',size))

        self.prev_font = event.height
            
class GameWindow(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.style = ttk.Style()
        self.style.configure('TFrame', background='black')
        self.style.configure('Frame1.TFrame',background='#07125B')
        self.style.configure('Frame2.TFrame',background='#F07610')
        self.style.configure('TLabel',background='#1A36DC',foreground='white')
        self.style.configure('Label1.TLabel',background='#07125B',foreground='white')
        self.style.configure('Label2.TLabel',background='black',foreground='white')

        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=0)
        self.rowconfigure(1,weight=1)
        self.score_board = ScoreBoard(self)
        self.score_board.grid(row=0,column=0,sticky='nwes',pady=(10,10),padx=(10,10))
        self.answerbox = AnswerBox(self)
        self.answerbox.grid(row=1,column=0,sticky='nwes',padx=(10,10))
    
    def revealAns(self, index):
        points = self.answerbox.revealAns(index)
        self.score_board.increaseCurrentScore(points)
        if points > 0:
            #This section is to play the correct answer sound that family fued plays
            self.update() #Forces update of window so that the sound is played after answer is revealed
            open( BASE_DIR + '\data\Correct_Answer.mp3') #Opens sound file
            playsound( BASE_DIR + '\data\Correct_Answer.mp3') #Plays sound file
            close() #Closes sound file

    def loadQuestionSet(self, questionSets):
        #self.answerbox.loadQuestionSet(questionSets[0])
        self.questionSets = questionSets

    def changeQuestionSet(self, index):
        self.answerbox.loadQuestionSet(self.questionSets[index])

    def clearBoard(self):
        self.answerbox.clearBoard()
    
    def getAnswers(self):
        return self.answerbox.getAnswers()
    
    def getQuestions(self):
        questions = []
        for questionSet in self.questionSets:
            questions.append(questionSet['question'])
        return questions
    
    def getQuestionIndex(self, question):
        for questionSet,i in zip(self.questionSets,range(len(questionSets))):
            if questionSet['question'] == question:
                return i
        return -1

    def updateName(self, team, name):
        self.score_board.updateName(team, name)

    def endRound(self, team):
        self.score_board.teamScoreAdd(team)
        self.answerbox.endRound()

    def resize(self,event):
        self.answerbox.resize(event)
        self.score_board.resize(event)

#Make it so on the control window, there is a panel on the right controlling team actions like giving points and switching teams and on the bottom is to control question

class ButtonGrid(ttk.Frame):
    prev_height = 0
    ansBtns = []

    def __init__(self, parent, GameWindow, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        self.style = ttk.Style()
        self.style.configure('ButtonGrid.TButton',font=('Arial',15))

        self.bind('<Configure>',self.resize)

        self.columnconfigure((0,1),weight=1, uniform='fred')
        self.rowconfigure((0,1,2,3),weight=1)

        for col in range(2):
            for row in range(4):
                i = row+col*4
                self.ansBtns.append(ttk.Button(self,text=(str(i+1)), command = partial(GameWindow.revealAns, i), style='ButtonGrid.TButton'))
                self.ansBtns[i].grid(row=row,column=col,padx=(10,10),pady=(10,10),sticky='nsew')

    #Changes answers displayed to answers in new questionSet
    def updateButtons(self, answerSet):
        for i in range(8):
            if i<len(answerSet):
                self.ansBtns[i].config(text=(str(i+1) + ': ' + answerSet[i]))
            else:
                self.ansBtns[i].config(text='')

    def resize(self, event):
        if event.width < 100:
            return
        width_size=int((event.width)/30)
        height_size=int((event.height)/17)
        if width_size<height_size:
            size = width_size
        else:
            size=height_size

        self.style.configure('ButtonGrid.TButton',font=('Arial',size))

class QuestionLoader(ttk.Frame):

    def __init__(self, parent, gw, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs) 
        self.parent = parent 

        self.style = ttk.Style()
        self.style.configure('BottomPanel.TMenubutton', font=('Arial', 20))
        self.style.configure('BottomPanel.TButton', font=('Arial', 20), anchor='center')
        self.style.configure('BottomPanel.TLabel',background='black',foreground='white', font=('Arial', 20))
        self.columnconfigure(0,weight=3)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=3)
        self.rowconfigure((0,1),weight=1)

        self.bind('<Configure>',self.resize)

        self.dropdown_label = ttk.Label(self,text='Choose Question to Load:',style='BottomPanel.TLabel')
        self.dropdown_label.grid(row=0,column=0,sticky='nws',padx=(10,0),pady=(10,0))

        self.question_selection = tk.StringVar(self)
        self.question_selection.set('Selection Question')
        self.dropdown_menu = ttk.OptionMenu(self, self.question_selection, 'Select Question', *gw.getQuestions(),style='BottomPanel.TMenubutton')
        self.dropdown_menu['menu'].configure(font=('Arial',20))
        self.dropdown_menu.grid(row=1,column=0,sticky='nsew',padx=(10,0),pady=(10,10))

        self.load_button = ttk.Button(self,text='Load',style='BottomPanel.TButton', command=self.load_question)
        self.load_button.grid(row=1,column=1,sticky='nsew',padx=(0,10),pady=(10,10))

    def load_question(self):
        self.parent.sidebar.endRound()
        index = gw.getQuestionIndex(self.question_selection.get())
        gw.changeQuestionSet(index)
        self.parent.controlbox.updateButtons(gw.getAnswers())

    def resize(self, event):
        width_size=int((event.width)/20)
        height_size=int((event.height)/3)
        if width_size<height_size:
            size = width_size
        else:
            size=height_size
        size=min(size,60)
        self.dropdown_menu['menu'].configure(font=('Arial',int(size*0.6)))
        self.style.configure('BottomPanel.TMenubutton',font=('Arial',int(size*0.5)))
        self.style.configure('BottomPanel.TButton', font=('Arial', int(size*0.7)))
        self.style.configure('BottomPanel.TLabel', font=('Arial', int(size*0.7)))

class SideBar(ttk.Frame):
    current_team = 1

    def __init__(self, parent, gw, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        self.style = ttk.Style()
        self.style.configure('Sidebar.TButton',font=('Arial',15))
        self.style.configure('Sidebar.TLabel',background='black',foreground='white', font=('Arial',15))
        self.style.configure('Sidebar.TEntry',font=('Arial',15))
        

        self.bind('<Configure>',self.resize)

        self.rowconfigure((0,1),weight=1)
        self.columnconfigure(0,weight=1)

        self.team_name_frame = ttk.Frame(self,relief='ridge')
        self.team_name_frame.grid(row=0,column=0,sticky='nsew',padx=(10,10),pady=(10,10))
        self.team_name_frame.columnconfigure(0,weight=1)
        #self.team_name_frame.rowconfigure((0,1,2,3),weight=1)

        self.team_one_name = tk.StringVar(self)
        self.team_one_name.set('Team One')
        self.team_one_label = ttk.Label(self.team_name_frame, text='Team One Name', style = 'Sidebar.TLabel')
        self.team_one_label.grid(padx=(10,10),pady=(5,0),sticky='n')
        self.team_one_name_entry = ttk.Entry(self.team_name_frame, textvariable=self.team_one_name, validate='focusout', validatecommand=partial(self.updateName, 1), style = 'Sidebar.TEntry')
        self.team_one_name_entry.grid(padx=(10,10),sticky='new')

        self.team_two_name = tk.StringVar(self)
        self.team_two_name.set('Team Two')
        self.team_two_label = ttk.Label(self.team_name_frame, text='Team Two Name', style = 'Sidebar.TLabel')
        self.team_two_label.grid(padx=(10,10),pady=(5,0),sticky='n')
        self.team_two_name_entry = ttk.Entry(self.team_name_frame, textvariable=self.team_two_name, validate='focusout', validatecommand=partial(self.updateName, 2), style = 'Sidebar.TEntry')
        self.team_two_name_entry.grid(padx=(10,10),pady=(0,10),sticky='new')

        self.point_manager_frame = ttk.Frame(self, relief='ridge')
        self.point_manager_frame.grid(row=1,column=0,sticky='nswe',padx=(10,10),pady=(10,10))
        self.point_manager_frame.columnconfigure(0,weight=1)
        
        self.team_switch_button = ttk.Button(self.point_manager_frame, text='Switch Teams', style='Sidebar.TButton', command=self.switchTeams)
        self.team_switch_button.grid(row=0,column=0,padx=(10,10),pady=(10,10),sticky='nsew')
        self.current_team_label = ttk.Label(self.point_manager_frame, text='Team: Team One', style = 'Sidebar.TLabel')
        self.current_team_label.grid(row=1,column=0,sticky='s')
        self.add_points_button = ttk.Button(self.point_manager_frame, text='End Round/Add Points', style='Sidebar.TButton', command=self.endRound)
        self.add_points_button.grid(row=2,column=0,padx=(10,10),pady=(10,10),sticky='nsew')

        #self.resetBtn = ttk.Button(self,text='reset', command= lambda: GameWindow.clearBoard())
        #self.resetBtn.grid()
    
    def updateName(self, team):
        if team == 1:
            gw.updateName(team, self.team_one_name.get())
            if self.current_team == 1:
                self.current_team_label.config(text='Team: '+self.team_one_name.get())
        else:
            gw.updateName(team, self.team_two_name.get())
            if self.current_team == 2:
                self.current_team_label.config(text='Team: '+self.team_two_name.get())
        return True
    
    def switchTeams(self):
        if self.current_team == 1:
            self.current_team = 2
            self.current_team_label.config(text='Team: '+self.team_two_name.get())
        else:
            self.current_team = 1
            self.current_team_label.config(text='Team: '+self.team_one_name.get())

    def endRound(self):
        gw.endRound(self.current_team)

    def resize(self, event):
        if event.width < 100:
            return
        width_size=int((event.width-60)/12)
        height_size=int((event.height-40)/15)
        if width_size<height_size:
            size = width_size
        else:
            size=height_size
        n=0.9
        self.style.configure('Sidebar.TButton',font=('Arial',int(size*n)))
        self.style.configure('Sidebar.TLabel',font=('Arial',int(size*n)))
        #self.style.configure('Sidebar.TEntry',font=('Arial',size))
        self.team_one_name_entry.configure(font=('Arial',int(size*n)))
        self.team_two_name_entry.configure(font=('Arial',int(size*n)))

class WrongAnswerPanel(ttk.Frame):

    def __init__(self, parent, gw, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs) 
        self.parent = parent 

        self.style = ttk.Style()
        self.style.configure('Answer.TButton',font=('Arial',20))
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        self.bind('<Configure>',self.resize)

        self.X_Button = ttk.Button(self, text='X',style='Answer.TButton',command=self.XButton)
        self.X_Button.grid(sticky='nsew',padx=(10,10),pady=(10,10))

    def XButton(self):
        open( BASE_DIR + '\data\Incorrect_Answer.mp3')
        playsound( BASE_DIR + '\data\Incorrect_Answer.mp3')
        close()

    def resize(self, event):
        width_size=int((event.width)/10)
        height_size=int((event.height)/8)
        if width_size<height_size:
            size = width_size
        else:
            size=height_size
        self.style.configure('Answer.TButton', font=('Arial', int(size*3)))

class ControlWindow(ttk.Frame):
    def __init__(self, parent, gw, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, *kwargs)

        self.style = ttk.Style()
        self.rowconfigure(0,weight=3,uniform='fred')
        self.rowconfigure(1,weight=1,uniform='fred')
        self.columnconfigure(0,weight=4,uniform='fred')
        self.columnconfigure(1,weight=3,uniform='fred')

        #self.top_frame = ttk.Frame(self)
        #self.top_frame.grid(row=0,column=0,sticky='nsew')
        #self.top_frame.columnconfigure((0,1),weight=1,uniform='fred')
        #self.top_frame.rowconfigure(0,weight=1)

        self.controlbox = ButtonGrid(self, gw, relief='ridge')
        self.controlbox.grid(row=0,column=0,sticky='nsew',padx=(10,10),pady=(10,10))
        self.sidebar = SideBar(self, gw)
        self.sidebar.grid(row=0,column=1,sticky='nsew')

        self.bottompanel = QuestionLoader(self, gw,relief='ridge')
        self.bottompanel.grid(row=1,column=0,sticky='nesw',padx=(10,10),pady=(0,10))
        self.wronganswerpanel = WrongAnswerPanel(self, gw, relief='ridge')
        self.wronganswerpanel.grid(row=1,column=1,sticky='nsew',padx=(10,10),pady=(0,10))
    
    def resize(self, event):
        self.controlbox.resize(event)
        self.sidebar.resize(event)

if __name__ == "__main__":
    

    root = tk.Tk()

    with open( BASE_DIR + '\data\questions.json') as f:
        questionSets = json.load(f)

    root.geometry('600x400')
    root.title('Family Feud')

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0,weight=1)

    gw = GameWindow(root)
    gw.grid(row=0,column=0,sticky='ewns')
    gw.loadQuestionSet(questionSets)
    #root.bind('<Configure>',gw.resize)
    
    Control = tk.Toplevel()
    Control.title('Control Panel')

    Control.rowconfigure(0, weight=1)
    Control.columnconfigure(0,weight=1)

    cw = ControlWindow(Control, gw)
    Control.geometry('600x400')
    cw.grid(row=0,column=0,sticky='ewns')
    #Control.bind('<Configure>',cw.resize)

    root.mainloop()