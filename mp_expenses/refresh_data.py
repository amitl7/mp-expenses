import get_data.datascrape as scrape
import os
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

if check_csv_file(file_path) == False:
   scrape.main()
   


#
##gd.scrapeexp

##gd.combinedata



