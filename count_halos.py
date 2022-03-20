import h5py
import numpy as np
import sys
import mass_from_peakhieght as mfp
from scipy.spatial import KDTree




fname = sys.argv[1]
counttype = int(sys.argv[2])
cosmo = fname.split("Data/c")[1].split("_")[0]
if cosmo=="pla":
   Om0 = 0.315
   h = 0.6731
elif cosmo=="bol":
   Om0 = 0.27
   h = 0.7
else:
   print(f"Cosmology {cosmo} not supported yet.")
   exit(11)
print(cosmo)
Lbox = float(fname.split("_l")[-1].split("_")[0])
a = float(fname.split("ria_")[-1].split(".hdf")[0])
print(Lbox,a)
     

def remove_subhalos(pos, mass, radius):
     sort_key = mass.argsort()
     
     m_rs = mass[sort_key[::-1]]
     r_rs = radius[sort_key[::-1]] /1000  # radius was in units of pkpc/h
     pos_rs = pos[sort_key[::-1]] * a     #position was in units of cMpc/h
     
     length = len(m_rs)
     print(length)
     for i in range(0,length):
     	print(i)
     	if i < len(m_rs):
     	   
     	   T = KDTree(pos_rs[i:])
     	   idx = T.query_ball_point(pos_rs[i],r=r_rs[i], return_sorted=True)
     	   print(len(idx))
     	   
     	   #print(idx)
     	   idx = np.array(idx) + i	
     	   #print(idx)	
     	   
     	   m_rs = np.delete(m_rs, idx[1:])
     	   r_rs = np.delete(r_rs, idx[1:])
     	   pos_rs = np.delete(pos_rs, idx[1:], 0)
     	   print(len(m_rs))
     	
     	else:
     	   break
     	   
     return(pos_rs, m_rs)   
     
     
     

mp = Om0 * Lbox**3 * 2.77 * 10**11 / 1024**3
#mp = round(Om0 * Lbox**3 * 2.77 / 1024**3, 2) * 10**11 
print("mp = %.2e" % mp)
mres = mp*100
print("mass resolution = %.2e" %mres)
#print(counttype)

with h5py.File(fname, "r") as fin:

     #print(fin.keys())
     pos = np.array(fin["x"])
     mass = np.array(fin["M200m_bnd_cat"])
     radius = np.array(fin["R200m_bnd_cat"])
     print(len(mass))
     pos, mass = remove_subhalos(pos, mass, radius)
     pos = pos/a
     
     
     
     if counttype == 1:
     	print("counting in mass resolution bins")
     	idx = (mass>mres) #& (mass<10**mmax)
     	print("halos above mres: %i" % np.sum(idx))
     
     	idx = (mass>mres) & (mass<mres*10)
     	print("0_1: %i" %np.sum(idx))
     
     	idx = (mass>mres) & (mass<mres*10**0.5)
     	print("0_0.5: %i" %np.sum(idx))
     
     	idx = (mass>mres*10**0.5) & (mass<mres*10**1)
     	print("0.5_1: %i" %np.sum(idx))
     
     	idx = (mass>mres*10**1) & (mass<mres*10**2)
     	print("1_2: %i" %np.sum(idx))
     
     	idx = (mass>mres*10**2) & (mass<mres*10**3)
     	print("2_3: %i" %np.sum(idx))
     
     elif counttype == 2:
     	print("counting in peakhieght bins")
     	mval, nubins = mfp.nutomass(cosmo, a)
     	print(mval)
     	print(len(mass))
     	for i in range(0,mval.size-1):
     	   idx = (mass>mval[i]) & (mass<mval[i+1])
     	   print(np.sum(idx))
     	

     	
     	
     	

    

     
