import pandas as pd

# ✅ Load and normalize CSV once
REFERENCE_PATH = "data/reference_ranges_age_gender.csv"

def load_reference_data():
    df = pd.read_csv(REFERENCE_PATH)

    # Normalize column names (prevents KeyError)
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df


df_ref = load_reference_data()


# ✅ Main interpretation function
def interpret_parameter(parameter_name, value, age, gender):
    """
    parameter_name : str  (e.g. Hemoglobin)
    value          : float
    age            : int
    gender         : str (Male/Female)
    """

    try:
        parameter_name = parameter_name.lower()
        gender = gender.lower()

        # Filter parameter
        df_param = df_ref[df_ref["parameter"].str.lower() == parameter_name]

        if df_param.empty:
            return {
                "status": "unknown",
                "message": "No reference range found"
            }

        # Filter gender if column exists
        if "gender" in df_param.columns:
            df_param = df_param[
                (df_param["gender"].str.lower() == gender) |
                (df_param["gender"].str.lower() == "both")
            ]

        # Filter age if columns exist
        if "age_min" in df_param.columns and "age_max" in df_param.columns:
            df_param = df_param[
                (df_param["age_min"] <= age) &
                (df_param["age_max"] >= age)
            ]

        if df_param.empty:
            return {
                "status": "unknown",
                "message": "No matching age/gender range"
            }

        row = df_param.iloc[0]
        low = row["low"]
        high = row["high"]

        # Determine status
        if value < low:
            status = "low"
        elif value > high:
            status = "high"
        else:
            status = "normal"

        return {
            "status": status,
            "low": low,
            "high": high,
            "value": value
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }