# Helper functions for lla 2 enu and enu 2 lla conversions
from math import sin, cos, sqrt, atan2

class GpsUtils(object):

    def __init__(self):
        self.a = 6378137.00                 # WGS-84 Earth semimajor axis (m)
        self.b = 6356752.31424518           # WGS-84 Eath semiminor axis (m)
        self.f = 0.0033528219061245246      # Ellipsoid Flatness
        self.e = 0.0818191908426391         # Ellipsoid Eccentricity
        self.e2 = 0.006694379990144198      # Square of Eccentricity
        self.ep = 0.0820944379496945        # Polar eccentricity
        self.pi = 3.14159265359             # Pi

    def deg2rad(self,deg):
        rad_ang = deg * self.pi / 180
        return rad_ang


    def rad2deg(self,rad):
        deg_ang = rad *180 / self.pi
        return deg_ang


    def lla2ecef(self, lla):
        #converts LLA to ECEF coordinates
        # lla = [ lat, lon, alt] (MSL)
        phi = self.deg2rad(lla[0])
        lmda = self.deg2rad(lla[1])
        h = lla[2]
        n = self.a / sqrt(1 - self.e2 * (sin(phi))**2)
        x = (h + n) * cos(phi) * cos(lmda)
        y = (h + n) * cos(phi) * sin(lmda)
        z = (((self.b)**2/(self.a)**2) * n + h) * sin(phi)
        ecef = [x, y, z]
        return ecef


    def enu2ecef(self,obj_enu,ref_lla):
        # Converts object enu position with respect to a reference lat, long,
        # alt, into stand-alone ECEF coordinates
        phi = self.deg2rad(ref_lla[0])
        lmda = self.deg2rad(ref_lla[1])
        alt = ref_lla[2]

        ref_ecef = self.lla2ecef(ref_lla)
        obj_x = obj_enu[0]
        obj_y = obj_enu[1]
        obj_z = obj_enu[2]

        x = -sin(lmda) * obj_x - sin(phi) * obj_y + cos(phi) * cos(lmda) * obj_z + ref_ecef[0]
        y = cos(lmda) * obj_x - sin(phi) * sin(lmda) * obj_y + cos(phi) * sin(lmda) * obj_z + ref_ecef[1]
        z = cos(phi) * obj_y + sin(phi) * obj_z + ref_ecef[2]
        ecef = [x, y, z]
        return ecef


    def ecef2lla(self, tgt_ecef):
        # this converts ECEF position to lat long alt
        # tgt_ecef = [ x, y, z ]
        a = self.a
        e2 = self.e2
        x = tgt_ecef[0]
        y = tgt_ecef[1]
        z = tgt_ecef[2]
        p = sqrt(x**2 + y**2)

        tgt_lon = atan2(y,x)
        tgt_lat = atan2( z , p*(1-e2))
        #iterative solution
        for i in range(0,5):
            n = a / sqrt(1-e2*(sin(tgt_lat))**2)
            tgt_alt = p / cos(tgt_lat) - n
            tgt_lat = atan2( z, p*(1 - (e2)*n / (n + tgt_alt)))
        tgt_lat_deg = self.rad2deg(tgt_lat)
        tgt_lon_deg = self.rad2deg(tgt_lon)
        tgt_lla = [tgt_lat_deg, tgt_lon_deg, tgt_alt]
        return tgt_lla
