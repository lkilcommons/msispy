# Copyright (C) 2012  VT SuperDARN Lab
# Full license can be found in LICENSE.txt
# Modified by Liam Kilcommons, CU Boulder, 2014
# (C) 2014 University of Colorado AES-CCAR-SEDA (Space Environment Data Analysis) Group
"""
*********************
**Module**: models.msis
*********************
This module contains the following functions:

    * :func:`msispy.msisFort.gtd7`
        * **INPUTS**:
            * **IYD** - year and day as YYDDD (day of year from 1 to 365 (or 366)) (Year ignored in current model)
            * **SEC** - UT (SEC)
            * **ALT** - altitude (KM)
            * **GLAT** - geodetic latitude (DEG)
            * **GLONG** - geodetic longitude (DEG)
            * **STL** - local aparent solar time (HRS; see Note below)
            * **F107A** - 81 day average of F10.7 flux (centered on day DDD)
            * **F107** - daily F10.7 flux for previous day
            * **AP** - magnetic index (daily) OR when SW(9)=-1., array containing:
                    * (1) daily AP
                    * (2) 3 HR AP index FOR current time
                    * (3) 3 HR AP index FOR 3 hrs before current time
                    * (4) 3 HR AP index FOR 6 hrs before current time
                    * (5) 3 HR AP index FOR 9 hrs before current time
                    * (6) average of height 3 HR AP indices from 12 TO 33 HRS prior to current time
                    * (7) average of height 3 HR AP indices from 36 TO 57 HRS prior to current time
            * **MASS** - mass number (only density for selected gass is calculated.  MASS 0 is temperature.
                MASS 48 for ALL. MASS 17 is Anomalous O ONLY.)
        * **OUTPUTS**:
            * **D(1)** - HE number density(CM-3)
            * **D(2)** - O number density(CM-3)
            * **D(3)** - N2 number density(CM-3)
            * **D(4)** - O2 number density(CM-3)
            * **D(5)** - AR number density(CM-3)
            * **D(6)** - total mass density(GM/CM3)
            * **D(7)** - H number density(CM-3)
            * **D(8)** - N number density(CM-3)
            * **D(9)** - Anomalous oxygen number density(CM-3)
            * **T(1)** - exospheric temperature
            * **T(2)** - temperature at ALT

"""

try:
        from msispy.msisFort import *
except Exception as e:
        print(__file__+' -> msis: ', e)

def getF107Ap(mydatetime=None):
    """
Obtain F107 and AP required for MSIS input from tabulated values in IRI data.

* **INPUT**:
    * mydatetime: python datetime object (defaults to last tabulated value)

* **OUTPUT**:
    * dictOut: a dictionnary containing:
        * datetime: the date and time as a python datetime object
        * f107: daily f10.7 flux for previous day
        * f107a: 81 day average of f10.7 flux (centered on date)
        * ap: magnetic index containing:
            * (1) daily AP
            * (2) 3 HR AP index for current time
            * (3) 3 HR AP index for 3 hours before current time
            * (4) 3 HR AP index for 6 hours before current time
            * (5) 3 HR AP index for 9 hours before current time
            * (6) Average of eight 3 hour AP indicies from 12 to 33 hrs prior to current time
            * (7) Average of eight 3 hour AP indicies from 36 to 57 hrs prior to current time

    """
    from datetime import datetime
    from numpy import mean, floor
    import os.path

    # Get current path to this code
    # data file will be with it
    msispath = __file__.partition('__init__.py')[0]

    # open apf107.dat file
    with open(os.path.join(msispath,'apf107.dat'), 'r') as fileh:
        data = []
        for line in fileh:
            data.append(line)

    # read into array
    # (cannot use genfromtext because some columns are not separated by anything)
    tdate = []
    tap = []
    tapd = []
    tf107 = []
    tf107a = []
    tf107y = []
    for ldat in data:
        yy = int(ldat[1:3])
        year = 1900+yy if (yy >= 58) else 2000+yy
        #Add a little extra flow control
        if mydatetime is not None:
            if year < mydatetime.year:
                continue
            elif year > mydatetime.year:
                break
        tdate.append( datetime(year, int(ldat[4:6]), int(ldat[7:9])).date() )
        ttap = []
        for iap in range(8):
            ttap.append( int(ldat[9+3*iap:9+3*iap+4]) )
        tap.append( ttap )
        tapd.append( int(ldat[33:36]) )
        tf107.append( float(ldat[39:44]) )
        tf107a.append( float(ldat[44:49]) )
        tf107y.append( float(ldat[49:54]) )

    # Get required datetime
    dictOut = {}
    if mydatetime is None:
        dictOut['datetime'] = datetime(tdate[-1].year, tdate[-1].month, tdate[-1].day)
    elif mydatetime.date() <= tdate[-1]:
        dictOut['datetime'] = mydatetime
    else:
        print('Invalid date {}'.format(mydatetime))
        print('Available dates in {} are {} to {}'.format(year,tdate[0],tdate[-1]))
        return

    # Find entry for date
    dtInd = tdate.index(dictOut['datetime'].date())
    # Find hour index
    hrInd = int( floor( dictOut['datetime'].hour/3. ) )

    # f107 output
    dictOut['f107'] = tf107[dtInd-1]
    dictOut['f107a'] = tf107a[dtInd]

    # AP output
    ttap = [ tap[dtInd][hrInd-i] for i in range(hrInd+1) ]
    for id in range(3):
        for ih in range(8):
            ttap.append(tap[dtInd-id-1][-ih-1])
    dictOut['ap'] = [ tapd[dtInd],
                                        ttap[0],
                                        ttap[1],
                                        ttap[2],
                                        ttap[3],
                                        mean(ttap[4:13]),
                                        mean(ttap[13:26])
                                    ]

    return dictOut

def msis(lat,lon,alt,dt=None,f107=None,ap_daily=None,f107a=None,ap3=None,ap33=None,ap36=None,ap39=None,apa1233=None,apa3657=None):
    import numpy
    from collections import OrderedDict
    import datetime
    """
    Calls the MSIS model with given solarwind inputs or with those of datetime dt if specified
    if the extra average and historical inputs are not specified,
    then will just use the values of f107 and ap to replace all averages

    Pass arrays of GEODETIC latitudes and longitudes and altitudes.

        INPUTS
        ------
            dt - a single datetime.datetime object
            lat - a [m x 1] numpy array of latitudes
            lon - a [m x 1] numpy array of longitudes
            alt - a [m x 1] numpy array of altitudes
            f107 - float
                daily f10.7 flux for previous day
            ap_daily - float
                daily AP magnetic index
            f107a - optional,float
                81 day average of f10.7 flux (centered on date)
            ap3 - optional, float
                3 hour AP for current time
            ap33 - optional, float
                3 hour AP for current time - 3 hours
            ap36 - optional, float
                3 hour AP for current time - 6 hours
            ap39 - optional, float
                3 hour AP for current time - 9 hours
            apa1233 - optional, float
                Average of eight 3 hour AP indicies from 12 to 33 hrs prior to current time
            apa3657
                Average of eight 3 hour AP indices from 36 to 57 hours prior to current time


        RETURNS
        -------
            species - a OrderedDictionary of [m x 1] numpy arrays
                The number density of various atmomic species, keys
                are HE, O, N2, O2, AR, H, N, AO (anomalous oxygen)
                and the mass density, in g / cm^3 (key is 'mass')
            t_exo - an [m x 1] numpy array
                Exospheric temperature
            t_alt - an [m x 1] numpy array
                temperature at altitude
            drivers - a dictionary with the following keys
                datetime: the date and time as a python datetime object
                f107: daily f10.7 flux for previous day
                f107a: 81 day average of f10.7 flux (centered on date)
                ap: magnetic index containing:
                (1) daily AP
                (2) 3 HR AP index for current time
                (3) 3 HR AP index for 3 hours before current time
                (4) 3 HR AP index for 6 hours before current time
                (5) 3 HR AP index for 9 hours before current time
                (6) Average of eight 3 hour AP indicies from 12 to 33 hrs prior to current time
                (7) Average of eight 3 hour AP indicies from 36 to 57 hrs prior to current time
    """
    # * :func:`msispy.msisFort.gtd7`
        # * **INPUTS**:
        #   * **IYD** - year and day as YYDDD (day of year from 1 to 365 (or 366)) (Year ignored in current model)
        #   * **SEC** - UT (SEC)
        #   * **ALT** - altitude (KM)
        #   * **GLAT** - geodetic latitude (DEG)
        #   * **GLONG** - geodetic longitude (DEG)
        #   * **STL** - local aparent solar time (HRS; see Note below)
        #   * **F107A** - 81 day average of F10.7 flux (centered on day DDD)
        #   * **F107** - daily F10.7 flux for previous day
        #   * **AP** - magnetic index (daily) OR when SW(9)=-1., array containing:
        #       * (1) daily AP
        #       * (2) 3 HR AP index FOR current time
        #       * (3) 3 HR AP index FOR 3 hrs before current time
        #       * (4) 3 HR AP index FOR 6 hrs before current time
        #       * (5) 3 HR AP index FOR 9 hrs before current time
        #       * (6) average of height 3 HR AP indices from 12 TO 33 HRS prior to current time
        #       * (7) average of height 3 HR AP indices from 36 TO 57 HRS prior to current time
        #   * **MASS** - mass number (only density for selected gass is calculated.  MASS 0 is temperature.
        #     MASS 48 for ALL. MASS 17 is Anomalous O ONLY.)
        # * **OUTPUTS**:
        #   * **D(1)** - HE number density(CM-3)
        #   * **D(2)** - O number density(CM-3)
        #   * **D(3)** - N2 number density(CM-3)
        #   * **D(4)** - O2 number density(CM-3)
        #   * **D(5)** - AR number density(CM-3)
        #   * **D(6)** - total mass density(GM/CM3)
        #   * **D(7)** - H number density(CM-3)
        #   * **D(8)** - N number density(CM-3)
        #   * **D(9)** - Anomalous oxygen number density(CM-3)
        #   * **T(1)** - exospheric temperature
        #   * **T(2)** - temperature at ALT

    # **INPUT**:
    # * mydatetime: python datetime object (defaults to last tabulated value)

    # * **OUTPUT**:
    # * dictOut: a dictionnary containing:
    # * datetime: the date and time as a python datetime object
    # * f107: daily f10.7 flux for previous day
    # * f107a: 81 day average of f10.7 flux (centered on date)
    # * ap: magnetic index containing:
    # * (1) daily AP
    # * (2) 3 HR AP index for current time
    # * (3) 3 HR AP index for 3 hours before current time
    # * (4) 3 HR AP index for 6 hours before current time
    # * (5) 3 HR AP index for 9 hours before current time
    # * (6) Average of eight 3 hour AP indicies from 12 to 33 hrs prior to current time
    # * (7) Average of eight 3 hour AP indicies from 36 to 57 hrs prior to current time
    # # Get the F10.7 and AP values for the current year
    #Sanity check inputs
    reference_shape = lat.flatten().shape

    if lon.flatten().shape != reference_shape or alt.flatten().shape != reference_shape:
        raise RuntimeError('Latitude, Longitude and Altitude arrays must be same shape!')

    #Handle manual vs. date lookup driver input
    if dt is not None: #If user has given a date use that to look up drivers
        realdrivers = getF107Ap(dt)
        #Pull the nessecary values so we don't break the logic
        if f107 is None:
            f107 = realdrivers['f107']
        if ap_daily is None:
            ap_daily = realdrivers['ap'][0] #daily
    else:
        if f107 is None or ap is None:
            raise RuntimeError('Please specify either (1) A datetime for driver lookup (dt=datetime.datetime), or (2) F10.7 and Daily AP values (f107=float,ap=float)')
        # Warn user if they are using no date and no historical driver info
        if f107a is None and ap3 is None and ap33 is None and ap36 is None and ap39 is None and apa1233 is None and apa3657 is None:
            print("--Warning! By not entering a date, and not specifing any of the historical/average drivers\n")
            print("--MSIS will be run with the following 'approximations'\n")
            print("--81 day average F10.7 = User given F10.7 (no seasonality!)\n")
            print("--3 HR AP history at t minus 3, 6, 9 12-33 hr average and 36-57 hr average set to user given daily AP!\n")

        # Create some fake 'realdrivers' by replicating the user's f10.7 and daily ap inputs into all of the average/historical value slots
        #
        realdrivers = dict()
        realdrivers['datetime']=None
        realdrivers['f107']=f107
        realdrivers['f107a']=f107
        realdrivers['ap']=[ap for i in range(7)]

    drivers = dict()

    #Create the model drivers based on what the user has filled out (and left blank)
    #I know the ternery operators are a little confusing, but it's so much eaiser to read
    drivers['f107'] = f107 if f107 is not None else realdrivers['f107']
    drivers['f107a'] = f107a if f107a is not None else realdrivers['f107a']
    drivers['ap_daily'] = ap_daily
    drivers['ap']=realdrivers['ap']
    drivers['dt']=dt
    drivers['ap'][0] = ap_daily if ap_daily is not None else realdrivers['ap'][0]
    drivers['ap'][1] = ap3 if ap3 is not None else realdrivers['ap'][1]
    drivers['ap'][2] = ap33 if ap33 is not None else realdrivers['ap'][2]
    drivers['ap'][3] = ap36 if ap36 is not None else realdrivers['ap'][3]
    drivers['ap'][4] = ap39 if ap39 is not None else realdrivers['ap'][4]
    drivers['ap'][5] = ap1233 if apa1233 is not None else realdrivers['ap'][5]
    drivers['ap'][6] = ap3657 if apa3657 is not None else realdrivers['ap'][6]

    npts = len(lat.flatten())
    temp = numpy.empty((npts,1))
    temp.fill(numpy.nan)
    #Preallocate for speed
    species = OrderedDict((('HE',temp.copy()), ('O',temp.copy()), ('N2',temp.copy()),('O2',temp.copy()),
     ('AR',temp.copy()),('mass',temp.copy()),('H',temp.copy()),('N',temp.copy()),('AO',temp.copy())))
    units, descriptions = OrderedDict(),OrderedDict()

    t_exo = temp.copy()
    t_alt = temp.copy()

    #Parse out the date and time
    #(2 digit year + 3 digit day of year as an integer) (yes...really)
    ydstr = "%.2d%.3d" % (numpy.mod(dt.year,100),dt.timetuple().tm_yday)
    iyd = int(ydstr)
    #UT second of day
    sec = (dt-datetime.datetime.combine(dt.date(),datetime.time(0))).total_seconds()
    for p in range(npts):
        slt = sec/3600.+lon.flatten()[p]/15. #Lazy compute local solar time for now
        d,t = gtd7(iyd,sec,alt.flatten()[p],lat.flatten()[p],lon.flatten()[p],\
                    slt,drivers['f107'],drivers['f107a'],drivers['ap'],48)
        for i,atom in enumerate(species):
            species[atom][p,0] = d[i]
            if d[i] < 0.:
                print("Warning: negative values output by msis!")
        t_exo[p] = t[0]
        t_alt[p] = t[1]

    for atom in species:
        if atom != 'mass':
            units[atom] = '#/cm^3'
            descriptions[atom] = "%s Number Density" % (atom)
        else:
            units[atom] = 'gm/cm^3'
            descriptions[atom] = 'Total Mass Density'
    descriptions['T_exo'],units['T_exo'] = 'Temperature at Exobase','K'
    descriptions['T'],units['T'] = 'Temperature','K'
    return species, t_exo, t_alt, units, descriptions, drivers

