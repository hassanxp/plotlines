import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import csv
import matplotlib.ticker as ticker



def readfile():

    # Build the raw and mean values
    # Raw: each entry is a list of all measurements
    raw={'date':[], 's':[], 'd':[], 'h':[]}

    # Mean: each entry is a scalar value and std dev
    mean={'date':[], 's':[], 'd':[], 'h':[]}

    dates = []
    sis = []
    sis_err = []
    dia = []
    dia_err = []
    hrt = []
    hrt_err = []

    with open('data.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            date = dt.datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S').date()

            sis_list = []
            dia_list = []
            hrt_list = []
            for m in row[1:]:
                (s, d, h) = extract(m)
                sis_list.append(s)
                dia_list.append(d)
                hrt_list.append(h)

            dates.append(date)
            sis_arr = np.array(sis_list)
            sis.append(sis_arr.mean())
            sis_err.append(sis_arr.std())

            dia_arr = np.array(dia_list)
            dia.append(dia_arr.mean())
            dia_err.append(dia_arr.std())

            hrt_arr = np.array(hrt_list)
            hrt.append(hrt_arr.mean())
            hrt_err.append(hrt_arr.std())

    return dates, sis, sis_err, dia, dia_err, hrt, hrt_err


def plot_data(dates, sis, sis_err, dia, dia_err, hrt, hrt_err):

    fig, ax = plt.subplots()
    ax.errorbar(dates, sis, yerr=sis_err, label="S", fmt="-bo")
    ax.errorbar(dates, dia, yerr=dia_err, label="D", fmt='-go')
    ax.errorbar(dates, hrt, yerr=hrt_err, label="H", fmt='-ro')
    ax.legend(loc='best')
    ax.grid()

    fig.autofmt_xdate()
    plt.show()

def plot_from_file():
    (dates, sis, sis_err, dia, dia_err, hrt, hrt_err) = readfile()
    plot_data(dates, sis, sis_err, dia, dia_err, hrt, hrt_err)


def example():

    a=(
        ("2018-08-10T08:40:00", "120/80;80"),
        ("2018-08-11T22:40:00", "117/75;82")
    )

    dates=[]
    sis=[]
    dia=[]
    hrt=[]

    for b in a:

        d=dt.datetime.strptime(b[0], '%Y-%m-%dT%H:%M:%S').date()
        print(d.year, d.day)
        dates.append(d)
        (s, d, h) = extract(b[1])
        sis.append(s)
        dia.append(d)
        hrt.append(h)

    plot_data(dates, sis, dia, hrt)


def extract(value:str):

    s, rhs = value.split("/")
    d, h = rhs.split(";")

    return float(s), float(d), float(h)


def main():
    plot_from_file()




if __name__ == "__main__":
    main()