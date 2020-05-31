from manimlib.imports import *

class NextTo(Scene):
    
    def construct(_):
        t1 = TextMobject("Text1")
        _.play(WiggleOutThenIn(t1))





class Starting(Scene):
    def construct(_):
        a=Rectangle(width=10,height=10,fill_color=WHITE)
        _.add(a)
        def spread_out(p):
            p = p**2
            return p
        _.play(ApplyPointwiseFunction(spread_out, a))
