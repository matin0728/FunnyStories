# Make me online, for EVER #

> Can write a Python script to shake mouse every 60s that running on MacOS to keep me looks 
> like active in chat app like Microsoft Teams.

    import time
    from Quartz import CGEventCreate, CGEventCreateMouseEvent, kCGEventMouseMoved, kCGMouseButtonLeft, CGEventPost
    from Quartz import kCGEventSourceStateHIDSystemState, CGPointMake

    def move_mouse():
        # Current mouse position (arbitrary, will cause a slight movement)
        current_position = CGPointMake(100, 100)
        # Create mouse move event
        move_event = CGEventCreateMouseEvent(None, kCGEventMouseMoved, current_position, kCGMouseButtonLeft)
        # Post the mouse event to simulate movement
        CGEventPost(kCGEventSourceStateHIDSystemState, move_event)

        # Move back slightly to create a small shake
        moved_position = CGPointMake(102, 102)
        move_event = CGEventCreateMouseEvent(None, kCGEventMouseMoved, moved_position, kCGMouseButtonLeft)
        CGEventPost(kCGEventSourceStateHIDSystemState, move_event)

    if __name__ == "__main__":
        print("Mouse Shaker is running...")

        try:
            while True:
                move_mouse()
                time.sleep(60)  # Wait 60 seconds before moving the mouse again
        except KeyboardInterrupt:
            print("Mouse Shaker stopped.")

## Install dependency ##

    brew install pyobjc
    pip3 install pyobjc-framework-Quartz --break-system-packages


