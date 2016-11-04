import os
import pandas as pd

REPORTS_DIR = 'data/moh_reports/Full text online/'


def get_file_names():
    '''Retrieve file names'''
    fileNames = [f for f in os.listdir(REPORTS_DIR) if f.endswith('txt')]
    return fileNames


def get_text_matches_from_two_lists(
    list_01=['woman', 'women'],
    list_02=['laundry', 'laundries'],
    reports_dir=REPORTS_DIR,
    tokens_buffer=50,
    outfile = 'data/output_from_search/search_termsFromTwoLists_woman_and_laundry_50WordsBuffer.csv'
    ):

    # Get the file names of all MOH reports
    file_list = get_file_names()

    all_text_extracts = []
    all_reports_filenames = []
    all_boroughs = []
    all_years = []
    all_b_numbers = []

    # Loop over the reports
    for report in file_list:
        with open(REPORTS_DIR + report) as f:

            # Get report attributes
            report_string_split = report.split('.')
            borough = report_string_split[0]
            year = report_string_split[1]
            b_number = report_string_split[2]

            for line in f:

                # Split text in word tokens
                tokens = line.split()

                # Transform to lowercase
                tokens = [s.lower() for s in tokens]

                for search_term in list_01:
                    for search_term_2 in list_02:
                        if search_term in tokens and search_term_2 in tokens:



                            # Get index of search terms 1 and 2
                            index_of_search_term = tokens.index(search_term)
                            index_of_search_term_2 = tokens.index(search_term_2)

                            # Check if the two terms are within a certain number of words
                            if abs(index_of_search_term - index_of_search_term_2) < 50:

                                print 'Match found!'

                                # Get buffer
                                idx_start_ref_text = index_of_search_term - tokens_buffer
                                idx_end_ref_text = index_of_search_term + tokens_buffer
                                if idx_start_ref_text < tokens_buffer:
                                    idx_start_ref_text = 0
                                if idx_end_ref_text > len(tokens):
                                    idx_end_ref_text = len(tokens)

                                # Slice the text
                                text_extract = ' '.join(tokens[idx_start_ref_text:idx_end_ref_text])

                                # Append to the lists
                                all_text_extracts.append(text_extract)
                                all_reports_filenames.append(report)
                                all_boroughs.append(borough)
                                all_years.append(year)
                                all_b_numbers.append(b_number)

    list_of_list_1 = ','.join(list_01)
    list_of_list_2 = ','.join(list_02)

    search_criteria = 'terms from two lists search'

    # Create a dataframe
    df = pd.DataFrame({
        'source_fileName': all_reports_filenames,
        'time_year': all_years,
        'location_fromMOH': all_boroughs,
        'source_bNumber': all_b_numbers,
        'contextText': all_text_extracts,
        'searchCriteria_type': search_criteria,
        'searchCriteria_list1': list_of_list_1,
        'searchCriteria_list2': list_of_list_2
        })

    # Sort the dataframe
    df = df.sort('time_year')

    # Create a csv
    df.to_csv(outfile, index=None)




def main():
    startTime = pd.datetime.now()
    get_text_matches_from_two_lists(
        list_01=['woman', 'women'],
        list_02=['laundry', 'laundries'],
        reports_dir=REPORTS_DIR,
        tokens_buffer=50,
        outfile = 'data/output_from_search/search_termsFromTwoLists_woman_and_laundry_50WordsBuffer.csv'
        )
    print '\nCompleted in ' + str(pd.datetime.now() - startTime)


if __name__ == '__main__':
    main()
