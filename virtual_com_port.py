import serial
import serial.tools.list_ports
import threading
import queue
import time
from typing import Optional, List, Tuple

class VirtualCOMPort:
    def __init__(self, port: str = None, baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.running = False
        self.data_queue = queue.Queue()
        self.read_thread = None
        self.callback = None
        
    def start(self, port: str = None) -> bool:
        """Start the virtual COM port"""
        if port:
            self.port = port
            
        if not self.port:
            return False
            
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1,
                write_timeout=1
            )
            self.running = True
            self.read_thread = threading.Thread(target=self._read_loop, daemon=True)
            self.read_thread.start()
            return True
        except Exception as e:
            print(f"Failed to open serial port {self.port}: {e}")
            return False
    
    def stop(self):
        """Stop the virtual COM port"""
        self.running = False
        if self.read_thread and self.read_thread.is_alive():
            self.read_thread.join(timeout=1.0)
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
    
    def send_data(self, data: str) -> bool:
        """Send data through the COM port"""
        if not self.serial_connection or not self.serial_connection.is_open:
            return False
            
        try:
            # Add newline to make it easier to read on the receiving end
            if not data.endswith('\n'):
                data += '\n'
                
            self.serial_connection.write(data.encode('utf-8'))
            self.serial_connection.flush()
            return True
        except Exception as e:
            print(f"Failed to send data: {e}")
            return False
    
    def set_callback(self, callback):
        """Set a callback function to be called when data is received"""
        self.callback = callback
    
    def _read_loop(self):
        """Background thread for reading data from the serial port"""
        buffer = ""
        while self.running and self.serial_connection and self.serial_connection.is_open:
            try:
                # Read available data
                if self.serial_connection.in_waiting > 0:
                    data = self.serial_connection.read(self.serial_connection.in_waiting).decode('utf-8', errors='ignore')
                    buffer += data
                    
                    # Process complete lines
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        if self.callback:
                            self.callback(line.strip())
                            
                time.sleep(0.01)  # Small delay to prevent high CPU usage
                
            except Exception as e:
                print(f"Error in read loop: {e}")
                time.sleep(1)  # Wait before retrying
    
    @staticmethod
    def list_available_ports() -> List[Tuple[str, str, str]]:
        """List all available serial ports"""
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append((port.device, port.description, port.hwid))
        return ports
    
    def __del__(self):
        self.stop()

# Global instance
virtual_port = VirtualCOMPort()

def start_virtual_port(port: str = None, baudrate: int = 115200) -> bool:
    """Start the virtual COM port"""
    virtual_port.baudrate = baudrate
    return virtual_port.start(port)

def stop_virtual_port():
    """Stop the virtual COM port"""
    virtual_port.stop()

def send_serial_data(data: str) -> bool:
    """Send data through the virtual COM port"""
    return virtual_port.send_data(data)

def set_serial_callback(callback):
    """Set a callback function for received data"""
    virtual_port.set_callback(callback)

def list_serial_ports() -> List[Tuple[str, str, str]]:
    """List all available serial ports"""
    return VirtualCOMPort.list_available_ports()
