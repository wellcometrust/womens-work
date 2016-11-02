import pandas as pd

DATA_FROM_SPREADSHEET = 'data/master_dataset/MASTER_DATASET_V2_partial.csv'
GEO_LOOKUP = 'data/centroids/london_borough_centroids.csv'
OUTFILE = 'data/dataset_for_visualisation/final_dataset_v1.csv'


def prepare_dataset(
    infile=DATA_FROM_SPREADSHEET,
    lookup=GEO_LOOKUP,
    outfile=OUTFILE):
    """
    Process the data from the Google Spreadsheet and prepare for visualisation.
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

    df['latitude'] = latitude_list
    df['longitude'] = longitude_list

    df = df.fillna(0)


    # Add URL
    list_of_bNumbers = list(df['source_bNumber'].values)
    list_of_urls = ['https://dlcs.io/pdf/wellcome/pdf-item/' + x + '/0' for x in list_of_bNumbers]
    df['source_url'] = list_of_urls

    df.to_csv(outfile, index=None)


def main():
    startTime = pd.datetime.now()
    prepare_dataset()
    print '\nCompleted in ' + str(pd.datetime.now() - startTime)


if __name__ == '__main__':
    main()
