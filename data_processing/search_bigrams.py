from __future__ import division
import pandas as pd
import os

from nltk import bigrams


REPORTS_DIR = 'data/moh_reports/Full text online/'

def get_file_names():
    '''Retrieve file names'''
    fileNames = [f for f in os.listdir(REPORTS_DIR) if f.endswith('txt')]
    return fileNames


def find_bigrams(
    reports_dir=REPORTS_DIR,
    list_of_terms_to_search=[('married', 'women'), ('married', 'woman')],
    outfile='data/output_from_search/bigram_search_marriedWoman.csv',
    bigram_buffer=100):
    """ Find occurencies of a bigram in the reports"""

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

                # Split text in word tokens
                tokens = line.split()

                # Create list of bigrams from the report
                all_bigrams = list(bigrams(tokens))

                sample_tuple = list_of_terms_to_search[0]

                if sample_tuple in all_bigrams:

                    # Get index of search terms 1 and 2
                    index_of_search_bigram = all_bigrams.index(sample_tuple)

                    # Get buffer
                    idx_start_ref_text = index_of_search_bigram - bigram_buffer
                    idx_end_ref_text = index_of_search_bigram + bigram_buffer
                    if idx_start_ref_text < bigram_buffer:
                        idx_start_ref_text = 0
                    if idx_end_ref_text > len(all_bigrams):
                        idx_end_ref_text = len(all_bigrams)

                    # Slice the text
                    text_extract_tuples = all_bigrams[idx_start_ref_text:idx_end_ref_text]

                    all_bigram_buffered_list = []
                    for x in text_extract_tuples:
                        all_bigram_buffered_list.append(x[0])
                    text_extract = ' '.join(all_bigram_buffered_list)

                    print 'Record found!'
                    print '-------------'
                    print text_extract
                    print '-------------'

                    # Append to the lists
                    all_text_extracts.append(text_extract)
                    all_reports_filenames.append(report)
                    all_boroughs.append(borough)
                    all_years.append(year)
                    all_b_numbers.append(b_number)


    list_of_list_1 = ','.join(list(list_of_terms_to_search[0]))
    search_criteria = 'bigram search'

    # Create a dataframe
    df = pd.DataFrame({
        'source_fileName': all_reports_filenames,
        'time_year': all_years,
        'location_fromMOH': all_boroughs,
        'source_bNumber': all_b_numbers,
        'contextText': all_text_extracts,
        'searchCriteria_bigram': list_of_list_1,
        'searchCriteria_type': search_criteria
        })

    # Sort the dataframe
    df = df.sort('time_year')

    # Create a csv
    df.to_csv(outfile, index=None)

    return df


def main():
    startTime = pd.datetime.now()

    find_bigrams(
        reports_dir=REPORTS_DIR,
        list_of_terms_to_search=[('single', 'woman'), ('single', 'women') ],
        outfile='data/output_from_search/search_bigram_singleWoman_50WordsBuffer.csv',
        bigram_buffer=100)

    find_bigrams(
        reports_dir=REPORTS_DIR,
        list_of_terms_to_search=[('married', 'women'), ('married', 'woman')],
        outfile='data/output_from_search/search_bigram_marriedWoman_50WordsBuffer.csv',
        bigram_buffer=100)

    print '\nCompleted in ' + str(pd.datetime.now() - startTime)


if __name__ == '__main__':
    main()
