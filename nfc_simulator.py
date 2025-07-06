import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, BooleanVar, StringVar
import json
import os
import uuid
import threading
import time
from datetime import datetime

# Import the virtual input module
try:
    from virtual_input import start_virtual_input, stop_virtual_input, send_nfc_data, virtual_input
    VIRTUAL_INPUT_AVAILABLE = True
except ImportError as e:
    print(f"Virtual input not available: {e}")
    VIRTUAL_INPUT_AVAILABLE = True  # pyautogui should be available

# Import the virtual COM port module
try:
    from virtual_com_port import (
        start_virtual_port, 
        stop_virtual_port, 
        send_serial_data,
        list_serial_ports,
        set_serial_callback
    )
    SERIAL_AVAILABLE = True
except ImportError as e:
    print(f"Serial port functionality not available: {e}")
    SERIAL_AVAILABLE = False

class NFCSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("NFC Simulator")
        self.root.geometry("800x600")
        
        # Initialize tag database
        self.tags = {}
        self.current_tag = None
        self.simulate_reading = False
        
        # Virtual input state
        self.virtual_input_enabled = BooleanVar(value=False)
        self.virtual_input_thread = None
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Create tabs
        self.tab_tags = ttk.Frame(self.notebook)
        self.tab_simulator = ttk.Frame(self.notebook)
        self.tab_serial = ttk.Frame(self.notebook)  # New tab for serial settings
        
        self.notebook.add(self.tab_tags, text='Tag Management')
        self.notebook.add(self.tab_simulator, text='NFC Simulator')
        self.notebook.add(self.tab_serial, text='Serial Port')  # Add serial tab
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frames
        self.setup_ui()
        
        # Load existing tags if available
        self.load_tags()
        
        # Initialize serial port tab if available
        if SERIAL_AVAILABLE:
            self.setup_serial_tab()
    
    def setup_ui(self):
        # Left panel - Tag management
        self.left_panel = ttk.LabelFrame(self.tab_tags, text="NFC Tag Manager", padding="10")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.left_panel.grid_columnconfigure(0, weight=1)
        
        # Right panel - Tag simulation
        self.right_panel = ttk.LabelFrame(self.tab_simulator, text="NFC Tag Simulator", padding="10")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        
        # Left panel widgets
        self.tag_listbox = tk.Listbox(self.left_panel, height=15, width=30)
        self.tag_listbox.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        self.tag_listbox.bind('<<ListboxSelect>>', self.on_tag_select)
        
        # Scrollbar for tag list
        scrollbar = ttk.Scrollbar(self.left_panel, orient="vertical", command=self.tag_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tag_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Tag controls
        ttk.Button(self.left_panel, text="New Tag", command=self.create_new_tag).grid(row=1, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Delete Tag", command=self.delete_tag).grid(row=2, column=0, sticky="ew", pady=2)
        
        # Tag data editor
        self.tag_data_label = ttk.Label(self.right_panel, text="Tag Data (JSON):")
        self.tag_data_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.tag_data_text = scrolledtext.ScrolledText(self.right_panel, height=15, width=50)
        self.tag_data_text.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        # Simulation controls
        button_frame = ttk.Frame(self.right_panel)
        button_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Button(button_frame, text="Simulate Read", command=self.simulate_read).grid(row=0, column=0, padx=5, sticky='e')
        ttk.Button(button_frame, text="Simulate Write", command=self.simulate_write).grid(row=0, column=1, padx=5, sticky='e')
        
        # Virtual input controls
        if VIRTUAL_INPUT_AVAILABLE:
            self.virtual_input_frame = ttk.LabelFrame(self.tab_simulator, text="Virtual Input Device", padding=5)
            self.virtual_input_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
            
            # Left side: Virtual Input (keyboard)
            input_left = ttk.Frame(self.virtual_input_frame)
            input_left.grid(row=0, column=0, sticky='nsew')
            
            self.virtual_input_enabled = BooleanVar(value=False)
            self.virtual_input_check = ttk.Checkbutton(
                input_left, 
                text="Enable Virtual Input",
                variable=self.virtual_input_enabled,
                command=self.toggle_virtual_input
            )
            self.virtual_input_check.grid(row=0, column=0, sticky='w')
            
            self.virtual_input_status = ttk.Label(
                input_left, 
                text="Virtual Input: OFF", 
                foreground='red'
            )
            self.virtual_input_status.grid(row=1, column=0, sticky='w')
            
            # Right side: Buttons
            input_right = ttk.Frame(self.virtual_input_frame)
            input_right.grid(row=0, column=1, sticky='ne', padx=5)
            
            self.btn_send_data = ttk.Button(
                input_right,
                text="Send Tag Data",
                command=self.send_current_tag_data,
                width=15
            )
            self.btn_send_data.grid(row=0, column=0, pady=2, sticky='e')
            
            self.btn_simulate_read = ttk.Button(
                input_right,
                text="Simulate Read",
                command=self.simulate_read,
                width=15
            )
            self.btn_simulate_read.grid(row=1, column=0, pady=2, sticky='e')
            
            # Configure grid weights
            self.virtual_input_frame.grid_columnconfigure(0, weight=1)
            self.virtual_input_frame.grid_columnconfigure(1, weight=0)
            
            # Update button state based on virtual input status
            self.virtual_input_enabled.trace('w', self._update_virtual_input_controls)
            
            # Status indicator for virtual input
            # Start with virtual input disabled
            self.virtual_input_enabled.set(False)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken', anchor='w')
        status_bar.grid(row=1, column=0, sticky='ew')
        
    def setup_serial_tab(self):
        """Set up the serial port configuration tab"""
        # Port selection
        port_frame = ttk.LabelFrame(self.tab_serial, text="Serial Port Settings", padding=5)
        port_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        port_frame.grid_columnconfigure(1, weight=1)
        
        # Port selection
        ttk.Label(port_frame, text="Port:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.port_var = StringVar()
        self.port_combobox = ttk.Combobox(port_frame, textvariable=self.port_var, width=15)
        self.port_combobox.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        # Refresh button
        ttk.Button(
            port_frame, 
            text="Refresh Ports", 
            command=self.refresh_serial_ports,
            width=15
        ).grid(row=0, column=2, padx=5, pady=2)
        
        # Baud rate
        ttk.Label(port_frame, text="Baud Rate:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.baud_var = StringVar(value="115200")
        ttk.Combobox(
            port_frame, 
            textvariable=self.baud_var, 
            values=["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"],
            width=15,
            state='readonly'
        ).grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        # Connection controls
        self.btn_connect = ttk.Button(
            port_frame,
            text="Connect",
            command=self.toggle_serial_connection,
            width=15
        )
        self.btn_connect.grid(row=1, column=2, padx=5, pady=2)
        
        # Status
        self.serial_status_var = StringVar(value="Not Connected")
        self.serial_status_label = ttk.Label(
            port_frame, 
            textvariable=self.serial_status_var,
            foreground='red'
        )
        self.serial_status_label.grid(row=2, column=0, columnspan=3, sticky='w', padx=5, pady=5)
        
        # Send test button and auto-send option
        button_frame = ttk.Frame(self.tab_serial)
        button_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(
            button_frame,
            text="Send Test Data",
            command=self.send_serial_test,
            width=20
        ).grid(row=0, column=0, padx=5)
        
        # Auto-send on read
        self.auto_send_var = BooleanVar(value=False)
        ttk.Checkbutton(
            button_frame,
            text="Auto-send on Read",
            variable=self.auto_send_var
        ).grid(row=0, column=1, padx=5)
        
        # Configure tab grid weights
        self.tab_serial.grid_rowconfigure(0, weight=0)
        self.tab_serial.grid_rowconfigure(1, weight=1)
        self.tab_serial.grid_columnconfigure(0, weight=1)
        
        # Initial refresh of ports
        self.refresh_serial_ports()
    
    def on_tag_select(self, event):
        """Handle tag selection from the list"""
        selection = self.tag_listbox.curselection()
        if selection:
            self.current_tag = list(self.tags.keys())[selection[0]]
            self.update_tag_editor()
    
    def create_new_tag(self):
        """Create a new virtual NFC tag"""
        tag_id = str(uuid.uuid4())
        tag_data = {
            "id": tag_id,
            "created_at": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "data": {
                "type": "virtual_nfc_tag",
                "version": "1.0",
                "content": "Sample NFC Tag Data"
            }
        }
        self.tags[tag_id] = tag_data
        self.current_tag = tag_id
        self.update_tag_list()
        self.update_tag_editor()
        self.save_tags()
        self.status_var.set(f"Created new tag: {tag_id[:8]}...")
        # Select the new tag in the list
        self.tag_listbox.selection_clear(0, tk.END)
        self.tag_listbox.selection_set(len(self.tags) - 1)
        self.tag_listbox.see(len(self.tags) - 1)
    
    def delete_tag(self):
        """Delete the currently selected tag"""
        if not self.current_tag:
            messagebox.showwarning("No Tag Selected", "Please select a tag to delete.")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this tag?"):
            del self.tags[self.current_tag]
            self.current_tag = next(iter(self.tags.keys()), None) if self.tags else None
            self.save_tags()
            self.update_tag_list()
            self.update_tag_editor()
            self.status_var.set("Tag deleted")
    
    def update_tag_list(self):
        """Update the tag list display"""
        current_selection = self.tag_listbox.curselection()
        current_selected = current_selection[0] if current_selection else None
        
        self.tag_listbox.delete(0, tk.END)
        for tag_id in self.tags:
            tag = self.tags[tag_id]
            display_text = f"{tag_id[:8]}... - {tag['last_modified'][:19]}"
            self.tag_listbox.insert(tk.END, display_text)
        
        # Restore selection if possible
        if current_selected is not None and current_selected < len(self.tags):
            self.tag_listbox.selection_set(current_selected)
        elif self.tags:
            self.tag_listbox.selection_set(0)
            self.current_tag = list(self.tags.keys())[0]
            self.update_tag_editor()
    
    def update_tag_editor(self):
        """Update the tag editor with the current tag's data"""
        self.tag_data_text.delete("1.0", tk.END)
        if self.current_tag and self.current_tag in self.tags:
            tag_data = self.tags[self.current_tag]
            self.tag_data_text.insert(tk.END, json.dumps(tag_data, indent=2))
    
    def toggle_virtual_input(self):
        """Toggle the virtual input device on/off"""
        if self.virtual_input_enabled.get():
            try:
                start_virtual_input()
                self.virtual_input_status.config(text="Virtual Input: ON", foreground="green")
                self.status_var.set("Virtual input device enabled - Focus on target window")
                
                # Show a countdown before sending data
                for i in range(5, 0, -1):
                    self.virtual_input_status.config(text=f"Sending in {i}... (focus target)")
                    self.root.update()
                    time.sleep(1)
                    
                self.virtual_input_status.config(text="Virtual Input: READY", foreground="blue")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start virtual input: {e}")
                self.virtual_input_enabled.set(False)
                self.virtual_input_status.config(text="Virtual Input: ERROR", foreground="red")
        else:
            stop_virtual_input()
            self.virtual_input_status.config(text="Virtual Input: OFF", foreground="red")
            self.status_var.set("Virtual input device disabled")
    
    def _update_virtual_input_controls(self, *args):
        """Update the state of virtual input controls"""
        if not VIRTUAL_INPUT_AVAILABLE:
            return
            
        state = "normal" if self.virtual_input_enabled.get() else "disabled"
        for widget in [child for child in self.right_panel.winfo_children() 
                      if isinstance(child, (ttk.Button, ttk.Checkbutton))]:
            if widget.winfo_name() != '!checkbutton':  # Don't disable the toggle button
                widget.configure(state=state)
    
    def send_current_tag_data(self):
        """Send the current tag's data through the virtual input device"""
        if not self.current_tag or self.current_tag not in self.tags:
            messagebox.showinfo("No Tag Selected", "Select or create a tag first.")
            return
            
        if not self.virtual_input_enabled.get():
            messagebox.showinfo("Virtual Input Disabled", "Enable virtual input first.")
            return
            
        try:
            # Get the tag data
            tag_data = self.tags[self.current_tag]
            
            # Show a countdown before sending
            self.status_var.set("Preparing to send data in 3 seconds...")
            self.root.update()
            time.sleep(1)
            
            self.status_var.set("Preparing to send data in 2 seconds...")
            self.root.update()
            time.sleep(1)
            
            self.status_var.set("Preparing to send data in 1 second...")
            self.root.update()
            time.sleep(1)
            
            # Convert the tag data to a string representation
            data_str = json.dumps(tag_data, indent=2)
            
            # Send the data through the virtual input device
            self.status_var.set("Sending data...")
            self.root.update()
            
            send_nfc_data(data_str)
            
            self.status_var.set(f"Sent tag data: {self.current_tag[:8]}...")
            
            # Flash the status to show completion
            for _ in range(2):
                self.virtual_input_status.config(foreground="green")
                self.root.update()
                time.sleep(0.2)
                self.virtual_input_status.config(foreground="blue")
                self.root.update()
                time.sleep(0.2)
            
        except Exception as e:
            self.virtual_input_status.config(text="Virtual Input: ERROR", foreground="red")
            messagebox.showerror("Error", f"Failed to send tag data: {e}")
        finally:
            if self.virtual_input_enabled.get():
                self.virtual_input_status.config(text="Virtual Input: READY", foreground="blue")
    
    def simulate_read(self):
        """Simulate reading an NFC tag"""
        if not self.tags:
            messagebox.showinfo("No Tags", "Create a tag first to simulate reading.")
            return
            
        self.simulate_reading = True
        self.status_var.set("Simulating NFC read operation...")
        
        # If virtual input is enabled, send the current tag data
        if VIRTUAL_INPUT_AVAILABLE and self.virtual_input_enabled.get() and self.current_tag:
            self.root.after(500, self.send_current_tag_data)
        
        self.root.after(1000, self.complete_read_simulation)
    
    def complete_read_simulation(self):
        """Complete the read simulation"""
        self.simulate_reading = False
        if not self.current_tag and self.tags:
            self.current_tag = next(iter(self.tags.keys()))
            # Update the selection in the listbox
            self.tag_listbox.selection_clear(0, tk.END)
            self.tag_listbox.selection_set(0)
        
        if self.current_tag:
            self.status_var.set(f"Read tag: {self.current_tag[:8]}...")
            self.update_tag_editor()
    
    def simulate_write(self):
        """Simulate writing to an NFC tag"""
        if not self.current_tag:
            messagebox.showinfo("No Tag Selected", "Select or create a tag to write to.")
            return
            
        try:
            new_data = json.loads(self.tag_data_text.get("1.0", "end-1c"))
            self.tags[self.current_tag] = new_data
            self.tags[self.current_tag]["last_modified"] = datetime.now().isoformat()
            self.save_tags()
            self.status_var.set(f"Successfully wrote to tag: {self.current_tag[:8]}...")
        except json.JSONDecodeError:
            messagebox.showerror("Invalid JSON", "The tag data contains invalid JSON.")
    
    def save_tags(self):
        """Save tags to a file"""
        try:
            with open("nfc_tags.json", "w") as f:
                json.dump({"tags": self.tags}, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tags: {str(e)}")
            raise
    
    def load_tags(self):
        """Load tags from file"""
        try:
            if os.path.exists("nfc_tags.json"):
                with open("nfc_tags.json", "r") as f:
                    data = json.load(f)
                    self.tags = data.get("tags", {})
                    if self.tags:
                        self.current_tag = next(iter(self.tags.keys()))
                        self.update_tag_editor()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tags: {str(e)}")
        
        self.update_tag_list()
        
    def refresh_serial_ports(self):
        """Refresh the list of available serial ports"""
        if not SERIAL_AVAILABLE:
            return
            
        try:
            # Get list of ports as (port, description, hwid) tuples
            port_info = list_serial_ports()
            
            # Extract just the port names and create display strings
            named_ports = []
            port_map = {}  # Maps display name to actual port name
            
            for port, desc, hwid in port_info:
                display_name = f"{port} - {desc}"
                named_ports.append(display_name)
                port_map[display_name] = port
            
            # Store the port map for later use
            self.port_map = port_map
            
            # Update the combobox
            self.port_combobox['values'] = named_ports
            if named_ports:
                self.port_combobox.set(named_ports[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list serial ports: {e}")
            self.serial_status_var.set("Error listing ports")
    
    def toggle_serial_connection(self):
        """Toggle serial port connection"""
        if not SERIAL_AVAILABLE:
            messagebox.showerror("Error", "Serial port functionality not available")
            return
            
        if self.btn_connect['text'] == "Connect":
            # Try to connect
            display_name = self.port_var.get()
            # Get the actual port name from our map
            port = self.port_map.get(display_name, display_name.split(' ')[0])
            baud = int(self.baud_var.get())
            
            try:
                start_virtual_port(port, baud)
                self.btn_connect.config(text="Disconnect")
                self.serial_status_var.set(f"Connected to {port}")
                self.serial_status_label.config(foreground='green')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to connect: {e}")
                self.serial_status_var.set("Connection failed")
                self.serial_status_label.config(foreground='red')
        else:
            # Disconnect
            try:
                stop_virtual_port()
                self.btn_connect.config(text="Connect")
                self.serial_status_label.config(text="Disconnected", foreground='red')
                self.serial_status_var.set("Disconnected")
            except Exception as e:
                messagebox.showerror("Error", f"Error disconnecting: {e}")
                self.serial_status_label.config(text="Error disconnecting", foreground='red')
                self.serial_status_var.set("Error disconnecting")
    
    def send_serial_test(self):
        """Send test data through the serial port"""
        if not SERIAL_AVAILABLE or self.btn_connect['text'] != "Disconnect":
            messagebox.showinfo("Not Connected", "Please connect to a serial port first")
            return
            
        try:
            test_data = "NFC Simulator Test\r\n"
            send_serial_data(test_data)
            self.serial_status_var.set("Test data sent")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send test data: {e}")
            self.serial_status_var.set("Send failed")
            self.serial_status_label.config(foreground='red')

def on_closing(root, app):
    """Handle application closing"""
    try:
        if hasattr(app, 'virtual_input_enabled') and app.virtual_input_enabled.get():
            stop_virtual_input()
    except Exception as e:
        print(f"Error during cleanup: {e}")
    root.destroy()

def main():
    root = tk.Tk()
    try:
        # Set window icon if available
        try:
            root.iconbitmap(default='nfc_icon.ico')
        except:
            pass  # Icon not found, use default
            
        app = NFCSimulator(root)
        
        # Set up window close handler
        root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, app))
        
        # Center the window
        window_width = 800
        window_height = 650  # Increased height to accommodate new controls
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Set minimum window size
        root.minsize(650, 500)
        
        # Check if virtual input is available
        if not VIRTUAL_INPUT_AVAILABLE:
            messagebox.showwarning(
                "Virtual Input Not Available",
                "The virtual input feature is not available on this system. "
                "Some functionality may be limited."
            )
        
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}\nPlease check if the tags file is not corrupted.")
        raise

if __name__ == "__main__":
    main()
