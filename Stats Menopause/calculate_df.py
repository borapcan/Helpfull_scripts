import pandas as pd


def process_excel_file(file_name):
    # Read the Excel file and extract the required columns
    df = pd.read_excel(file_name, usecols=["Name", "S", "B", "F", "G2", "G1", "G0"])

    # Create a function to extract the timepoint from the 'Name' column
    def extract_timepoint(name):
        timepoint_str = name[2:4]
        try:
            return int(timepoint_str)
        except ValueError:
            return -1

    # Extract timepoint and person number from the 'Name' column
    df["Timepoint"] = df["Name"].apply(extract_timepoint)
    df["Person"] = (
        df["Name"].str.extract(r"GM\d{2}(\d{2})_", expand=False).fillna(-1).astype(int)
    )

    # Filter out rows where the 'Name' column starts with 'stand' and '_S'
    df = df[~df["Name"].str.startswith("stand")]
    df = df[~df["Name"].str.contains("_S")]

    # Format the 'Person' and 'Timepoint' columns with leading zeros
    df["Person"] = df["Person"].apply(lambda x: f"{x:02d}")
    df["Timepoint"] = df["Timepoint"].apply(lambda x: f"{x:02d}")

    # Create a new DataFrame with 'Person Code', 'Timepoint Code', 'S', 'B', 'F', 'G2', 'G1', and 'G0'
    output_df = df[["Person", "Timepoint", "S", "B", "F", "G2", "G1", "G0"]].copy()
    output_df.columns = [
        "Person",
        "Timepoint",
        "S",
        "B",
        "F",
        "G2",
        "G1",
        "G0",
    ]

    # Sort the table first by person and then by timepoint
    output_df.sort_values(by=["Person", "Timepoint"], inplace=True)

    # Calculate normalized values for all traits by the first timepoint ('01')
    for trait in ["S", "B", "F", "G2", "G1", "G0"]:
        trait_column_name = f"{trait}_Normalized"
        normalized_values_df = pd.DataFrame(
            columns=["Person", "Timepoint", trait_column_name]
        )

        for person in output_df["Person"].unique():
            person_df = output_df[output_df["Person"] == person]
            person_01_trait_df = person_df[person_df["Timepoint"] == "01"][trait]

            # Check if the person_df contains data for the '01' timepoint and trait before proceeding
            if not person_01_trait_df.empty:
                person_01_trait = person_01_trait_df.values[0]

                for timepoint in person_df["Timepoint"]:
                    trait_value = person_df[person_df["Timepoint"] == timepoint][
                        trait
                    ].values[0]
                    normalized_trait = trait_value / person_01_trait
                    normalized_values_df = pd.concat(
                        [
                            normalized_values_df,
                            pd.DataFrame(
                                {
                                    "Person": [person],
                                    "Timepoint": [timepoint],
                                    trait_column_name: [normalized_trait],
                                }
                            ),
                        ]
                    )

        # Merge normalized values back to the original output_df for the current trait
        output_df = pd.merge(
            output_df, normalized_values_df, on=["Person", "Timepoint"]
        )

    return output_df
