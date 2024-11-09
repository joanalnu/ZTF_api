# ZTF_API
API to access ZTF (Zwicky Transient Facility) data. This is an API which aims to provide an easier access to the ZTF photometry database. It is faster and perfect for large lists and typing errors will be avoided by using it.

[![repo](https://img.shields.io/badge/GitHub-joanalnu%2FZTF_api-blue.svg?style=flat)](https://github.com/joanalnu/ZTF_api)
[![license](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/joanalnu/ZTF_api/LICENSE)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)
[![DOI](https://zenodo.org/badge/820854715.svg)](https://doi.org/10.5281/zenodo.12568639)

## Installation
Firstly, clone this repository into your local machine
```bash
git clone https://github.com/joanalnu/ZTF_api.git
```
or using github features to clone, open in Github Desktop or download a ZIP.

Then install the repository as a package by using ```bash cd``` to navigate to the cloned repository and running the following command:
```bash
pip install .
```

### The ZTF Survey

There are many things that change in the sky, for instance comments and asteroids, stars going supernova, active galactic nuclei, or other active regions of space (transients). Surveys like ZTF scan the sky aiming to detect this type of changing events.

The Zwicky Transient Facility (ZTF) is a wide-field survey aimed at a systematic exploration of the optical transient sky. Since March 2018 it covers the full sky visible from the northern Palomar Observatory in three filters (g, r, i). It uses the Samuel Oschin Telescope, a 48-inch Schmidt at Palomar, with 16 6k x 6k CCDs filling the focal plane with a 47 square degrees field of view. It is supported by the National Science Foundation and collaborations including current partners Caltech, IPAC, the Oskar Klein Center at Stockholm University, the University of Maryland, University of California, Berkeley, the University of Wisconsin at Milkwaukee, University of Warwick, Ruhr University, Cornell University, Northwestern University, and Drexel University. Operations of the observatory are conducted by COO, IPAC and UW. You may read more about the data processing system at Masci et al. (2019) and about the technical specifictions and survey design at Bellm et al. (2019).

The ZTF requests website enables everybody with the needed credentials (see https://irsa.ipac.caltech.edu/data/ZTF/docs/forcedphot.pdf) to access the photometric light curve data from the ZTF survey. These light curves are generated by subtracting one image with another one to see if there are differences in the fields of the picture. One may compute different physical magnitudes using the difference of flux generated by a specific object.

This is an API which aims to provide an easier access to the ZTF photometry database. It is faster and typing errors will be avoided by using this code. To effectively download the data, the API must be separated in two parts, here we explain the functionalities of each one.

## Instructions
Here is an explanation on how to use this code to download ZTF forced photometry data. For a more in depth explanation of the functioning of the code, please refer to the [code explanation](#code-explanation) section.

Before using the API, you must have created an account in the ZTF requests website and have the needed credentials to access the data. You will need to copy your credentials ('email' and 'password') into the ```credentials.txt``` file in the root of the repository.

To use the API you have to import it in your code
```python
import ztf_api
```
and call the functions you want to using:
```python
ztf_api.download()
```

All the files you use (request and download txt files) need to be stored in the same path as the cloned API directory.

### Request function
The request function is uesd to query data to the ZTF Photometry Database. To use the request you will have to provide a ```txt``` file containing the following information:
```
Name DateObs RA Dec
```
Where: the date of observation can be in Julian Date (JD), Modified Julian Date (MJD) or hour angles; and the coordinates can be in degrees or hours.

### Download function
Once all your request have been completed (which you can check here. [https://ztfweb.ipac.caltech.edu/cgi-bin/getForcedPhotometryRequests.cgi](https://ztfweb.ipac.caltech.edu/cgi-bin/getForcedPhotometryRequests.cgi)), you will have to copy paste the table on that website into a txt file. When you call the download function you will have to provide to arguments following:
```python
ztf_api.download(name_of_request_file, name_of_download_file)
```

## Contributing

To contribute, please contact me via [email](mailto:joanalnu@outlook.com), open an issue or send a pull request.

## Citing ZTF API

If you make use of this code, please cite it:

```bibtex
@software{joanalnu_2024,
  author       = {Alcaide-Núñez, joan},
  title        = {joanalnu/ZTF\_api},
  month        = july,
  year         = 2024,
  publisher    = {Zenodo},
  version      = {v1.0},
  doi          = {10.5281/zenodo.12568639},
  url          = {https://github.com/joanalnu/ZTF_api}
}
```


## Acknowledgements

First of all, I would like to thank the team behind the ZTF survey and the IPAC Caltech project, which manages this survey, for their service to the astrophysics community and their responsibility providing open access to data.

Further, a very bold thank to Claudia Gutiérrez, Lluís Galbany and Tomás E. Müller-Bravo from ICE-CSIC for their support and insightful explanations.

I also acknowledge the use of the open-source Python libraries: subprocess, os, astropy, requests, and math.


## Code Explanation
### request function
The first part is named ```request()``` and its job is to request the required data to the ZTF server. Let's analyse what it does:

First we want to import the needed libraries, note that you will need to install those libraries (see requirements.txt) and we read the folder path.

```python
#Part 1: request forced photometry using wget command
import subprocess
import os
from astropy.coordinates import Angle
from astropy import units as u
from astropy.time import Time
dirpath = os.path.dirname(os.parh.abspath(__file__))
```

Next we will open the file and read the data. You will have to change the ```code file.txt``` by your file's name. Also note that the input file must be saved in the same folder as the downloaded API, otherwise you will need to copy the code or change the directory path.

```python
# open input file in the same folder as this code
with open(f'{dirpath}/file.txt', 'r') as file:
    for line in file:
        if line[0]!='W':
            # input file format: Name DateObs ra dec
            # DateObs preferred in JD, but also hourangles and MJD work
            # coords preferred in degree, but also hours work
            if '\t' in line:
                try:
                    name, date, ra, dec = line.split('\t')
                except ValueError:
                    name, date, ra, dec, comment = line.split('\t')
                    print(f'Comment for {name}: \t {comment}')
            else:
                try:
                    name, date, ra, dec = line.split()
                except ValueError:
                    name, date, ra, dec, comment = line.split()
                    print(f'Comment for {name}: \t {comment}')
```

Moreover, this makes sure that the input data is in the right format for the ZTF request, otherwise is converts the data to the required units. It also defines the start and end date to be 200 days before the provided observation date and 400 days after the provided observation date respectively (you may change that with you preferences).

```python
        # Get the Julian Date
        def identify_date_format(date_string):
            gregorian_pattern = r'^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?$'
            if re.match(gregorian_pattern, date_string):
                try:
                    t = Time(date_string, format='iso', scale='utc')
                    return t.jd
                except ValueError:
                    pass
            try:
                t = Time(float(date_string), format='mjd', scale='utc')
                return t.jd
            except ValueError:
                pass
            return date # already in jd format

        # define start and end dates
        jd_start = date-200 # you can update this preferences as you want
        jd_end = date+400
        
        # coordinates to degrees
        if ':' in ra:
            ra_deg = Angle(ra, unit=u.hourangle).degree
        if ':' in dec:
            dec_deg = Angle(dec, unit=u.hourangle).degree
        else:
            ra_deg, dec_deg = ra, dec
```

Next, you will need to substitute these lines with your personal credentials provided by the ZTF team (see documentation).

```python
        # getting credentials
        email='me@email.com' # change for you email for ZTF login
        pswd='strongpassword' # change for you ZTF user password
```

Finally, after collecting the needed information we can request the forced photometry to the ZTF server using this wget command, which opens in a new terminal window to execute.

```python
        # request data to ZTF server (using the wget ommand provided by ZTF, see documentation)
        command = f''' 
        osascript -e 'tell application "Terminal" to do script "wget --http-user=ztffps --http-passwd=dontgocrazy! -O log.txt \\"https://ztfweb.ipac.caltech.edu/cgi-bin/requestForcedPhotometry.cgi?ra={ra_deg}&dec={dec_deg}&jdstart={jd_start}&jdend={jd_end}&email={email}&userpass={pswd}\\""'
        '''
        subprocess.Popen(command, shell=True) # You can set shell to false to avoid terminal windows popping-up
        # os._exit() # change that to exit system after completion
```

### download function

Next, the second part will download the data when available and its named ```download())```. Let's go throught the code as for the first part.

As always, we import the needed libraries and define the folder path of this script.

```python
# Part 2: open requested query copied from html website and download txt files with the photometry data
import os
import requests
import math
from astropy import units as u
dirpath = os.path.dirname(os.path.abspath(__file__))
```

You will need to go to the ZTF Requests website ([https://ztfweb.ipac.caltech.edu/cgi-bin/getForcedPhotometryRequests.cgi](https://ztfweb.ipac.caltech.edu/cgi-bin/getForcedPhotometryRequests.cgi)), authenticate yourself, select 'All recent jobs' and click query database.

![Image of ZTF website](https://github.com/joanalnu/ztf_api/raw/main/main/ztf_website.png)

Here you can see the status of your jobs. When all of them are finished, copy-paste the table into a txt file in the API folder (ztf_api).

This snippet opens that file and reads the data.
```python
file = open(f'{dirpath}/Requested_Query_ZTF_ForcedPhotometry_Service.txt', 'r')
# file format (from ZTF query table):
# reqId ra  dec startJD endJD   created started ended   exitcode    lightcurve
for line in file:
    if line[0]!='r': # avoid header
        # accessing photometry file
        print(line)
        line = line.split('\t')
        path = line[10]
        url = f'https://ztfweb.ipac.caltech.edu{path}'
```

Next we will search in the original submitted file for the name of the object using the coordinates. Therefore, we open that file and make sure that the coordinates are in the same format. Then we will search for equal coordinates and save the name.

```python
        # get name of SN from the original submitted file
        ra = float(line[1])
        dec = float(line[2])
        name=''
        with open(f'{dirpath}/file.txt', 'r') as f: # opening original submission file
            for line in f:
                if line[0]!='N' or line[0]!='n': # avoiding header
                    fields = line.strip().split('\t')

                    # checking units of coordinates
                    if ':' in fields[2]:
                        ra_deg = Angle(fields[2], unit=u.hourangle).degree
                    if ':' in fields[3]:
                        dec_deg = Angle(fields[3], unit=u.hourangle).degree
                    else:
                        ra_deg, dec_deg = fields[2], fields[3]

                    # searching for name
                    tol=1e-9
                    if math.isclose(ra, float(ra_deg)) and math.isclose(dec, float(dec_deg)):
                        name = fields[0]
                        break
```

Finally, we use requests to access the txt data file and write the content into our folder.

```python
        # retrieve photometry data and write in computer
        with requests.Session() as s:
            textdata = s.get(url, auth=('ztffps', 'dontgocrazy!')).text
            with open(f'{dirpath}/ZTF/ZTF_{name}.txt', 'w') as f:
                for lin in textdata:
                    f.write(line)
```

By the end you should have a folder named ```code ZTF``` under this API's directory in which the files from ZTF forced photometry are downloaded as txt files.