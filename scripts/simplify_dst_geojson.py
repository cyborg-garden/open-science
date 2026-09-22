#!/usr/bin/env python3
"""Simplify the Stats NZ regional GeoJSON for the dashboard.
Pure-python Douglas-Peucker per ring; drop attribute bloat; keep topological shape adequate for a choropleth at national zoom."""
import json, math

TOL = 0.005  # degrees (~500m) — fine for national-scale choropleth

def perp_dist(pt, a, b):
    (x, y), (x1, y1), (x2, y2) = pt, a, b
    dx, dy = x2 - x1, y2 - y1
    if dx == dy == 0:
        return math.hypot(x - x1, y - y1)
    t = ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))
    return math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))

def dp(points, tol):
    if len(points) <= 2:
        return points
    dmax, idx = 0, 0
    for i in range(1, len(points) - 1):
        d = perp_dist(points[i], points[0], points[-1])
        if d > dmax:
            dmax, idx = d, i
    if dmax > tol:
        left = dp(points[:idx + 1], tol)
        right = dp(points[idx:], tol)
        return left[:-1] + right
    return [points[0], points[-1]]

def simplify_coords(coords, tol):
    """Handle arbitrary Polygon/MultiPolygon nesting: at each level, if the
    first element's first element is a number, this level is a ring of points."""
    if isinstance(coords[0][0], (int, float)):
        return dp(coords, tol)
    return [simplify_coords(c, tol) for c in coords]

src = json.load(open('/opt/data/dst_dashboard/nz_regions_raw.geojson'))
feats = []
for f in src['features']:
    raw_name = f['properties']['REGC2023_V1_00_NAME']
    if raw_name == 'Area Outside Region':
        continue
    name = raw_name.replace(' Region', '')
    feats.append({
        "type": "Feature",
        "properties": {"name": name, "id": f['properties']['REGC2023_V1_00']},
        "geometry": {"type": f['geometry']['type'],
                      "coordinates": simplify_coords(f['geometry']['coordinates'], TOL)}
    })

out = {"type": "FeatureCollection", "features": feats}
with open('/opt/data/dst_dashboard/nz_regions_simple.geojson', 'w') as fo:
    json.dump(out, fo, separators=(',', ':'))
import os
print(f"features: {len(feats)}")
print(f"raw size: {os.path.getsize('/opt/data/dst_dashboard/nz_regions_raw.geojson')/1e6:.1f} MB")
print(f"simple size: {os.path.getsize('/opt/data/dst_dashboard/nz_regions_simple.geojson')/1e3:.0f} KB")
print(f"total points: {sum(len(str(f['geometry']['coordinates']).split(',')) for f in feats)}")