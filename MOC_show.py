from astropy.table import Table
from mocpy import MOC, WCS # World2ScreenMPL
from astropy.coordinates import Angle, SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt

import pdb
def read(moc_fitsfile):
    if moc_fitsfile is None:
        return None
    # or:
    # moc=MOC.from_fits(moc_fitsfile)
    return  MOC.load(moc_fitsfile, 'fits')
    

def draw(moc, moc1=None,border='intersection'):
    fig = plt.figure(111, figsize=(15, 15))

    wcs1=WCS(fig, fov=300* u.deg, center=SkyCoord(0, 0, unit='deg', frame='icrs'),
             coordsys="icrs", rotation=Angle(0, u.degree), projection="AIT") # "AIT"
    
    with wcs1 as wcs:
        ax = fig.add_subplot(1, 1, 1, projection=wcs)
    
        # Call fill giving the matplotlib axe and the 'astropy.wcs.WCS` object.
        # We will set the matplotlib keyword linewidth to 0 so that it does not plot
        # the border of each HEALPix cell.
        # The color can also be specified along with an alpha value.
        
        moc.fill(ax=ax, wcs=wcs, linewidth=0, alpha=0.5, fill=True, color="green")
        moc_union=moc
        if moc1:
            moc1.fill(ax=ax, wcs=wcs, linewidth=0, alpha=0.5, fill=True, color="blue")
            moc_union= moc1.union(moc1)
            
        moc_union.border(ax=ax, wcs=wcs, alpha=1, color="red")

    plt.xlabel('ra')
    plt.ylabel('dec')
    plt.grid(color="black", linestyle="dotted")
    plt.show(block=True)
    
def this_parser():
    import argparse
    parser = argparse.ArgumentParser(
                    prog = 'MOC_show',
                    description = 'Show the coverage of one or several MOC files')
    parser.add_argument('filename', nargs='+', help='MOC fits filename')           # positional arguments
    parser.add_argument('-b', '--border', choices=['intersection','union'], default='intersection')      # option that takes a value and limited choices
    #parser.add_argument('-v', '--verbose',
    #                    action='store_true')
    
    return parser

if __name__=='__main__':
    ## Enter filenames and option without command line;
    mypath="/home/mvannier/Euclid/SGS_SDC_Fr/SDC_France/Survey/"
    moc_ff1= mypath+"rsd2022g-wide-footprint-year-1-equ-order-13-moc.fits"
    moc_ff2= mypath+"rsd2022g-wide-footprint-year-2-equ-order-13-moc.fits"
    border='intersection'
    #border='union'
    try:
        myargs=this_parser()
        args=myargs.parse_args()
    except:
        print("No arguments in command line. Looking into the code __main__ section")
        args=myargs.parse_args(['--border',border,moc_ff1,moc_ff2])
    
    print("*******")

    moc1 =read(args.filename[0])
    if len(args.filename)==1:
        args.filename.append(None)
        
    #moc = moc1.intersection(read(moc_ff2))
    draw(moc1, read(args.filename[1]), border=args.border)
