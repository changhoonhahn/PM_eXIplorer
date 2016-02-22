import os 
import stat
import numpy as np

import matplotlib.pyplot as plt 
from scipy.interpolate import interp1d

from defutility.plotting import prettyplot
from defutility.plotting import prettycolors


def BashCPM(nside=128, rcube=64, nstep=20, ngrid=256, z_init=19): 
    ''' Write out executable Bash script with input parameters

    Parameters
    ----------
    nside : int
        Number of particles is (nside)^3

    rcube : int
        Length of box side. 

    nstep : int
        Number of time steps to take 

    ngrid : int
        FFT grid size (force resolution)

    z_init : initial redshift 

    '''
    bash_file = ''.join([
        'sh.2pcf_cpm_',
        'nside', str(nside), '_',
        'rcube', str(rcube), '_', 
        'nstep', str(nstep), '_', 
        'ngrid', str(ngrid), '_', 
        'zinit', str(z_init)
        ])

    bash_f = open(bash_file, 'w')

    a_start = round(1./(z_init + 1.),2)

    bash_content = '\n'.join([
        "#! /bin/csh -f",
        "set echo",
        "set pp = /home/users/tinker/exec",
        "",
        "##VARIABLES FOR RANFIELD_CDM",
        "",
        "set nside = "+str(nside)+" # number of particles ^(1/3)",
        "set rcube = "+str(rcube)+" # size of box in Mpc/h",
        "set h0 = "+str(h0),
        "set omega_m = 1",
        "set omega_l = 0",
        "set omega_b = 0.045",
        "set gamma = 0.2 # this does not matter",
        "set n = 0.96 # spectral index",
        "set rsm = 0",
        "set rgauss = 0",
        "set rtophat = 8",
        "set sig8 = 0.82",
        "set iseed = -$1",
        "set itrans = 5 # Eisenstein & Hu 1998",
        "",
        "##VARIABLES FOR CPMFFTW",
        "",
        "set nsteps = "+str(nstep),
        "set ngrid = "+str(ngrid)+" # size of grid (per side) for FFT",
        "set astart = "+str(a_start)+" # starting expansion factor (if a0=1)",
        "set z_init = "+str(z_init)+" # starting redshift (must be 1/astart-1)",
        "",
        "",
        "if ( 1 ) then ",
        "$pp/test_ranphfldb $nside $rcube $h0 $n $rsm $itrans $rgauss $rtophat $sig8 $iseed $omega_m $omega_b > cdm.out",
        "",
        "echo $rcube > a01",
        "echo $ngrid > a02",
        "echo $nside > a03",
        "echo $omega_m > a04",
        "echo $omega_l > a05",
        "echo $z_init > a06",
        "echo $nsteps > a07",
        "echo 19 5 3 1 0.5 0 > a08",
        "cat a?? > cpm.bat",
        "rm -f a??",
        "",
        "",
        "#",
        "#the last line is all the redshifts for output",
        "#",
        "#cp /a/osu2782/cosmo/wisdomfiles/wisdom1800 ./wisdom",
        "",
        "$pp/cpm cpm.bat $nside < cdm.out",
        "",
        "endif",
        "",
        "set i = 1",
        "while ( $i <= 6 ) ",
        "$pp/sample_ff 100000 555 < out.0$i > output/ascii.nside$nside.rcube$rcube.nstep$nstep.ngrid=$ngrid.zinit$z_init.0$i", 
        "$pp/covar3 0.1 20 15 "+str(rcube)+" 0 "+str(rcube)+" 1 output/ascii.nside$nside.rcube$rcube.nstep$nstep.ngrid=$ngrid.zinit$z_init.0$i a 0 1 auto > output/xi.nside$nside.rcube$rcube.nstep$nstep.ngrid=$ngrid.zinit$z_init.0$i", 
        "@ i = $i + 1",
        "end",
        "",
        "",
        "exit",
        ])

    bash_f.write(bash_content)
    bash_f.close()
    
    st = os.stat(bash_file)
    os.chmod(bash_file, st.st_mode | stat.S_IEXEC)
    
    return None

def RunBashCPM(nside=128, rcube=64): 
    ''' Execute CPM bash script
    '''
    bash_file = ''.join([
        'sh.2pcf_cpm_',
        'nside', str(nside), '_',
        'rcube', str(rcube), '_', 
        'nstep', str(nstep), '_', 
        'ngrid', str(ngrid), '_', 
        'zinit', str(z_init)
        ])

    bash_cmd = './'+bash_file
    os.system(bash_cmd)

    return bash_cmd
