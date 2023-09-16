# Family Fued

Thank you for choosing Zack's Family Feud Program for your Family Feud Game Needs.  
The rest of this document will instruct you on how to use the program. 
Make sure to atleast read the Important Notes at the bottom! 

## To Run Program:  
To run program just run the FamilyFeud.py file in the python folder. 
This will pop up two windows, one named Family Feud and the other name control panel.  

## How to Display Program:  
The Family Feud window is what should be projected for everyone to see  
while the control panel window should only be visible to the person controling the computer. 
To do this make sure your computer is connected to some sort of addition display(Like projector) and that it is set to extend display. 
Then drag the family feud window to the projector display and keep the control panel window on the computer's screen.  

## How to use Control Panel:  
I tried to make it as simple as possible with only 5 main parts of the panel:  
Answer Reveal Button Grid(Top Left), Team Name Changer(Top Right), Points Manager(Middle Right), 
Incorrect Answer Button(Bottom Right), and Question Loader(Button Left).  

### First the Question Loader:  
This section will allow you to change the current question being display, 
simply click on the drop down and selected a question then his 'Load' 
By doing this it resets all revealed questions and it will add the current score to the current selected team.  

### Answer Reveal Button Grid:  
This grid of buttons is used to reveal answers when correct answers are given. 
Once a question is selected the answer grid will change to display what the correct answers are, clicking these buttons 
will play the correct answer sound and display the corresponding asnwer on the Family Feud window and adding the points of that 
answer to the current score which then can be later added to a team. 
(!) Please note that when you click the button and the sound it playing, the window will not respond for about a second. Do not try 
to click buttons while the window is frozen. 
If you click the button of an already revealed answer, it will hide it again and subtract the score from the current score.
This is incase an answer was mistakenly shown. 
One last thing to know is that once the 'End Round/Add Points' Button has been hit, points of newly revealed answers will 
not be counted towards the current score. This is so that you can reveal what the remaining answers are after 
the round has ended.  

### Team Name Changer:  
This section lets you change the team names displayed on the Family Feud window. 
Just type the name you want in the box and then once you have the name you want, click on the other input box or outside the window. 
You have to click the other box or outside the window so you 'deselect' that box, if you don't the name won't update.  

### Points Manager:  
This section is used to add the current points to a team and ends the round. 
The 'Switch Teams' button will change the currently selected team, this only shows on the control panel and does not change anything 
on the Family Feud window. 
Below the 'Switch Teams' button is some text that shows the currently selected team. 
The 'End Round/Add Points' button will end the round and adds the current points to the selected team shown above the button. 
Ending the round also means that no more points will be added to any team until a new question is loaded.  

### Incorrect Answer Button:  
This is the simpliest one, its just a button that makes the incorrect answer sound, nothing else.  

## Important Notes(!!):  
1. To reset scores just restart the program. This means each time a new set of teams is coming up you should restart the program. 
2. There can only be 18 questions loaded into the question file at once, this is because of the amount of questions that can be displayed 
in the drop down menu. So in order to use more than 18 questions you will have to change the question.json file in the data folder. 
To change the current question set (which is the question.json file that 
is in the data folder) you must move out the current questions.json file and replace it with a new questions.json file. 
Once this is done you will have to restart the program for it to load the new question set. This means that all scores will be reset. 
3. If you want to create more question sets with your own questions and answers just create a new json file and follow to format of the 
given question set which is a list of objects with a question string field and answers list of strings field.
4. If there are no question.json files in the data folder itself, then the code will not run. Also know that you can not
have two question.json files in the data folder.