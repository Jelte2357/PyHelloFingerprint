import asyncio
from winrt.windows.security.credentials.ui import UserConsentVerificationResult, UserConsentVerifier, UserConsentVerifierAvailability
# note you can NOT just install winrt, you have to "pip install winrt.windows.security.credentials.ui"
import pygetwindow as gw
import win32gui
import pyautogui as pag
from ctypes import windll, create_string_buffer

def get_class_name(hwnd):
    buf_size = 256
    buffer = create_string_buffer(buf_size)
    windll.user32.GetClassNameA(hwnd, buffer, buf_size)
    return buffer.value.decode("utf-8")

def bring_window_to_front(window_name):
    """Do I hate this? Yes. Does it work? Also yes. So will I change it? No."""
    hwnd = False
    while not hwnd:
        windows = gw.getAllWindows()
        for window in windows:
            if window_name == get_class_name(window._hWnd):
                
                new_x, new_y = "", "" # empty strings because -1, -1 may bring problems on a secondary display, since that can result in coords -1, -1
                while window.left != new_x or window.top != new_y:
                    
                    hwnd = window._hWnd
                    win32gui.SetForegroundWindow(hwnd)
                    
                    window_width, window_height = window.size
                    screen_width, screen_height = pag.size()
                    
                    while (window_width == screen_width or window_height == screen_height):
                        window_width, window_height = window.size
                        screen_width, screen_height = pag.size()
                        
                    new_x = (screen_width - window_width) // 2
                    new_y = (screen_height - window_height) // 3
                    
                    win32gui.MoveWindow(hwnd, new_x, new_y, window_width, window_height, True)

async def request_verification():
    availability = await UserConsentVerifier.check_availability_async()
    if availability == UserConsentVerifierAvailability.AVAILABLE:
        verifier = UserConsentVerifier.request_verification_async("Please verify your identity.")
        bring_window_to_front("Credential Dialog Xaml Host")
        
        result = await verifier
        
        if result == UserConsentVerificationResult.VERIFIED:
            print("Verification successful!")
        else:
            print("Verification failed.")
    else:
        print("Windows Hello is not available.")

asyncio.run(request_verification())
