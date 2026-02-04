REQUIRED_COLUMNS = ["Revenue", "Expenses"]


def validate_dataframe(df):
    """Ensure required columns are present in the DataFrame.

    Returns (is_valid: bool, message: str)
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return False, f"Missing required columns: {', '.join(missing)}"
    return True, "OK"