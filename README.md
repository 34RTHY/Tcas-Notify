# TCAS Notify

TCAS Notify is a Python application designed to notify you when your TCAS result page changes. The application compares the baseline HTML with the current HTML fetched from the TCAS profile page. When a change is detected, it prints out the differences and plays a loud alarm to alert you.

## Features

- **Automated Login**: Logs into the TCAS website using provided credentials.
- **HTML Comparison**: Compares the baseline HTML with the current HTML.
- **Alert System**: Plays an alarm when a change is detected.
- **Scheduled Checks**: Periodically checks for changes and notifies you.

## Prerequisites

- Python 3.11
- Google Chrome
- ChromeDriver
- Required Python packages

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/Tcas-Notify.git
    cd Tcas-Notify
    ```

2. **Install Required Packages**:
    ```bash
    pip install selenium beautifulsoup4 playsound
    ```

3. **Download ChromeDriver**:
    - Download the ChromeDriver from and place it in the `chromedriver-win64` directory or use the preexisted one in the directory.

4. **Setup Credentials**:
    - Create a `credentials.json` file in the `Credentials` directory with the following structure:
      ```json
      {
          "user_id": "YOUR-ID",
          "password": "YOUR-PASSWORD"
      }
      ```

## Usage

### Step 1: Create Baseline HTML

Run the script to create a baseline HTML file that will be used for comparison and the fetched html will be in Generatedcontent folder :

```bash
python create_baseline.py
```
### Step 2: Monitor Changes

Run the script to start monitoring the TCAS profile page for changes :

```bash
python python detect_changes.py
```
or
```bash
run start.bat
```

## File Structure
- create_baseline.py: Fetches and saves the baseline HTML for future comparisons.
- detect_changes.py: Monitors the TCAS profile page, compares it with the baseline, and alerts you if there are changes.
- credentials.json: Stores the login credentials required to access the TCAS profile page.
- alarm.mp3: The alarm sound played when a change is detected.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

