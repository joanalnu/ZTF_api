#Part 1: request forced photometry using wget command
import subprocess
import os
from astropy.coordinates import Angle
from astropy import units as u
from astropy.time import Time
dirpath = os.path.dirname(os.parh.abspath(__file__))

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

        # getting credentials
        email='me@email.com' # change for you email for ZTF login
        pswd='strongpassword' # change for you ZTF user password

        # request data to ZTF server (using the wget ommand provided by ZTF, see documentation)
        command = f''' 
        osascript -e 'tell application "Terminal" to do script "wget --http-user=ztffps --http-passwd=dontgocrazy! -O log.txt \\"https://ztfweb.ipac.caltech.edu/cgi-bin/requestForcedPhotometry.cgi?ra={ra_deg}&dec={dec_deg}&jdstart={jd_start}&jdend={jd_end}&email={email}&userpass={pswd}\\""'
        '''
        subprocess.Popen(command, shell=True) # You can set shell to false to avoid terminal windows popping-up
        # os._exit()
