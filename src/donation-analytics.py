import csv, re
from collections import defaultdict
import numpy as np

dateformat = re.compile(r'[0-9]{8}\b')
zipformat = re.compile(r'[0-9]{5}\b')
nameformat = re.compile(r'[A-Za-z,\s]+')

def find_repeat_donors(INDIV_Data_Headers):

    donor_dict = defaultdict(list)
    recipient_dict = defaultdict(list)

    inputdata = 'input/itcont.txt'
    with open(inputdata, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')
        for index, line in enumerate(csvreader):
            if not check_record_legal(line, INDIV_Data_Headers):
                print('Line {} in {} is invalid.'.format(index+1, inputdata))
            else:
                CmetId, Name, ZipCode, TransactionDate, TransactionAmount, OtherID = extract_fields(line, INDIV_Data_Headers)
                # Use the combination to identify a unique donor
                DonorId = re.sub(r',?\s+', '_', Name) + '_' + ZipCode

                TransactionYear = TransactionDate[4:]
                donor_dict[DonorId].append(int(TransactionYear))

                # Reference: https://stackoverflow.com/a/39537308/2709595
                target = TransactionYear + '_' + CmetId + '_' + ZipCode
                recipient_dict[target].append(int(TransactionAmount))

    repeat_donor_latest_year = {}

    for DonorId, years in donor_dict.items():
        if len(years) > 1:
            # Save the latest calendar year only
            repeat_donor_latest_year[DonorId] = str(max(years))

    return repeat_donor_latest_year, recipient_dict

def extract_fields(line, INDIV_Data_Headers):

    # Recipient of contribution
    CmetId = line[INDIV_Data_Headers.index('CMTE_ID')]
    # Name of the donor
    Name = line[INDIV_Data_Headers.index('NAME')]
    # Zip code of contributor (use the first five digits/characters)
    ZipCode = line[INDIV_Data_Headers.index('ZIP_CODE')][:5]
    # Date of transaction
    TransactionDate = line[INDIV_Data_Headers.index('TRANSACTION_DT')]
    # Amount of transaction
    TransactionAmount = line[INDIV_Data_Headers.index('TRANSACTION_AMT')]
    # Whether contribution came from a person or an entity
    OtherID = line[INDIV_Data_Headers.index('OTHER_ID')]

    return CmetId, Name, ZipCode, TransactionDate, TransactionAmount, OtherID

def check_record_legal(line, INDIV_Data_Headers):
    
    CmetId, Name, ZipCode, TransactionDate, TransactionAmount, OtherID = extract_fields(line, INDIV_Data_Headers)

    if (OtherID is '') and (TransactionDate is not '') and (dateformat.match(TransactionDate)) and (ZipCode is not '') and (zipformat.match(ZipCode)) and (Name is not '') and (nameformat.match(Name)) and (CmetId is not '') and (TransactionAmount is not ''):
        return True
    else:
        return False

def read_percentile():

    with open('input/percentile.txt') as f:
        percentile = f.readline()
    # 1-100
    if 1 <= float(percentile) <= 100:
        return percentile
    else:
        print('The percentile input is invalid.')
        return None

def calculate_running_percentile(contributions, percentile):

    # Reference: https://stackoverflow.com/a/26071170/2709595
    idx = float(percentile) / 100 * (len(contributions) - 1)
    idx = int(idx + 0.5)
    return round(contributions[np.argpartition(contributions, idx)[idx]])

def main():

    # Source: https://classic.fec.gov/finance/disclosure/metadata/indiv_header_file.csv
    INDIV_Data_Headers = 'CMTE_ID,AMNDT_IND,RPT_TP,TRANSACTION_PGI,IMAGE_NUM,TRANSACTION_TP,ENTITY_TP,NAME,CITY,STATE,ZIP_CODE,EMPLOYER,OCCUPATION,TRANSACTION_DT,TRANSACTION_AMT,OTHER_ID,TRAN_ID,FILE_NUM,MEMO_CD,MEMO_TEXT,SUB_ID'.split(',')

    repeat_donor_latest_year, recipient_dict = find_repeat_donors(INDIV_Data_Headers)
    percentile = read_percentile()

    outputfile = 'output/repeat_donors.txt'
    with open(outputfile, 'w') as output:
        for target, value in recipient_dict.items():
            TransactionYear = target.split('_')[0]
            CmetId = target.split('_')[1]
            ZipCode = target.split('_')[2]
            contributions = []
            TotalAmount = 0
            for index, DonorId in enumerate(list(repeat_donor_latest_year.keys())):
                LatestYear = repeat_donor_latest_year[DonorId]
                if (LatestYear == TransactionYear) and (percentile is not None):
                    TotalAmount += value[index]
                    contributions.append(TotalAmount)
                    nearest_rank_amt = calculate_running_percentile(contributions, percentile)
                    result = '|'.join([CmetId, ZipCode, TransactionYear, str(nearest_rank_amt), str(TotalAmount), str(index+1)])
                    output.write(result)
                    output.write('\n')

if __name__ == '__main__':
    main()