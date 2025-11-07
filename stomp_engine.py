# stomp_engine.py  ←  SAVE THIS EXACTLY
import turtle as t
import time

# === DRAW THE ENGINE FIRST ===
t.speed(2); t.pensize(4); t.color("dodgerblue")

# Cylinder
t.penup(); t.goto(-60,150); t.pendown()
t.setheading(270); t.circle(60,180)
t.setheading(90); t.forward(300)

# PISTON
t.penup(); t.goto(-50,80); t.pendown()
t.color("red"); t.begin_fill()
for _ in range(2):
    t.forward(100); t.circle(15,90)
    t.forward(50); t.circle(15,90)
t.end_fill()

# Rod + Crank
t.color("gray"); t.penup(); t.goto(0,30); t.pendown()
t.setheading(270); t.forward(100)
t.penup(); t.goto(0,-70); t.pendown()
t.color("black"); t.circle(40)

# Labels
t.penup(); t.goto(100,-70); t.pendown()
t.write("SPIN → WHEELS", font=("Arial",16,"bold"))
t.penup(); t.goto(-30,100); t.pendown()
t.color("orange"); t.write("HAMMER BLOW!", font=("Comic Sans MS",20,"bold"))

t.hideturtle()
t.update()          # Force screen refresh
t.done()            # Window stays open

# === NOW MAKE IT ROAR (after drawing) ===
try:
    import winsound
    for i in range(5):
        winsound.Beep(200 + i*100, 90)   # 200 → 600 Hz VROOOM
        time.sleep(0.12)
    winsound.Beep(800, 300)   # Final BANG!
except:
    print("Mac/Linux? No beep → but drawing still works!")