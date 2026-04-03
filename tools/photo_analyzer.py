#!/usr/bin/env python3
"""
photo_analyzer.py

Extracts EXIF metadata (timestamp, GPS coordinates) from photos to build
a relationship timeline and identify frequently visited locations.

Usage:
    python3 photo_analyzer.py --dir <photo_dir> --output <output_path>
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def get_exif_data(image_path: str) -> dict:
    """Extract EXIF data from a single image."""
    if not HAS_PIL:
        return {'error': 'Pillow is not installed. Cannot read EXIF.'}
    
    try:
        img = Image.open(image_path)
        exif_raw = img._getexif()
        if not exif_raw:
            return {}
        
        exif = {}
        for tag_id, value in exif_raw.items():
            tag = TAGS.get(tag_id, tag_id)
            exif[tag] = value
        
        result = {
            'file': os.path.basename(image_path),
            'path': image_path,
        }
        
        # Date taken
        date_taken = exif.get('DateTimeOriginal') or exif.get('DateTime')
        if date_taken:
            result['date_taken'] = str(date_taken)
        
        # GPS Info
        gps_info = exif.get('GPSInfo')
        if gps_info:
            gps_data = {}
            for key in gps_info:
                decode = GPSTAGS.get(key, key)
                gps_data[decode] = gps_info[key]
            
            if 'GPSLatitude' in gps_data and 'GPSLongitude' in gps_data:
                lat = _convert_to_degrees(gps_data['GPSLatitude'])
                lon = _convert_to_degrees(gps_data['GPSLongitude'])
                if gps_data.get('GPSLatitudeRef') == 'S':
                    lat = -lat
                if gps_data.get('GPSLongitudeRef') == 'W':
                    lon = -lon
                result['gps'] = {'lat': lat, 'lon': lon}
        
        return result
    except Exception as e:
        return {'file': os.path.basename(image_path), 'error': str(e)}


def _convert_to_degrees(value):
    """Convert GPS coordinates to decimal degrees."""
    d, m, s = value
    return float(d) + float(m) / 60 + float(s) / 3600


def main():
    parser = argparse.ArgumentParser(description='Photo Metadata Analyzer')
    parser.add_argument('--dir', required=True, help='Directory containing photos')
    parser.add_argument('--output', required=True, help='Output markdown file path')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.dir):
        print(f"Error: Directory does not exist: {args.dir}", file=sys.stderr)
        sys.exit(1)
    
    image_exts = {'.jpg', '.jpeg', '.png', '.heic', '.heif'}
    photos = []
    
    for root, dirs, files in os.walk(args.dir):
        for fname in sorted(files):
            if Path(fname).suffix.lower() in image_exts:
                fpath = os.path.join(root, fname)
                exif = get_exif_data(fpath)
                photos.append(exif)
    
    # Sort by date
    dated_photos = [p for p in photos if p.get('date_taken')]
    dated_photos.sort(key=lambda x: x['date_taken'])
    undated_photos = [p for p in photos if not p.get('date_taken')]
    
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(f"# Photo Timeline Analysis\n\n")
        f.write(f"Scanned directory: {args.dir}\n")
        f.write(f"Total photos: {len(photos)}\n")
        f.write(f"With timestamp: {len(dated_photos)}\n")
        f.write(f"With GPS data: {len([p for p in photos if p.get('gps')])}\n\n")
        
        if dated_photos:
            f.write("## Timeline\n\n")
            for p in dated_photos:
                line = f"- **{p['date_taken'][:10]}** — {p['file']}"
                if p.get('gps'):
                    line += f" (GPS: {p['gps']['lat']:.4f}, {p['gps']['lon']:.4f})"
                f.write(line + "\n")
            f.write("\n")
        
        if undated_photos:
            f.write(f"## Photos without timestamp ({len(undated_photos)})\n\n")
            for p in undated_photos:
                f.write(f"- {p.get('file', p.get('path', 'unknown'))}\n")
        
        if not HAS_PIL:
            f.write("\n⚠️ Pillow is not installed. Only file names are listed. Run: pip3 install Pillow\n")
    
    print(f"Analysis complete. Results written to {args.output}")


if __name__ == '__main__':
    main()
