from manimlib.imports import *

class Shadow_around(VGroup):

    CONFIG = {
        'shadow_color': DARK_GRAY,
        'shadow_opacity': 0.3,
        'blur_width': 0.1,
        'layer_num': 10,
        'scale_factor': 1,
        'shadow_out': True,
        'show_basic_shape': True,
        'rate_func': lambda t: t ** 0.5,
    }

    def __init__(_, mob_or_points, **kwargs):
        VGroup.__init__(_, **kwargs)

        if type(mob_or_points) == list:
            _.shape = Polygon(*mob_or_points, stroke_width=0)
        else:
            _.shape = mob_or_points.set_stroke(width=0)

        _.shape.set_fill(color=_.shadow_color, opacity=_.shadow_opacity * (1 if _.show_basic_shape else 0)).scale(_.scale_factor)
        _.blur_outline = VGroup()
        s = (_.shape.get_height() + _.shape.get_width())/2
        if _.blur_width > 1e-4:
            for i in range(_.layer_num):
                layer_i = _.shape.copy().set_stroke(color=_.shadow_color, width=51 * _.blur_width/_.layer_num, opacity=_.shadow_opacity * (1-_.rate_func(i/_.layer_num))).\
                    set_fill(opacity=0).scale((s + (1 if _.shadow_out else -1) * _.blur_width/_.layer_num * (i+0.5))/ s)
                _.blur_outline.add(layer_i)
        _.add(_.shape, _.blur_outline)

class Message_box(VGroup):

    CONFIG = {
        'buffe': 0.3,
        'id_text': "Sample",
        'col': BLUE,
        'texes': "This is a sample text with formula $\\sum_{d | m}\\mu(d) g (m/d)$",
        'dire': True,
        'avatar':"D:\\music\\dialog\\mp.png",
        'UL':"D:\\3b1b\\manim\\assets\\svg_images\\blank.png",
        'UR':'D:\\3b1b\\manim\\assets\\svg_images\\UR3.png',
        'DL':"D:\\3b1b\\manim\\assets\\svg_images\\blank.png",
        'DR':"D:\\3b1b\\manim\\assets\\svg_images\\blank.png"
    }
    
    def __init__(_,direction,Bubble,Bar,**kwargs):
        VGroup.__init__(_, **kwargs)
        buff = _.buffe
        id_text = _.id_text
        col = _.col
        texes = _.texes
        _.avatar = ImageMobject(_.avatar).scale(0.65)
        avatar = _.avatar
        _.vcirc = Shadow_around(Circle(radius = avatar.get_width()/2-0.2).move_to(avatar.get_center())).shift(0.03*DOWN)
        vcirc = _.vcirc
        if(direction ):
            _.text = TextMobject(texes,plot_depth=99999,color = BLACK,font="Segoe UI Emoji").next_to(avatar,LEFT,aligned_edge = DOWN).scale(0.5,about_point=avatar.get_center()+avatar.get_width()/2*LEFT).shift(0.25*UP)
        else:
            _.text = TextMobject(texes,plot_depth=99999,color = BLACK,font="Segoe UI Emoji").next_to(avatar,aligned_edge = DOWN).scale(0.5,about_point=avatar.get_center()+avatar.get_width()/2*RIGHT).shift(0.25*UP)
        text = _.text
        person_id = Text(id_text,color = BLACK,font="思源宋体 CN").scale(0.3)
        person_id.next_to(avatar,UP,buff = -0.1)
        print(text.get_width())
        w = text.get_width()
        h = text.get_height()   
        # _.background = RoundedRectangle(corner_radius = 0.2,height = text.get_height()+buff,width =text.get_width()+buff,fill_opacity = 1.0,color=col,stroke_color = GREEN,stroke_opacity =0.0).move_to(text.get_center())
        _.background = Bubble.move_to(text.get_center()).set_height(text.get_height()+buff,stretch=True).set_width(text.get_width()+buff,stretch=True)
        if(direction):
            _.ll = RIGHT
            _.rr = LEFT
        else:
            _.ll = LEFT
            _.rr = RIGHT
        
        background = _.background
        bubble = Bar.scale(0.4).move_to(background.get_center()).shift(w/2*LEFT+h/2*DOWN)
        # bubble = SVGMobject("bubble.svg",plot_depth=3,color=col,fill_color=col,fill_opacity=1.0).scale(0.4).move_to(background.get_center()).shift(w/2*LEFT+h/2*DOWN)

        if (direction) :
            _.bg = VGroup(bubble,background).flip().shift(0.15*RIGHT)
        else:
            _.bg = VGroup(bubble,background)
        
        bg = _.bg
        sd2 = Shadow_around(bg.copy(),blur_width=0.2).shift(0.02*DOWN)
        _.mobs = VGroup(vcirc,sd2,bg,person_id)
        _.add(avatar)
        _.add(avatar,_.mobs,text)
    def get_starting_point(_):
        return _.avatar.get_center()+_.avatar.get_width()*LEFT/2+_.avatar.get_height()*DOWN/2
    def get_mobs(_):
        return _.mobs
    def get_vci(_):
        return _.vcirc
    def get_avatar(_):
        return _.avatar
    def get_txt(_):
        return _.text

class MsgAnimation(Animation):
    def __init__(_, msg, **kwargs):
        super().__init__(msg, **kwargs)



class MsgScene(Scene):

    def feed_data(_):
        # 显示文本
        _.texts = ["据说是0.0000034\\%",
                    "名为德雷克公式的",
                    "类似于妄想般的方程式",
                    "这个公式用来推测宇宙中",
                    "外星智慧生命体的数量",
                    "不过有人用这一公式",
                    "来计算和命中注定之人相遇的概率",
                    "那个概率据说是0.0000034\\%",
                    "然而这一公式并没有什么可信度",
                    "固些得出的肯定不是正确的数字吧",
                    "不过我觉得公式或许没错",
                    "第一次看到她时",
                    "我就觉得这肯定是命中注定",
                    "不需要什么理由",
                    "也不需要寻求他人的理解",
                    "但是我似乎找到了",
                    "从出生之前就一直在寻找的人",
                    "伯恩哈德·黎曼曾经预测过",
                    "$\\zeta$函数的素数有着某种规则",
                    "而世界上的数学家们" , 
                    "花费了15O年想要证明这一猜想" , 
                    "所谓重力波" , 
                    "也是爱因斯坦最先提出的猜想" , 
                    "真正被发现的则是100年后" , 
                    "这个世界上最为科学的理论" , 
                    "往往都是通过直觉进行猜想" , 
                    "随后才能证明其真伪" , 
                    "比起你来说" ,
                    "或许我的确还不太了解她",
                    "但我打算花一辈子去论明自己的爱",
                    "并非证明有爱之后才去和\\texttt{ Hiiro }结婚",
                    "是为了证明自己的爱而和\\texttt{ Hiiro }结婚",
                    ]
        # 聊天者ID
        _.id = ["junble2"]*50
        # 飞入方向
        _.dir = [0]*50
        # 头像
        _.img = ["D:\\music\\dialog\\"+i+".png" for i in _.id]
        # 颜色
        _.clrs = [GREEN,BLUE,GOLD]
        # 表情(偏移量,表情图片)
        _.emoji = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        # 装饰
        _.style = [0]*50

    def get_bubble(_,i,col):
        if i==1:
            t = SVGMobject("bubble1",plot_depth=5,fill_color=WHITE,fill_opacity=1.0,stroke_color=BLACK,stroke_opacity=1.0,stroke_width=3)
            # t.set_color(BLACK)
            return t
        elif i==2:
            return RoundedRectangle(corner_radius = 0.2,plot_depth=5,fill_opacity=1.0,stroke_color=col).set_color(["#b9d6fa","#c9c4e2"]).set_sheen_direction(DOWN)
        elif i==3:
            return SVGMobject("bubble2",plot_depth=5,fill_opacity=1.0,stroke_color=BLACK,stroke_opacity=1.0,stroke_width=3).set_color(["#393485","#1a1548"]).set_sheen_direction(DR)
        elif i==4:
            return RoundedRectangle(corner_radius = 0.2,plot_depth=5,fill_opacity=1.0,stroke_color=col).set_color(["#171a3e","#121435"]).set_sheen_direction(DOWN)
        elif i==5:
            t=SVGMobject("bubble3",plot_depth=5,fill_opacity=1.0,stroke_color=BLACK,stroke_opacity=1.0,stroke_width=0)
            t[0].set_color(["#9aa0b4","#3f4554","#9aa0b4"]).set_sheen_direction(DOWN)
            t[1].set_color(["#9aa0bb","#3f4553","#9aa0bb"]).set_sheen_direction(DOWN)
            t[2].set_color(["#fafcfb","#e3fafc"]).set_sheen_direction(DOWN)
            t[3].set_color(["#a0e0f6","#e3fafc"]).set_sheen_direction(DOWN)
            t[4].set_color(["#a0e0f6","#e3fafc"]).set_sheen_direction(UP)
            t[5].set_color(["#a0e0f6","#e3fafc"]).set_sheen_direction(DOWN)
            t[6].set_color(["#a0e0f6","#e3fafc"]).set_sheen_direction(UP)
            t[7].set_color(["#a0e0f6","#e3fafc"]).set_sheen_direction(DOWN)
            t[8].set_color(["#9aa0b4","#3f4554"]).set_sheen_direction(DOWN)
            t[9].set_color(["#9aa0b4","#3f4554"]).set_sheen_direction(DOWN)
            t[10].set_color(["#a0e0f6","#e3fafc"])
            t[11].set_color(["#a0e0f6","#e3fafc"])
            return t
        elif i==6:
            t=SVGMobject("bubble4",plot_depth=5,fill_opacity=1.0,stroke_color=BLACK,stroke_opacity=1.0,stroke_width=0)
            t[0].set_color(["#fbd9dc","#fad5db","#f7c2cc"])
            t[1].set_color("#ce6baf")
            t[2].set_color("#9b5385")
            return t
        elif i==7:
            t=SVGMobject("bubble5",plot_depth=5,fill_opacity=1.0,stroke_color=BLACK,stroke_opacity=1.0,stroke_width=0)
            t[0].set_color("#754232").set_sheen_direction(RIGHT)
            t[1].set_color("#644537")
            t[2].set_color("#4c3123")
            return t
        elif i==8:
            t=SVGMobject("bubble6",plot_depth=5,fill_opacity=1.0,stroke_color=BLACK,stroke_opacity=1.0,stroke_width=0)
            t[0].set_color("#754232").set_sheen_direction(RIGHT)
            t[1].set_color(WHITE)
            t[2].set_color("#fff5de")
            t[3].set_color("#b3b68b")
            return t
        else:
            return RoundedRectangle(corner_radius = 0.2,fill_color=col,plot_depth=5,fill_opacity=1.0,stroke_color=col)

    def get_bar(_,i,col):
        if i==1:
            return SVGMobject("bubble.svg",plot_depth=0,color=col,fill_color=col,fill_opacity=1.0).scale(0.01)
        elif i==2 or i==3 or i==5 or i==6 or i==7 or i==8:
            return SVGMobject("bubble.svg",plot_depth=0,color=col,fill_color=col,fill_opacity=1.0).scale(0.01)
        elif i==4:
            return SVGMobject("bubble.svg",plot_depth=0,color="#121435",fill_color="#121435",fill_opacity=1.0).scale(0.5)
        else:
            return SVGMobject("bubble.svg",plot_depth=0,color=col,fill_color=col,fill_opacity=1.0,stroke_color=col).scale(0.5)

    def init(_):
        
        _.cd = []
        for i in range(len(_.texts)):
            if _.dir[i] == 0:
                print("Left")
                _.cd.append(Message_box(0,_.get_bubble(_.style[i],_.clrs[i%3]),_.get_bar(_.style[i],_.clrs[i%3]),texes = _.texts[i],id_text=_.id[i]))
            else:
                print("Right")
                _.cd.append(Message_box(1,_.get_bubble(_.style[i],_.clrs[i%3]),_.get_bar(_.style[i],_.clrs[i%3]),texes = _.texts[i],id_text=_.id[i]))

        _.mob = [i.get_mobs() for i in _.cd ]
        _.txt = [i.get_txt() for i in _.cd ]
        _.ava = [i.get_avatar() for i in _.cd ]
        _.vc = [i.get_vci() for i in _.cd ]
        for i in range(len(_.texts)):
            if(_.dir[i]):
                _.ll = RIGHT
                _.rr = LEFT
            else:
                _.ll = LEFT
                _.rr = RIGHT
        for i in range(len(_.cd)):
            if(_.dir[i]==0):
                _.cd[i].shift(4*LEFT)
            else :
                _.cd[i].shift(2*RIGHT)
        _.ULs = [ImageMobject(_.cd[i].UL,plot_depth=999).move_to(_.txt[i].get_center()+(_.txt[i].get_height()/2+_.cd[i].buffe/2)*UP+_.txt[i].get_width()/2*_.ll).scale(0.2) for i in range(len(_.cd)) ]
        _.URs = [ImageMobject(_.cd[i].UR,plot_depth=999).move_to(_.txt[i].get_center()+(_.txt[i].get_height()/2+_.cd[i].buffe/2)*UP-_.txt[i].get_width()/2*_.ll).scale(0.2) for i in range(len(_.cd)) ]
        _.DLs = [ImageMobject(_.cd[i].DL,plot_depth=999).move_to(_.txt[i].get_center()+(_.txt[i].get_height()/2+_.cd[i].buffe/2)*DOWN+_.txt[i].get_width()/2*_.ll).scale(0.2) for i in range(len(_.cd))  ]
        _.DRs = [ImageMobject(_.cd[i].DR,plot_depth=999).move_to(_.txt[i].get_center()+(_.txt[i].get_height()/2+_.cd[i].buffe/2)*DOWN-_.txt[i].get_width()/2*_.ll).scale(0.2) for i in range(len(_.cd)) ]
        _.VG = VGroup()
    
           

    def anime(_,i):
        
        def update(obj):
            obj.become(ImageMobject(_.img[i]).move_to(_.vc[i].get_center()).set_width(_.vc[i].get_width()))
        _.ava[i].add_updater(update)
        _.play(_.VG.shift,1.5*UP,GrowFromPoint(_.mob[i],_.cd[i].get_starting_point()),FadeIn(_.ava[i]))
        emo = [ImageMobject("D:\\3b1b\\manim\\assets\\svg_images\\"+j[1]+".png",plot_depth=999999).move_to(_.mob[i]).shift(j[0]*LEFT).scale(0.3) for j in _.emoji[i] ]
        print(emo)
        if(len(emo)>0):
            _.play(Write(_.txt[i]),FadeIn(_.ULs[i]),FadeIn(_.URs[i]),FadeIn(_.DLs[i]),FadeIn(_.DRs[i]),run_time = 0.5)
        else:
            _.play(Write(_.txt[i]),FadeIn(_.ULs[i]),FadeIn(_.URs[i]),FadeIn(_.DLs[i]),FadeIn(_.DRs[i]),run_time = 0.5)
            
        _.ava[i].remove_updater(update)
        _.VG.add(_.cd[i])
        _.VG.add(_.ULs[i],_.URs[i],_.DLs[i],_.DRs[i])
        if(len(emo)>0):
            for i in range(len(emo)):
                _.play(FadeIn(emo[i]))
                _.VG.add(emo[i])
        
        if(i>4):
            _.VG.remove(_.cd[i-4])
            _.VG.remove(_.DLs[i-4])
            _.VG.remove(_.DRs[i-4])
            _.VG.remove(_.ULs[i-4])
            _.VG.remove(_.URs[i-4])
        _.clear()
        _.add(_.VG)
        
    
    def construct(_):
        _.feed_data()
        _.init()
        for i in range(len(_.cd)):
            _.anime(i)
            _.wait(1)
        # _.anime(1)
        # _.anime(2)
        # _.anime(3)
        # _.add(_.get_bubble(9,GRAY))