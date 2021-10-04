import sys
import subprocess
 
try:
    import keyboard
except ImportError as e:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "keyboard", "-q"])
    import keyboard