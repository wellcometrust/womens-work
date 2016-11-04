import pandas as pd
import re

DATA_FROM_SPREADSHEET = 'data/master_dataset/MASTER_DATASET_V3_20161104.csv'
GEO_LOOKUP = 'data/centroids/london_borough_centroids.csv'
GEO_LOOKUP_MOH = 'data/geo_lookup/moh-place-mappings.csv'
OUTFILE = 'data/dataset_for_visualisation/final_dataset_v4.csv'
OUTFILE_2 = 'data/dataset_for_visualisation/final_dataset_v4_withMoh_names.csv'


def prepare_dataset(
    infile=DATA_FROM_SPREADSHEET,
    lookup=GEO_LOOKUP,
    outfile=OUTFILE):
    """
    Get the data from the Google Spreadsheet, add current location name, latitude,
    longitude and URLs.
    """

    # Create geo dict
    df_lookup = pd.read_csv(lookup)
    all_lat = list(df_lookup['latitude'])
    all_long = list(df_lookup['longitude'])
    all_borough_name = list(df_lookup['borough name'])

    geodict = {}
    for i in range(len(all_lat)):
        geodict[all_borough_name[i]] = {
            'latitude': all_lat[i],
            'longitude': all_long[i]
        }

    # Add location
    df = pd.read_csv(infile)
    all_current_boroughs = list(df['location_current'].values)

    latitude_list = []
    longitude_list =[]
    for x in all_current_boroughs:
        if x in geodict.keys():
            latitude = geodict[x]['latitude']
            longitude = geodict[x]['longitude']
            latitude_list.append(latitude)
            longitude_list.append(longitude)
        else:
            latitude_list.append(0)
            longitude_list.append(0)

    df['location_latitude'] = latitude_list
    df['location_longitude'] = longitude_list

    df = df.fillna(0)

    # Add Moh place
    df_moh_places = pd.read_csv(GEO_LOOKUP_MOH)
    print df_moh_places

    # Add URL
    list_of_bNumbers = list(df['source_bNumber'].values)
    list_of_urls = ['http://wellcomelibrary.org/item/' + x for x in list_of_bNumbers]
    df['source_url'] = list_of_urls

    df.to_csv(outfile, index=None)


def get_oldLocationNames_to_currentBoroughNames(
    lookup=GEO_LOOKUP_MOH,
    infile=OUTFILE,
    outfile=OUTFILE_2):
    """
    Transform the MOH name to a current borough name.
    """

    df = pd.read_csv(lookup)
    df = df[['NormalisedPlace', 'NormalisedMoHPlace', 'MoHPlace']]
    moh_places_list = list(df['MoHPlace'].values)
    moh_name_list = list(df['NormalisedMoHPlace'].values)
    borough_name_list = list(df['NormalisedPlace'].values)


    # Replace spaces and punctuation to adapt to filenames of moh reports
    moh_name_list = [x.replace(' ', '') for x in moh_name_list]
    moh_name_list = [re.sub(r'[^\w\s]','', x) for x in moh_name_list]

    # Make lowercase
    moh_name_list = [x.lower() for x in moh_name_list]


    dict_mohPlaceNormalised_to_currentLocation = dict(zip(moh_name_list, borough_name_list))
    dict_mohPlace_to_mohPlaceNormalised = dict(zip(moh_name_list, moh_places_list))

    df = pd.read_csv(infile)
    names_to_normalise = list(df['location_fromMOH'].values)

    # Make lowercase
    names_to_normalise = [x.lower() for x in names_to_normalise]

    borough_name_list_normalised = []
    moh_places = []
    for x in names_to_normalise:
        borough_name_list_normalised.append(dict_mohPlaceNormalised_to_currentLocation[x])
        moh_places.append(dict_mohPlace_to_mohPlaceNormalised[x])

    df['location_current'] = borough_name_list_normalised
    df['location_mohPlace'] = moh_places

    df.to_csv(outfile, index=None)

    return



def main():
    startTime = pd.datetime.now()
    prepare_dataset()
    get_oldLocationNames_to_currentBoroughNames()
    print '\nCompleted in ' + str(pd.datetime.now() - startTime)


if __name__ == '__main__':
    main()
