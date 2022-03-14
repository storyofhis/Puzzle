import sys
import copy
import time
goalState=[[1,2,3],[8,0,4],[7,6,5]]
startState=[[7,2,4],[5,0,6],[8,3,1]]

class Node:
    def __init__(self,starts=None,d=None,path=None,move=None,h=None):
        self.state=starts
        self.depth=d
        self.curPath=path
        self.operation=move
        self.hValue=h
        
    #generating and returning children of a state with moves in 4 directions
    def generatechildren(self,parent,visited,h=None,totalNodes=None):
        children=[]
        xpos,ypos=None,None
        for i in range(0,3):
            for j in range(0,3):
                if(parent.state[i][j]==0 ):
                    xpos=i
                    ypos=j
                    break
            if xpos is not None:
                break

        if xpos is not 2:  # move down
            tpath = copy.deepcopy(parent.curPath)
            tpath.append("DOWN")
            child = Node(copy.deepcopy(parent.state), parent.depth + 1, tpath, "DOWN",h)
            child.state[xpos + 1][ypos], child.state[xpos][ypos] = child.state[xpos][ypos], child.state[xpos + 1][ypos]
            if (self.toString(child.state) not in visited):
                children.append(child)
                totalNodes+=1

        if ypos is not 0 : #move left
            tpath=copy.deepcopy(parent.curPath)
            tpath.append("LEFT")
            child=Node(copy.deepcopy(parent.state),parent.depth+1,tpath,"LEFT",h)
            child.state[xpos][ypos-1],child.state[xpos][ypos]=child.state[xpos][ypos],child.state[xpos][ypos-1]
            if (self.toString(child.state) not in visited):
                children.append(child)
                totalNodes+=1

        if ypos is not 2:  # move right
            tpath = copy.deepcopy(parent.curPath)
            tpath.append("RIGHT")
            child = Node(copy.deepcopy(parent.state), parent.depth + 1,tpath, "RIGHT",h)
            child.state[xpos][ypos+1], child.state[xpos][ ypos] = child.state[xpos][ypos], child.state[xpos][ypos+1]
            if (self.toString(child.state) not in visited):
                children.append(child)
                totalNodes+=1

        if xpos is not 0:  # move top
            tpath = copy.deepcopy(parent.curPath)
            tpath.append("UP")
            child = Node(copy.deepcopy(parent.state), parent.depth + 1,tpath, "TOP",h)
            child.state[xpos-1][ypos], child.state[xpos][ ypos] = child.state[xpos][ypos], child.state[xpos-1][ypos]
            if (self.toString(child.state) not in visited):
                children.append(child)
                totalNodes+=1

        return children,totalNodes
    
    def displayConfig(self,tlist):
        k=tlist[0]

        #Converting a state to string for storage in set
    def toString(self,tempState):
        s=''
        for i in tempState:
            for j in i:
                s+=str(j)
        return s

    #Calculating manhatten heuristic value
    def heuristic_manhatten(self,state):
        score = 0
        goalx = [1, 0, 0, 0, 1, 2, 2, 2, 1]
        goaly = [1, 0, 1, 2, 2, 2, 1, 0, 0]
        for i in range(0, 3):
            for j in range(0,3):
                num=state[i][j]
                if(num!=0):
                    score += abs(i-goalx[num])+abs(j-goaly[num])
        return score

    def astar_Manhatten(self):
        maxListSize=-sys.maxint-1
        totalNodes=0
        timeFlag=0
        start_time = time.time()
        q = []
        flag = 0
        visited = set()
        startNode = Node(startState, 1, [], '', 1+self.heuristic_manhatten(startState))
        q.append(startNode)
        while (q):
            if len(q)>maxListSize:
                maxListSize=len(q)
            temp_time = time.time()
            if (temp_time - start_time >= 10 * 60):
                timeFlag = 1
                break
            q.sort(key=lambda x: (x.hValue))
            currentNode = q.pop(0)
            stateString = self.toString(currentNode.state)
            visited.add(stateString)
            if (currentNode.state == goalState):
                print ("Moves="+str(len(currentNode.curPath)))
                print (str(currentNode.curPath))
                flag = 1
                print ('')
                print ("Total Nodes Visited="+str(totalNodes))
                print ("A* with Manhatten Heuristic Time "+ str(time.time()-start_time))
                print ("Maximum List Size="+str(maxListSize))

            if flag is 1:
                break
            tchilds,totalNodes=self.generatechildren(currentNode, visited, currentNode.depth + self.heuristic_manhatten(currentNode.state),
                                  totalNodes)
            q.extend(tchilds)# Adding the expanded chidrens to the list
        if timeFlag is 1:
            print ("Total Nodes Visited=" + str(totalNodes))
            print ("A* with Manhatten Heuristic terminated due to time out")
            
if __name__ == "__main__":
    obj = Node()
    obj.astar_Manhatten()
    