from manimlib.imports import *
from PrimoCreature import *

class StartingScene(Scene):
    def construct(_):
        name = TextMobject("<","/",">").shift(2*UP).scale(2)
        mane = TextMobject("Micoael ","$\\rho$","rimo")
        name[0].shift(8*LEFT).set_color(BLUE)
        name[1].shift(8*UP).set_color(LIGHT_BROWN)
        name[2].shift(8*RIGHT).set_color(BLUE)
        _.play(name[0].shift,(8*RIGHT),
                name[1].shift,(8*DOWN),
                name[2].shift,(8*LEFT),)
        mane[1].shift(0.1*UP)
        _.play(FadeInFromDown(mane))

class StrMatcher:
    
    def gen_next(s2):
        k = -1
        n = len(s2)
        j = 0
        next_list = [0 for i in range(n)]
        next_list[0] = -1
        while j < n-1:
            if k == -1 or s2[k] == s2[j]:
                k += 1
                j += 1
                next_list[j] = k
            else:
                k = next_list[k]
        return next_list

    def match(s1, s2, next_list):
        ans = -1
        i = 0
        j = 0
        while i < len(s1):
            if s1[i] == s2[j] or j == -1:
                i += 1
                j += 1
            else:
                j = next_list[j]
            if j == len(s2):
                ans = i - len(s2)
                break
        return ans

class Introduction(Scene):
    def construct(self):
        primo = PrimoCreature(color=BLUE).shift(2*DOWN+4*LEFT)
        
        self.play(FadeIn(primo))
        texts = TextMobject("aaaaaaafsdiaaawsss\\\\dfsaaws","awsl","wsdawasa\\\\dwaawwaslwasawl").shift(2*RIGHT+DOWN)
        primo.look_at(texts)
        self.play(Write(texts))
        palabras_ale = TextMobject("awsl ???")
        self.play(PrimoCreatureSays(
            primo, palabras_ale,
            bubble_kwargs={"height": 5, "width": 6},
            target_mode="plain"
        ))
        self.wait(1.5)
        self.play(texts[1].set_color,YELLOW,
                  texts[1].scale,2)
        self.play(texts[1].scale,0.5)
        palabras_ale = TextMobject("让计算机完成字符串查找?")
        primo.look_at(palabras_ale)
        self.play(PrimoCreatureSays(
            primo, palabras_ale,
            bubble_kwargs={"height": 5, "width": 6},
            target_mode="plain"
        ))
        self.wait(5)
        palabras_ale = TextMobject("这不是很简单的吗?")
        primo.look_at(palabras_ale)
        self.play(PrimoCreatureSays(
            primo, palabras_ale,
            bubble_kwargs={"height": 5, "width": 6},
            target_mode="plain"
        ))

class BasicAlgorithm(Scene):
    
    def construct(_):
        _.str1="aaaaaaafsdiaaawslsdfsaawsawslwsda"
        _.str2="awsl"
        _.init(_.str1,_.str2)
        _.matchord(_.str1,_.str2)
    
    def init(_,str1,str2):
        _.a = 0
        _.b = 0
        _.comp = 0
        _.len1 = len(str1)
        _.len2 = len(str2)
        _.moshi = VGroup()
        _.yuanlai = VGroup()
        _.next = VGroup()
        _.rect = Rectangle(width=0.5,height=1,fill_color=GREEN,fill_opacity=0.3).move_to(np.array([-6,2.75,0]))
        for i in range(0,len(str1)):
            pos = np.array((-6+0.5*i,3,0.0))
            square = TextMobject(str1[i])
            square.move_to(pos)
            _.moshi.add(square)
        for i in range(0,len(str2)):
            pos = np.array((-6+0.5*i,2.5,0.0))
            square = TextMobject(str2[i])
            _.yuanlai.add(square)
            square.move_to(pos)
        for i in range(0,len(str2)):
            pos = np.array((-6+0.5*i,2,0.0))
            square = TextMobject(str(StrMatcher.gen_next(str2)[i]))
            _.next.add(square)
            square.move_to(pos)
        _.addTextsToScreen()
        _.add(_.rect)

    def addTextsToScreen(_):
        _.play(Write(_.yuanlai),Write(_.moshi))
    
    def shifts(_,val):
        _.play(_.yuanlai.shift,(val*0.5*RIGHT),
               _.next.shift,(val*0.5*RIGHT), run_time=0.5)
        _.b += val
    
    def shiftto(_,val):
        _.play(_.yuanlai.shift,((val-_.b)*0.5*RIGHT),
               _.next.shift,((val-_.b)*0.5*RIGHT) ,run_time=0.5)
        _.b = val
    
    def shiftgreen(_,val):
        _.play(_.rect.shift,(val*0.5*RIGHT),run_time=0.5)
        _.comp += val
    
    def shiftgto(_,val):
        _.play(_.rect.shift,((val-_.comp)*0.5*RIGHT),run_time=0.5)
        _.comp = val
    
    def compare(_,dig):
        _.write(rect)
    
    def alignw(_,bb,aa):
        _.shiftto(bb-aa)
        _.shiftgto(bb)
        if _.str1[bb]==_.str2[aa]:
            _.play(_.rect.set_color,(GREEN),run_time = 0.5)
        else:
            _.play(_.rect.set_color,(RED),run_time = 0.5)
    
    def matchord(_,t, p):
            i, j = 0, 0
            n, m = len(t), len(p)
            while i < n and j < m:
                _.alignw(i,j)
                if t[i] == p[j]:
                    i, j = i+1, j+1
                else:
                    i, j = i-j+1, 0
            if j == m:
                return i-j
            return -1

    def match(_,s1, s2, next_list):
            ans = -1
            i = 0
            j = 0
            while i < len(s1):
                _.alignw(i,j)
                if s1[i] == s2[j] or j == -1:
                    i += 1
                    j += 1
                else:
                    j = next_list[j]
                if j == len(s2):
                    ans = i - len(s2)
                    break
            return ans

class ProblemWithCommonAlgorithm(Scene):
    
    def construct(_):
        _.str1="aaaaaaafsdiaaawslsdfsaawsawslwsda"
        _.str2="aaaf"
        _.init(_.str1,_.str2)
        _.matchord(_.str1,_.str2)
    
    def init(_,str1,str2):
        _.a = 0
        _.b = 0
        _.comp = 0
        _.len1 = len(str1)
        _.len2 = len(str2)
        _.moshi = VGroup()
        _.yuanlai = VGroup()
        _.next = VGroup()
        _.rect = Rectangle(width=0.5,height=1,fill_color=GREEN,fill_opacity=0.3).move_to(np.array([-6,2.75,0]))
        for i in range(0,len(str1)):
            pos = np.array((-6+0.5*i,3,0.0))
            square = TextMobject(str1[i])
            square.move_to(pos)
            _.moshi.add(square)
        for i in range(0,len(str2)):
            pos = np.array((-6+0.5*i,2.5,0.0))
            square = TextMobject(str2[i])
            _.yuanlai.add(square)
            square.move_to(pos)
        for i in range(0,len(str2)):
            pos = np.array((-6+0.5*i,2,0.0))
            square = TextMobject(str(StrMatcher.gen_next(str2)[i]))
            _.next.add(square)
            square.move_to(pos)
        _.addTextsToScreen()
        _.add(_.rect)

    def addTextsToScreen(_):
        _.play(Write(_.yuanlai),Write(_.moshi))
    
    def shifts(_,val):
        _.play(_.yuanlai.shift,(val*0.5*RIGHT),
                run_time=0.5)
        _.b += val
    
    def shiftto(_,val):
        _.play(_.yuanlai.shift,((val-_.b)*0.5*RIGHT),
                run_time=0.5)
        _.b = val
    
    def shiftgreen(_,val):
        _.play(_.rect.shift,(val*0.5*RIGHT),run_time=0.5)
        _.comp += val
    
    def shiftgto(_,val):
        _.play(_.rect.shift,((val-_.comp)*0.5*RIGHT),run_time=0.5)
        _.comp = val
    
    def compare(_,dig):
        _.write(rect)
    
    def alignw(_,bb,aa):
        _.shiftto(bb-aa)
        _.shiftgto(bb)
        if _.str1[bb]==_.str2[aa]:
            _.play(_.rect.set_color,(GREEN),run_time = 0.5)
        else:
            _.play(_.rect.set_color,(RED),run_time = 0.5)
    
    def matchord(_,t, p):
            i, j = 0, 0
            n, m = len(t), len(p)
            while i < n and j < m:
                _.alignw(i,j)
                if t[i] == p[j]:
                    i, j = i+1, j+1
                else:
                    i, j = i-j+1, 0
            if j == m:
                return i-j
            return -1

    def match(_,s1, s2, next_list):
            ans = -1
            i = 0
            j = 0
            while i < len(s1):
                _.alignw(i,j)
                if s1[i] == s2[j] or j == -1:
                    i += 1
                    j += 1
                else:
                    j = next_list[j]
                if j == len(s2):
                    ans = i - len(s2)
                    break
            return ans
    
class HowToImprove(Scene):
    def construct(_):
        primo = PrimoCreature(color=BLUE).shift(2*DOWN+4*LEFT)
        
        _.play(FadeIn(primo))
        palabras_ale = TextMobject("减少重复的移动?!")
        _.play(PrimoCreatureSays(
            primo, palabras_ale,
            bubble_kwargs={"height": 5, "width": 6},
            target_mode="plain"
        ))
        _.wait(1.5)
        _.clear()
        ori  = TextMobject("MicoaelPrim","p")
        patt = TextMobject("MicoaelPrim","o")
        
        al = VGroup(ori,patt).arrange(DOWN)
        _.play(Write(al))
        _.play(ori[1].set_color,RED,
                patt[1].set_color,RED)
        _.play(FadeOut(al))
        ori  = TextMobject("MicoaelMico","p")
        patt = TextMobject("Mico","ael","Mico","o")
        al = VGroup(ori,patt).arrange(DOWN)
        _.play(Write(al))
        _.play(ori[1].set_color,RED,
                patt[3].set_color,RED)
        
        _.play(patt[0].set_color,YELLOW,
                patt[2].set_color,YELLOW)
        _.play(patt.shift,1.8*RIGHT,)
        _.wait(3)
        _.clear()
        _.play(FadeIn(primo))
        palabras_ale = TextMobject("也就是说找到前后长度对称\\\\的最大长度是吧？")
        _.play(PrimoCreatureSays(
            primo, palabras_ale,
            bubble_kwargs={"height": 5, "width": 6},
            target_mode="plain"
        ))
        _.wait(3)
        _.clear()
        exam = TextMobject("M","i","c","o","a","M","i","c","o").scale(2)
        _.play(Write(exam))
        _.play( exam[0].set_color,YELLOW,
                exam[5].set_color,YELLOW)
        _.wait(0.5)
        _.play( exam[1].set_color,YELLOW,
                exam[6].set_color,YELLOW)
        _.wait(0.5)
        _.play( exam[2].set_color,YELLOW,
                exam[7].set_color,YELLOW)
        _.wait(0.5)
        _.play( exam[3].set_color,YELLOW,
                exam[8].set_color,YELLOW)
        txt = TextMobject("$G=4$").shift(2*UP)
        _.play(Transform(exam.copy(),txt)) 

class TheConnectionBetweenPatternAndTheOrigin(Scene):
    def construct(_):
        pat = "MicoaMico"
        _.init("MicoaMickcMicoa",pat)
        _.shiftgreen(8)
        _.play(_.yuanlai[0].set_color,YELLOW,_.yuanlai[5].set_color,YELLOW)
        _.play(_.yuanlai[1].set_color,YELLOW,_.yuanlai[6].set_color,YELLOW)
        _.play(_.yuanlai[2].set_color,YELLOW,_.yuanlai[7].set_color,YELLOW)
        size = TextMobject("$G=3$")
        _.play(FadeInFromDown(size))
        _.play(FocusOn(_.yuanlai[3]))
        _.shifts(5)
        _.wait(3)
        mask = TextMobject("----","我们不知道原来的字符串","----").add_background_rectangle().move_to(_.moshi)
        _.play(_.yuanlai[0].set_color,WHITE,_.yuanlai[5].set_color,WHITE,run_time=0.1)
        _.play(_.yuanlai[1].set_color,WHITE,_.yuanlai[6].set_color,WHITE,run_time=0.1)
        _.play(_.yuanlai[2].set_color,WHITE,_.yuanlai[7].set_color,WHITE,run_time=0.1)
        _.play(Write(mask))

        gr = VGroup()
        for i in range (len(pat)+1):
            stri = ""
            for j in range(i):
                stri=stri+(pat[j])
            gr.add(TextMobject(stri))
        gr.arrange(DOWN).shift(0.5*DOWN)
        _.play(FadeOut(size))
        _.play(Transform(_.yuanlai.copy(),gr))

        primo = PrimoCreature(color=BLUE).shift(2*DOWN+4*LEFT)
        
        _.play(FadeIn(primo))
        palabras_ale = TextMobject("也就是说我们把这一堆东西\\\\的最长公共前后缀算出来就好了吧")

        _.play(PrimoCreatureSays(
            primo, palabras_ale,
            bubble_kwargs={"height": 5, "width": 6},
            target_mode="plain"
        ) )
        _.wait(3)
        _.clear()
        _.add(gr)
        for i in range(1,len(gr)):
            _.play(ShowCreationThenDestructionAround(gr[i]))
        primo = PrimoCreature(color=BLUE).shift(2*DOWN+4*LEFT)
        
        _.play(FadeIn(primo))
        palabras_ale = TextMobject("看上去好简单的样子！")

        _.play(PrimoCreatureSays(
            primo, palabras_ale,
            bubble_kwargs={"height": 5, "width": 6},
            target_mode="plain"
        ) )
        _.wait(3)
        
        



    def init(_,str1,str2):
        _.a = 0
        _.b = 0
        _.comp = 0
        _.len1 = len(str1)
        _.len2 = len(str2)
        _.moshi = VGroup()
        _.yuanlai = VGroup()
        _.next = VGroup()
        _.rect = Rectangle(width=0.5,height=1,fill_color=GREEN,fill_opacity=0.3).move_to(np.array([-3,2.75,0]))
        for i in range(0,len(str1)):
            pos = np.array((-3+0.5*i,3,0.0))
            square = TextMobject(str1[i])
            square.move_to(pos)
            _.moshi.add(square)
        for i in range(0,len(str2)):
            pos = np.array((-3+0.5*i,2.5,0.0))
            square = TextMobject(str2[i])
            _.yuanlai.add(square)
            square.move_to(pos)
        for i in range(0,len(str2)):
            pos = np.array((-3+0.5*i,2,0.0))
            square = TextMobject(str(i))
            _.next.add(square)
            square.move_to(pos)
        _.addTextsToScreen()
        _.add(_.rect)
        _.play(_.rect.set_color,RED)

    def addTextsToScreen(_):
        _.play(Write(_.yuanlai),Write(_.moshi),Write(_.next))
    
    def shifts(_,val):
        _.play(_.yuanlai.shift,(val*0.5*RIGHT),
               _.next.shift,(val*0.5*RIGHT), run_time=0.5)
        _.b += val
    
    def shiftto(_,val):
        _.play(_.yuanlai.shift,((val-_.b)*0.5*RIGHT),
               _.next.shift,((val-_.b)*0.5*RIGHT) ,run_time=0.5)
        _.b = val
    
    def shiftgreen(_,val):
        _.play(_.rect.shift,(val*0.5*RIGHT),run_time=0.5)
        _.comp += val
    
    def shiftgto(_,val):
        _.play(_.rect.shift,((val-_.comp)*0.5*RIGHT),run_time=0.5)
        _.comp = val
    
    def compare(_):
        _.play(Write(_.rect))
    
    def alignw(_,bb,aa):
        _.shiftto(bb-aa)
        _.shiftgto(bb)
        if _.str1[bb]==_.str2[aa]:
            _.play(_.rect.set_color,(GREEN),run_time = 0.5)
        else:
            _.play(_.rect.set_color,(RED),run_time = 0.5)
    
    def matchord(_,t, p):
            i, j = 0, 0
            n, m = len(t), len(p)
            while i < n and j < m:
                _.alignw(i,j)
                if t[i] == p[j]:
                    i, j = i+1, j+1
                else:
                    i, j = i-j+1, 0
            if j == m:
                return i-j
            return -1

    def match(_,s1, s2, next_list):
            ans = -1
            i = 0
            j = 0
            while i < len(s1):
                _.alignw(i,j)
                if s1[i] == s2[j] or j == -1:
                    i += 1
                    j += 1
                else:
                    j = next_list[j]
                if j == len(s2):
                    ans = i - len(s2)
                    break
            return ans

class HardToFigure(Scene):
    def construct(_):
        _.str1="AGCAxxx"
        _.str2="AGCT"
        _.init(_.str1,_.str2)
        _.match(_.str1,_.str2,StrMatcher.gen_next(_.str2))
    
    def init(_,str1,str2):
        _.a = 0
        _.b = 0
        _.comp = 0
        _.len1 = len(str1)
        _.len2 = len(str2)
        _.moshi = VGroup()
        _.yuanlai = VGroup()
        _.next = VGroup()
        _.rect = Rectangle(width=0.5,height=1,fill_color=GREEN,fill_opacity=0.3).move_to(np.array([-3,2.75,0]))
        for i in range(0,len(str1)):
            pos = np.array((-3+0.5*i,3,0.0))
            square = TextMobject(str1[i])
            square.move_to(pos)
            _.moshi.add(square)
        for i in range(0,len(str2)):
            pos = np.array((-3+0.5*i,2.5,0.0))
            square = TextMobject(str2[i])
            _.yuanlai.add(square)
            square.move_to(pos)
        for i in range(0,len(str2)):
            pos = np.array((-3+0.5*i,2,0.0))
            square = TextMobject(str(StrMatcher.gen_next(str2)[i]))
            _.next.add(square)
            square.move_to(pos)
        _.addTextsToScreen()
        _.add(_.rect)

    def addTextsToScreen(_):
        _.play(Write(_.yuanlai),Write(_.moshi),Write(_.next))
    
    def shifts(_,val):
        _.play(_.yuanlai.shift,(val*0.5*RIGHT),
               _.next.shift,(val*0.5*RIGHT), run_time=0.5)
        _.b += val
    
    def shiftto(_,val):
        _.play(_.yuanlai.shift,((val-_.b)*0.5*RIGHT),
               _.next.shift,((val-_.b)*0.5*RIGHT) ,run_time=0.5)
        _.b = val
    
    def shiftgreen(_,val):
        _.play(_.rect.shift,(val*0.5*RIGHT),run_time=0.5)
        _.comp += val
    
    def shiftgto(_,val):
        _.play(_.rect.shift,((val-_.comp)*0.5*RIGHT),run_time=0.5)
        _.comp = val
    
    def compare(_,dig):
        _.write(rect)
    
    def alignw(_,bb,aa):
        _.shiftto(bb-aa)
        _.shiftgto(bb)
        if _.str1[bb]==_.str2[aa]:
            _.play(_.rect.set_color,(GREEN),run_time = 0.5)
        else:
            _.play(_.rect.set_color,(RED),run_time = 0.5)
    
    def matchord(_,t, p):
            i, j = 0, 0
            n, m = len(t), len(p)
            while i < n and j < m:
                _.alignw(i,j)
                if t[i] == p[j]:
                    i, j = i+1, j+1
                else:
                    i, j = i-j+1, 0
            if j == m:
                return i-j
            return -1

    def match(_,s1, s2, next_list):
            ans = -1
            i = 0
            j = 0
            while i < len(s1):
                _.alignw(i,j)
                if s1[i] == s2[j] or j == -1:
                    i += 1
                    j += 1
                else:
                    j = next_list[j]
                if j == len(s2):
                    ans = i - len(s2)
                    break
            return ans
    
class UnderstandRousThought(Scene):
    def construct(_):
        pat = "MicoaMico"
        gr = VGroup()
        for i in range (len(pat)+1):
            stri = ""
            for j in range(i):
                stri=stri+(pat[j])
            gr.add(TextMobject(stri))
        gr.arrange(DOWN).shift(0.5*DOWN)
        _.play(Write(gr))

        primo = PrimoCreature(color=BLUE).shift(2*DOWN+4*LEFT)
        
        _.play(FadeIn(primo))
        palabras_ale = TextMobject("遍历一遍不就好了吗？！")
        _.play(PrimoCreatureSays(
            primo, palabras_ale,
            bubble_kwargs={"height": 5, "width": 6},
            target_mode="plain"
        ))
        _.wait(3)
        _.clear()
        _.add(gr)
        primo = PrimoCreature(color=LIGHT_BROWN).shift(2*DOWN+4*RIGHT).flip()
        
        _.play(FadeIn(primo))
        palabras_ale = TextMobject("试着递推一下！")
        _.play(PrimoCreatureSays(
            primo, palabras_ale,
            bubble_kwargs={"height": 5, "width": 6},
            target_mode="plain"
        ))
        m = ValueTracker(0)
        def upd(obj):
            obj.tex_string = "G="+str( int(m.get_value()))
        _.G = TextMobject("G=",str(int(m.get_value()))).add_updater(upd).shift(2*DOWN)
        
        _.wait(3)
        _.clear()
        _.txt0 = TextMobject("A","G","C","T","A","G","C","A","G","C","T","G","C","A");
        _.show(0)
        _.add(_.G)
        _.moveto(0)

        _.wait(1)
        _.show(1)
        _.changeval(0)
        _.moveto(1)

        _.wait(1)
        _.show(2)
        _.changeval(0)
        _.moveto(2)

        _.wait(1)
        _.show(3)
        _.changeval(0)
        _.moveto(3)

        _.wait(1)
        _.show(4)
        _.compare(0,4)
        _.changeval(1)
        _.moveto(4)
        _.cls()
        _.cc(0,4)

        _.wait(1)
        _.show(5)
        _.compare(1,5)
        _.changeval(2)
        _.moveto(5)
        _.cc(1,5)

        _.wait(1)
        _.show(6)
        _.compare(2,6)
        _.changeval(3)
        _.moveto(6)
        _.cc(2,6)

        _.wait(1)
        _.show(7)
        _.compare(3,7)
        _.changeval("?")


        a = TextMobject("每检验到一个不匹配的就要归零吗？").add_background_rectangle()
        _.play(Write(a))
        _.wait(3)
        _.play(Uncreate(a))

        a = TextMobject("有没有更小的区间让他们相同呢？").add_background_rectangle()
        _.play(Write(a))
        _.wait(3)
        _.play(Uncreate(a))

        a = TextMobject("如果有，该怎么找到呢？").add_background_rectangle()
        _.play(Write(a))
        _.wait(3)
        _.play(Uncreate(a))

        _.compare(6,6)

        a = TextMobject("下一个公共前后缀有可能存在这里的next").add_background_rectangle().shift(2.5*UP)
        _.play(Write(a))
        _.wait(1)

        a = TextMobject("如果发现他两个字符相等或$next$是$0$就不用继续下去了").add_background_rectangle().shift(2*UP)
        _.play(Write(a))
        _.wait(1)

        a = TextMobject("(到头也没发现相同的)").add_background_rectangle().shift(1.5*UP)
        _.play(Write(a))
        _.wait(1)

        _.compare(6,6)
        _.compare(3,3)
        _.compare(0,0)

        _.changeval(1)
        _.moveto(7)
        _.cls()
        _.cc(0,7)
        _.show(8)
        _.compare(1,8)
        _.changeval(2)
        _.moveto(8)
        _.cc(1,8)

        _.show(9)
        _.changeval(3)
        _.moveto(9)
        _.compare(2,9)
        _.cc(2,9)
        _.wait(1)

        _.show(10)
        _.changeval(4)
        _.compare(3,10)
        _.cc(3,10)
        _.moveto(10)
        _.wait(1)

        _.show(11)
        _.compare(10,10)
        _.compare(4,4)
        _.compare(0,0)
        _.changeval(0)
        _.moveto(11)
        _.wait(1)
        _.cls()

        _.show(12)
        _.compare(11,11)
        _.compare(0,0)
        _.changeval(0)
        _.moveto(12)
        _.wait(1)

        _.show(13)
        _.compare(12,12)
        _.compare(0,0)
        _.changeval(1)
        _.moveto(13)
        _.wait(1)

        _.txt0.shift(0.5*LEFT)
        _.wait(3)

    
    def cc(_,a,b):
        _.play(_.txt0[a].set_color,BLUE,_.txt0[b].set_color,BLUE)

    def cls(_):
        for i in range (len(_.txt0)):
            _.txt0[i].set_color(WHITE)

    def moveto(_,to):
        p = _.G[1].copy()
        _.play(p.move_to,_.txt0[to],p.shift,0.8*DOWN)
        
    def changeval(_,a):
        _.G.become(TextMobject("G=",str(a)).shift(2*DOWN))

    def compare(_,a,b):
        _.play(ShowCreationThenDestructionAround(_.txt0[a]),ShowCreationThenDestructionAround(_.txt0[b]))
    
    def show(_,m):
        _.play(FadeInFromDown(_.txt0[m]))

    def init(_,str1,str2):
        _.a = 0
        _.b = 0
        _.comp = 0
        _.len1 = len(str1)
        _.len2 = len(str2)
        _.moshi = VGroup()
        _.yuanlai = VGroup()
        _.next = VGroup()
        _.rect = Rectangle(width=0.5,height=1,fill_color=GREEN,fill_opacity=0.3).move_to(np.array([-3,2.75,0]))
        for i in range(0,len(str1)):
            pos = np.array((-3+0.5*i,3,0.0))
            square = TextMobject(str1[i])
            square.move_to(pos)
            _.moshi.add(square)
        for i in range(0,len(str2)):
            pos = np.array((-3+0.5*i,2.5,0.0))
            square = TextMobject(str2[i])
            _.yuanlai.add(square)
            square.move_to(pos)
        for i in range(0,len(str2)):
            pos = np.array((-3+0.5*i,2,0.0))
            square = TextMobject(str(i))
            _.next.add(square)
            square.move_to(pos)
        _.addTextsToScreen()
        _.add(_.rect)
        _.play(_.rect.set_color,RED)



    def addTextsToScreen(_):
        _.play(Write(_.yuanlai),Write(_.moshi),Write(_.next))
    
    def shifts(_,val):
        _.play(_.yuanlai.shift,(val*0.5*RIGHT),
               _.next.shift,(val*0.5*RIGHT), run_time=0.5)
        _.b += val
    
    def shiftto(_,val):
        _.play(_.yuanlai.shift,((val-_.b)*0.5*RIGHT),
               _.next.shift,((val-_.b)*0.5*RIGHT) ,run_time=0.5)
        _.b = val
    
    def shiftgreen(_,val):
        _.play(_.rect.shift,(val*0.5*RIGHT),run_time=0.5)
        _.comp += val
    
    def shiftgto(_,val):
        _.play(_.rect.shift,((val-_.comp)*0.5*RIGHT),run_time=0.5)
        _.comp = val
    
    
    
    def alignw(_,bb,aa):
        _.shiftto(bb-aa)
        _.shiftgto(bb)
        if _.str1[bb]==_.str2[aa]:
            _.play(_.rect.set_color,(GREEN),run_time = 0.5)
        else:
            _.play(_.rect.set_color,(RED),run_time = 0.5)
    
    def matchord(_,t, p):
            i, j = 0, 0
            n, m = len(t), len(p)
            while i < n and j < m:
                _.alignw(i,j)
                if t[i] == p[j]:
                    i, j = i+1, j+1
                else:
                    i, j = i-j+1, 0
            if j == m:
                return i-j
            return -1

    def match(_,s1, s2, next_list):
            ans = -1
            i = 0
            j = 0
            while i < len(s1):
                _.alignw(i,j)
                if s1[i] == s2[j] or j == -1:
                    i += 1
                    j += 1
                else:
                    j = next_list[j]
                if j == len(s2):
                    ans = i - len(s2)
                    break
            return ans

class AlmostDone(Scene):
    def construct(_):
        _.str1="1我们1我们11我们1我终于1完成了1next数组1的查找"
        _.str2="1我们1我终于1"
        _.init(_.str1,_.str2)
        _.match(_.str1,_.str2,StrMatcher.gen_next(_.str2))
    
    def init(_,str1,str2):
        _.a = 0
        _.b = 0
        _.comp = 0
        _.len1 = len(str1)
        _.len2 = len(str2)
        _.moshi = VGroup()
        _.yuanlai = VGroup()
        _.next = VGroup()
        _.rect = Rectangle(width=0.5,height=1,fill_color=GREEN,fill_opacity=0.3).move_to(np.array([-3,2.75,0]))
        for i in range(0,len(str1)):
            pos = np.array((-3+0.5*i,3,0.0))
            square = TextMobject(str1[i])
            square.move_to(pos)
            _.moshi.add(square)
        for i in range(0,len(str2)):
            pos = np.array((-3+0.5*i,2.5,0.0))
            square = TextMobject(str2[i])
            _.yuanlai.add(square)
            square.move_to(pos)
        for i in range(0,len(str2)):
            pos = np.array((-3+0.5*i,2,0.0))
            square = TextMobject(str(StrMatcher.gen_next(str2)[i]))
            _.next.add(square)
            square.move_to(pos)
        _.addTextsToScreen()
        _.add(_.rect)

    def addTextsToScreen(_):
        _.play(Write(_.yuanlai),Write(_.moshi),Write(_.next))
    
    def shifts(_,val):
        _.play(_.yuanlai.shift,(val*0.5*RIGHT),
               _.next.shift,(val*0.5*RIGHT), run_time=0.5)
        _.b += val
    
    def shiftto(_,val):
        _.play(_.yuanlai.shift,((val-_.b)*0.5*RIGHT),
               _.next.shift,((val-_.b)*0.5*RIGHT) ,run_time=0.5)
        _.b = val
    
    def shiftgreen(_,val):
        _.play(_.rect.shift,(val*0.5*RIGHT),run_time=0.5)
        _.comp += val
    
    def shiftgto(_,val):
        _.play(_.rect.shift,((val-_.comp)*0.5*RIGHT),run_time=0.5)
        _.comp = val
    
    def compare(_,dig):
        _.write(rect)
    
    def alignw(_,bb,aa):
        _.shiftto(bb-aa)
        _.shiftgto(bb)
        if _.str1[bb]==_.str2[aa]:
            _.play(_.rect.set_color,(GREEN),run_time = 0.5)
        else:
            _.play(_.rect.set_color,(RED),run_time = 0.5)
    
    def matchord(_,t, p):
            i, j = 0, 0
            n, m = len(t), len(p)
            while i < n and j < m:
                _.alignw(i,j)
                if t[i] == p[j]:
                    i, j = i+1, j+1
                else:
                    i, j = i-j+1, 0
            if j == m:
                return i-j
            return -1

    def match(_,s1, s2, next_list):
            ans = -1
            i = 0
            j = 0
            while i < len(s1):
                _.alignw(i,j)
                if s1[i] == s2[j] or j == -1:
                    i += 1
                    j += 1
                else:
                    j = next_list[j]
                if j == len(s2):
                    ans = i - len(s2)
                    break
            return ans
    
class Demostrate3(Scene):
    
    def construct(_):
        _.str1="ji0de0san0lian0"
        _.str2="0san0lian0"
        _.init(_.str1,_.str2)
        _.match(_.str1,_.str2,StrMatcher.gen_next(_.str2))
    
    def init(_,str1,str2):
        _.a = 0
        _.b = 0
        _.comp = 0
        _.len1 = len(str1)
        _.len2 = len(str2)
        _.moshi = VGroup()
        _.yuanlai = VGroup()
        _.next = VGroup()
        _.rect = Rectangle(width=0.5,height=1,fill_color=GREEN,fill_opacity=0.3).move_to(np.array([-3,2.75,0]))
        for i in range(0,len(str1)):
            pos = np.array((-3+0.5*i,3,0.0))
            square = TextMobject(str1[i])
            square.move_to(pos)
            _.moshi.add(square)
        for i in range(0,len(str2)):
            pos = np.array((-3+0.5*i,2.5,0.0))
            square = TextMobject(str2[i])
            _.yuanlai.add(square)
            square.move_to(pos)
        for i in range(0,len(str2)):
            pos = np.array((-3+0.5*i,2,0.0))
            square = TextMobject(str(StrMatcher.gen_next(str2)[i]))
            _.next.add(square)
            square.move_to(pos)
        _.addTextsToScreen()
        _.add(_.rect)

    def addTextsToScreen(_):
        _.play(Write(_.yuanlai),Write(_.moshi),Write(_.next))
    
    def shifts(_,val):
        _.play(_.yuanlai.shift,(val*0.5*RIGHT),
               _.next.shift,(val*0.5*RIGHT), run_time=0.5)
        _.b += val
    
    def shiftto(_,val):
        _.play(_.yuanlai.shift,((val-_.b)*0.5*RIGHT),
               _.next.shift,((val-_.b)*0.5*RIGHT) ,run_time=0.5)
        _.b = val
    
    def shiftgreen(_,val):
        _.play(_.rect.shift,(val*0.5*RIGHT),run_time=0.5)
        _.comp += val
    
    def shiftgto(_,val):
        _.play(_.rect.shift,((val-_.comp)*0.5*RIGHT),run_time=0.5)
        _.comp = val
    
    def compare(_,dig):
        _.write(rect)
    
    def alignw(_,bb,aa):
        _.shiftto(bb-aa)
        _.shiftgto(bb)
        if _.str1[bb]==_.str2[aa]:
            _.play(_.rect.set_color,(GREEN),run_time = 0.5)
        else:
            _.play(_.rect.set_color,(RED),run_time = 0.5)
    
    def matchord(_,t, p):
            i, j = 0, 0
            n, m = len(t), len(p)
            while i < n and j < m:
                _.alignw(i,j)
                if t[i] == p[j]:
                    i, j = i+1, j+1
                else:
                    i, j = i-j+1, 0
            if j == m:
                return i-j
            return -1

    def match(_,s1, s2, next_list):
            ans = -1
            i = 0
            j = 0
            while i < len(s1):
                _.alignw(i,j)
                if s1[i] == s2[j] or j == -1:
                    i += 1
                    j += 1
                else:
                    j = next_list[j]
                if j == len(s2):
                    ans = i - len(s2)
                    break
            return ans
    
