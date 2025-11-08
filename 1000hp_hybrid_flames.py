# 1000hp_hybrid_flames.py
# Real piston physics + exhaust flames + 120 FPS
import turtle as t
import time
import math
import threading
import random

# ── CONFIG ──
RPM = 7800
SOUND = True
FLAMES = True

# ── PHYSICS CONSTANTS ──
CRANK_RADIUS = 43      # mm
ROD_LENGTH = 135       # mm
BORE = 86              # mm
STROKE = 86            # mm
COMPRESSION = 10.5

# ── GLOBALS ──
angle = 0
cycle = 0
exhaust_particles = []

# ── WINDOW ──
wn = t.Screen()
wn.title("1000 HP | Real Physics + Flames | 7800 RPM")
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

# ── FLAME PARTICLES ──
flame_turtles = [t.Turtle() for _ in range(20)]
for f in flame_turtles:
    f.hideturtle(); f.speed(0)

# ── SOUND ──
def engine_sound():
    if not SOUND: return
    while True:
        freq = 180 + (int(angle) % 700)
        duration = 20 if angle % 720 < 360 else 35
        try:
            import winsound
            winsound.Beep(freq, duration)
        except:
            pass
        time.sleep(0.015)
threading.Thread(target=engine_sound, daemon=True).start()

# ── PISTON PHYSICS EXPLAINED ──
def piston_position(crank_angle_deg):
    """
    REAL ENGINE MATH:
    piston_y = crank_radius * sin(θ) + rod_length * sqrt(1 - (crank_radius/rod_length * cos(θ))^2)
    This is the EXACT motion of a real piston.
    """
    theta = math.radians(crank_angle_deg)
    s = CRANK_RADIUS * math.sin(theta)
    c = CRANK_RADIUS * math.cos(theta)
    piston_height = s + math.sqrt(ROD_LENGTH**2 - c**2)
    return piston_height

# ── EXHAUST FLAME SPAWNER ──
def spawn_flame():
    if not FLAMES: return
    if 350 < angle % 720 < 370:  # Exhaust stroke
        x = 320 + random.randint(-10, 10)
        y = -100 + random.randint(-15, 15)
        size = random.randint(15, 35)
        life = random.randint(8, 15)
        exhaust_particles.append([x, y, size, life, random.choice(["#ff3300","#ff8800","#ffff00"])])

# ── UPDATE FLAMES ──
def update_flames():
    for p in exhaust_particles[:]:
        x, y, size, life, color = p
        life -= 1
        y -= 3
        size *= 0.95
        p[1] = y; p[2] = size; p[3] = life
        if life <= 0:
            exhaust_particles.remove(p)
            continue
        i = exhaust_particles.index(p)
        f = flame_turtles[i % len(flame_turtles)]
        f.clear()
        f.penup(); f.goto(x, y); f.color(color)
        f.dot(size)

# ── MAIN TURTLES ──
piston = t.Turtle(); piston.hideturtle()
rod = t.Turtle(); rod.hideturtle()
crank = t.Turtle(); crank.hideturtle()
spark = t.Turtle(); spark.hideturtle()
hud = t.Turtle(); hud.hideturtle()

# ── MAIN LOOP (120 FPS) ──
last_time = time.time()
while True:
    now = time.time()
    dt = now - last_time
    last_time = now

    # 120 FPS lock
    wn.update()
    time.sleep(max(0, 1/120 - dt))

    # ── REAL PHYSICS UPDATE ──
    angle = (angle + RPM * 6 * dt) % 720  # 720° = 1 full cycle
    piston_y = piston_position(angle % 360)

    # Spawn flame
    spawn_flame()
    update_flames()

    # Clear moving parts
    piston.clear(); rod.clear(); crank.clear(); spark.clear(); hud.clear()

    # ── PISTON (REAL SHAPE) ──
    piston.color("#ff0066"); piston.penup()
    piston.goto(-50, piston_y + 80); piston.pendown()
    piston.begin_fill()
    for _ in range(2):
        piston.forward(100); piston.circle(18,90)
        piston.forward(55); piston.circle(18,90)
    piston.end_fill()

    # ── ROD ──
    rod.color("#aaa"); rod.pensize(10)
    rod.penup(); rod.goto(0, CRANK_RADIUS * math.sin(math.radians(angle % 360)))
    rod.pendown(); rod.goto(0, piston_y + 80)

    # ── CRANKSHAFT ──
    crank.color("#00ff99"); crank.pensize(8)
    crank.penup(); crank.goto(0,0); crank.pendown()
    crank.circle(CRANK_RADIUS)

    # ── SPARK PLUG FIRE ──
    if 355 < angle % 360 < 5:
        spark.color("white"); spark.penup(); spark.goto(0, 180)
        spark.dot(50); spark.color("yellow"); spark.dot(35)

    # ── HUD ──
    hud.color("lime"); hud.penup()
    hud.goto(-580, 340); hud.write("REAL PHYSICS ENGINE", font=("Courier",20,"bold"))
    hud.goto(-580, 310); hud.write(f"RPM: {RPM:,}", font=("Courier",18))
    hud.goto(-580, 280); hud.write("BOOST: 2.1 bar", font=("Courier",18))
    hud.goto(-580, 250); hud.write("POWER: 1000 HP", font=("Courier",18))
    hud.goto(-580, 220); hud.write("EXHAUST: FLAME ON", font=("Courier",18))

    cycle += 1

wn.onkey(wn.bye, "Escape")
wn.listen()
wn.mainloop()