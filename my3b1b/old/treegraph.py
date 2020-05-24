from manimlib.imports import *

class Edge():
    def __init__(self, _nxt, _to):
        #链式前向星存图
        self.nxt = _nxt 
        self.to = _to


class Graph():
    def __init__(self):
        self.lines = VMobject()
        self.edg = [Edge(0,0)]
        for i in range(21):
            x=Edge(0,0)
            self.edg.append(x)
        self.cnt = 0
        self.head = [0]*20
        self.dep = [0]*20
        self.fa = [0]*20
        self.pos = [2*UP]
        self.out = [0]*20
        for i in range(21):
            x=2*UP
            self.pos.append(x)
        self.hasone=[False]*20
        self.dfsxord[0]*20
    def adde(self, u, v):
        self.hasone[u] = True
        self.hasone[v] = True
        self.out[u]=self.out[u]+1
        self.cnt = self.cnt+1
        self.edg[self.cnt].nxt = self.head[u]
        self.edg[self.cnt].to = v
        self.head[u] = self.cnt

    def dfs(self, x,layer,fat):
        print("x="+str(x))
        self.dep[x] = layer
        self.fa[x] = fat
        i = self.head[x]
        while i != int(0):
            self.dfs(self.edg[i].to,layer+1,x)
            i = self.edg[i].nxt

    def getxy(self):
        tree = VMobject() 
        ids = VMobject() 
        for i in range(1,20):
            if i==1:
                self.pos[1]=2*UP
            else:
                if self.hasone[i]:
                    self.pos[i] = self.pos[self.fa[i]]+DOWN+0.8*self.out[i]*LEFT +0.5*RIGHT
                    self.out[i]= self.out[i]-1;
                else:
                    self.pos[i] = 20*DOWN
        for i in range(1,20):
            p=Circle(fill_color=BLUE,radius=0.3,fill_opacity=0,color=BLUE)
            p.move_to(self.pos[i])
            tree.add(p)
        
        return tree


    def getid(self):
        ids = VMobject() 
        for i in range(1,20):
            ics=TextMobject(str(i))
            ics.move_to(self.pos[i])
            ids.add(ics)
        return ids
    
    def drawbder(self,x,fa):
        if fa==0:
            pass
        else:
            ln = Line(self.pos[fa]+0.3*DOWN,self.pos[x]+0.3*UP)
            self.lines.add(ln)
        
        print("border:x="+str(x))
        i = self.head[x]
        while i != int(0):
            self.drawbder(self.edg[i].to,x)
            i = self.edg[i].nxt
        return self.lines



class ShowTree(Scene):

    def construct(self):
        g = Graph()
        g.adde(1,2)
        g.adde(1,3)
        g.adde(2,9)
        g.adde(3,4)
        g.adde(6,8)
        g.adde(3,5)
        g.adde(5,6)
        g.dfs(1,0,0)
        s = g.getxy()
        ids = g.getid()
        bdr = g.drawbder(1,0)
        self.play(Write(s))
        self.play(Write(ids))
        self.play(Write(bdr))

        