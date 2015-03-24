NRL Mass Spectrometer and Incoherent Scatter Radar 2000 (NRLMSISE-00)
=====================================================================
---------------------------------------------------------------------

This model is maintained and developed by the Naval Research Laboratory, Space Science Division. Please visit 
<http://www.nrl.navy.mil/research/nrl-review/2003/atmospheric-science/picone/>

**SuperDARN's contribution consists of Python wrappers to this model. This contribution is covered under DaViTpy license.**
**The CU-SEDA contribution consists of making this model useable independent of DavitPy**

We have added some additional functionality to SuperDARNs wrapper which vectorizes the call to the model
and provides the return values in a dictionary with keys that name each variable. The interface is designed to 
generally useful as well as compatible with [AtModWeb](https://github.com/lkilcommons/atmodweb) and [AtModExplorer](https://github.com/lkilcommons/atmodexplorer)

The msispy.msis function is the vectorized interface. See it's source for more info.
