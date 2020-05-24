from manimlib.imports import *
from PrimoCreature import *
class Edge():
    def __init__(self, _nxt, _to):
        self.nxt = _nxt
        self.to = _to
class Graph():
    def __init__(self):
        self.cnt = 0
        self.edgnum = 21
        self.treeroot = 1
        self.edg = [Edge(0,0)]
        self.head = [0]*self.edgnum
        self.dep = [0]*self.edgnum
        self.fa = [0]*self.edgnum
        self.pos = [np.array([0,0,0])]
        self.dfsord=[0]
        self.hasone=[False]*self.edgnum
        self.omega = [2*PI]*self.edgnum
        self.tau = [0]*self.edgnum
        self.size=[1]*self.edgnum
        for i in range(self.edgnum):
            x=Edge(0,0)
            self.edg.append(x)
        for i in range(self.edgnum):
            x=np.array([0,2,0])
            self.pos.append(x)
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
            v = self.edg[i].to
            if v != fat:
                self.dfs(self.edg[i].to,layer+1,x)
            self.size[x]=self.size[x]+self.size[self.edg[i].to]
            if self.size[self.edg[i].to]>=self.size[self.son[x]]:
                self.son[x] = self.edg[i].to
            i = self.edg[i].nxt
    
    def get_connection_for_dfs2(self,u,t,fa):
        if fa==0:
            pass
        else:
            l = Line(self.pos[u],self.pos[fa])
            self.linefordfs2.add(l)
            txt=TextMobject(str(len(self.linefordfs2)-1),color=WHITE)
            txt.move_to(l).scale(0.5)
            self.edgmkafterdfs2.add(txt)
        if self.son[u]!=0:
            self.get_connection_for_dfs2(self.son[u],t,u)
        i = self.head[u]
        while i != int(0):
            v = self.edg[i].to
            if v != self.fa[u] and v!=self.son[u]:
                self.get_connection_for_dfs2(v,v,u)
            i = self.edg[i].nxt
        return self.linefordfs2
    def getpos(self,v):
        if v!=self.treeroot:
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
    
    
    
   

class Test(Scene):
    def construct(self):
        g=Graph()
        FocusOn
        g.adde(1,2)
        g.get_arguments()
        ids = g.get_id()
        id_after = g.get_nodes_of_pf()
        bdr = g.get_connection(1,0)
        self.play(Write(bdr),Write(ids),Write(g.edgemk),Write(g.drawsize()))