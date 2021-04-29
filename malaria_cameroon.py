import argparse
import os
import pathlib #used to work with the cdv file and shapefile

import geopandas as gpd #used to look at geodata shapefiles. I downloaded shapefiles for Cameroon regions to be used in this mapping
import matplotlib.pyplot as plt #Used to create the charts and labels
import numpy as np #used to calculate percentages
import pandas as pd #It helped me import the csv file


def parse_arguments(): #took in the arguemnts and allowed me to write arguments more succintly
    parser = argparse.ArgumentParser(description='Map Mosquito Infection Rate') #this is the title of my project
    parser.add_argument('--shp', type=pathlib.Path, help='Path to Shape file.') #The shapefile I downloaded for use in ArcGIS and Python
    parser.add_argument('--csv', type=pathlib.Path, help='Path to infection rate data csv') #The path to intake my csv file
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    figure_path = os.path.dirname(args.csv)
    print (figure_path)
    df = pd.read_csv(args.csv) #imports and reads the arguemnts within the csv file. Instead of converting my excel into a csv in python, I saved the file as a csv
    df['Infection Rate'] = df['# Positive'] / df['# Tested'] * 100 #This was used to calculate the infection rate
    df = df.dropna()

    gdf = gpd.read_file(args.shp)


    for by, group in df.groupby(['Species']): #I used species of mosquito as the focal point
        if group.empty:
            continue
        merg = gdf.merge(group, on='ADM1_EN') #This argument merges the adminstrative names of Cameroon from the shapefile into this argument
        if merg.empty: #Not all mosquito species are found in every region
            continue
        fig = plt.figure(figsize=(8, 8)) #creates the map per region
        plt.title('Infection Rate of Mosquito, ' + by)
        ax = fig.add_subplot(111)
        merg.plot(column='Infection Rate', ax=ax)
      
        fig.savefig(os.path.join(figure_path, by + '.png'))