def BJDConvert(times, RA, Dec, date_format='mjd', telescope='Palomar',scale='tcb'):
    '''Function for converting a series of timestamps to Barycentric Julian
    Date format in Barycentric Dynamical time'''
    import numpy as np
    from astropy.time import Time
    from astropy.coordinates import EarthLocation
    from astropy.coordinates import SkyCoord  # High-level coordinates
    from astropy.coordinates import ICRS, Galactic, FK4, FK5, BarycentricTrueEcliptic  # Low-level frames
    from astropy.coordinates import Angle, Latitude, Longitude  # Angles
    import astropy.units as u

    # Create sky coordinate
    c = SkyCoord(RA,Dec, unit="deg")

    # Create Astropy Time object
    t = Time(times,format=date_format,scale='utc')

    # Convert to desired timescale
    if scale == 'tcb': # Barycentric Coordinate Time
        t2=t.tcb
    elif scale == 'tdb': # Barycentric Dynamical Time
        t2=t.tdb

    # Observatory location
    Observatory=EarthLocation.of_site(telescope)

    # Calculate light travel time to correct for motion of the Earth rel. barycenter
    delta=t2.light_travel_time(c,kind='barycentric',location=Observatory)

    # Add the light travel time
    BJD=t2+delta

    return BJD
