"""RS3 geometry and footer helpers retained from the prior raw-radar test."""
import math
import re
import struct

MARK = b'\x99\x99\xff\xff'
SITE_TAG = b'Site Data\x00'
MODES = {(7, 2), (7, 3)}  # Export-calibrated family only.


def dms(text):
    deg, minute, sec, direction = text.split()
    absolute = float(deg) + float(minute) / 60 + float(sec) / 3600
    return -absolute if direction in ('S', 'W') else absolute


def project(site, slant_range_nm, bearing):
    lat, lon, distance, az = map(math.radians, (*site, slant_range_nm / 60, bearing))
    lat2 = math.asin(math.sin(lat) * math.cos(distance) +
                     math.cos(lat) * math.sin(distance) * math.cos(az))
    lon2 = lon + math.atan2(math.sin(az) * math.sin(distance) * math.cos(lat),
                            math.cos(distance) - math.sin(lat) * math.sin(lat2))
    return math.degrees(lat2), math.degrees(lon2)


def distance_nm(a, b):
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    h = math.sin((lat2 - lat1) / 2) ** 2 + (
        math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 60 * math.degrees(2 * math.asin(math.sqrt(h)))


def unpack_site_footer(data, footer):
    # The footer stores each site in order, with length-prefixed strings.
    sites = []
    for found in re.finditer(re.escape(SITE_TAG), data[footer:]):
        offset = footer + found.end()
        fields = []
        pos = offset + 8
        for _ in range(4):
            n = struct.unpack_from('<I', data, pos)[0]
            assert 1 < n < 100 and data[pos + 3 + n] == 0
            fields.append(data[pos + 4:pos + 3 + n].decode('ascii'))
            pos += 4 + n
        alias, name, latitude, longitude = fields
        sites.append({'ordinal': len(sites), 'alias': alias, 'name': name,
                      'latitude_dms': latitude, 'longitude_dms': longitude,
                      'latlon': [dms(latitude), dms(longitude)], 'offset': offset - len(SITE_TAG)})
    return sites
