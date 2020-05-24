from manimlib.imports import *

class NextTo(Scene):
    
    def construct(_):
        t1 = TextMobject("Text1")
        t2 = TextMobject("Text2").next_to(t1.get_center(),direction=DOWN)
        vg1 = VGroup(
            Square(side_length=0.5).shift(LEFT*2),
            Square(side_length=0.5).shift(LEFT*1),
            Square(side_length=0.5),
            Square(side_length=0.5).shift(RIGHT*1),
            Square(side_length=0.5).shift(RIGHT*2),
        )
        vg2 = VGroup(
            Circle(radius=0.5).shift(LEFT),
            Circle(radius=0.5),
            Circle(radius=0.5).shift(RIGHT),
            Circle(radius=0.5).shift(2*RIGHT),
        ).next_to(vg1,DOWN,buff=1,index_of_submobject_to_align=1)
        a = DoubleArrow((vg1[2].get_center()),(vg2[2].get_center()),color=YELLOW)
        tx = Text("buff="+str(round(vg1[2].get_center()[1]-vg2[2].get_center()[1])),size=0.25,font="Consolas").move_to(a).add_background_rectangle()
        _.add(vg1,vg2,a,tx)





class Starting(Scene):
    def construct(_):
        a=Rectangle(width=10,height=10,fill_color=WHITE)
        _.add(a)
        def spread_out(p):
            p = p**2
            return p
        _.play(ApplyPointwiseFunction(spread_out, a))
