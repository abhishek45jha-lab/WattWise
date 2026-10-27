# WattWise Execution Guide — Windows

## 1. Prerequisites

- 64-bit **Python 3.12** recommended (a standard Python 3 installation).
- Visual Studio Code or another Python IDE.
- Internet access only for the initial pip installation. The application itself needs no external API, database, paid service, or cloud account.

Check your installed Python launchers:

```bat
py -0p
```

If Python 3.12 is not listed, install it from python.org and enable the Python Launcher. You may replace `py -3.12` with `py -3` if another supported Python 3 version is installed.

## 2. Open the project

Extract/copy the `WattWise` folder, for example to:

```text
C:\Users\YourName\Documents\WattWise
```

### Command Prompt

```bat
cd /d "C:\Users\YourName\Documents\WattWise"
```

### PowerShell

```powershell
cd "C:\Users\YourName\Documents\WattWise"
```

Confirm that `app.py` and `requirements.txt` are in the current folder:

```bat
dir
```

## 3. Create and activate a virtual environment

### Command Prompt

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
```

### PowerShell

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation only for this session, you can use Command Prompt instead, or run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

The prompt should now begin with `(.venv)`.

## 4. Install dependencies

```bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Check the environment:

```bat
python --version
python -c "import numpy, pandas, matplotlib, streamlit; print('Core imports successful')"
```

## 5. Generate the reproducible synthetic sample

```bat
python data_generator.py
```

Expected console message includes:

```text
Saved 1,440 synthetic rows
```

The default uses seed 42 and 60 days of hourly observations. Optional parameters:

```bat
python data_generator.py --seed 42 --days 60 --output sample_data.csv
```

Do not describe this generated CSV as real measured data.

## 6. Run unit tests

```bat
python -m unittest discover -s tests -v
```

The verified reference run contains **18 tests**. A successful run ends with `OK`. If a test fails on your machine, report the actual failure rather than claiming success.

## 7. Reproduce the analytical outputs

```bat
python validate_project.py
```

This recreates:

- `results/descriptive_statistics.csv`
- `results/data_quality_report.csv`
- `results/daily_consumption.csv`
- `results/weekday_weekend_summary.csv`
- `results/anomaly_report.csv`
- `results/hypothetical_savings_scenarios.csv`
- `results/validation_summary.json`
- five labelled chart images in `presentation_assets/`

For the default synthetic data, the script checks 1,440 generated/valid rows, one-hour regular intervals, and 60 complete days.

## 8. Smoke-test the Streamlit application

```bat
python validate_app.py
```

This uses Streamlit's headless `AppTest` with the built-in synthetic dataset. It verifies application execution and key rendered elements, not pixel-perfect browser layout.

## 9. Launch WattWise

```bat
streamlit run app.py
```

Open the URL shown in the terminal, normally:

```text
http://localhost:8501
```

Use the sidebar to select the synthetic demonstration or upload a CSV. Required columns are `timestamp` and `electricity_kwh`.

Stop the server with `Ctrl+C`. Deactivate the environment afterwards:

```bat
deactivate
```

## 10. Run in Visual Studio Code

1. Extract the project ZIP. In VS Code, select **File → Open Folder** and open the `WattWise` folder that directly contains `app.py`.
2. Install Microsoft's **Python** extension if it is not already installed.
3. Select **Terminal → New Terminal** in VS Code.
4. Create the environment and install the dependencies using the commands in Sections 3–5 above.
5. Press **Ctrl+Shift+P**, choose **Python: Select Interpreter**, and select the interpreter ending in `.venv\Scripts\python.exe`. If it is not listed, choose **Enter interpreter path** and browse to that file.
6. Start the application in either of these ways:

   **Terminal method:**

   ```bat
   python run_wattwise.py
   ```

   **F5 method:** open the **Run and Debug** panel, select **WattWise: Run app**, and press **F5**. The supplied `.vscode/launch.json` also includes configurations for unit tests, sample generation, and result validation.

7. Open `http://localhost:8501`. To use another port:

   ```bat
   python run_wattwise.py --port 8502
   ```

8. Stop the app with **Ctrl+C** in the VS Code terminal. Do not close the terminal while WattWise is running.

The launcher uses the Python interpreter selected in VS Code, so selecting the `.venv` interpreter is essential.

## 11. Uploading your own CSV

Example:

```csv
timestamp,electricity_kwh
2025-04-01 00:00:00,0.410
2025-04-01 01:00:00,0.385
```

Before interpretation, confirm:

1. Values are interval energy in **kWh**, not kW and not a cumulative meter register.
2. One timestamp represents one non-overlapping interval.
3. The timestamp convention and time zone are documented.
4. Missing intervals and duplicate timestamps are understood.
5. Any monetary scenario uses an appropriate user-assumed INR/kWh tariff.

WattWise preserves optional columns but does not require them.

## Troubleshooting

### `py` is not recognized

Reinstall Python with the Python Launcher enabled, or use the full path to `python.exe`.

### `streamlit` is not recognized

Activate `.venv` and reinstall requirements:

```bat
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### Missing required column error

Open the CSV and verify the exact headers `timestamp` and `electricity_kwh`. Surrounding header spaces are stripped; missing columns are not guessed.

### No daily chart appears

The application could not verify regular intervals and complete expected daily counts. Inspect the data-quality report and interval message. This safeguard is intentional.

### No anomalies appear

This can mean no values exceed the upper fence, there are fewer than four valid observations, all valid values are constant, or there is no valid data. Read the displayed method status.

## Verified reference environment

The project was executed in a Linux sandbox on 27 October 2026 with Python 3.13.16. All 18 tests, synthetic-result validation, and the headless Streamlit smoke test passed there. Native Windows execution remains the user's local verification step.
