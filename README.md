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


##Open Source 4 Life! 
###Spark Spark Spark ^^

# GERMAN VERSION

# NFC Simulator für Windows

Eine leichte Windows-Anwendung zum Simulieren von NFC-Tag-Lese- und Schreibvorgängen. Dieses Tool ist perfekt zum Testen der NFC-Funktionalität ohne physische Hardware.

## Funktionen

- Erstellen und Verwalten von virtuellen NFC-Tags
- Simulieren von Lesevorgängen
- Simulieren von Schreibvorgängen
- Speichern und Laden von Tags zwischen Sitzungen
- Einfache und intuitive Benutzeroberfläche
- Keine externen Abhängigkeiten außer Pythons Standardbibliothek

## Installation

1. Stellen Sie sicher, dass Python 3.6 oder höher installiert ist
2. Es werden keine zusätzlichen Pakete benötigt - verwendet nur Standardbibliotheksmodule

## Installation

1. Klonen Sie dieses Repository:

   ```bash
   git clone https://github.com/yourusername/nfc-simulator.git
   cd nfc-simulator
   ```

2. Installieren Sie die erforderlichen Pakete:

   ```bash
   pip install -r requirements.txt
   ```

## Verwendung

1. Starten Sie die Anwendung:

   ```bash
   python nfc_simulator.py
   ```

2. **Neues Tag erstellen**:
   - Klicken Sie auf die Schaltfläche "New Tag", um ein neues virtuelles NFC-Tag zu erstellen
   - Eine eindeutige ID wird automatisch generiert

3. **Lesevorgänge simulieren**:
   - Wählen Sie ein Tag aus der linken Liste aus
   - Klicken Sie auf "Simulate Read", um das Lesen des Tags zu simulieren
   - Die Daten des Tags werden im Editor angezeigt
   - Optional können Sie die Tag-Daten mit virtuellen Eingaben an das aktive Fenster senden

4. **Schreibvorgänge simulieren**:
   - Wählen Sie ein Tag aus der Liste aus
   - Ändern Sie die JSON-Daten im Editor
   - Klicken Sie auf "Simulate Write", um die Änderungen am Tag zu speichern

5. **Tags löschen**:
   - Wählen Sie ein Tag aus der Liste aus
   - Klicken Sie auf "Delete Tag", um es zu entfernen

6. **Serielle Kommunikation**:
   - Wählen Sie einen verfügbaren COM-Port aus

## Tag-Datenformat

Tags speichern Daten im JSON-Format. Die Standardstruktur enthält:

```json
{
  "id": "eindeutige-tag-id",
  "created_at": "zeitstempel",
  "last_modified": "zeitstempel",
  "data": {
    "type": "virtual_nfc_tag",
    "version": "1.0",
    "content": "Ihre benutzerdefinierten Daten hier"
  }
}
```

## Anforderungen

- Python 3.6 oder höher (nur Standardbibliothek)
- Windows-Betriebssystem (für beste Kompatibilität)
- Erforderliche Python-Pakete (siehe `requirements.txt`):
  - pyserial
  - pyautogui
  - keyboard

## Datenspeicherung

Alle Tags werden automatisch in der Datei `nfc_tags.json` im Anwendungsverzeichnis gespeichert. Diese Datei wird automatisch erstellt, wenn Sie Ihr erstes Tag anlegen.

## Fehlerbehebung

### Keine COM-Ports verfügbar

1. Stellen Sie sicher, dass die virtuellen COM-Port-Treiber installiert sind (z.B. com0com)
2. Überprüfen Sie den Geräte-Manager auf Hardwarekonflikte
3. Versuchen Sie, USB-Geräte aus- und wieder anzuschließen

### Virtuelle Eingabe funktioniert nicht

1. Führen Sie die Anwendung als Administrator aus
2. Überprüfen Sie, ob eine andere Anwendung die Eingabe blockiert
3. Versuchen Sie es mit der Zwischenablagenmethode anstelle der direkten Eingabe

## Lizenz

Dieses Projekt ist Open Source und steht unter der MIT-Lizenz.


##Open Source 4 Life! 
###Spark Spark Spark ^^
