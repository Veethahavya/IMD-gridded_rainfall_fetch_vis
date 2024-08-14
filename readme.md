# 1. Fetch Rainfall Data
Thanks to the work of [Pai et al. (2014)](https://www.imdpune.gov.in/cmpg/Griddata/ref_paper_MAUSAM.pdf), 0.25x0.25 degree gridded datasets ara made available to the public by the [Indian Meteorological Department (IMD)](https://mausam.imd.gov.in/) with datasets starting from 1901 until 2023 (as of 30.07.2024).
The Python script `./fetch.py` automates the download of said datasets from the [Indian Meteorological Department (IMD) Pune website](https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_NetCDF.html), where the dataset is available. It retrieves the list of available years from the dropdown menu and downloads the corresponding datasets that are offered in NetCDF format.


## Directory Structure
The downloaded files are stored in `./data/`
```
./data/
├── RF25_ind<yyyy>_rfp25.nc
├── ...
└── RF25_ind<YYYY>_rfp25.nc
```
where:
- yyyy is `<int:: from_year>` of four digits, 
- YYYY is `<int:: to_year>` of four digits, and
- Each file is named according to the year of the data it contains.


## Requirements
- Python 3.x (tested with python 3.10.14)
- `requests`
- `beautifulsoup4`
- `tqdm`

You can install these packages using pip (or conda, or your preferred package manager):
```bash
pip install requests beautifulsoup4 tqdm
```


## Usage
Run the script:
```bash
python fetch.py
```

This will:
- Scrape the available years from the dropdown menu on the IMD Pune website.
- Download the rainfall data for each year into the rainfall_data directory.

Alternatively, specify the period for which you want to download the datasets like so:
```bash
python fetch.py --from_year <int::from_year> --to_year <int:: to_year>
```
OR
```bash
python fetch.py -f <int::from_year> -t <int:: to_year>
```


## Script Details
- URL: The script accesses this [webpage](https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_NetCDF.html) (https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_NetCDF.html) to find the available years.
- Download URL: The data is downloaded via this [link](https://www.imdpune.gov.in/cmpg/Griddata/RF25.php) (https://www.imdpune.gov.in/cmpg/Griddata/RF25.php).
- Data Format: The files are assumed to be in NetCDF format (.nc).


## Customization
- Output Directory: By default, data files are saved in the rainfall_data directory. You can change this by modifying the output_dir variable.
- Error Handling: The script currently prints download progress. You can modify it to handle errors like network issues, unavailable years, etc.



# 2. Rainfall Data Animation
The aforementioned downloaded data can be viewed and saved as interactive HTML files. 

## Directory Structure
- `./data/`: Directory containing the input netCDF files.
- `./vis/`: Directory where the resulting HTML animations will be saved.
- The netCDF files should follow this naming pattern: `RF25_ind<YYYY>_rfp25.nc`, where `<int:: YYYY>` represents the corresponding year as four digits.
- The name of the saved visualisation is of the format `<int:: YYYY>.html`, where `<int:: YYYY>` represents the corresponding year as four digits.


## Requirements
- Python 3.x (tested with python 3.10.14)
- `numpy`
- `netCDF4`
- `matplotlib`
- `tqdm`

You can install these packages using pip (or conda, or your preferred package manager):
```bash
pip install numpy netCDF4 matplotlib tqdm
```


## Usage
Run the script:
```bash
python vis.py
```
This will generate and save the visualisations for all years and store it under `./vis/`

Alternatively, specify the period for which you want to download the datasets like so:
```bash
python vis.py --from_year <int::from_year> --to_year <int:: to_year>
```
OR
```bash
python vis.py -f <int::from_year> -t <int:: to_year>
```

Additionally, an interpolation method can also be specified so:
```bash
python vis.py --interpolation <str:: method>
```
OR
```bash
python vis.py -i <str:: method>
```
where the `method` is one of `['nearest', 'bilinear', 'bicubic', 'lanczos']`.
Refer [docs:: (imshow)@matplotlib.pyplot.imshow](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html#matplotlib-pyplot-imshow)

Additionally, the Jupyter Notebook `vis.ipynb` offers an interactive implementation of the same program.


## Script Details
- The script uses `matplotlib`'s `FuncAnimation` to create animations.
- The resulting HTML animations are interactive and can be viewed in a web browser.


## Customization
- **Directories**: Modify `data_dir` and `vis_dir` in the script to change input and output directories.


## Notes
- The script uses a regex pattern to extract the year from filenames. Ensure your files follow the naming convention.
- Be aware of any terms of use or data usage policies of the IMD Pune website.


# 0. Metadata
## Author
Veethahavya Kootanoor Sheshadrivasan
## e-mail
veethahavya@gmail.com
## Acknowledgements
Acknowledging the use of [Github Copilot](https://github.com/features/copilot), and subsequently contributions from various contributors to numerous FOSS projects.
