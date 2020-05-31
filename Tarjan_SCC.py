# from: @Micoael_Primo
from manimlib.imports import *


class Edge():
    def __init__(self, _nxt, _to):
        self.nxt = _nxt
        self.to = _to
        
class MCSCene(Scene):
    # Use your PR and MC to produce image...
    pass

class PPTSCene(Scene):
    # Use your PR and MC to produce image...
    pass

class TreeScene(Scene):
    
    def init(self):
        '''
        Initilize the tree.
        '''
        self.cnt = 0
        self.edgnum = 21
        self.treeroot = 1
        self.factor = 1
        self.shiftup = 3
        self.radius = 0.3
        self.verbose = False

        self.lines = VMobject()
        self.tree = VMobject() 
        self.ids = VMobject()
        self.treeMobject = VGroup()
        self.edgemk = VMobject()

        self.edg = [Edge(0,0)]
        self.head = [0]*self.edgnum
        self.dep = [0]*self.edgnum
        self.sidecnt = [(0,0)]
        self.fa = [0]*self.edgnum
        self.pos = [np.array([0,self.shiftup,0])]
        self.out = [0]*self.edgnum
        self.dfsord=[0]
        self.hasone=[False]*self.edgnum
        self.omega = [2*PI]*self.edgnum
        self.tau = [0]*self.edgnum
        self.size=[1]*self.edgnum
        self.edgeQ = [(0,0)]
        self.vis = [False]*self.edgnum
        self.curv = [(0,0)]

        for i in range(self.edgnum):
            x=Edge(0,0)
            self.edg.append(x)
        for i in range(self.edgnum):
            x=np.array([0,self.shiftup,0])
            self.pos.append(x)
        
    
    def add_edge(self,u,v):
        '''
        Add an edge from u to v.
        '''
        self.edgeQ.append((u,v));

    def remove_edge(self,u,v):
        '''
        Remove an edge from u to v.
        '''
        self.edgeQ.remove((u,v))
    
    def apply_edge(self):
        '''
        (private)
        Finally apply the edge.
        Appies the edge
        '''
        for (u,v) in self.edgeQ:
            if u==v:
                continue
            self.adde(u,v)

    def adde(self, u, v):
        '''
        (private)
        Add an edge applied on arraies inside.
        '''
        if self.verbose:
            print("Added edge  from and to"+str(u)+" "+str(v))
        self.hasone[u] = True
        self.hasone[v] = True

        self.out[u]=self.out[u]+1
        self.cnt = self.cnt+1

        self.edg[self.cnt].nxt = self.head[u]
        self.edg[self.cnt].to = v
        self.edg[self.cnt].top = 0
        self.edg[self.head[u]].top = self.cnt
        self.edg[self.cnt].bot = self.head[u]
        self.head[u] = self.cnt


    def dfs(self, x,layer,fat):
        '''
        (private)
        Get the basic arguments of the tree.
        '''
        self.dfsord.append(x)
        self.dep[x] = layer
        self.vis[x]=True
        self.fa[x] = fat
        i = self.head[x]
        if i==0:
            self.size[x]=1
        while i != int(0):
            v = self.edg[i].to
            if v != fat and self.vis[v]==False:
                self.dfs(self.edg[i].to,layer+1,x)
            self.size[x]=self.size[x]+self.size[self.edg[i].to]
            i = self.edg[i].nxt

    def getpos(self,v):
        '''
        (private)
        Get the x-y crood position between of a tree.
        '''

        if v!= self.treeroot:
            u=self.fa[v]
            self.pos[v] = self.pos[u]+2*np.array([math.cos(self.tau[v]+self.omega[v]/2),math.sin(self.tau[v]+self.omega[v]/2),0])  
        yita = self.tau[v]
        i = self.head[v]
        self.vis[v]=True
        while i != int(0):
            w = self.edg[i].to
            self.omega[w] = self.size[w]/self.size[1]*-self.factor*PI
            self.tau[w] = yita
            yita = yita+self.omega[w]
            if w!=self.fa[v] and self.vis[w]==False:
                self.getpos(self.edg[i].to)
            i = self.edg[i].nxt
            if self.verbose:
                print(i)

    def getxy(self):
        '''
        (private)
        Get the position between of a tree.
        '''
        self.getpos(self.treeroot)
        for i in range(1,self.edgnum):
            if self.hasone[i]:
                p=Circle(fill_color=GREEN,radius=0.25,fill_opacity=0.8,color=GREEN)
                p.move_to(self.pos[i])
                self.tree.add(p)
            else:
                p=Circle(fill_color=GREEN,radius=0.25,fill_opacity=0.8,color=GREEN)
                p.move_to(8*DOWN)
                self.tree.add(p)
        return self.tree

    def get_id(self):
        '''
        (private)
        Get the id between of a tree.
        '''
        for i in range(1,self.edgnum):
            if self.hasone[i]==True:
                ics=TextMobject(str(i))
                ics.move_to(self.pos[i]).shift((self.radius+0.1)*DOWN).scale(0.6)
                self.ids.add(ics)
        return self.ids

    def get_nodes(self):
        '''
        (private)
        Get the node (circle around the txts) of a tree.
        '''
        return self.tree
    
    def get_connection(self,x,fa):
        '''
        (private)
        Get the lines between of a tree.
        '''
        # In order to make all the arrow better, 
        # I modified Geometry.py Line 627 tip length = 0.2.
        for i in range(0,len(self.edgeQ)):
            found = False
            for j in range(len(self.curv)):
                print(self.curv[j])
                if(self.curv[j][0]==self.edgeQ[i][0] and self.curv[j][1]==self.edgeQ[i][1]):
                    found = True
            
            if found:
                ln = CurvedArrow(self.get_instance_of_id(self.edgeQ[i][0]).get_center(),self.get_instance_of_id(self.edgeQ[i][1]).get_center(),angle=PI/1.2,color=BLUE).set_sheen(0.9,UL)
            else:
                ln = Arrow(self.get_instance_of_id(self.edgeQ[i][0]).get_center(),self.get_instance_of_id(self.edgeQ[i][1]).get_center(),color=BLUE).set_sheen(0.9,UL)
            self.lines.add(ln)

            
        
        return self.lines

    def highlight_point(self,id):
        """
        Focuses on a node to stress
        """
        if self.hasone[id]:
            self.play(FocusOn(self.pos[id]))
        else:
            p=Circle(fill_color=YELLOW,radius=0.25,fill_opacity=0.9,color=YELLOW)
            p.move_to(8*DOWN)
    
    def highlight_edge(self,frm,to):
        """
        Focuses on an edge to stress
        """
        for i in range(0,len(self.sidecnt)):
            u = self.sidecnt[i][0]
            v = self.sidecnt[i][1]
            if u!=0 and v!=0:
                if frm==u and to==v:
                    self.play(FocusOn(self.lines[i-1]))
                    break
    
    def get_instance_of_id(self,x):
        """
        Returns a instance of node which you can apply methods on.
        """
        return self.tree[x-1]

    def get_instance_of_edge(self,frm,to):
        '''
        Returns a instance of edge which you can apply methods on.
        
        '''
        for i in range(0,len(self.sidecnt)):
            u = self.sidecnt[i][0]
            v = self.sidecnt[i][1]
            if u!=0 and v!=0:
                if frm==u and to==v:
                    return (self.lines[i-1])
                    break
    
    def get_arguments(self):
        '''
        (private)
        Get the datas of a tree.
        '''
        self.apply_edge()
        self.clear_visit_tag()
        self.dfs(self.treeroot,self.treeroot,0)
        self.clear_visit_tag()
        self.treeMobject.add(self.getxy())
        self.clear_visit_tag()
        self.treeMobject.add(self.get_nodes())
        self.clear_visit_tag()
        self.treeMobject.add(self.get_id())
        self.clear_visit_tag()
        self.treeMobject.add(self.get_connection(self.treeroot,0))

    def restart(self):
        '''
        (private)
        Restart the tree. Clear all the mobjects and datas.
        '''
        self.cnt = 0
        self.edg = [Edge(0,0)]
        self.head = [0]*self.edgnum
        self.dep = [0]*self.edgnum
        self.sidecnt = [(0,0)]
        self.fa = [0]*self.edgnum
        self.pos = [np.array([0,self.shiftup,0])]
        self.out = [0]*self.edgnum
        self.dfsord=[0]
        self.hasone=[False]*self.edgnum
        self.omega = [2*PI]*self.edgnum
        self.tau = [0]*self.edgnum
        self.size=[1]*self.edgnum
        for i in range(self.edgnum):
            x=Edge(0,0)
            self.edg.append(x)
        for i in range(self.edgnum):
            x=np.array([0,self.shiftup,0])
            self.pos.append(x)
        self.lines = VMobject()
        self.tree = VMobject() 
        self.ids = VMobject()
        self.treeMobject = VGroup()

    def draw_tree(self):
        '''
        Show up the tree onto the screen.
        '''
        self.clear_visit_tag()
        self.apply_edge()
        self.clear_visit_tag()
        self.dfs(self.treeroot,self.treeroot,0)
        self.clear_visit_tag()
        self.treeMobject.add(self.getxy())
        self.clear_visit_tag()
        self.treeMobject.add(self.get_nodes())
        self.clear_visit_tag()
        self.treeMobject.add(self.get_id())
        self.clear_visit_tag()
        self.treeMobject.add(self.get_connection(self.treeroot,0))
        self.play(Write(self.treeMobject))

    def update_transform(self):
        '''
        Update the tree on the screen, which uses the latest data to 
        reposition and rebuild the tree.
        '''

        utter = self.treeMobject.copy()
        self.remove(self.treeMobject)
        self.clear_visit_tag()
        self.restart()
        self.clear_visit_tag()
        self.get_arguments()
        self.play(Transform(utter,self.treeMobject))
        self.add(self.treeMobject)
        self.remove(utter)
        #self.play(Write(self.treeMobject))
    
    def dynamic_add_edge(self,frm,to):
        '''
        Dynamic add an edge onto the screen while play a short animation.
        TODO: The animation is not smooth...
        '''
        self.add_edge(frm,to)
        self.update_transform()

    def dynamic_remove_edge(self,frm,to):
        '''
        Dynamic remove an edge onto the screen while play a short animation.
        TODO: The animation is not smooth...
        '''
        self.remove_edge(frm,to)
        self.update_transform()

    def clear_visit_tag(self):
        for i in range(len(self.vis)):
            self.vis[i]=False



class Demonstrate(TreeScene):
    def construct(_):
        _.curv.append((3,4))
        _.curv.append((8,1))
        _.init()
        _.add_edge(1,2)
        _.add_edge(2,3)
        _.add_edge(3,4)
        _.add_edge(4,5)
        _.add_edge(5,2)
        _.add_edge(4,3)
        _.add_edge(3,5)
        _.draw_tree()
        


class Starting(Scene):
    def construct(_):
        t = TextMobject("强连通分量")
        t_sub = TextMobject("Strongly Connect Compoment").scale(0.6)
        VG = VGroup(t,t_sub)
        VG.arrange(DOWN)
        _.play(Write(t),Write(t_sub),run_timee=5)


class IntroductionByMC(Scene):
    # Will be introducted by MC...
    pass

class TarjanAlgorithmIntro(Scene):
    pass

class TextCollection(Scene):
    def construct(_):
        txt = TextMobject("This node can ","$also$"," \\textbf{go back to 1} $\\rightarrow$ ")
        txt[1].set_color(YELLOW)
        _.play(Write(txt))
        _.wait(5)
        _.play(Uncreate(txt))
        txt = TextMobject("If the node end up\\\\ with \\textbf{the same} ","$dfn$"," and ","$low$","\\\\ it has to be a root of SCC").shift(0.5*LEFT)
        arr = TextMobject("$\\rightarrow$").shift(3*RIGHT)
        txt[3].set_color(YELLOW)
        txt[1].set_color(YELLOW)

        _.play(Write(txt))
        _.play(Write(arr))
        _.wait(5)
        _.play(Uncreate(txt),Uncreate(arr))
        _.wait(2)



class Working1(TreeScene):

    def construct(_):
        def prepare_for_tarjan():
            _.init()
            # _.add_edge(1,2)
            # _.add_edge(2,3)
            # _.add_edge(3,4)
            # _.add_edge(4,2)
            # _.add_edge(3,5)
            # _.add_edge(4,5)
            # _.add_edge(1,6)
            # _.add_edge(6,7)
            # _.add_edge(7,1)
            _.curv.append((3,4))
            _.curv.append((8,1))
            _.add_edge(1,2)
            _.add_edge(1,6)
            _.add_edge(2,3)
            _.add_edge(3,1)
            _.draw_tree()
            _.stele = VGroup()
            _.cnttt = 0
        def Tarjan():
            _.dfn = [0]*_.edgnum
            _.low = [0]*_.edgnum
            _.timee = 0
            _.sta = []
            _.clear_visit_tag()
        
        def instk(k):
            for i in _.sta :
                if(i==k) :
                    return True
            return False
        def getins(k):

            
            _.sta.append(k)
            # _.stele.add(TextMobject(str(k)).move_to(np.array([2,_.cnttt*0.5-3,1])))
            x = TextMobject(str(k)).move_to(np.array([4,_.cnttt*0.5-3,1]))
            _.play(FadeIn(x,direction=UP))
            _.stele.add(x)
            _.cnttt = _.cnttt+1
        
        def getot():
            k = _.sta.pop()
            _.play(FadeOut(_.stele[len(_.stele)-1],direction = UP))
            _.stele.remove(_.stele[len(_.stele)-1])
            _.cnttt=_.cnttt-1
            return k


        def tj(u):
            _.play(ShowCreationThenDestructionAround(_.get_instance_of_id(u)))
            _.timee = _.timee+1
            _.timeers.become(TextMobject(str(_.timee)).move_to(UL*2))
            _.wait(0.5)
            _.dfn[u] = _.timee
            _.low[u] = _.timee
            _.play(_.vgp[u].scale,(2))
            _.vgp[u].become(TextMobject("(",str(int(_.dfn[u])),",",str(int(_.low[u])),")").move_to(_.get_instance_of_id(u)).scale(1))
            _.play(_.vgp[u].scale,(0.5))
            getins(u)
            i = _.head[u]
            _.vis[u]=True
            while i != int(0):
                w = _.edg[i].to
                g = _.get_instance_of_edge(u,w)
                expl = Arrow(_.get_instance_of_id(u).get_center(),_.get_instance_of_id(w).get_center(),color = YELLOW)
                _.play(Write(expl))
                _.play(Uncreate(expl))
                if _.vis[w] == False :
                    
                    tj(w)
                    
                    #_.play(_.vgp[u][3].scale,(5),_.vgp[w][3].scale,(5))
                    _.low[u] = min(_.low[u],_.low[w])
                    #_.play(_.vgp[u][3].scale,(0.2),_.vgp[w][3].scale,(0.2))
                    _.play(FocusOn(_.get_instance_of_id(u)))
                    _.play(_.vgp[u].scale,(2))
                    _.vgp[u].become(TextMobject("(",str(int(_.dfn[u])),",",str(int(_.low[u])),")").move_to(_.get_instance_of_id(u)).scale(1))
                    _.play(_.vgp[u].scale,(0.5))
                    _.wait(1)
                elif instk(w):
                    
                    #_.play(_.vgp[u][3].scale,(5),_.vgp[w][1].scale,(5))
                    _.low[u] = min(_.low[u],_.dfn[w])
                    #_.play(_.vgp[u][3].scale,(0.2),_.vgp[w][1].scale,(0.2))
                    _.play(FocusOn(_.get_instance_of_id(u)))
                    _.play(_.vgp[u].scale,(2))
                    _.vgp[u].become(TextMobject("(",str(int(_.dfn[u])),",",str(int(_.low[u])),")").move_to(_.get_instance_of_id(u)).scale(1))
                    _.play(_.vgp[u].scale,(0.5))
                    _.wait(1)
                i = _.edg[i].nxt
                
            _.play(ShowCreationThenDestruction(_.get_instance_of_id(u)))
            
            if(_.dfn[u]==_.low[u]):
                v = getot()
                print(str(v))
                while u!=v:
                    v = getot()
                    print(str(v))
                    
                
                print("----")
        
        def summon_txt():
            _.timeers = TextMobject("0").move_to(UL*2)
            _.play(Write(_.timeers))
            _.vgp = VGroup()
            for i in range((_.edgnum)) :
               tx = TextMobject("(0,0)").move_to(_.get_instance_of_id(i)).scale(0.5)
               _.vgp.add(tx)
            _.play(Write(_.vgp))
        
        
           

        prepare_for_tarjan()
        summon_txt()
        Tarjan()
        tj(1)
        
        _.wait(2)


class AlgoDemo(TreeScene):

    def construct(_):
        def prepare_for_tarjan():
            _.init()
            # _.add_edge(1,2)
            # _.add_edge(2,3)
            # _.add_edge(3,4)
            # _.add_edge(4,2)
            # _.add_edge(3,5)
            # _.add_edge(4,5)
            # _.add_edge(1,6)
            # _.add_edge(6,7)
            # _.add_edge(7,1)
            _.curv.append((3,4))
            _.curv.append((8,1))
            _.add_edge(1,2)
            _.add_edge(1,6)
            _.add_edge(2,3)
            _.add_edge(3,4)
            _.add_edge(4,5)
            _.add_edge(5,2)
            _.add_edge(4,3)
            _.add_edge(3,5)
            _.add_edge(6,8)
            _.add_edge(8,1)
            _.add_edge(1,9)
            _.draw_tree()
            _.stele = VGroup()
            _.cnttt = 0
        def Tarjan():
            _.dfn = [0]*_.edgnum
            _.low = [0]*_.edgnum
            _.timee = 0
            _.sta = []
            _.clear_visit_tag()
        
        def instk(k):
            for i in _.sta :
                if(i==k) :
                    return True
            return False
        def getins(k):

            
            _.sta.append(k)
            # _.stele.add(TextMobject(str(k)).move_to(np.array([2,_.cnttt*0.5-3,1])))
            x = TextMobject(str(k)).move_to(np.array([4,_.cnttt*0.5-3,1]))
            _.play(FadeIn(x,direction=UP))
            _.stele.add(x)
            _.cnttt = _.cnttt+1
        
        def getot():
            k = _.sta.pop()
            _.play(FadeOut(_.stele[len(_.stele)-1],direction = UP))
            _.stele.remove(_.stele[len(_.stele)-1])
            _.cnttt=_.cnttt-1
            return k


        def tj(u):
            _.play(ShowCreationThenDestructionAround(_.get_instance_of_id(u)))
            _.timee = _.timee+1
            _.timeers.become(TextMobject(str(_.timee)).move_to(UL*2))
            _.wait(0.5)
            _.dfn[u] = _.timee
            _.low[u] = _.timee
            _.play(_.vgp[u].scale,(2))
            _.vgp[u].become(TextMobject("(",str(int(_.dfn[u])),",",str(int(_.low[u])),")").move_to(_.get_instance_of_id(u)).scale(1))
            _.play(_.vgp[u].scale,(0.5))
            getins(u)
            i = _.head[u]
            _.vis[u]=True
            while i != int(0):
                w = _.edg[i].to
                g = _.get_instance_of_edge(u,w)
                expl = Arrow(_.get_instance_of_id(u).get_center(),_.get_instance_of_id(w).get_center(),color = YELLOW)
                _.play(Write(expl))
                _.play(Uncreate(expl))
                if _.vis[w] == False :
                    
                    tj(w)
                    
                    _.play(_.vgp[u][3].scale,(5),_.vgp[w][3].scale,(5))
                    _.low[u] = min(_.low[u],_.low[w])
                    _.play(_.vgp[u][3].scale,(0.2),_.vgp[w][3].scale,(0.2))
                    _.play(FocusOn(_.get_instance_of_id(u)))
                    _.play(_.vgp[u].scale,(2))
                    _.vgp[u].become(TextMobject("(",str(int(_.dfn[u])),",",str(int(_.low[u])),")").move_to(_.get_instance_of_id(u)).scale(1))
                    _.play(_.vgp[u].scale,(0.5))
                    _.wait(1)
                elif instk(w):
                    
                    _.play(_.vgp[u][3].scale,(5),_.vgp[w][1].scale,(5))
                    _.low[u] = min(_.low[u],_.dfn[w])
                    _.play(_.vgp[u][3].scale,(0.2),_.vgp[w][1].scale,(0.2))
                    _.play(FocusOn(_.get_instance_of_id(u)))
                    _.play(_.vgp[u].scale,(2))
                    _.vgp[u].become(TextMobject("(",str(int(_.dfn[u])),",",str(int(_.low[u])),")").move_to(_.get_instance_of_id(u)).scale(1))
                    _.play(_.vgp[u].scale,(0.5))
                    _.wait(1)
                i = _.edg[i].nxt
                
            _.play(ShowCreationThenDestruction(_.get_instance_of_id(u)))
            
            if(_.dfn[u]==_.low[u]):
                v = getot()
                print(str(v))
                while u!=v:
                    v = getot()
                    print(str(v))
                    
                
                print("----")
        
        def summon_txt():
            _.timeers = TextMobject("0").move_to(UL*2)
            _.play(Write(_.timeers))
            _.vgp = VGroup()
            for i in range((_.edgnum)) :
               tx = TextMobject("(0,0)").move_to(_.get_instance_of_id(i)).scale(0.5)
               _.vgp.add(tx)
            _.play(Write(_.vgp))
        
        
           

        prepare_for_tarjan()
        summon_txt()
        Tarjan()
        tj(1)
        
        _.wait(2)
