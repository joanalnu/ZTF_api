# Part 2: open requested query copied from html website and download txt files with the photometry data
import os
import requests
import math
from astropy import units as u
dirpath = os.path.dirname(os.path.abspath(__file__))

file = open(f'{dirpath}/ZTF/Requested_Query_ZTF_ForcedPhotometry_Service.txt', 'r')
# file format:
# reqId ra  dec startJD endJD   created started ended   exitcode    lightcurve
for line in file:
    if line[0]!='r': # avoid header
        # accessing photometry file
        print(line)
        line = line.split('\t')
        path = line[10]
        url = f'https://ztfweb.ipac.caltech.edu{path}'

        # get name of SN from the original submited file
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
        
        # retrieve photometry data and write in computer
        with requests.sessions() as s:
            textdata = s.get(url, auth=('ztffps', 'dontgocrazy!')).text
            with open(f'{dirpath}/ZTF/ZTF_{name}.txt', 'w') as f:
                for lin in textdata:
                    f.write(line)
