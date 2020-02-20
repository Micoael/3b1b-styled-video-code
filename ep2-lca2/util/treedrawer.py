from manimlib.imports import *

class Edge():
    def __init__(self, _nxt, _to):
        self.nxt = _nxt
        self.to = _to


class Graph():
    def __init__(self):
        # The lines that connects all the mobjects(circles)
        # must call dfs first and then getxy modified by get_connection
        self.lines = VMobject()
        # 21Edges Your graph should no more than 21 edegs
        self.edg = [Edge(0,0)]
        for i in range(21):
            x=Edge(0,0)
            self.edg.append(x)
        #Chain Forward Pointer
        self.cnt = 0
        self.head = [0]*20
        # depth of the vertex
        self.dep = [0]*20
        # how many points are there in each depth
        self.eachdepth = [0]*20
        # father of the vertex
        self.fa = [0]*20
        # position of the vertex,modified by getxy, call dfs first.
        self.pos = [np.array([0,0,0])]
        # outedge(deprecated)
        self.out = [0]*20
        # saves the DFS order for video
        self.dfsord=[0]
        #adds the position of the original position array
        for i in range(21):
            x=np.array([0,2,0])
            self.pos.append(x)
        #Check which point was mentioned
        self.hasone=[False]*20
        # Mark the edgenum. Modified by drawbdr, must call dfs and 
        # getxy first.
        self.edgemk=VMobject()

        self.left=[np.array([0,0,0])]
        self.right=[np.array([0,0,0])]
        for i in range(20):
            x=2*UP
            self.left.append(np.array([0,0,0]))
            self.right.append(np.array([0,0,0]))

        self.tree = VMobject() 
        self.ids = VMobject()

        #drawer
        self.omega = [2*PI]*20
        self.tau = [0]*20
        self.size=[1]*20

    def adde(self, u, v):
        self.hasone[u] = True
        self.hasone[v] = True
        self.out[u]=self.out[u]+1
        self.cnt = self.cnt+1
        self.edg[self.cnt].nxt = self.head[u]
        self.edg[self.cnt].to = v
        self.head[u] = self.cnt

    def dfs(self, x,layer,fat):
        self.dfsord.append(x)
        self.dep[x] = layer
        self.eachdepth[layer] = self.eachdepth[layer]+1
        self.fa[x] = fat
        i = self.head[x]
        if i==0:
            self.size[x]=1
        while i != int(0):
            self.dfs(self.edg[i].to,layer+1,x)
            self.size[x]=self.size[x]+self.size[self.edg[i].to]
            i = self.edg[i].nxt

    def getpos(self,v):
        if v!=1:
            u=self.fa[v]
            self.pos[v] = self.pos[u]+2*np.array([math.cos(self.tau[v]+self.omega[v]/2),math.sin(self.tau[v]+self.omega[v]/2),0])  
        yita = self.tau[v]
        i = self.head[v]
        while i != int(0):
            w = self.edg[i].to
            self.omega[w] = self.size[w]/self.size[1]*-1*PI
            self.tau[w] = yita
            yita = yita+self.omega[w]
            self.getpos(self.edg[i].to)
            i = self.edg[i].nxt


    def getxy(self):
        
        self.getpos(1)
        for i in range(1,20):
            if self.hasone[i]:
                p=Circle(fill_color=BLUE,radius=0.3,fill_opacity=0.8,color=BLUE)
                p.move_to(self.pos[i])
                self.tree.add(p)
            else:
                p=Circle(fill_color=BLUE,radius=0.3,fill_opacity=0.8,color=BLUE)
                p.move_to(20*DOWN)
                self.tree.add(p)
        return self.tree


    def get_id(self):
        """
        Get each point;s id
        """
        for i in range(1,20):
            if self.hasone[i]==True:
                ics=TextMobject(str(i))
                ics.move_to(self.pos[i])
                self.ids.add(ics)
        return self.ids
    
    def get_connection(self,x,fa):
        if fa==0:
            pass
        else:
            ln = Line(self.pos[fa]+0.3*DOWN,self.pos[x]+0.3*UP,color=BLUE)
            self.lines.add(ln)
            txt=TextMobject(str(len(self.lines)-1),color=WHITE)
            txt.move_to(ln).scale(0.5)
            self.edgemk.add(txt)

        i = self.head[x]
        while i != int(0):
            self.get_connection(self.edg[i].to,x)
            i = self.edg[i].nxt
        return self.lines

    def highlight_point(self,id):
        p=Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.2,color=YELLOW)
        p.move_to(self.pos[id])
        return p
    
    def get_arguments(self):
        self.dfs(1,0,0)
        self.getxy()

    def get_nodes(self):
        return self.tree

    



    

class Test(Scene):
    
    def construct(self):

        g = Graph()
        g.adde(1,2)
        g.adde(1,4)
        g.adde(1,3)
        g.adde(2,5)
        g.adde(5,10)
        g.adde(3,6)
        g.adde(6,7)
        g.adde(6,8)
        g.adde(6,9)
        g.adde(6,13)
        g.adde(2,15)
        g.get_arguments()
        s = g.get_nodes()
        ids = g.get_id()
        bdr = g.get_connection(1,0)
        print(g.eachdepth[2])
        
        self.play(Write(bdr),Write(s),Write(ids),Write(g.edgemk),Write(g.highlight_point(3)))
        print(g.size)

        
