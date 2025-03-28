import sys
import time
import threading

def loading_animation(func):
    def wrapper(*args, **kwargs):
        loading_chars = ['|', '/', '-', '\\']
        
        def animate():
            while not stop_animation:
                for char in loading_chars:
                    sys.stdout.write(f'\r{char} ')
                    sys.stdout.flush()
                    time.sleep(0.2)

        global stop_animation
        stop_animation = False
        
        animation_thread = threading.Thread(target=animate)
        animation_thread.daemon = True
        animation_thread.start()

        try:
            result = func(*args, **kwargs)
        except KeyboardInterrupt:
            stop_animation = True
            sys.stdout.flush()
            raise
        finally:
            stop_animation = True
            sys.stdout.flush()

        return result
    return wrapper