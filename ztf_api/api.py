# importing libraries
import subprocess
import os
from astropy.coordinates import Angle
from astropy import units as u
from astropy.time import Time
import requests
import math
import re
dirpath = os.path.dirname(os.path.abspath(__file__))[:-8]
print(dirpath)


def get_credentials(typeof):
    with open(dirpath+'/credentials.txt', 'r') as f:
        content = f.readlines()
        email = content[0].split('=')[1]
        pswd = content[1].split('=')[1]
    return (email, pswd)

def request(filename):
    with open(f'{dirpath}/{filename}.txt', 'r') as file:
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
                ra_deg, dec_deg = float(ra), float(dec)

            # get credentials
            email, pswd = get_credentials()

            # request data to ZTF server (using the wget ommand provided by ZTF, see documentation)
            command = f''' 
            osascript -e 'tell application "Terminal" to do script "wget --http-user=ztffps --http-passwd=dontgocrazy! -O log.txt \\"https://ztfweb.ipac.caltech.edu/cgi-bin/requestForcedPhotometry.cgi?ra={ra_deg}&dec={dec_deg}&jdstart={jd_start}&jdend={jd_end}&email={email}&userpass={pswd}\\""'
            '''
            subprocess.Popen(command, shell=False) # You can set shell to false to avoid terminal windows popping-up
            # os._exit()

def downloads(request_filename, download_filename):
    file = open(f'{dirpath}/ZTF/{download_filename}.txt', 'r')
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
            with open(f'{dirpath}/{request_filename}.txt', 'r') as f: # opening original submission file
                for line in f:
                    if line[0] not in ['N', 'n']:
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
            with requests.Session() as s:
                textdata = s.get(url, auth=('ztffps', 'dontgocrazy!')).text
                with open(f'{dirpath}/ZTF/ZTF_{name}.txt', 'w') as f:
                    for line in textdata:
                        f.write(line)