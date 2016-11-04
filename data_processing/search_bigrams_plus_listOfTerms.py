from __future__ import division
import pandas as pd
from search_bigrams import find_bigrams


def compositeSearch_bigram_and_list(
    list_of_terms=['employment', 'employed', 'employee', 'work', 'working', 'worked', 'job', 'occupation'],
    outfile='data/output_from_search/search_bigramPlusList_marriedWoman_plus_employmentList_50WordsBuffer.csv'):


    df = find_bigrams(
            list_of_terms_to_search=[('married', 'women'), ('married', 'woman')],
            outfile='data/output_from_search/bigram_search_marriedWoman_50WordsBuffer.csv',
            bigram_buffer=100)

    list_of_text_extracts = list(df['contextText'].values)

    # Find indexes of records that contain any words of the list of terms
    indexes_of_items_to_keep = []
    for i in range(len(list_of_text_extracts)):
        for x in list_of_terms:
            if x in list_of_text_extracts[i]:
                indexes_of_items_to_keep.append(i)

    indexes_of_items_to_keep = list(set(indexes_of_items_to_keep))

    # Filter the dataframe
    filtered_df = df.iloc[indexes_of_items_to_keep]
    filtered_df['list of search terms'] = [','.join(list_of_terms)] * len(filtered_df)
    filtered_df['search criteria'] = ['bigram + list of terms'] * len(filtered_df)

    # Save to csv
    filtered_df.to_csv(outfile, index=None)


def main():
    startTime = pd.datetime.now()
    compositeSearch_bigram_and_list()
    print '\nCompleted in ' + str(pd.datetime.now() - startTime)


if __name__ == '__main__':
    main()
