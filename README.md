# NFC Simulator for Windows

A lightweight Windows application to simulate NFC tag reading and writing operations. This tool is perfect for testing NFC functionality without physical hardware.

## Features

- Create and manage virtual NFC tags
- Simulate NFC read operations
- Simulate NFC write operations
- Save and load tags between sessions
- Simple and intuitive user interface
- No external dependencies beyond Python's standard library

## Installation

1. Make sure you have Python 3.6 or higher installed
2. No additional packages needed - uses only standard library modules

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/nfc-simulator.git
   cd nfc-simulator
   ```

2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:

   ```bash
   python nfc_simulator.py
   ```

2. **Creating a New Tag**:
   - Click the "New Tag" button to create a new virtual NFC tag
   - A unique ID will be automatically generated

3. **Simulating Read Operations**:
   - Select a tag from the list on the left
   - Click "Simulate Read" to simulate reading the tag
   - The tag's data will be displayed in the editor
   - Optionally, send the tag data to the active window using virtual input

4. **Simulating Write Operations**:
   - Select a tag from the list
   - Modify the JSON data in the editor
   - Click "Simulate Write" to save changes to the tag

5. **Deleting Tags**:
   - Select a tag from the list
   - Click "Delete Tag" to remove it

6. **Serial Port Communication**:
   - Select an available COM port

## Tag Data Format

Tags store data in JSON format. The default structure includes:

```json
{
  "id": "unique-tag-id",
  "created_at": "timestamp",
  "last_modified": "timestamp",
  "data": {
    "type": "virtual_nfc_tag",
    "version": "1.0",
    "content": "Your custom data here"
  }
}
```
```

## Requirements

- Python 3.6 or higher (standard library only)
- Windows operating system (for best compatibility)
- Required Python packages (see `requirements.txt`):
  - pyserial
  - pyautogui
  - keyboard

## Data Storage

All tags are automatically saved to `nfc_tags.json` in the application directory. This file will be created automatically when you create your first tag.

## Troubleshooting

### No COM Ports Available

1. Ensure virtual COM port drivers are installed (e.g., com0com)
2. Check Device Manager for any hardware conflicts
3. Try unplugging and replugging USB devices

### Virtual Input Not Working

1. Run the application as administrator
2. Check if another application is blocking input
3. Try using the clipboard method instead of direct input

## License

This project is open source and available under the MIT License.
