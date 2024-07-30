import os
import requests
import argparse
from bs4 import BeautifulSoup
from tqdm import tqdm


def fetch_data(from_year=None, to_year=None):
    # URL of the page with the dropdown
    url = 'https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_NetCDF.html'
    download_url = 'https://www.imdpune.gov.in/cmpg/Griddata/RF25.php'

    # Directory to save downloaded files
    output_dir = './data'
    os.makedirs(output_dir, exist_ok=True)

    # Get the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract available years from the dropdown
    dropdown = soup.find('select', {'name': 'RF25'})
    options = dropdown.find_all('option')
    years = [int(option['value']) for option in options if option['value'].isdigit()]

    # Validate year range
    if from_year is not None and to_year is not None:
        if from_year > to_year:
            raise ValueError("from_year cannot be greater than to_year")
        if from_year < min(years) or to_year > max(years):
            raise ValueError("Year range is out of bounds")

        years = [year for year in years if from_year <= year <= to_year]
    elif from_year is not None:
        if from_year < min(years) or from_year > max(years):
            raise ValueError("Year is out of bounds")
        years = [year for year in years if year >= from_year]
    elif to_year is not None:
        if to_year < min(years) or to_year > max(years):
            raise ValueError("Year is out of bounds")
        years = [year for year in years if year <= to_year]

    # Check if no years are in the final list
    if not years:
        raise ValueError("No available years match the criteria")

    years = sorted(years)
    # Print the years being downloaded
    print(f"Downloading dataset(s) for years: {', '.join(map(str, years))}")

    # Download each file
    for year in tqdm(years):
        # Prepare the data for POST request
        data = {'RF25': year}
        # Send the request to download the file
        response = requests.post(download_url, data=data, stream=True)
        filename = f'{output_dir}/RF25_ind{year}_rfp25.nc'  # Assuming the files are NetCDF format

        # Save the file
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download rainfall data for specified years.")
    parser.add_argument('-f', '--from_year', type=int, help="Start year for data download.")
    parser.add_argument('-t', '--to_year', type=int, help="End year for data download.")

    args = parser.parse_args()

    try:
        fetch_data(args.from_year, args.to_year)
    except ValueError as e:
        print(f"Error: {e}")
        parser.print_usage()
