import RPi.GPIO as GPIO
import time

# Pin Definitions
PIN_A = 14   # Channel A pin
PIN_B = 15   # Channel B pin

# Variables to track state, direction, and debounce timing
last_state_A = 0
last_state_B = 0
counter = 0
direction = None
last_time = time.time()  # Track time to debounce

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Debounce threshold (in seconds)
DEBOUNCE_TIME = 0.005  # 5 milliseconds

def rotary_callback(channel):
    global last_state_A, last_state_B, counter, direction, last_time

    current_time = time.time()
    if current_time - last_time < DEBOUNCE_TIME:
        return  # Ignore if within debounce time

    # Update the last time the interrupt was triggered
    last_time = current_time

    # Read current states of A and B
    state_A = GPIO.input(PIN_A)
    state_B = GPIO.input(PIN_B)

    # Determine direction
    if state_A != last_state_A:  # If A changed
        if state_A == state_B:  # A and B are the same (CW)
            counter += 1
            direction = "Clockwise"
        else:  # A and B are different (CCW)
            counter -= 1
            direction = "Counterclockwise"

    # Save the current states for the next interrupt
    last_state_A = state_A
    last_state_B = state_B

    # Output the current state (for debugging)
    print(f"Direction: {direction}, Counter: {counter}")

# Attach interrupts to both channels with both edges
GPIO.add_event_detect(PIN_A, GPIO.BOTH, callback=rotary_callback)
GPIO.add_event_detect(PIN_B, GPIO.BOTH, callback=rotary_callback)

# Main loop
try:
    while True:
        pass  # Keep the program running
except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on Ctrl+C exit
