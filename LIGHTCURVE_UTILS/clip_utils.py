import numpy as np

def clip_iqr(t, y, dy, pos_iqr=3, neg_iqr=10):
    t, y, dy = t[~np.isnan(y)], y[~np.isnan(y)], dy[~np.isnan(y)]
    
    q3, q1 = np.percentile(y, [75 ,25])
    iqr=(q3-q1)/2

    good_idx=(y-np.median(y))<pos_iqr*iqr # !! 3 
    t=t[good_idx]
    dy=dy[good_idx]
    y=y[good_idx]

    good_idx=(np.median(y)-y)<neg_iqr*iqr
    t=t[good_idx]
    dy=dy[good_idx]
    y=y[good_idx]

    good_idx=dy>0
    t=t[good_idx]
    y=y[good_idx]
    dy=dy[good_idx]

    return t, y, dy

def clip_err(t, y, dy, ensig=5):
    avg = np.nanmean(dy)
    sig = np.nanstd(dy)

    good_idx = np.nonzero( np.abs(dy-avg) < ensig*sig )
    t, y, dy = t[good_idx], y[good_idx], dy[good_idx]

    return t, y, dy
