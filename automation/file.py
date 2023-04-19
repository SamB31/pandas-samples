import pandas as pd
import os

program_dir = os.path.dirname(os.path.abspath(__file__))

def run_file(file_name):
    
    # find the name of the file
    name = os.path.basename(file_name)
    
    # Split the file name to extract the name without the extension
    name2 = name.rsplit(".", 1)[0]
    
    # Check if the file exists
    exists = os.path.isfile(file_name)
    
    # Redirect print statements to the tkinter text widget
    print(f"Cleaning {name2}\n")    
    
    # If the file does not exist, print an error message and exit the function
    if exists == False:
        print("File not found\n")
        exit
    
    # Create an ExcelFile object from the Excel file
    xls_file = pd.ExcelFile(file_name)

    # Get the names of the two sheets in the XLS file
    sheet_names = xls_file.sheet_names

    # Create a tuple with the quarter names
    quarter = ("Q4", "Q1", "Q2", "Q3")

    # Split the XLS file into two dataframes, one for each sheet
    df1 = pd.read_excel(xls_file, sheet_name=sheet_names[0])
    df2 = pd.read_excel(xls_file, sheet_name=sheet_names[1])

    # Exclude the first row of the first & second sheet
    df2 = df2.iloc[1:]

    # Rename the columns of the first & second sheet
    df1.columns = ['Date', 'Quarter', 'Year', 'Name', 'Gross Wages']
    df2.columns = ['Quarter', 'Payroll', '941_Report', 'Difference']


    # Convert the 'Date' column of the first sheet to datetime format
    df1['Date'] = pd.to_datetime(df1['Date'])
    
    
    count = 0
    # Loop through each quarter
    for q in quarter:
        
        # Append the year to the quarter name
        q_year = q + " 2021"
        if q == "Q4":
            q_year = q + " 2020"
        
        # Calculate the sum of Gross Wages for the given quarter and year range in the first sheet
        payroll_sum = df1[(df1['Quarter'] == q) & (df1['Date'] >= '2020-10-01')]['Gross Wages'].sum()
        formatted_payroll_sum = "${:,}".format(round(payroll_sum, 2))
        
        # Calculate the sum of Payroll for the given quarter and year in the second sheet
        comp_sum = df2[(df2['Quarter'] == q_year)]['Payroll'].sum()
        formatted_comp_sum = "${:,}".format(round(comp_sum, 2))
        
        # Calculate the sum of 941 Report for the given quarter and year in the second sheet
        report = df2[(df2['Quarter'] == q_year)]['941_Report'].sum()
        formatted_report = "${:,}".format(round(report, 2))
        
        # If the sum of Gross Wages does not match the sum of Payroll, print an error message
        if round(payroll_sum, 2) != round(comp_sum, 2):
            print(f"There was a mistake in {q_year} adding the sum please check the file, if file is correct please reach out to app creator\n")
        
        # If the sum of Gross Wages is greater than the sum of 941 Report, adjust the Gross Wages and print a message
        if payroll_sum > report:
            difference = payroll_sum - report
            ratio = 1 - (difference/payroll_sum)
            ratio = round(ratio, 15)
            
                        
            # This line of code multiplies Gross Wages column with the ratio value for given quarter and year
            df1.loc[(df1['Quarter'] == q) & (df1['Date'] >= '2020-10-01'), 'Gross Wages'] *= ratio

            # Saving new adjusted quarter values for formatting
            adjusted_payroll = "${:,}".format(round(df1[(df1['Quarter'] == q) & (df1['Date'] >= '2020-10-01')]['Gross Wages'].sum(), 2))
             

            # This line prints the adjusted sum of Gross Wages for given quarter and year
            print(f"Payroll Comparison Sum for  {q_year}: {formatted_comp_sum} \n")
            print(f"Original Gross Wage Sum for {q_year}: {formatted_payroll_sum} \n")
            print(f"Reported 941 TSSWs          {q_year}: {formatted_report} \n")
            print(f"Adjusted Gross Wage Sum for {q_year}: {adjusted_payroll} \n\n")

            # This condition checks if the rounded sum of Gross Wages is not equal to the report value
            if round(df1[(df1['Quarter'] == q) & (df1['Date'] >= '2020-10-01')]['Gross Wages'].sum(), 2) != round(report, 2):
                print("Weird Error Sum is different from report total.\n")

        else:
            # If the sum is equal to the report value, print this message and continue the loop
            print(f"This {q} does not require altering.\n")
            count +=1
            continue
       

    # If count is less than 4, round Gross Wages column to 2 decimal places and export to csv file
    if count < 4: 
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        full = os.path.join(desktop_path, "CSV")
        # Check if CSV folder exists in the current working directory
        if not os.path.exists(full):
            # Create CSV folder if it does not exist
            os.mkdir(full)
            
        df1['Gross Wages'] = df1['Gross Wages']
        df_subset = df1[['Date', 'Quarter', 'Year', 'Name', 'Gross Wages']]
        name2 = f"{name2}.csv"
        df_subset.to_csv(os.path.join(full, name2), index=False, header=True)
            
        print("File exported successfully.\n\n\n\n")
    else:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        full = os.path.join(desktop_path, "CSV")
        # Check if CSV folder exists in the current working directory
        if not os.path.exists(full):
            # Create CSV folder if it does not exist
            os.mkdir(full)
            
        # If count is greater than or equal to 4, print this message and export to csv file
        print("CSV created no Columns need to be adjusted")
        df1['Gross Wages'] = df1['Gross Wages']
        df_subset = df1[['Date', 'Quarter', 'Year', 'Name', 'Gross Wages']]
        name2 = f"{name2}.csv"
        df_subset.to_csv(os.path.join(full, name2), index=False, header=True)