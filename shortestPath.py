import random
import tkinter as tk
from tkinter import messagebox
from sys import exit

maxSize = 32


class Node():
    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

#Create a random board to search  through
def createBoard(size, start, end):
    board = [[1 for x in range(size)] for y in range(size)]
    
    #Assign walkable boxes
    for arr in board:
        for x in range(len(arr)):
            if random.randint(1, 10) < 7:
                arr[x] = 0
    
    #Define the starting spots
    board[start[0]][start[1]] = 0
    board[end[0]][end[1]] = 0
    
    return board
   

#Implementation of A* Pathfinding Algorithm
def Astar(board, start, end):
    
    openList = []
    closedList = []
    searchedNode = []
    
    #Init start and end node
    startNode = Node(None,start)
    endNode = Node(None, end)
    
    #Start with the start node
    openList.append(startNode)
    
    while len(openList) > 0 and len(openList) < 1000:
        currNode = openList[0]
        currIndex = 0
        
        #Find the smallest f value to add to the closedList
        for index, node in enumerate(openList):
            if node.f < currNode.f:
                currNode = node
                currIndex = index
        
        #Take node off openList and add to closedList
        openList.pop(currIndex)
        closedList.append(currNode)
        
        
        #Check if current node is the end node
        if currNode.position == endNode.position:      
            shortestPath = []
            curr = currNode
            while curr is not None:
                shortestPath.append(curr.position)
                curr = curr.parent
              
            return shortestPath[::-1],searchedNode
        
        
        children = []
        
        for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: 
            
            #Get node position
            nodePos = (currNode.position[0] + newPos[0], currNode.position[1] + newPos[1])

            #Make sure within range
            if nodePos[0] > (len(board) - 1) or nodePos[0] < 0 or nodePos[1] > (len(board[len(board)-1]) -1) or nodePos[1] < 0:
                continue

            #Make sure walkable terrain
            if board[nodePos[0]][nodePos[1]] != 0:
                continue

            #Create new node
            newNode = Node(currNode, nodePos)
            
            if nodePos != start and nodePos != end:
                searchedNode.append(nodePos)
            
            #Append
            children.append(newNode)

        #Loop through children
        for child in children:

            #Child is on the closed list
            for closedChild in closedList:
                if child == closedChild:
                    continue

            #Create the f, g, and h values
            child.g = currNode.g + 1
            child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)
            child.f = child.g + child.h

            #Child is already in the open list
            for openNode in openList:
                if child == openNode and child.g > openNode.g:
                    continue

            #Add the child to the open list
            openList.append(child)
        
    return None,None

#See if the current cordinates are valid
def isValid(cord1,cord2):
    global maxSize
    if((cord1[0] < maxSize and cord1[0] >= 0) and (cord1[1] < maxSize and cord1[1] >= 0) and (cord2[0] < maxSize and cord2[0] >= 0) and (cord2[1] < maxSize and cord2[1] >= 0)):
        return True
    return False


class startGUI(tk.Tk): 
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        
        self.startLabel1 = tk.Label(self,text = "Start Point: X,Y")
        self.startLabel2 = tk.Label(self,text = "End Point: X,Y")
        self.startLabel3 = tk.Label(self,text= "NOTE: Enter integers from 0 to 31")
        
        self.startLabel1.grid(row=0,column=0)
        self.startLabel2.grid(row=0,column=1)
        self.startLabel3.grid(row=2,column=0)
        
        self.startEnt = tk.Entry(self)
        self.endEnt = tk.Entry(self)
        self.startEnt.grid(row=1,column=0)
        self.endEnt.grid(row=1,column=1)
        
        self.submit = tk.Button(self, text= "Submit", command=self.check)
        self.submit.grid(row=2,column=2)
        
        self.currState = False
        self.checkBox = tk.Checkbutton(self, text='Show Steps?', command=self.state)
        self.checkBox.grid(row=2,column=1)
        
        self.startCord = None
        self.endCord = None
        
    def state(self):
        if self.currState == True:
            self.currState = False
        else:
            self.currState = True
   
    
    def check(self):
        e1 = self.startEnt.get()
        e2 = self.endEnt.get()
    
        cord1 = e1.split(',')
        cord2 = e2.split(',')
     
        for num in range(len(cord1)):
            try:
                cord1[num] = int(cord1[num])
            except ValueError:
                messagebox.showerror("Invalid Type", "ERROR: Please type integers")
                return
    
    
        for num in range(len(cord2)):
            try:
                cord2[num] = int(cord2[num])
            except ValueError:
                messagebox.showerror("Invalid Type", "ERROR: Please type integers")
                return
    
        if(len(cord1) == 2 and len(cord2) == 2):         
            if isValid(cord1,cord2):
                self.startCord = cord1
                self.endCord = cord2
                self.destroy()
                return
                
            else:
                return


class gridGUI(tk.Tk): 
    def __init__(self,parent,board,start,end):
        global maxSize
        
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.board = board
        self.start = start
        self.end = end
        self.box =  [[tk.Label() for x in range(32)] for y in range(32)]
        self.final = None
        self.currCord = 0
        self.solCord = 1
        self.searchedNode = []
        self.showSteps = False
        
        for i in range(maxSize):
            for j in range(maxSize):
                if board[i][j] == 1:
                    mainFrame = tk.Frame(self,
                                  relief="raised",
                                  width=1,
                                  height=1)
                
                    mainFrame.pack_propagate(0)
                    mainFrame.grid(row=i,column=j)
                
                    self.box[i][j] = tk.Label(mainFrame, bg="black", width=2,height=1)
                    self.box[i][j].grid(row=i,column=j)
                else:
                    mainFrame = tk.Frame(self,
                                  relief="raised",
                                  width=1,
                                  height=1)
                
                    mainFrame.pack_propagate(0)
                    mainFrame.grid(row=i,column=j)
                
                    self.box[i][j] = tk.Label(mainFrame, bg="white", width=2,height=1)
                    self.box[i][j].grid(row=i,column=j)
            
            self.box[self.start[0]][self.start[1]].configure(bg="red")
            self.box[self.end[0]][self.end[1]].configure(bg="blue")
             
  
    
    def showSolution(self):
        if self.solCord != len(self.final)-1:
            self.box[self.final[self.solCord][0]][self.final[self.solCord][1]].configure(bg="purple")
            self.solCord+=1
            self.after(150, self.showSolution)
        else:
            self.title("Shortest Path Found!")
            messagebox.showinfo("A* Pathfinding", "Shortest path has been found!")
            
  
    def printSteps(self):
        if self.currCord != len(self.searchedNode)-1:
            self.box[self.searchedNode[self.currCord][0]][self.searchedNode[self.currCord][1]].configure(bg="pink")
            self.currCord+=1
            self.after(25, self.printSteps)
        else:
            self.after(1000, maze.showSolution)
        pass
    

if __name__ == '__main__':  
        
        window = startGUI(None)
        window.title("Enter Start and End Points")
        window.geometry("450x75")
        
        window.mainloop()
        
        start = window.startCord
        end = window.endCord
        
        if start == None or end == None:
            exit()
        else:
           newStart = (start[1],start[0])
           newEnd = (end[1],end[0])
           
           board = createBoard(maxSize,newStart,newEnd)
           solution, steps = Astar(board,newStart,newEnd)
           
           while solution == None:
               board = createBoard(maxSize,newStart,newEnd)
               solution, steps = Astar(board,newStart,newEnd)
           
           maze = gridGUI(None,board,newStart,newEnd)
           
           maze.title("Finding shortest path...")
           maze.final = solution
           maze.searchedNode = steps
           maze.showSteps = window.currState
             
           if maze.showSteps:
               maze.after(2000,maze.printSteps)
           else:    
               maze.after(2000, maze.showSolution)
           
           maze.mainloop()
            


