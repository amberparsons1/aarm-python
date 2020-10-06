# aarm-python

This tool implements the absolute arrival-time recovery method (AARM) as developed in Boyce et al. (2017)**[1]**. It is written in python based off the bash tool developed alongside the paper **[2]**.

This python tool is only an **initial prototype** with currently limited implementation as detailed below.

## Requirements
* Python 3 (only tested in version 3.7.3 on a macOS system)
* Dependencies in requirements.txt (install with `pip install -r /path/to/requirements.txt`)
* SAC data files formatted as detailed in the 'AARM code user guide' accompanying the bash tool (Section 2)

## Using the tool
Navigate inside the directory containing the event directories (e.g EXAMPLE_DATA). Run script calc_arr_times.py.

This will:
1. Get the event directory paths
1. For each event:
   1. Create a prepared event stream ready to stack: each trace is read in, cut around their alignment point t0 to 60 s, and normalized.
   1. Form 1st stack (nth-root method) and plot.

Implementing creating the 2nd stack and interactive picking to calculate absolute arrival-times is yet to be done.


## TODOs/Cautions of current implementation
* Stacking is done using nth-root method. Phase-weight stacking is preferred and should work using the obspy Stream.stack method (replacing the current stack_type argument '('root', 2)' with '('pw', 4))'. However this seems to produce no stack data (unless pw order is 0 - corresponding to linear stacking). Root stacking is instead used in the meantime.
* After preparing and cutting a trace around t0 ready for stacking (prep_trace), the number of points in the trace (npts) is not always the same for each trace within an event. A tolerance (npts_tol) is specified for stacking which cuts the traces to match the shortest's length, enabling stacking. If the number of points to cut is greater than the tolerance an error is thrown and processing of the particular event is not continued (the event being moved into bad_events). This should be fixed so a tolerance is not needed, the preparation steps having ensured each trace is the same length.


### References
1. Boyce et al. (2017), 'From Relative to Absolute Teleseismic Travel Times: The Absolute Arrival-Time Recovery Method (AARM)', _Bulletin of the Seismological Society of America_, 107(5), pp. 2511–2520.
2. https://github.com/alistairboyce11/AARM
