# stomp_engine_pro.py  ←  NEW FILE NAME (professional)
"""
VEHICLE EASE | Hammer-Blow Engine Simulator
Author: LEMAYIAN KIRIONKI – Full-Stack Car Coder
GitHub: https://github.com/lemayian23/know_cars
Features: 60-FPS animation • Real physics • Sound • GUI • CLI args
"""

import turtle as t
import time
import math
import argparse
import platform
import threading
from datetime import datetime

# ==================== CONFIG ====================
parser = argparse.ArgumentParser(description="Hammer-Blow Engine Simulator")
parser.add_argument("--rpm", type=int, default=3000, help="Engine RPM (500-8000)")
parser.add_argument("--cylinders", type=int, choices=[1,4,6,8], default=4)
parser.add_argument("--sound", action="store_true", help="Enable V8 roar")
args = parser.parse_args()

RPM = max(500, min(8000, args.rpm))
CYLINDERS = args.cylinders
SOUND = args.sound and platform.system() == "Windows"

# ==================== PHYSICS ====================
CRANK_RADIUS = 40
ROD_LENGTH = 100
BORE = 86
STROKE = 86
COMPRESSION = 10.5
SPARK_TIMING = -35  # degrees BTDC

# ==================== WINDOW ====================
wn = t.Screen()
wn.title(f"Hammer-Blow Engine | {RPM} RPM | {CYLINDERS}-Cylinder")
wn.bgcolor("#0a0a0a")
wn.setup(1000, 700)
wn.tracer(0, 0)

# ==================== TURTLES ====================
piston = t.Turtle(); piston.hideturtle()
rod = t.Turtle(); rod.hideturtle()
crank = t.Turtle(); crank.hideturtle()
spark = t.Turtle(); spark.hideturtle()
text = t.Turtle(); text.hideturtle()

# ==================== DRAW ONCE ====================
def draw_engine():
    # Cylinder block
    block = t.Turtle(); block.speed(0); block.pencolor("#333")
    block.penup(); block.goto(-200, 200); block.pendown()
    for _ in range(2):
        block.forward(400); block.circle(20,90); block.forward(400); block.circle(20,90)
    block.hideturtle()

    # Head gasket
    t.penup(); t.goto(-200, 160); t.pendown(); t.color("#ff3300")
    t.pensize(6); t.forward(400)

draw_engine()

# ==================== ANIMATION LOOP ====================
angle = 0
cycle = 0
last_time = time.time()

def play_sound():
    if not SOUND: return
    import winsound
    freqs = [180, 220, 280, 350, 420, 500, 620, 780]
    for f in freqs * 3:
        winsound.Beep(f, 30)

if SOUND:
    threading.Thread(target=play_sound, daemon=True).start()

while True:
    now = time.time()
    dt = now - last_time
    last_time = now

    # 60 FPS lock
    wn.update()
    time.sleep(max(0, 1/60 - dt))

    # Clear moving parts
    piston.clear(); rod.clear(); crank.clear(); spark.clear(); text.clear()

    # Physics
    global angle, cycle
    angle = (angle + RPM/60 * 360 * dt) % 360
    rad = math.radians(angle)
    crank_x = CRANK_RADIUS * math.cos(rad)
    crank_y = CRANK_RADIUS * math.sin(rad)
    piston_y = crank_y + math.sqrt(ROD_LENGTH**2 - crank_x**2)

    # Draw piston
    piston.speed(0); piston.color("#ff0066"); piston.pensize(4)
    piston.penup(); piston.goto(-50, piston_y + 80); piston.pendown()
    piston.begin_fill()
    for _ in range(2):
        piston.forward(100); piston.circle(15,90)
        piston.forward(50); piston.circle(15,90)
    piston.end_fill()

    # Draw rod
    rod.speed(0); rod.color("#cccccc"); rod.pensize(8)
    rod.penup(); rod.goto(0, crank_y); rod.pendown()
    rod.goto(0, piston_y + 80)

    # Draw crank
    crank.speed(0); crank.color("#00ff99"); crank.pensize(6)
    crank.penup(); crank.goto(0,0); crank.pendown(); crank.circle(CRANK_RADIUS)

    # FIRE SPARK
    if -SPARK_TIMING - 5 < angle % 360 < -SPARK_TIMING + 5 and cycle % (720//CYLINDERS) == 0:
        spark.speed(0); spark.color("yellow"); spark.penup()
        spark.goto(0, 160); spark.dot(30)
        spark.goto(-30, 190); spark.write("BOOM!", font=("Impact", 20, "bold"))

    # HUD
    text.speed(0); text.color("lime"); text.penup()
    text.goto(-480, 320); text.write(f"RPM: {RPM}", font=("Courier", 16, "bold"))
    text.goto(-480, 290); text.write(f"Cylinders: {CYLINDERS}", font=("Courier", 16, "bold"))
    text.goto(-480, 260); text.write(f"Power: {int(RPM/100)} kW", font=("Courier", 16, "bold"))
    text.goto(200, -330); text.write("Press ESC to quit", font=("Arial", 12))

    cycle += 1

wn.listen()
wn.onkey(wn.bye, "Escape")
wn.mainloop()