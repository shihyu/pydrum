#!/usr/bin/env python3
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    moving_average = 0
    if len(sys.argv) > 2:
        moving_average = int(sys.argv[2])

    with open(sys.argv[1], "r", newline="") as f:
        reader = csv.reader(f)
        reader.__next__()
        if moving_average > 0:
            window = [0.0] * moving_average
        x = []
        y = []
        for row in reader:
            # if 8.5 < float(row[0]) < 10.0:
            x.append(float(row[0]))
            if moving_average:
                window.pop(0)
                window.append(float(row[1]))
                y.append(sum(window) / moving_average)
            else:
                y.append(float(row[1]))
        x = np.array(x)
        y = np.array(y)
        plt.plot(x, y)
        
        # peak detection
        peak_pos = signal.argrelmax(y, order=3)[0]
        peak_pos = peak_pos[y[peak_pos] > 100]
        plt.vlines(x[peak_pos], 0, np.max(y) + 100, colors='r')

        last_change = 0.0
        last_intensity = 0.0
        for t, intensity, in zip(x, y):
            change = intensity - last_intensity
            # if intensity > 100 and changes[0] >= 0 and changes[1] >= 0 and changes[2] <= 0 and changes[3] <= 0:
            #if intensity > 150 and last_change >= 0 and change <= 0: # peak recognized
            #    plt.annotate(str(intensity), xy=(t, last_intensity))
            last_intensity = intensity
            last_change = change

        if len(sys.argv) > 3:
            plt.savefig(sys.argv[3])
        else:
            plt.show()
