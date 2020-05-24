from manimlib.imports import *

class VideoStart(Scene):
    CONFIG = {
        "Author"        : "Micoael_Primo",
        "title_name"    : "Micoael\_Primo",
        "subtitle_name" : "Null",
        "svg_filename"  : "D:\\3b1b\\manim\\assets\\ec.PNG",
    }
    def construct(self):
        author = TextMobject(
            "$\\bold{Completely}$ understanding $LCA$"
        ).scale(1.5)
        svg_file = TextMobject("$\\bold{</>}$").scale(3)
        svg_file.to_corner(UP)

        title = TextMobject(self.title_name)
        title.to_corner((BOTTOM + ORIGIN))
        self.play(
            ShowCreation(svg_file),
            ShowCreation(author),run_time=4
        )
        self.play(
            Write(title),
        )
        self.wait(5)
        self.play(
            Uncreate(author),
            Uncreate(title),
             Uncreate(svg_file),
            run_time = 3,
        )


class Intro(Scene):
    def construct(self):
        lca=[TexMobject("LCA"),TextMobject("Least common ancestors"),TextMobject("...Using multiplication").shift(3.5*UP),TextMobject("Multiplication").shift(3.5*UP)]
        self.play(Write(lca[0]))
        self.wait(3)
        self.play(Transform(lca[0],lca[1]))
        self.remove(lca[0])
        self.play(ApplyMethod(lca[1].shift,3.5*UP))


        shape=[Rectangle(width=500,height=0)]
        shape[0].shift(2.8*UP)
        self.play(GrowFromCenter(shape[0]))


        trees=[]
        mo = VMobject()
        
        for n in range (0,5):
            p=Circle(fill_color=BLUE,radius=0.3,fill_opacity=1.0,color=BLUE)
            if n==0:
                p.shift(2*UP)
            else:
                if n%2==1:
                    p.move_to(trees[int(n/2)].get_center()+2*DOWN+1.5*LEFT)
                else:
                    p.move_to(trees[int(n/2)-1].get_center()+2*DOWN+1.5*RIGHT)
            s=TextMobject(str(n))
            s.next_to(p)
            mo.add(s)
            trees.append(p)
            mo.add(p)
        for n in range(1,5):
            if n%2==1:
                l = Line(trees[(int)(n/2)].get_center()+0.3*DOWN,trees[(int)(n)].get_center()-0.3*DOWN)
            else:
                l = Line(trees[(int)(n/2-1)].get_center()+0.3*DOWN,trees[(int)(n)].get_center()-0.3*DOWN)
            mo.add(l)
        
        self.play(Write(mo),run_time=5)


        self.play(ApplyMethod(trees[3].scale,1.5))
        self.play(ApplyMethod(trees[4].scale,1.5))
        self.wait(1)
        self.play(ApplyMethod(trees[1].scale,1.5))
        self.wait(1)
        self.play(ApplyMethod(trees[3].scale,2/3),ApplyMethod(trees[4].scale,2/3),ApplyMethod(trees[1].scale,2/3))
        self.play(FadeOutAndShiftDown(mo))

        self.play(Transform(lca[1],lca[2]))
        self.wait(0.5)
        self.remove(lca[1])
        self.play(Transform(lca[2],lca[3]))
        self.remove(lca[2])
        self.wait(6)
        
class MultiplicationIntro(Scene):
    def construct(self):
        # Draw title here
        title=TextMobject("Multiplication").shift(3.5*UP)
        split = Rectangle(width=500,height=0).shift(3*UP)
        self.add(title,split)

        #Robust method
        txts=[TextMobject("BF").to_edge(DOWN).scale(0.8)]
        self.wait(5)
        ##tree start
        trees=[]
        deps=[]
        mo = VMobject()
        
        for n in range (0,15):
            layer = int((n+1)**0.5)+1
            if n==0:
                layer=1
            if n==7:
                layer=4
            p=Circle(fill_color=BLUE,radius=0.3,fill_opacity=0,color=BLUE)
            if n==0:
                p.shift(2.5*UP)
            else:
                if n%2==1:
                    p.move_to(trees[int(n/2)].get_center()+layer*0.4*DOWN+(4-0.8*layer)*LEFT)
                else:
                    p.move_to(trees[int(n/2)-1].get_center()+DOWN+(4-0.8*layer)*RIGHT)
            s=TextMobject(str(n))
            s.move_to(p.get_center()).scale(0.5).shift(0.15*UP)
            d=TextMobject("dep=%s"%layer).move_to(p.get_center()).shift(0.15*DOWN).scale(0.3)
            mo.add(d)
            mo.add(s)
            deps.append(d)
            trees.append(p)
            mo.add(p)
        for n in range(1,15):
            if n%2==1:
                l = Line(trees[(int)(n/2)].get_center()+0.3*DOWN,trees[(int)(n)].get_center()-0.3*DOWN)
            else:
                l = Line(trees[(int)(n/2-1)].get_center()+0.3*DOWN,trees[(int)(n)].get_center()-0.3*DOWN)
            mo.add(l)
        
        self.play(Write(txts[0]))
        self.wait(2)
        self.play(Write(mo),run_time=5)
        ## trees end
        self.wait(5)
        # show lca(3,9)
        indis=[Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.5,color=YELLOW).move_to(trees[3].get_center()),
               Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.5,color=YELLOW).move_to(trees[9].get_center()) ]
        
        for i in range(len(indis)):
            self.play(Write(indis[i]))
        self.wait(3)
        self.play(ApplyMethod(deps[3].scale,3),ApplyMethod(deps[9].scale,3))
        self.play(ApplyMethod(deps[3].scale,1/3),ApplyMethod(deps[9].scale,1/3))
        self.wait(5)
        self.play(ApplyMethod(indis[1].move_to,trees[4].get_center()))
        self.wait(1)
        self.play(ApplyMethod(indis[0].move_to,trees[1].get_center()),ApplyMethod(indis[1].move_to,trees[1].get_center()))
        self.wait(1)
        self.play(FadeOut(indis[0]),FadeOut(indis[1]))
        self.wait(5)
        #show lca(1,10)
        indis=[Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.5,color=YELLOW).move_to(trees[1].get_center()),
               Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.5,color=YELLOW).move_to(trees[10].get_center()) ]
        
        for i in range(len(indis)):
            self.play(Write(indis[i]))
        self.wait(3)
        self.play(ApplyMethod(deps[1].scale,3),ApplyMethod(deps[10].scale,3))
        self.play(ApplyMethod(deps[1].scale,1/3),ApplyMethod(deps[10].scale,1/3))
        self.play(ApplyMethod(indis[1].move_to,trees[4].get_center()))
        self.wait(1)
        self.play(ApplyMethod(indis[1].move_to,trees[1].get_center()))
        self.wait(3)
        self.play(FadeOut(indis[0]),FadeOut(indis[1]))
        self.wait(5)
        self.wait(1)
        self.play(FadeOutAndShiftDown(mo),FadeOutAndShiftDown(txts[0]))

class Multiplication(Scene):
    def construct(self):
        #Title
        title=TextMobject("Multiplication").shift(3.5*UP)
        split = Rectangle(width=500,height=0).shift(3*UP)
        self.add(title,split)

        #Intro
        mo=VGroup()
        blk=[]
        for i in range(-4,5):
            rect = Rectangle(width=5,height=1).shift(i*RIGHT)
            mo.add(rect)
            blk.append(rect)
        for i in range(-6,7):
            txtr=TextMobject(str(i+6)).shift(i*RIGHT)
            mo.add(txtr)

        txts=[TextMobject("Suppose you are going to 7 blocks away...").shift(DOWN),
              TextMobject("You may go one block by one...").shift(DOWN) ]
        self.play(Write(mo))
        
        self.play(Write(txts[0]))
        self.wait(5)
        person=Rectangle(width=1,height=1,fill_color=YELLOW,fill_opacity=0.3).move_to(blk[0].get_center()+2*LEFT)
        self.play(Write(person))
        self.play(FadeOut(txts[0]),Write(txts[1]))
        for i in range(0,7):
            self.play(ApplyMethod(person.shift,RIGHT))

        self.play(FadeOut(txts[1]))
        self.play(ApplyMethod(person.shift,(7*LEFT)))

        eq=[TexMobject("2^0,2,2^2,2^3 ...").shift(DOWN),
            TexMobject("1,2,4,8").shift(DOWN),
            TexMobject("f[1][0]=2").shift(DOWN),
            TextMobject("From block 1 move 1 blocks ends up at block 2.").shift(2*DOWN),
            TexMobject("f[1][1]=3").shift(DOWN),
            TextMobject("From block 1 move 2 blocks ends up at block 3.").shift(2*DOWN),
            TexMobject("f[2][0]=3").shift(DOWN),
            TextMobject("From block 2 move 1 blocks ends up at block 3.").shift(2*DOWN),
            TexMobject("f[i][j]=w").shift(DOWN),
            TextMobject("From block i move $2^j$ blocks ends up at block w.").shift(2*DOWN)]
        self.wait(5)
        self.play(Write(eq[0]))
        self.wait(5)
        self.play(Transform(eq[0],eq[1]))
        self.wait(5)
        self.remove(eq[1],eq[0])
        self.play(Transform(eq[1],eq[2]))
        self.play(Write(eq[3]))
        self.wait(5)
        self.remove(eq[1])
        self.play(Transform(eq[2],eq[4]),Transform(eq[3],eq[5]))
        self.wait(5)
        self.remove(eq[2],eq[3])
        self.play(Transform(eq[4],eq[6]),Transform(eq[5],eq[7]))
        self.wait(5)
        self.remove(eq[4],eq[5])
        self.play(Transform(eq[6],eq[8]),Transform(eq[7],eq[9]))
        self.wait(5)
        self.play(FadeOutAndShiftDown(eq[8]),FadeOutAndShiftDown(eq[9]),FadeOutAndShiftDown(eq[6]),FadeOutAndShiftDown(eq[7]))

        #reveal dituishi
        td=[TexMobject("2^2=2^1 \\times 2^1").shift(DOWN),
            TexMobject("f[i][j]=","f[","f[i][j-1]","]","[j-1]").shift(2*DOWN),
            TextMobject("""\\begin{table}[]
\\begin{tabular}{|l|l|l|l|l|l|l|l|}
\\hline
 $i,j$   & $0$ & $1$ & $2$ & $3$ & $4$ & $5$ & $6$ \\\\ \\hline
$2^0$ & $1$ & $2$ & $3$ & $4$ & $5$ & $6$ & $7$ \\\\ \\hline
$2^1$ & $2$ & $3$ & $4$ & $5$ & $6$ & $7$ & $8$  \\\\ \\hline
$2^2$ & $4$ & $5$ & $6$ & $7$ & $8$ & $9$ & $10$  \\\\ \\hline
$2^3$ & $8$ & $9$ & $10$ & $11$ & $12$ & $-1$ & $-1$  \\\\ \\hline
\\end{tabular}
\\end{table}""").shift(2.5*DOWN)]
        self.play(Write(td[0]))
        self.play(ApplyMethod(person.shift,4*RIGHT))
        self.wait(6)
        self.play(ApplyMethod(person.shift,4*LEFT),run_time=0.2)
        for i in range(0,2):
            self.play(ApplyMethod(person.shift,2*RIGHT))
        self.wait(5)
        self.play(ApplyMethod(person.shift,4*LEFT),run_time=0.2)

        self.play(Write(td[1][0]),run_time=2)
        self.wait(1)
        self.play(Write(td[1][2]),run_time=2)
        self.wait(1)
        self.play(Write(td[1][1]),Write(td[1][3]),run_time=2)
        self.wait(1)
        self.play(Write(td[1][4]),run_time=2)

        self.play(FadeOutAndShiftDown(td[0]))
        self.play(ApplyMethod(td[1].shift,3*UP))
        
        self.play(Write(td[2]))
        TR = np.array([0.85,0,0])
        TU = np.array([0,0.6,0])
        rec = Rectangle(width=0.85,height=0.6,fill_color=YELLOW,fill_opacity=0.3).shift(1.25*DOWN+2.7*LEFT)
        self.play(Write(rec))

        self.play(ApplyMethod(rec.shift,-4*TU))
        self.wait(5)
        self.play(ApplyMethod(rec.shift,TU))
        self.play(ApplyMethod(person.shift,(4*RIGHT)))
        self.play(ApplyMethod(rec.shift,3*TU))
        self.play(ApplyMethod(rec.shift,4.5*TR))
        self.wait(2)
        self.play(ApplyMethod(rec.shift,-4*TU))
        self.play(ApplyMethod(rec.shift,TU))
        self.play(ApplyMethod(rec.shift,TU))
        self.play(ApplyMethod(person.shift,(2*RIGHT)))
        self.play(ApplyMethod(rec.shift,2*TU))
        self.play(ApplyMethod(rec.shift,3*TR))
        self.wait(2)
        self.play(ApplyMethod(rec.shift,-4*TU))
        self.play(ApplyMethod(rec.shift,TU))
        self.play(ApplyMethod(rec.shift,TU))
        self.play(ApplyMethod(rec.shift,TU))
        self.play(ApplyMethod(person.shift,(RIGHT)))
        self.wait(5)

        title2=TextMobject("LCA problem").shift(3.5*UP)
        self.play(Transform(title,title2))
        self.play(FadeOutAndShiftDown(mo),FadeOutAndShiftDown(rec),FadeOutAndShiftDown(person),FadeOutAndShiftDown(td[2]),FadeOutAndShiftDown(td[1]))


class LCA(Scene):
    def construct(self):
        #Title
        title=TextMobject("LCA problem").shift(3.5*UP)
        split = Rectangle(width=500,height=0).shift(3*UP)
        self.add(title,split)

        #steps
        steps=[TextMobject("Jump to the same depth ","using Multiplication").shift(2*UP),
               TextMobject("Jump until they meet "," using Multiplication").shift(UP),
               TextMobject("Jump so that they don't meet up"," by using Multiplication").shift(UP) ]
        
        self.play(Write(steps[0][0]))
        self.play(Write(steps[1][0]))
        self.wait(2)
        self.play(Write(steps[0][1]))
        self.play(Write(steps[1][1]))
        self.wait(2)

        self.play(FadeOut(steps[0]),FadeOut(steps[1]))

        ##tree start
        trees=[]
        deps=[]
        mo = VMobject()
        
        for n in range (0,15):
            layer = int((n+1)**0.5)+1
            if n==0:
                layer=1
            if n==7:
                layer=4
            p=Circle(fill_color=BLUE,radius=0.3,fill_opacity=0,color=BLUE)
            if n==0:
                p.shift(2.5*UP)
            else:
                if n%2==1:
                    p.move_to(trees[int(n/2)].get_center()+layer*0.4*DOWN+(4-0.8*layer)*LEFT)
                else:
                    p.move_to(trees[int(n/2)-1].get_center()+DOWN+(4-0.8*layer)*RIGHT)
            s=TextMobject(str(n))
            s.move_to(p.get_center()).scale(0.5).shift(0.15*UP)
            d=TextMobject("dep=%s"%layer).move_to(p.get_center()).shift(0.15*DOWN).scale(0.3)
            mo.add(d)
            mo.add(s)
            deps.append(d)
            trees.append(p)
            mo.add(p)
        for n in range(1,15):
            if n%2==1:
                l = Line(trees[(int)(n/2)].get_center()+0.3*DOWN,trees[(int)(n)].get_center()-0.3*DOWN)
            else:
                l = Line(trees[(int)(n/2-1)].get_center()+0.3*DOWN,trees[(int)(n)].get_center()-0.3*DOWN)
            mo.add(l)
        
        
        self.play(Write(mo),run_time=5)
        ## trees end
        self.wait(5)
        indis=[Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.5,color=YELLOW).move_to(trees[1].get_center()),
               Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.5,color=YELLOW).move_to(trees[14].get_center()) ]
        
        txt=[TextMobject("$f[i][j]$ means the $2^j$th father of i").to_edge(DOWN),
             TextMobject("Jump as much as we can!"),
             TextMobject("$2^{10}$th father"),
             TextMobject("$2^9$th father"),
             TextMobject("$2^{...}$th father"),
             TextMobject("$2^2$th father"),
             TextMobject("$2^1$th father"),
             TextMobject("Are they the $same$ point?"),
             TextMobject("$2^0$th father"),
             TextMobject("Their father is the LCA.")]

        self.play(Write(txt[0]))
        self.wait(3)
        self.play(Write(indis[0]))
        self.play(Write(indis[1]))
        self.wait(3)
        self.play(Write(txt[1]))
        self.wait(2)
        self.play(FadeOutAndShiftDown(txt[1]))
        self.wait(2)
        self.play(Write(txt[2]))
        self.wait(2)
        self.play(FadeOut(txt[2]))
        self.play(Write(txt[3]))
        self.wait(2)
        self.play(FadeOut(txt[3]))
        self.play(Write(txt[4]))
        self.wait(2)
        self.play(FadeOut(txt[4]))
        self.play(Write(txt[5]))
        self.wait(2)
        self.play(FadeOut(txt[5]))
        self.play(Write(txt[6]))
        self.wait(4)
        self.play(ApplyMethod(indis[1].move_to,trees[2].get_center()))
        self.play(FadeOut(txt[6]))
        self.play(Write(txt[7]))
        self.wait(5)

        self.play(FadeOut(mo),FadeOut(indis[0]),FadeOut(indis[1]),FadeOut(txt[7]))
        self.play(Write(steps[0]),Write(steps[1]))
        self.wait(2)
        self.play(FadeOut(steps[0]),FadeOut(steps[1]))
        self.play(Write(mo))

        indis=[Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.5,color=YELLOW).move_to(trees[7].get_center()),
               Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.5,color=YELLOW).move_to(trees[8].get_center()) ]

        self.play(Write(indis[0]))
        self.play(Write(indis[1]))
        self.play(Write(txt[2]))
        self.wait(0.5)
        self.play(FadeOut(txt[2]))
        self.play(Write(txt[3]))
        self.wait(0.5)
        self.play(FadeOut(txt[3]))
        self.play(Write(txt[4]))
        self.wait(0.5)
        self.play(FadeOut(txt[4]))
        self.play(Write(txt[5]))
        self.wait(0.5)
        self.play(FadeOut(txt[5]))
        self.play(Write(txt[6]))
        self.wait(0.5)
        self.play(FadeOut(txt[6]))
        self.play(ApplyMethod(indis[1].move_to,trees[1].get_center()),indis[0].move_to,trees[1].get_center())
        #self.play(ApplyMethod()
        self.wait(3)
        self.play(FadeOut(mo),FadeOut(indis[0]),FadeOut(indis[1]))
        self.play(Write(steps[0]),Write(steps[1]))
        self.wait(6)
        self.play(Transform(steps[1],steps[2]))
        self.wait(2)
        self.remove(steps[1])

        self.play(FadeOut(steps[0]),FadeOut(steps[2]))
        self.play(Write(mo))
        indis=[Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.5,color=YELLOW).move_to(trees[7].get_center()),
               Circle(fill_color=YELLOW,radius=0.3,fill_opacity=0.5,color=YELLOW).move_to(trees[8].get_center()) ]
        self.play(Write(txt[6]))
        self.play(ApplyMethod(indis[1].move_to,trees[1].get_center()),ApplyMethod(indis[0].move_to,trees[1].get_center()))
        # self.play()
        self.play(ApplyMethod(indis[1].move_to,trees[7].get_center()),ApplyMethod(indis[0].move_to,trees[8].get_center()))
        # self.play()
        self.play(FadeOut(txt[6]))

        self.play(Write(txt[8]))
        
        self.play(ApplyMethod(indis[1].move_to,trees[3].get_center()),ApplyMethod(indis[0].move_to,trees[3].get_center()))
        # self.play()
        self.play(ApplyMethod(indis[1].move_to,trees[7].get_center()),ApplyMethod(indis[0].move_to,trees[8].get_center()))
        # self.play()
        self.play(FadeOut(txt[8]))

        self.play(Write(txt[9]))

        self.wait(5)
        self.play(FadeOut(mo),FadeOut(indis[0]),FadeOut(indis[1]),FadeOut(txt[0]),FadeOut(txt[9]))

        title2=TextMobject("Realizing by C++").shift(3.5*UP)
        self.play(Transform(title,title2))



class CodeRealize(Scene):
    def construct(self):
        #Title
        title=TextMobject("Realizing by C++").shift(3.5*UP)
        split = Rectangle(width=500,height=0).shift(3*UP)
        self.add(title,split)
        
    




        


