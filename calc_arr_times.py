#!/usr/bin/env python3

import glob
import matplotlib.pyplot as plt
import obspy
from obspy import read
from obspy.core import Stream
import os
import shutil


CWD = os.getcwd()
BAD_EVENTS_PATH = f"{CWD}/bad_events"


def main():
    # Event directory paths
    evdirs = [evdir for evdir in glob.glob(f"{CWD}/??????????????") if os.path.isdir(evdir)]

    for event in evdirs:
        print(f"*** {event.split('/')[-1]} ***")

        # Get stream with event traces prepared for stacking
        event_stream = prepared_event_stream(event)

        # 1st stack
        try:
            stack1 = event_stream.copy().stack(stack_type=('root', 2), npts_tol=2)  # TODO: use pw stacking
        except ValueError as e:  # Skip event if npts for each trace too different
            print(f"Skipping event as bad: {e}")
            shutil.move(event, BAD_EVENTS_PATH)
            continue

        stack1.plot()


def prepared_event_stream(event_path):
    """
    Read in each trace of an event, prepare trace for stacking (cut around t0,
    normalize), and return as prepared stream.

    Args:
        event_path: path to event directory
    """
    seislist = glob.glob(f"{event_path}/*HZ")
    stream = Stream()

    for sac_file in seislist:
        st = read(sac_file)
        # Ensure only 1 trace read from sac_file, skip file otherwise
        if len(st) != 1:
            print(f"{len(st)} traces in {sac_file.split('/')[-1]}! Expected 1.")
            continue
        prep_trace(st[0])
        stream += st

    # stream.plot(size=(800,700))
    return stream


def prep_trace(tr):
    """
    Prepare trace for stacking.

    Set sampling rate at 40Hz, cut around t0 to 60s, normalize.

    Args:
        tr: obspy trace object
    """
    tr.decimate(2)
    tr.interpolate(sampling_rate=40.0)
    tr.taper(max_percentage=0.3)

    # Ensure scaling of each trace is equal so can be stacked
    if tr.stats.calib != 1.0:
        tr.stats.calib = 1.0
        # del tr.stats.sac['scale']

    cut_trace_around_t0(tr)
    tr.normalize()
    # tr.plot()


def cut_trace_around_t0(tr, pre_t0=30, post_t0=30, pad=True):
    """
    Cut trace around t0

    Args:
        tr: obspy trace object
        pre_t0: time in seconds before t0 to cut
        post_t0: time in seconds after t0 to cut
    """
    t0 = tr.stats.sac["t0"]
    b = tr.stats.sac["b"]
    e = tr.stats.sac["e"]
    t_start = tr.stats.starttime + t0 - b - pre_t0
    t_end = tr.stats.endtime + t0 - e + post_t0
    tr.trim(t_start, t_end, pad=pad)


if __name__ == "__main__":
    if not os.path.exists(BAD_EVENTS_PATH):
        os.mkdir(BAD_EVENTS_PATH)

    main()
    print("Run finished.")
