from __future__ import division
import pandas as pd
import os


REPORTS_DIR = 'data/moh_reports/Full text online/'


def get_file_names():
    '''Retrieve file names'''
    fileNames = [f for f in os.listdir(REPORTS_DIR) if f.endswith('txt')]
    return fileNames


def single_term_search(
    reports_dir=REPORTS_DIR,
    term_to_search='spinster',
    word_buffer=50,
    outfile='data/output_from_search/search_singleTerm_spinster_50WordsBuffer.csv'):

    file_list = get_file_names()

    all_text_extracts = []
    all_reports_filenames = []
    all_boroughs = []
    all_years = []
    all_b_numbers = []
    for report in file_list[:]:

        with open(REPORTS_DIR + report) as f:
            # Get report attributes
            report_string_split = report.split('.')
            borough = report_string_split[0]
            year = report_string_split[1]
            b_number = report_string_split[2]

            for line in f:
                line = line.decode("utf8")

                # Split text in word tokens
                tokens = line.split()

                # Transform to lowercase
                tokens = [s.lower() for s in tokens]


                if term_to_search in tokens:
                    index_of_search_term = tokens.index(term_to_search)
                    print 'Match found!'

                    # Get buffer
                    idx_start_ref_text = index_of_search_term - word_buffer
                    idx_end_ref_text = index_of_search_term + word_buffer
                    if idx_start_ref_text < word_buffer:
                        idx_start_ref_text = 0
                    if idx_end_ref_text > len(tokens):
                        idx_end_ref_text = len(tokens)

                    # Slice the text
                    text_extract = ' '.join(tokens[idx_start_ref_text:idx_end_ref_text])

                    # Append to the lists
                    all_text_extracts.append(text_extract.encode("utf8"))
                    all_reports_filenames.append(report)
                    all_boroughs.append(borough)
                    all_years.append(year)
                    all_b_numbers.append(b_number)

    search_criteria = 'single term search'
    single_term = term_to_search

    # Create a dataframe
    df = pd.DataFrame({
        'source_fileName': all_reports_filenames,
        'time_year': all_years,
        'location_fromMOH': all_boroughs,
        'source_bNumber': all_b_numbers,
        'contextText': all_text_extracts,
        'searchCriteria_type': search_criteria,
        'searchCriteria_list1': single_term
    })

    # Sort the dataframe
    df = df.sort('time_year')

    # Create a csv
    df.to_csv(outfile, index=None)
    print outfile + ' saved.'

    return df



def main():
    startTime = pd.datetime.now()
    single_term_search(
        reports_dir=REPORTS_DIR,
        term_to_search='wife',
        word_buffer=50,
        outfile='data/output_from_search/search_singleTerm_wife_50WordsBuffer.csv')

    single_term_search(
        reports_dir=REPORTS_DIR,
        term_to_search='wives',
        word_buffer=50,
        outfile='data/output_from_search/search_singleTerm_wives_50WordsBuffer.csv')

    single_term_search(
        reports_dir=REPORTS_DIR,
        term_to_search='spinster',
        word_buffer=50,
        outfile='data/output_from_search/search_singleTerm_spinster_50WordsBuffer.csv')

    print '\nCompleted in ' + str(pd.datetime.now() - startTime)


if __name__ == '__main__':
    main()
