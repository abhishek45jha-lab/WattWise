"""Headless Streamlit smoke test using the built-in synthetic demonstration.

Run with: python validate_app.py
This verifies script execution, not visual appearance in every web browser.
"""

from pathlib import Path

from streamlit.testing.v1 import AppTest


def main():
    app_path = Path(__file__).resolve().with_name("app.py")
    app = AppTest.from_file(str(app_path), default_timeout=60)
    app.run()

    if app.exception:
        messages = "\n".join(str(item.value) for item in app.exception)
        raise AssertionError("Streamlit raised an exception:\n" + messages)
    if not app.title or "WattWise" not in app.title[0].value:
        raise AssertionError("WattWise title was not rendered")
    if len(app.tabs) != 5:
        raise AssertionError(f"Expected 5 tabs, found {len(app.tabs)}")
    if len(app.metric) < 10:
        raise AssertionError("Expected overview, IQR, and savings metrics were not rendered")
    if not app.dataframe:
        raise AssertionError("Expected data tables were not rendered")

    print("Streamlit smoke test passed.")
    print(f"Rendered {len(app.tabs)} tabs, {len(app.metric)} metrics, and {len(app.dataframe)} data tables.")
    print("This is a headless execution check; it is not a claim of browser screenshot validation.")


if __name__ == "__main__":
    main()
