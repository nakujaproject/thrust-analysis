import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import RPi.GPIO as GPIO

presses = 0
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def writeFile(val, f):
    global presses
    if (GPIO.input(18) == False):
        presses = presses + 1
        print("pressed")
    #print("{0: 4.4f}".format(val))
    #print(presses)
    if (presses == 1):
        f.write(str(val) + "\n")
    elif (presses > 1):
        f.close()

# This function is called periodically from FuncAnimation
def animate(i, xs, ys, ax, scale, f):

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%S.%f'))
    thrust = scale.getMeasure()
    writeFile(thrust, f)
    ys.append(thrust)

    # Limit x and y lists to 40 items
    xs = xs[-40:]
    ys = ys[-40:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Thrust data')
    plt.ylabel('Thrust (grams)')
