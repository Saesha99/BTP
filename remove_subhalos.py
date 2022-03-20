import h5py
import numpy as np
import sys
from scipy.spatial import KDTree
import mass_from_peakhieght as mfp

fname = sys.argv[1]

cosmo = fname.split("_l")[0].split("/c")[-1]
a = 1
massval, nubins = mfp.nutomass(cosmo, a)


with h5py.File(fname, "r") as fin:

     Lbox = float(fname.split("_l")[-1].split("_")[0])
     #print(fin.keys())
     print(Lbox)

     pos = np.array(fin["x"])
     mass = np.array(fin["M200m_bnd_cat"])
     radius = np.array(fin["R200m_bnd_cat"])
     print(len(pos))
     
     '''idxx = (mass>massval[mmin]) & (mass<massval[mmax])
     pos = pos[idxx]
     mass = mass[idxx]
     radius = radius[idxx]
     print (len(pos))'''
     
     sort_key = mass.argsort()
     
     m_rs = mass[sort_key[::-1]]
     r_rs = radius[sort_key[::-1]] /1000
     pos_rs = pos[sort_key[::-1]] * a 
     #print(m_rs, r_rs)
     #print(pos_rs)
     #check sorting
     #j = 407
     #print(m_rs[j], r_rs[j], pos_rs[j])
     
     #i = np.where(mass == m_rs[j])
     #print(mass[i], radius[i], pos[i])
     '''i = 0
     T = KDTree(pos_rs)
     idx = T.query_ball_point(pos_rs[i],r=r_rs[i])
     print(len(pos),len(pos_rs[idx]))
     print(idx)
     print(idx[1:])
     
     m_rs = np.delete(m_rs, idx[1:])
     r_rs = np.delete(r_rs, idx[1:])
     pos_rs = np.delete(pos_rs, idx[1:])
     print(len(mass), len(m_rs))'''
     length = len(m_rs)
     print(length)
     for i in range(0,2):
     	if i < len(m_rs):
     	   print(i)
     	   #print(pos_rs)
     	   #print(pos_rs[i])
     	   
     	   T = KDTree(pos_rs)
     	   idx = T.query_ball_point(pos_rs[i],r=r_rs[i], return_sorted=True)
     	   print(len(idx))
     	   print(idx)
     	   #if len(idx) == 1:
     	   #	break
     	   #print(idx)
     	   
     	   m_rs = np.delete(m_rs, idx[1:])
     	   r_rs = np.delete(r_rs, idx[1:])
     	   pos_rs = np.delete(pos_rs, idx[1:], 0)
     	   print(len(m_rs))
     	
     	else:
     	   break
     	
     
