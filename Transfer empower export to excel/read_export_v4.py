import os
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

# Set the directory path where the txt files are located
file_path = "C:/Users/vajma/Desktop/Genos Repos/Helpfull-scripts/Transfer empower export to excel"
dir_path= file_path.replace("/", "\\")

# Loop through all files in the directory
for filename in os.listdir(dir_path):
    if filename.endswith(".txt"):
        # Open the txt file and read its content
        with open(os.path.join(dir_path, filename), "r") as f:
            lines = f.readlines()

            # Create a dictionary to store the data for each sample name
            sample_data = {}

            # Extract data from each line and group it by sample name
            for line in lines:
                sample_name, percent_area, area, start_time, height = line.strip().split("\t")

                if percent_area == "%Area":
                    continue

                if sample_name not in sample_data:
                    sample_data[sample_name] = {"percent_areas": [], "areas": []}

                # Convert percent_area to float and append it to the list
                if "," in percent_area:
                    percent_area = percent_area.replace(",", ".")
                try:
                    percent_area_float = float(percent_area)
                except ValueError:
                    continue
                sample_data[sample_name]["percent_areas"].append(percent_area_float)

                # Convert area to integer and append it to the list
                try:
                    area_int = float(area)
                except ValueError:
                    area_int = ""
                sample_data[sample_name]["areas"].append(area_int)

            # Create a list of header labels for the Excel file
            header = ["Sample Name"] + [f"GP{i+1}" for i in range(len(sample_data[sample_name]["percent_areas"]))]
            # Create a list to store the rows for the Excel file
            rows = []

            # Add a row for each sample name
            for sample_name, data in sample_data.items():
                if sample_name == "SampleName":
                    continue

                percent_areas = [str(round(float(val), 5)) for val in data["percent_areas"]]
                areas = [str(val) if val != "" else "" for val in data["areas"]]

                # Check if the percent_areas list is not empty before adding the row
                if percent_areas:
                    row = [sample_name] + percent_areas
                    rows.append(row)
                    row = [sample_name] + areas
                    rows.append(row)

            # Sort the rows by the first column (sample name)
            rows = sorted(rows, key=lambda row: row[0])

            # Write the data to an Excel file with the same name as the txt file
            excel_filename = os.path.splitext(filename)[0] + ".xlsx"
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Data"
            sheet.append(header)
           # Write the data to the sheet
            for row in rows:
                sheet.append(row)

            workbook.save(os.path.join(dir_path, excel_filename))