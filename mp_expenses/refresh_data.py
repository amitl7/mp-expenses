import get_data as gd
import os
### order of data refresh 


#gd.datascrape

def check_csv_exists():
    file_path = '/datasets/weblinks.csv'
    return os.path.exists(file_path)
#
gd.scrapeexp

gd.combinedata

def main():
    if not check_csv_exists():
        gd.datascrap.get_mp_info()
    else:
        print('weblinks csv exists moving onto next check')


if __name__ == "__main__":
    main()

