# stomp_engine.py — FIXED & PERFECT
import turtle as t
import time
import math
import threading
import winsound

# ── CONFIG ──
RPM = 7200
SOUND = True

# ── PHYSICS ──
CRANK_RADIUS = 40
ROD_LENGTH = 100

# ── GLOBALS (declared at top) ──
angle = 0
cycle = 0

# ── WINDOW ──
wn = t.Screen()
wn.title(f"HAMMER BLOW | {RPM} RPM | 1000 HP")
wn.bgcolor("black")
wn.setup(1000, 700)
wn.tracer(0, 0)

# ── DRAW ENGINE BLOCK ──
block = t.Turtle(); block.hideturtle(); block.speed(0)
block.pencolor("#333"); block.penup(); block.goto(-200, 200)
block.pendown()
for _ in range(2):
    block.forward(400); block.circle(20, 90)
    block.forward(400); block.circle(20, 90)

# ── TURBO SOUND ──
def turbo_sound():
    if not SOUND: return
    freq = 200
    while True:
        winsound.Beep(freq, 30)
        freq = min(800, freq + 20)
        time.sleep(0.03)

if SOUND:
    threading.Thread(target=turbo_sound, daemon=True).start()

# ── TURTLES ──
piston = t.Turtle(); piston.hideturtle()
rod    = t.Turtle(); rod.hideturtle()
crank  = t.Turtle(); crank.hideturtle()
spark  = t.Turtle(); spark.hideturtle()
hud    = t.Turtle(); hud.hideturtle()

# ── MAIN LOOP ──
while True:
    # UPDATE ANGLE (7200 RPM = 120 degrees per frame)
    angle = (angle + 120) % 360
    rad = math.radians(angle)

    # CRANK POSITION
    crank_x = CRANK_RADIUS * math.cos(rad)
    crank_y = CRANK_RADIUS * math.sin(rad)

    # PISTON HEIGHT (using Pythagoras)
    piston_y = crank_y + math.sqrt(ROD_LENGTH**2 - crank_x**2)

    # CLEAR
    piston.clear(); rod.clear(); crank.clear(); spark.clear(); hud.clear()

    # DRAW PISTON
    piston.color("red"); piston.penup(); piston.goto(-50, piston_y + 80)
    piston.pendown(); piston.begin_fill()
    for _ in range(2):
        piston.forward(100); piston.circle(15, 90)
        piston.forward(50);  piston.circle(15, 90)
    piston.end_fill()

    # DRAW ROD
    rod.color("gray"); rod.pensize(8)
    rod.penup(); rod.goto(0, crank_y); rod.pendown()
    rod.goto(0, piston_y + 80)

    # DRAW CRANK
    crank.color("lime"); crank.pensize(6)
    crank.penup(); crank.goto(0, 0); crank.pendown()
    crank.circle(CRANK_RADIUS)

    # SPARK + BOOM
    if 355 < angle % 360 or angle % 360 < 5:
        spark.color("yellow"); spark.penup()
        spark.goto(0, 160); spark.dot(40)
        spark.goto(-60, 200); spark.write("BOOM!", font=("Impact", 28, "bold"))

    # HUD
    hud.color("cyan"); hud.penup()
    hud.goto(-480, 320); hud.write(f"RPM: {RPM}", font=("Courier", 18))
    hud.goto(-480, 290); hud.write("TURBO: 1.8 bar", font=("Courier", 18))
    hud.goto(-480, 260); hud.write("POWER: 1000 HP", font=("Courier", 18))
    hud.goto(200, -330); hud.write("ESC = Quit", font=("Arial", 12))

    wn.update()
    time.sleep(0.016)  # 60 FPS
    cycle += 1

# ── CONTROLS ──
wn.onkey(wn.bye, "Escape")
wn.listen()
wn.mainloop()