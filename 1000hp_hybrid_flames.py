# 1000hp_hybrid_flames_boost.py
# Now with REAL BOOST GAUGE + NEEDLE
import turtle as t
import time
import math
import threading
import random

# ── CONFIG ──
RPM = 7800
MAX_BOOST = 2.1
SOUND = True
FLAMES = True

# ── PHYSICS ──
CRANK_RADIUS = 43
ROD_LENGTH = 135
angle = 0
cycle = 0
current_boost = 0.0
exhaust_particles = []

# ── WINDOW ──
wn = t.Screen()
wn.title("1000 HP | Boost Gauge + Flames | 7800 RPM")
wn.bgcolor("#0a0a0a")
wn.setup(1200, 750)
wn.tracer(0, 0)

# ── ENGINE BLOCK ──
block = t.Turtle(); block.hideturtle(); block.speed(0)
block.pencolor("#222"); block.fillcolor("#111")
block.penup(); block.goto(-250, 230); block.begin_fill()
for _ in range(2):
    block.forward(500); block.circle(30,90); block.forward(460); block.circle(30,90)
block.end_fill()

# ── EXHAUST PIPE ──
exhaust = t.Turtle(); exhaust.hideturtle()
exhaust.color("#333"); exhaust.penup(); exhaust.goto(250, -100)
exhaust.pendown(); exhaust.pensize(40); exhaust.goto(350, -100)

# ── BOOST GAUGE (BOTTOM-RIGHT) ──
gauge = t.Turtle(); gauge.hideturtle()
needle = t.Turtle(); needle.hideturtle()
def draw_gauge():
    gauge.clear()
    gauge.penup(); gauge.goto(400, -280); gauge.pendown()
    gauge.color("white"); gauge.pensize(4)
    gauge.circle(80)  # gauge circle
    gauge.penup(); gauge.goto(400, -200); gauge.write("BOOST", font=("Arial",14,"bold"))
    gauge.goto(400, -320); gauge.write("bar", font=("Arial",12))
    for i in range(11):
        angle_deg = 180 + i*18
        x = 400 + 75 * math.cos(math.radians(angle_deg))
        y = -280 + 75 * math.sin(math.radians(angle_deg))
        gauge.penup(); gauge.goto(x,y); gauge.dot(6,"white")
        if i % 2 == 0:
            gauge.goto(400 + 65 * math.cos(math.radians(angle_deg)), -280 + 65 * math.sin(math.radians(angle_deg)))
            gauge.write(f"{i*0.2:.1f}", font=("Arial",8))

# ── FLAME PARTICLES ──
flame_turtles = [t.Turtle() for _ in range(20)]
for f in flame_turtles: f.hideturtle(); f.speed(0)

# ── SOUND ──
def engine_sound():
    if not SOUND: return
    while True:
        freq = 180 + (int(angle) % 700)
        duration = 20 if angle % 720 < 360 else 35
        try: import winsound; winsound.Beep(freq, duration)
        except: pass
        time.sleep(0.015)
threading.Thread(target=engine_sound, daemon=True).start()

# ── PISTON PHYSICS ──
def piston_position(a):
    theta = math.radians(a)
    s = CRANK_RADIUS * math.sin(theta)
    c = CRANK_RADIUS * math.cos(theta)
    return s + math.sqrt(ROD_LENGTH**2 - c**2)

# ── FLAME SPAWN ──
def spawn_flame():
    if not FLAMES or not (350 < angle % 720 < 370): return
    x = 320 + random.randint(-10,10)
    y = -100 + random.randint(-15,15)
    size = random.randint(15,35)
    life = random.randint(8,15)
    color = random.choice(["#ff3300","#ff8800","#ffff00"])
    exhaust_particles.append([x,y,size,life,color])

# ── UPDATE FLAMES ──
def update_flames():
    for p in exhaust_particles[:]:
        p[1] -= 3; p[2] *= 0.95; p[3] -= 1
        if p[3] <= 0:
            exhaust_particles.remove(p); continue
        i = exhaust_particles.index(p)
        f = flame_turtles[i % len(flame_turtles)]
        f.clear(); f.penup(); f.goto(p[0],p[1]); f.color(p[4]); f.dot(p[2])

# ── UPDATE NEEDLE ──
def update_needle():
    needle.clear()
    boost_angle = 180 + (current_boost / MAX_BOOST) * 180
    x = 400 + 70 * math.cos(math.radians(boost_angle))
    y = -280 + 70 * math.sin(math.radians(boost_angle))
    needle.penup(); needle.goto(400, -280)
    needle.pendown(); needle.color("red"); needle.pensize(4)
    needle.goto(x,y)

# ── TURTLES ──
piston = t.Turtle(); piston.hideturtle()
rod = t.Turtle(); rod.hideturtle()
crank = t.Turtle(); crank.hideturtle()
spark = t.Turtle(); spark.hideturtle()
hud = t.Turtle(); hud.hideturtle()

# ── MAIN LOOP (120 FPS) ──
last_time = time.time()
draw_gauge()
while True:
    now = time.time()
    dt = now - last_time
    last_time = now
    wn.update()
    time.sleep(max(0, 1/120 - dt))

    # BOOST LOGIC (spools up with RPM)
    target_boost = min(MAX_BOOST, (RPM/3000) * MAX_BOOST)
    current_boost += (target_boost - current_boost) * 0.05

    angle = (angle + RPM * 6 * dt) % 720
    piston_y = piston_position(angle % 360)
    spawn_flame()
    update_flames()
    update_needle()

    piston.clear(); rod.clear(); crank.clear(); spark.clear(); hud.clear()
    
    # PISTON
    piston.color("#ff0066"); piston.penup(); piston.goto(-50, piston_y + 80)
    piston.pendown(); piston.begin_fill()
    for _ in range(2):
        piston.forward(100); piston.circle(18,90); piston.forward(55); piston.circle(18,90)
    piston.end_fill()

    # ROD & CRANK
    rod.color("#aaa"); rod.pensize(10); rod.penup()
    rod.goto(0, CRANK_RADIUS * math.sin(math.radians(angle % 360)))
    rod.pendown(); rod.goto(0, piston_y + 80)
    crank.color("#00ff99"); crank.pensize(8)
    crank.penup(); crank.goto(0,0); crank.pendown(); crank.circle(CRANK_RADIUS)

    # SPARK
    if 355 < angle % 360 < 5:
        spark.color("white"); spark.penup(); spark.goto(0,180); spark.dot(50)
        spark.color("yellow"); spark.dot(35)

    # HUD
    hud.color("lime"); hud.penup()
    hud.goto(-580,340); hud.write("1000 HP + BOOST GAUGE", font=("Courier",20,"bold"))
    hud.goto(-580,310); hud.write(f"RPM: {RPM:,}", font=("Courier",18))
    hud.goto(-580,280); hud.write(f"BOOST: {current_boost:.2f} bar", font=("Courier",18))

    cycle += 1

wn.onkey(wn.bye, "Escape")
wn.listen()
wn.mainloop()