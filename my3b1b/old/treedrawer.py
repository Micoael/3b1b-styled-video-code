from manimlib.imports import *
from PrimoCreature import *

# These are utils
class Edge():
    def __init__(self, _nxt, _to):
        self.nxt = _nxt
        self.to = _to


class Graph():
    
    def __init__(self):
        self.cnt = 0
        self.cnt2=0
        self.edgnum = 21
        self.treeroot = 1

        self.lines = VMobject()
        self.edgemk=VMobject()
        self.tree = VMobject() 
        self.linefordfs2 = VMobject()
        self.ids = VMobject()
        self.edgmkafterdfs = VMobject()
        self.edgmkafterdfs2 = VMobject()
        self.childsize=VMobject()


        self.edg = [Edge(0,0)]
        self.head = [0]*self.edgnum
        self.dep = [0]*self.edgnum
        self.eachdepth = [0]*self.edgnum
        self.fa = [0]*self.edgnum
        self.pos = [np.array([0,0,0])]
        self.out = [0]*self.edgnum
        self.dfsord=[0]
        self.son=[0]*self.edgnum
        self.id=[0]*self.edgnum
        self.a=[0]*self.edgnum
        self.top=[0]*self.edgnum
        self.w=[1,2,3,4,5,6,7,8,9,10]*2
        self.dfsxord=[0]*self.edgnum
        self.left=[np.array([0,0,0])]
        self.right=[np.array([0,0,0])]
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
        for i in range(self.edgnum):
            x=2*UP
            self.left.append(np.array([0,0,0]))
            self.right.append(np.array([0,0,0]))

        

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

    def dfs2(self,u,t,fa):
        self.dfsxord.append(u)
        self.cnt2 =self.cnt2 +1
        self.id[u] = self.cnt2
        self.a[self.cnt]=self.w[u]
        self.top[u]=t


        if self.son[u]!=0:
            self.dfs2(self.son[u],t,u)
        
        i = self.head[u]
        
        while i != int(0):
            v = self.edg[i].to


            if v != self.fa[u] and v!=self.son[u]:
                self.dfs2(v,v,u)
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

    def getxy(self):
        
        self.getpos(self.treeroot)


        for i in range(1,self.edgnum):


            if self.hasone[i]:
                p=Circle(fill_color=BLUE,radius=0.25,fill_opacity=0.8,color=BLUE)
                p.move_to(self.pos[i])
                self.tree.add(p)
            else:
                p=Circle(fill_color=BLUE,radius=0.25,fill_opacity=0.8,color=BLUE)
                p.move_to(20*DOWN)
                self.tree.add(p)


        return self.tree

    def get_id(self):


        for i in range(1,self.edgnum):
            if self.hasone[i]==True:
                ics=TextMobject(str(i))
                ics.move_to(self.pos[i])
                self.ids.add(ics)


        return self.ids
    
    def get_connection(self,x,fa):


        if fa==0:
            pass
        else:
            ln = Line(self.pos[fa],self.pos[x],color=BLUE)
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


        if self.hasone[id]:
            p=Circle(fill_color=YELLOW,radius=0.25,fill_opacity=0.9,color=YELLOW)
            p.move_to(self.pos[id])
        else:
            p=Circle(fill_color=YELLOW,radius=0.25,fill_opacity=0.9,color=YELLOW)
            p.move_to(20*DOWN)


        return p
    
    def get_arguments(self):

        self.dfs(self.treeroot,0,0)
        self.getxy()


    def get_nodes(self):

        return self.tree

    def get_nodes_of_pf(self):

        for i in range(1,self.edgnum):
            print(self.id[i])
            if self.hasone[i]==True:
                ics=TextMobject(str(self.id[i]))
                ics.move_to(self.pos[i])
                self.edgmkafterdfs.add(ics)
            else:
                ics=TextMobject(str(self.id[i]))
                ics.move_to(20*DOWN)
                self.edgmkafterdfs.add(ics)

        return self.edgmkafterdfs
    
    def drawsize(self):

        for i in range(1,self.edgnum):
            if self.hasone[i]==True:
                ics=TextMobject("$size=$"+str(self.size[i]))
                ics.move_to(self.pos[i]).shift(0.3*DOWN).scale(0.4)
                self.childsize.add(ics)
            else:
                ics=TextMobject(str(i))
                ics.move_to(20*DOWN)
                self.childsize.add(ics)

        return self.childsize

#These are also utils
class Edge0():
    def __init__(self, _nxt, _to):
        self.nxt = _nxt
        self.to = _to


class Graph0():
    
    def __init__(self):
        self.cnt2=0
        self.lines = VMobject()
        self.edg = [Edge(0,0)]
        for i in range(21):
            x=Edge(0,0)
            self.edg.append(x)
        self.cnt = 0
        self.head = [0]*20
        self.dep = [0]*20
        self.eachdepth = [0]*20
        self.fa = [0]*20
        self.pos = [np.array([0,0,0])]
        self.out = [0]*20
        self.dfsord=[0]
        self.son=[0]*20
        self.id=[0]*20
        self.a=[0]*50
        self.top=[0]*20
        self.w=[1,2,3,4,5,6,7,8,9,10]*2
        for i in range(21):
            x=np.array([0,2,0])
            self.pos.append(x)
        self.hasone=[False]*20
        self.edgemk=VMobject()

        self.left=[np.array([0,0,0])]
        self.right=[np.array([0,0,0])]
        for i in range(20):
            x=2*UP
            self.left.append(np.array([0,0,0]))
            self.right.append(np.array([0,0,0]))

        self.tree = VMobject() 
        self.ids = VMobject()
        self.edgmkafterdfs = VMobject()

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
            if self.size[self.edg[i].to]>self.size[self.son[x]]:
                self.son[x] = self.edg[i].to
            i = self.edg[i].nxt

    def dfs2(self,u,t):
        self.cnt2 =self.cnt2 +1
        self.id[u] = self.cnt2
        self.a[self.cnt]=self.w[u]
        self.top[u]=t
        if self.son[u]!=0:
            self.dfs2(self.son[u],t)
        
        i = self.head[u]
        
        while i != int(0):
            v = self.edg[i].to
            if v != self.fa[u] and v!=self.son[u]:
                self.dfs2(v,v)
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
                p=Circle(fill_color=BLUE,radius=0.3,fill_opacity=0.9,color=BLUE)
                p.move_to(self.pos[i])
                self.tree.add(p)
            else:
                p=Circle(fill_color=BLUE,radius=0.3,fill_opacity=0.9,color=BLUE)
                p.move_to(20*DOWN)
                self.tree.add(p)
        return self.tree

    def get_id(self):
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
            ln = Line(self.pos[fa],self.pos[x],color=BLUE)
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
        if self.hasone[id]:
            p=Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.2,color=YELLOW)
            p.move_to(self.pos[id])
        else:
            p=Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.2,color=YELLOW)
            p.move_to(20*DOWN)
        return p
    
    def get_arguments(self):
        self.dfs(1,0,0)
        self.getxy()

    def get_nodes(self):
        return self.tree

#These are animations
class PrimoDice(Scene):
    def construct(self):
        Ale = PrimoCreature()
        Ale.look_at(np.array([0, 0, 0]))
        Ale.init_colors()
        palabras_ale = TextMobject("我会说中文啦~")
        self.add(Ale)
        self.play(PrimoCreatureSays(
            Ale, palabras_ale,
            bubble_kwargs={"height": 4, "width": 6},
            target_mode="speaking"
        ))
        self.wait()
        self.play(Blink(Ale))
        self.wait(1)
        self.play(Blink(Ale))
        self.wait(1)
        self.play(Blink(Ale))
        self.wait(1)
        self.play(Blink(Ale))
        self.wait(1)


class PerformDFSOrder(Scene):
    
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
        
        g.dfs(1,0,1)
        for i in range(0,19):
            print("layer"+str(i))
            print(g.eachdepth[g.dep[i]])
        s = g.getxy()
        print(g.pos)
        ids = g.get_id()
        bdr = g.get_connection(1,0)
        self.play(Write(s),Write(bdr),Write(g.edgemk),Write(ids))

        dfsod = VMobject()
        highlight=VMobject()
        ulmo =VMobject()
        for i in range(1,len(g.dfsord)):
            pt = g.highlight_point(g.dfsord[i])
            highlight.add(pt)
            self.play(ShowCreation(pt))
            t = TextMobject("\\#"+str(i)).move_to(g.pos[g.dfsord[i]]+0.3*RIGHT).scale(0.4)
            dfsod.add(t)
            self.play(Write(t),run_time=0.5)
            tt=t.copy()
            ulmo.add(tt)
            self.play(ApplyMethod(tt.move_to,3*DL+0.5*i*RIGHT))
            if i>len(g.lines):
                pass
            else:
                self.play(ApplyMethod(g.lines[i-1].set_color,YELLOW),run_time=0.5)
                self.play(ApplyMethod(g.lines[i-1].set_color,BLUE),run_time=0.5)
        
        self.wait(1)

        self.play(FadeOut(highlight))

        self.play(ShowCreation(g.highlight_point(6)),ShowCreation(g.highlight_point(7)),ShowCreation(g.highlight_point(8)),ShowCreation(g.highlight_point(9)))
        self.wait(3)
        self.play(
            ulmo[2].scale,(2),
            ulmo[3].scale,(2),
            ulmo[4].scale,(2),
            ulmo[5].scale,(2),
        )


class Starting(Scene):
    def construct(self):
        primo = PrimoCreature().shift(2*DOWN).scale(0.5)
        primo.look_at(UP+LEFT)
        self.play(FadeIn(primo))
        self.wait(2)
        palabras_ale = TextMobject("用倍增法求解LCA")
        self.play(PrimoCreatureSays(
            primo, palabras_ale,
            bubble_kwargs={"height": 5, "width": 6},
            target_mode="plain"
        ))

    
class IntroOfDT(Scene):
    
    def construct(self):

        g = Graph()
        g.adde(1,2)
        g.adde(1,4)
        g.adde(1,3)
        g.adde(2,5)
        g.adde(5,10)
        g.adde(3,6)
        g.adde(4,7)
        g.adde(4,8)
        g.adde(4,9)
        g.adde(4,13)
        g.adde(4,15)
        g.get_arguments()
        g.dfs2(1,0,0)
        
        s = g.get_nodes()
        ids = g.get_id()
        id_after = g.get_nodes_of_pf()
        bdr = g.get_connection(1,0)
        print("son:")
        print(g.id)
        print(g.hasone)
        
        self.play(Write(bdr),Write(s),Write(ids),Write(g.edgemk),Write(g.drawsize()),run_time=5)

        txt=TextMobject("按照子树的大小分成重($heavy$)儿子和轻($light$)儿子").move_to(3.5*UP).scale(0.8)

        self.play(FadeInFromDown(txt))
        self.wait(3)
        self.play(FadeOutAndShiftDown(txt))

        self.play(
            g.childsize[1].scale,2,
            g.childsize[2].scale,2,
            g.childsize[3].scale,2,
        )

        self.wait(5)
        self.play(FocusOn(g.pos[1]))


        self.play(ApplyMethod(g.childsize[3].scale,2))


        self.wait()
        self.play(
            g.childsize[1].scale,0.5,
            g.childsize[2].scale,0.5,
            g.childsize[3].scale,0.25,
        )


        gm = VMobject()

        for i in range(1,len(g.son)):
            if g.hasone[g.son[i]]:
                i = g.highlight_point(g.son[i])
                gm.add(i)
                self.play(ShowCreation(i))

        self.play(FadeOut(g.edgemk),FadeOut(ids))

        a = g.get_connection_for_dfs2(1,1,0)
        for i in range (0,len(a)):
            self.play(Write(a[i]),run_time=0.4)
            self.play(Write(g.edgmkafterdfs2[i]),run_time=0.4)

        
        self.play(Write(g.edgmkafterdfs),run_time=3)

        self.wait(2)

        txt=TextMobject("用重($heavy$)边把所有的重孩子连接起来").move_to(3.5*UP).scale(0.8)

        self.play(FadeInFromDown(txt))
        self.wait()
        self.play(FadeOutAndShiftDown(txt))
        self.play(
            a[0].set_color,YELLOW,
            a[0].scale,0.2,
            a[7].set_color,YELLOW,
            a[7].scale,0.2,
            a[1].set_color,YELLOW,
            a[1].scale,0.2,
            a[9].set_color,YELLOW,
            a[9].scale,0.2,
            a[10].set_color,YELLOW,
            a[10].scale,0.2,
        )
        
        self.play(
            WiggleOutThenIn(a[0]),
            WiggleOutThenIn(a[7]),
            WiggleOutThenIn(a[1]),
            WiggleOutThenIn(a[9]),
            WiggleOutThenIn(a[10]),
            a[0].scale,5,
            a[7].scale,5,
            a[1].scale,5,
            a[9].scale,5,
            a[10].scale,5,
        )



        self.remove(bdr)
        self.wait()
        
        txt=TextMobject("重($heavy$)链").move_to(3*UP).scale(0.8)

        self.play(FadeInFromDown(txt))
        self.wait(5)
        self.play(FadeOutAndShiftDown(txt))
        
        x1 = TextMobject("我们需要维护...")
        x8 = TextMobject("head[x]")
        x2 = TextMobject("fa[x],dep[x],size[x]")
        x3 = TextMobject("id[x]")
        x4 = TextMobject("val[x]")
        x5 = TextMobject("top[x]")
        xs = VGroup(x1,x8,x2,x3,x4,x5,)
        xs.arrange(DOWN)
        xs.add_background_rectangle()
        self.play(Write(xs),run_time=5)
        self.play(
            x3.set_color,YELLOW
        )
        self.wait(3)
        self.play(
            x4.set_color,YELLOW
        )
        self.wait(5)
        self.play(
            x5.set_color,YELLOW
        )
        self.wait(3)

        self.play(FadeOut(xs))

        
class LCA(Scene):
    def construct(self):
        x = Text("LCA <==> ?",font='Consolas')
        self.play(Write(x))
        self.wait(2)
        self.remove(x)
        g = Graph()
        g.adde(1,4)
        g.adde(4,7)
        g.get_arguments()
        s = g.get_nodes().shift(4*LEFT)
        ids = g.get_id().shift(4*LEFT)
        bdr = g.get_connection(1,0).shift(4*LEFT)
        self.play(Write(bdr),Write(s),Write(ids))
        x = TextMobject("如果他们在同一条链上:").shift(3.5*UP)
        self.play(Write(x))
        a = g.highlight_point(1).shift(4*LEFT)
        b = g.highlight_point(4).shift(4*LEFT)
        self.play(Write(a),Write(b))
        self.play(
            b.scale,2
        )
        self.play(FadeOut(a),FadeOut(b))
        y = TextMobject("如果他们不在同一条链上:").shift(3.5*UP)
        self.play(Transform(x,y))
        f = Graph()
        f.adde(1,8)
        f.adde(8,9)
        f.adde(9,10)
        f.adde(1,5)
        f.get_arguments()
        sf = f.get_nodes().shift(4*LEFT)
        idsf = f.get_id().shift(4*LEFT)
        bdrf = f.get_connection(1,0).shift(4*LEFT)
        self.play(Write(bdrf),Write(sf),Write(idsf))

        a = f.highlight_point(9).shift(4*LEFT)
        b = g.highlight_point(7).shift(4*LEFT)
        self.play(
            f.lines[1].set_color,YELLOW,
            f.lines[2].set_color,YELLOW,
            f.lines[3].set_color,YELLOW,
            g.lines[1].set_color,YELLOW,
        )
        self.play(
            ShowCreation(a),
            ShowCreation(b)
        )
        self.play(
            a.scale,2,
            b.scale,2
        )
        self.play(
            a.scale,0.5,
            b.scale,0.5
        )
        y = TextMobject("转换到同一条链上..").add_background_rectangle()
        self.play(Write(y))
        self.wait(2)
        self.play(FadeOutAndShiftDown(y))

        y = TextMobject("top[a] = top[b] ").add_background_rectangle()
        self.play(Write(y))
        self.wait(2)
        self.play(FadeOutAndShiftDown(y))
        
        self.wait(3)
        y = TextMobject("应该让哪个点先到哪呢？").add_background_rectangle()
        self.play(Write(y))
        self.wait(2)
        self.play(FadeOutAndShiftDown(y))
        
        self.play(
            a.move_to,(f.pos[8])+4*LEFT
        )
        y = TextMobject("$$top[a] \\not = top[b] $$").add_background_rectangle()
        self.play(Write(y))
        self.play(
            a.move_to,(f.pos[1])+4*LEFT
        )
        self.wait(5)
        self.play(y.scale,1.5,run_time=0.5)
        self.play(y.scale,2/3,run_time=0.5)
        self.play(FadeOutAndShiftDown(y))

        self.play(
            a.move_to,(f.pos[9])+4*LEFT
        )
        self.wait(5)
        self.play(
            b.move_to,(g.pos[1])+4*LEFT
        )
        self.wait(15)
        
        y = Text("√",font="等线")
        self.play(Write(y),run_time=3)

        x = TextMobject("$\\rightarrow$ To be continued "," $now$...").shift(3*DOWN+RIGHT)
        self.play(Write(x[0]))
        self.wait(5)
        self.play(Write(x[1]))


class FootScript(Scene):
    def construct(self):
        txt = [TextMobject("重新DFS有什么用?"),
               TextMobject("一切的真相…","——维护数据结构") ]
        self.play(FadeInFromDown(txt[0]))
        self.play(FadeOut(txt[0]))
        self.play(FadeInFromDown(txt[1][0]))
        self.play(Write(txt[1][1]))
        self.play(FadeOut(txt[1][0]))
        self.play(txt[1][1].shift,3.5*UP)

        conc = TextMobject("原来的树"," $\\rightarrow$ ","重链优化"," $\\rightarrow$ ","用其他数据结构维护")
        conc[0].set_color(GRAY)
        conc[1].set_color(GRAY)
        conc[3].set_color(GRAY)
        conc[2].set_color(GRAY)
        conc[4].set_color(GRAY)
        for i in range(5):
            self.play(Write(conc[i]))

        self.play(
            conc[0].set_color,(BLUE),
            conc[2].set_color,(BLUE),
            conc[1].set_color,(YELLOW),
            FocusOn(conc[1])
        )
        tip1 = TextMobject("重链选不好，时间短不了").move_to(conc[1]).shift(0.5*UP).add_background_rectangle().scale(0.8)
        self.play(Write(tip1))
        self.wait(2)
        x1 = TextMobject("性质").shift(3.5*UP)
        x2 = TextMobject("· 轻边$(u,v)$中, $size(u) \\geq size( \\frac{v}{2} )$ \\\\ · 根到某一点的路径中,不超过$\\log_2 x$个轻链和$\\log_2 x$个重链")
        xs = VGroup(x1,x2)
        xs.arrange(DOWN)
        xs.add_background_rectangle()
        self.play(Write(xs))
        self.wait(2)
        self.play(FadeOutAndShift(xs))
        self.play(FadeOutAndShiftDown(tip1))
        self.play(
            conc[1].set_color,(GRAY),
            conc[0].set_color,(GRAY),
            conc[2].set_color,(BLUE),
            conc[4].set_color,(BLUE),
            conc[3].set_color,(YELLOW),
            FocusOn(conc[3])
        )
        tip1 = TextMobject("$\\leftarrow$连续区间").move_to(conc[3]).shift(0.5*UP).add_background_rectangle().scale(0.8)
        self.play(Write(tip1))
        self.wait(2)
        self.play(FadeOutAndShiftDown(tip1))
        self.play(FadeOut(txt[1][1]))

        self.play(
            FadeOutAndShiftDown(conc[1]),
            FadeOutAndShiftDown(conc[0]),
            FadeOutAndShiftDown(conc[2]),
            FadeOutAndShiftDown(conc[3]),
            conc[4].shift,2*LEFT
        )
        self.wait(2)
        st = TextMobject("线段树($Segment$ $Tree$)")
        self.play(Transform(conc[4],st))
        self.wait(5)
        

class Modifys(Scene):
    def construct(self):
        
        
        tit = TextMobject("·", " 统计$x$到$y$最短路径的权值和 ","·").shift(3.5*UP)
        tit[0].set_color(BLUE)
        tit[2].set_color(BLUE)
        self.play(Write(tit))
        sums = TextMobject("SUM").shift(3*DOWN)
        self.play(Write(sums))
        f = Graph()
        f.adde(1,2)
        f.adde(2,3)
        f.adde(3,4)
        f.adde(1,5)
        f.adde(1,6)
        f.adde(6,7)
        f.get_arguments()
        sf = f.get_nodes()
        idsf = f.get_id()
        bdrf = f.get_connection(1,0)
        self.play(Write(bdrf),Write(sf),Write(idsf))
        self.play(
            f.lines[1].set_color,YELLOW,
            f.lines[5].set_color,YELLOW,
            f.lines[3].set_color,YELLOW,
            f.lines[4].set_color,YELLOW,
        )

        a = f.highlight_point(4).set_opacity(0.5)
        b = f.highlight_point(7).set_opacity(0.5)
        self.play(Write(a),Write(b))
        self.wait(2)
        
        hint = [TextMobject("id[6]").add_background_rectangle().move_to(f.pos[6]).scale(0.8),
                TextMobject("id[7]").add_background_rectangle().move_to(f.pos[7]).scale(0.8),
                TextMobject("id[1]").add_background_rectangle().move_to(f.pos[1]).scale(0.8),
                TextMobject("id[4]").add_background_rectangle().move_to(f.pos[4]).scale(0.8),]
        self.play(Write(hint[0]),Write(hint[1]))
        self.play(
            hint[0].move_to,(sums),
            hint[1].move_to,(sums),
        )
        self.play(
            FadeOut(hint[0]),
            FadeOut(hint[1]),
        )

        self.wait()
        self.play(
            b.move_to,(f.pos[1])
        )

        self.play(Write(hint[2]),Write(hint[3]))
        self.play(
            hint[2].move_to,(sums),
            hint[3].move_to,(sums),
        )
        self.play(
            FadeOut(hint[2]),
            FadeOut(hint[3]),
        )
        
        
class Adds(Scene):
    def construct(self):
        self.wait()
        
        a = TextMobject("树上修改和查询").scale(1.5)
        b = TextMobject("· $DFS$ 序\\ \\ \\ \\ \\ ").shift(0.2*DOWN)
        c = TextMobject("· 一些数据结构")
        d = VGroup(a,b,c).arrange(DOWN)
        self.play(FadeInFromDown(a),run_time=1)
        self.play(a.shift,UP)
        self.play(FadeInFromDown(b),run_time=1)
        
        self.play(FadeInFromDown(c),run_time=1)
        self.wait()
        self.play(
            d.shift,8*UP
        )
        tit = TextMobject("·", " 从 $x$ 到 $y$ 的路径中加 $m$ ","·").shift(3.5*UP)
        tit[0].set_color(BLUE)
        tit[2].set_color(BLUE)
        self.play(Write(tit))
        sums = TextMobject("SUM").shift(3*DOWN)
        f = Graph()
        f.adde(1,2)
        f.adde(2,3)
        f.adde(3,4)
        f.adde(1,5)
        f.adde(1,6)
        f.adde(6,7)
        f.get_arguments()
        sf = f.get_nodes()
        idsf = f.get_id()
        bdrf = f.get_connection(1,0)
        self.play(Write(bdrf),Write(sf),Write(idsf))
        self.play(
            f.lines[1].set_color,YELLOW,
            f.lines[5].set_color,YELLOW,
            f.lines[3].set_color,YELLOW,
            f.lines[4].set_color,YELLOW,
        )

        a = f.highlight_point(4).set_opacity(0.5)
        b = f.highlight_point(7).set_opacity(0.5)
        self.play(Write(a),Write(b))
        self.wait(2)
        
        hint = [TextMobject("id[6]").add_background_rectangle().move_to(f.pos[6]).scale(0.8),
                TextMobject("id[7]").add_background_rectangle().move_to(f.pos[7]).scale(0.8),
                TextMobject("id[1]").add_background_rectangle().move_to(f.pos[1]).scale(0.8),
                TextMobject("id[4]").add_background_rectangle().move_to(f.pos[4]).scale(0.8),]
        self.play(FadeInFromDown(hint[0]),FadeInFromDown(hint[1]))
        self.wait(5)
        self.play(
            FadeOut(hint[0]),
            FadeOut(hint[1]),
        )
        
        self.wait()
        self.play(
            b.move_to,(f.pos[1])
        )
        self.wait(5)
        self.play(FadeInFromDown(hint[2]),FadeInFromDown(hint[3]))
        self.wait(5)
        self.play(
            FadeOut(hint[2]),
            FadeOut(hint[3]),
        )  


class Adds2(Scene):
    def construct(self):
        tit = TextMobject("·", " 从 $x$ 为根节点的子树加 $m$ ","·").shift(3.5*UP)
        tit[0].set_color(BLUE)
        tit[2].set_color(BLUE)
        self.play(Write(tit))
        sums = TextMobject("SUM").shift(3*DOWN)
        f = Graph()
        f.adde(1,2)
        f.adde(2,3)
        f.adde(3,4)
        f.adde(1,5)
        f.adde(1,6)
        f.adde(6,7)
        f.get_arguments()
        sf = f.get_nodes()
        idsf = f.get_id()
        bdrf = f.get_connection(1,0)
        self.play(Write(bdrf),Write(sf),Write(idsf))
        self.play(
            f.lines[1].set_color,YELLOW,
            f.lines[5].set_color,YELLOW,
            f.lines[3].set_color,YELLOW,
            f.lines[4].set_color,YELLOW,
        )

        a = f.highlight_point(1).set_opacity(0.5)
        
        self.play(ShowCreation(a))
        self.wait(2)
        
        hint = [TextMobject("id[6]").add_background_rectangle().move_to(f.pos[6]).scale(0.8),
                TextMobject("id[7]").add_background_rectangle().move_to(f.pos[7]).scale(0.8),
                TextMobject("id[1]").add_background_rectangle().move_to(f.pos[1]).scale(0.8),
                TextMobject("id[4]").add_background_rectangle().move_to(f.pos[4]).scale(0.8),]
        mp = idsf.copy()
        size = TextMobject("$\\ $","$size(x)$","$=7$").add_background_rectangle()
        self.play(Transform(mp,size))
        size = TextMobject("$x+$","$size(x)$","$-1$").add_background_rectangle()
        self.wait(2)
        self.play(Transform(mp,size),run_time=2)
        
        tit2 = TextMobject("·", " 从 $x$ 为根节点的子树查找节点值的和 ","·").shift(3.5*UP)
        tit2[0].set_color(BLUE)
        tit2[2].set_color(BLUE)
        self.wait(2)
        self.play(Transform(tit,tit2),run_time=3)


class Ending(Scene):
    def construct(self):
        txt =[TextMobject(" Sleator & Tarjan (1983) "),
              TextMobject("A Data Structure for Dynamic Trees")]