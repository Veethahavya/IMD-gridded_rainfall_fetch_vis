import os
import glob
import re
import argparse
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(description="Generate and save animations of rainfall data.")
    parser.add_argument('-f', '--from_year', type=int, help="Starting year for filtering netCDF files.")
    parser.add_argument('-t', '--to_year', type=int, help="Ending year for filtering netCDF files.")
    parser.add_argument(
        '-i',
        '--interpolation',
        type=str,
        choices=['nearest', 'bilinear', 'bicubic', 'lanczos'],
        default=None,
        help="Interpolation method for visualizing data. Options: 'nearest', 'bilinear', 'bicubic', 'lanczos'. Default is None.",
    )
    return parser.parse_args()


def create_animation(file_path, output_path, interpolation):
    # Open the dataset
    rainfall_dataset = nc.Dataset(file_path, 'r')

    # Retrieve latitude and longitude
    longitude = rainfall_dataset['LONGITUDE'][:]
    latitude = rainfall_dataset['LATITUDE'][:]

    # Retrieve the rainfall values
    rainfall = rainfall_dataset['RAINFALL']

    # Create a figure and axis for the plot
    fig, ax = plt.subplots()

    # Initialize the image plot with dummy data
    dummy_data = np.zeros_like(rainfall[0])
    cax = ax.imshow(
        dummy_data,
        cmap='Blues',
        interpolation=interpolation,
        extent=[longitude.min(), longitude.max(), latitude.min(), latitude.max()],
    )
    cbar = fig.colorbar(cax, ax=ax)
    cbar.set_label("Rainfall (mm)")
    ax.set_title("Day 0")

    # Function to update the plot for each frame
    def update(day):
        data = np.flipud(rainfall[day])
        cax.set_data(data)
        cax.set_clim(vmin=np.nanmin(data), vmax=np.nanmax(data))  # Update color limits
        ax.set_title(f"Day {day}")
        return (cax,)

    # Set axis labels to show longitude and latitude
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_xticks(np.linspace(longitude.min(), longitude.max(), num=5))  # Adjust the number of ticks as needed
    ax.set_yticks(np.linspace(latitude.min(), latitude.max(), num=5))

    # Create the animation
    ani = FuncAnimation(fig, update, frames=365, blit=False)

    # Save the animation as HTML
    with open(output_path, 'w') as f:
        f.write(ani.to_jshtml())

    # Close the figure
    plt.close(fig)


def main():
    # Parse command-line arguments
    args = parse_args()
    from_year = args.from_year
    to_year = args.to_year
    interpolation = args.interpolation

    # Define directories
    data_dir = './data'
    vis_dir = './vis'

    # Ensure the output directory exists
    os.makedirs(vis_dir, exist_ok=True)

    # Get a list of all files matching the pattern
    file_pattern = os.path.join(data_dir, 'RF25_ind*_rfp25.nc')
    files = glob.glob(file_pattern)

    # Extract years from filenames
    available_years = set()
    for file in files:
        match = re.search(r'RF25_ind(\d{4})_rfp25\.nc', os.path.basename(file))
        if match:
            available_years.add(match.group(1))

    available_years = sorted(available_years)

    # Check if the provided years are valid
    if from_year is not None:
        if str(from_year) not in available_years:
            raise ValueError(f"Year {from_year} not found in the data files.")
    if to_year is not None:
        if str(to_year) not in available_years:
            raise ValueError(f"Year {to_year} not found in the data files.")

    # Determine years to process
    if from_year is not None and to_year is not None:
        years_to_process = set(str(year) for year in range(from_year, to_year + 1))
    elif from_year is not None:
        years_to_process = {str(from_year)}
    elif to_year is not None:
        years_to_process = {str(to_year)}
    else:
        years_to_process = set(available_years)

    files_to_process = [
        f for f in files if re.search(r'RF25_ind(\d{4})_rfp25\.nc', os.path.basename(f)).group(1) in years_to_process
    ]

    if not files_to_process:
        if from_year > to_year:
            raise ValueError("from_year cannot be greater than to_year")
        if from_year < min(available_years) or to_year > max(available_years):
            raise ValueError("Year range is out of bounds")
        raise ValueError("No files found for the specified year range.")

    # Print years being processed
    print(f"Processing years: {', '.join(sorted(years_to_process))}")

    # Process each file
    for file in tqdm(files_to_process):
        year = re.search(r'RF25_ind(\d{4})_rfp25\.nc', os.path.basename(file)).group(1)

        # Define output file path
        output_file = os.path.join(vis_dir, f'{year}.html')

        # Create and save the animation
        create_animation(file, output_file, interpolation)

        print(f"Animation saved as {output_file}")


if __name__ == '__main__':
    main()
