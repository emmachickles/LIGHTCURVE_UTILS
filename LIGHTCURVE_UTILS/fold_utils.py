import numpy as np

def phase_fold(t, P, t0=0, centr_0=False):
    t = t - t0
    phases = (t % P) / P
    if centr_0:
        inds = np.nonzero(phases > 0.5)
        phases[inds] += -1
    return phases

def binning(t,y,dy,P,t0=0,N=500,cycles=3,median=False):

    # remove nans
    inds = np.nonzero(~np.isnan(y))
    t, y, dy = t[inds], y[inds], dy[inds]
    
    binned_LC=[]
    mean_phases=np.linspace(0,1-1/N,N)
    phases=phase_fold(t, P, t0)
    lightcurve=np.array((phases,y,dy)).T
    lightcurve=lightcurve[np.argsort(lightcurve[:,0])]
    for i in mean_phases:
        lightcurve_bin=lightcurve[lightcurve[:,0]>i]
        lightcurve_bin=lightcurve_bin[lightcurve_bin[:,0]<i+1/N]

        if len(lightcurve_bin) == 0:
            print('No data points in phase bin! This phase will have nan flux.')
        weights=1/(lightcurve_bin[:,2]**2)
        if median:
            weighted_mean_flux = np.median(lightcurve_bin[:,1])
        else:
            weighted_mean_flux=np.sum(lightcurve_bin[:,1]*weights)/np.sum(weights)
        weighted_mean_flux_error=np.sqrt(1/np.sum(weights))
        binned_LC.append((i+0.5/N,weighted_mean_flux,weighted_mean_flux_error))
    binned_LC=np.array(binned_LC)
    # binned_LC[:,2]=binned_LC[:,2]/np.nanmedian(binned_LC[:,1])
    # binned_LC[:,1]=binned_LC[:,1]/np.nanmedian(binned_LC[:,1])    

    if cycles==1:
        binned_LC=binned_LC
    elif cycles==2:
        binned_LC2=np.array((binned_LC[:,0]-1,binned_LC[:,1],binned_LC[:,2])).T
        binned_LC=np.vstack((binned_LC2,binned_LC))
    elif cycles==3:
    	binned_LC2=np.array((binned_LC[:,0]-1,binned_LC[:,1],binned_LC[:,2])).T
    	binned_LC3=np.array((binned_LC[:,0]+1,binned_LC[:,1],binned_LC[:,2])).T
    	binned_LC=np.vstack((binned_LC2,binned_LC))    
    	binned_LC=np.vstack((binned_LC,binned_LC3))  	

    return binned_LC
