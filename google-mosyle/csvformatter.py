import pandas as pd
import csv

user_df = pd.read_csv("users.csv")

user_df["userid"] = user_df["First Name"] + "." + user_df["Last Name"]
user_df["Name"] = user_df["First Name"] + " " + user_df["Last Name"]

with open("output.csv", mode="w", newline="") as file:
    writer = csv.writer(file)

    # write header row to CSV file
    writer.writerow(["Full Name", "Person ID", "Email","Managed Apple ID", "Location", "Grade Level", "Serial Number"])

    # write data rows to CSV file
    for index, row in user_df.iterrows():
        writer.writerow([row["Name"], row["userid"], row["Email"],"","Madison Ridgeland Academy","Unassigned",""])