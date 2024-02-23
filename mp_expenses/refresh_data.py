import get_data.datascrape as scrape
import get_data.scrapeexp as scrape_exp
import os
import pandas as pd
### order of data refresh 


#gd.datascrape

def check_csv_file(file_path):
    if os.path.isfile(file_path) and file_path.endswith('.csv'):
        print(f"The CSV file '{file_path}' exists. we'll move on to checking other stuff")
        return True
    else:
        print(f"The CSV file '{file_path}' does not exist.... So lets make one!!!")
        return False

# Replace 'your_folder' and 'your_file.csv' with the actual folder and file name you want to check
folder_path = 'datasets/'
file_name = 'weblinks.csv'
file_path = os.path.join(folder_path, file_name)

if check_csv_file(file_path) == True:
   scrape.main()
   

##gd.scrapeexp

    
# create all individual csv for ever mp 
expense = 'row align-items-center text-center pt-1 pb-1'
    
lastrow =  'row border-bottom align-items-center text-center pt-1 pb-1'

scrape_exp.create_csv(expense, lastrow)

#create a combined data set.
data_path = 'datasets/mp_exp_csv'

files = os.listdir(data_path)

#combine all files in the list
combined_expenses = pd.concat([pd.read_csv(f'datasets/mp_exp_csv/{fi}') for fi in files ])
#export to csv
combined_expenses.to_csv( 'datasets/combined_expenses.csv', index=False)

##gd.combinedata



