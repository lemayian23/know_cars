# 1000hp_hybrid.py
# WORKS IN PYCHARM + TERMINAL + ANYWHERE
import turtle as t
import time
import math
import threading
try:
    import winsound
except:
    winsound = None

# ── GLOBALS (declared at top) ──
angle = 0
cycle = 0

# ── WINDOW ──
wn = t.Screen()
wn.title("1000 HP Hybrid | 7200 RPM")
wn.bgcolor("black")
wn.setup(1100, 700)
wn.tracer(0, 0)

# ── DRAW ENGINE BLOCK ──
block = t.Turtle()
block.hideturtle()
block.speed(0)
block.pencolor("#333")
block.penup()
block.goto(-220, 220)
block.pendown()
for _ in range(2):
    block.forward(440)
    block.circle(25, 90)
    block.forward(440)
    block.circle(25, 90)

# ── TURBO SOUND ──
def sound():
    if not winsound: return
    while True:
        freq = 200 + (int(angle) % 600)
        winsound.Beep(freq, 30)
        time.sleep(0.02)
threading.Thread(target=sound, daemon=True).start()

# ── TURTLES ──
piston = t.Turtle(); piston.hideturtle()
rod = t.Turtle(); rod.hideturtle()
crank = t.Turtle(); crank.hideturtle()
spark = t.Turtle(); spark.hideturtle()
hud = t.Turtle(); hud.hideturtle()

# ── MAIN LOOP ──
while True:
    # Physics
    angle = (angle + 120) % 360  # 7200 RPM = 120 deg/sec
    rad = math.radians(angle)
    crank_y = 40 * math.sin(rad)
    crank_x = 40 * math.cos(rad)
    piston_y = crank_y + math.sqrt(100**2 - crank_x**2)

    # Clear
    piston.clear()
    rod.clear()
    crank.clear()
    spark.clear()
    hud.clear()

    # PISTON
    piston.color("red")
    piston.penup()
    piston.goto(-50, piston_y + 80)
    piston.pendown()
    piston.begin_fill()
    for _ in range(2):
        piston.forward(100)
        piston.circle(15, 90)
        piston.forward(50)
        piston.circle(15, 90)
    piston.end_fill()

    # ROD
    rod.color("gray")
    rod.pensize(8)
    rod.penup()
    rod.goto(0, crank_y)
    rod.pendown()
    rod.goto(0, piston_y + 80)

    # CRANK
    crank.color("lime")
    crank.pensize(6)
    crank.penup()
    crank.goto(0, 0)
    crank.pendown()
    crank.circle(40)

    # SPARK
    if 355 < angle % 360 or angle % 360 < 5:
        spark.color("yellow")
        spark.penup()
        spark.goto(0, 160)
        spark.dot(40)
        spark.goto(-60, 200)
        spark.write("BOOM!", font=("Impact", 28, "bold"))

    # HUD
    hud.color("cyan")
    hud.penup()
    hud.goto(-530, 320)
    hud.write("RPM: 7200", font=("Courier", 18))
    hud.goto(-530, 290)
    hud.write("BOOST: 1.8 bar", font=("Courier", 18))
    hud.goto(-530, 260)
    hud.write("POWER: 1000 HP", font=("Courier", 18))

    wn.update()
    time.sleep(0.016)  # ~60 FPS
    cycle += 1

wn.onkey(wn.bye, "Escape")
wn.listen()
wn.mainloop()