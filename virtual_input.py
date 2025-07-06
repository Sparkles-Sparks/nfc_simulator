import time
import threading
import pyautogui
import pyperclip
from typing import Optional

class VirtualInputDevice:
    def __init__(self):
        self.is_active = False
        self._stop_event = threading.Event()
        self._current_window = None
        
        # Configure pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.01  # Short delay between actions
        
    def start(self):
        """Start the virtual input device"""
        if self.is_active:
            return
            
        self.is_active = True
        self._stop_event.clear()
        
    def stop(self):
        """Stop the virtual input device"""
        if not self.is_active:
            return
            
        self.is_active = False
        self._stop_event.set()
    
    def send_nfc_data(self, data):
        """
        Send NFC data as keyboard input to the active window
        
        Args:
            data: The data to send (will be converted to string)
        """
        if not self.is_active:
            return
            
        try:
            # Convert data to string
            data_str = str(data)
            
            # Save current clipboard content
            saved_clipboard = pyperclip.paste()
            
            try:
                # Copy data to clipboard
                pyperclip.copy(data_str)
                
                # Use Ctrl+V to paste the data (more reliable than typing)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.1)  # Small delay to ensure paste completes
                
                # Press Enter to submit
                pyautogui.press('enter')
                
            finally:
                # Restore clipboard
                pyperclip.copy(saved_clipboard)
                
        except Exception as e:
            # Fallback to typing if clipboard method fails
            try:
                # Type the data directly
                pyautogui.write(data_str, interval=0.01)
                pyautogui.press('enter')
            except Exception as e2:
                print(f"Failed to send data: {e2}")
                raise


# Global instance of the virtual input device
virtual_input = VirtualInputDevice()

def start_virtual_input():
    """Start the virtual input device"""
    virtual_input.start()

def stop_virtual_input():
    """Stop the virtual input device"""
    virtual_input.stop()

def send_nfc_data(data):
    """
    Send NFC data through the virtual input device
    
    Args:
        data: The data to send (will be converted to string)
    """
    virtual_input.send_nfc_data(data)
