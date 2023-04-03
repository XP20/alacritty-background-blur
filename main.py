from pywinauto import Application
from ctypes import c_int, Structure, POINTER, windll, byref, sizeof, cast, pointer
import sys

def IsWin11():
    if sys.getwindowsversion().build > 20000: return True
    else: return False

class ACCENT_POLICY(Structure):
    _fields_ = [("AccentState", c_int),
                ("AccentFlags", c_int),
                ("GradientColor", c_int),
                ("AnimationId", c_int)]
 
# Get the window handle
hwnd = Application().connect(path="alacritty.exe").top_window().handle

accent_policy = ACCENT_POLICY()
accent_policy.AccentState = 3 # ACCENT_ENABLE_BLURBEHIND value is 3

if IsWin11():
    accent_policy.AccentFlags = 0x20 | 0x40 # Set the ACCENT_ENABLE_BLURBEHIND and ACCENT_INVALID_OPACITY flag

class WINDOWCOMPOSITIONATTRIB(Structure):
    _fields_ = [("Attribute", c_int),
                ("Data", POINTER(ACCENT_POLICY)),
                ("SizeOfData", c_int)]

wca = WINDOWCOMPOSITIONATTRIB()
wca.Attribute = 19 # WCA_ACCENT_POLICY value is 19
wca.Data = POINTER(ACCENT_POLICY)()
wca.SizeOfData = sizeof(accent_policy)

# Get the pointer to the ACCENT_POLICY instance
p_accent_policy = cast(pointer(accent_policy), POINTER(c_int))
wca.Data = cast(p_accent_policy, POINTER(ACCENT_POLICY))

SetWindowCompositionAttribute = windll.user32.SetWindowCompositionAttribute
SetWindowCompositionAttribute(hwnd, byref(wca))
