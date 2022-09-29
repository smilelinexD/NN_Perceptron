import tkinter.ttk as ttk
import tkinter as tk
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
import numpy as np


def main():
    learnRate = float(learnrate_entry.get())
    N = int(cycle_entry.get())
    f = open('./NN_HW1_DataSet/' +
             explorer_comboboxText.get() + '.txt', 'r')
    stoprate = float(condition_entry.get())
    dim = 2
    w = []
    for i in range(0, dim + 1):
        w.append(random.randrange(-2, 2))
    lines = 0
    xs = []
    xmin = 100.0
    xmax = -100.0
    alltestcases_plot.clear()
    traincase_plot.clear()
    testcase_plot.clear()
    for l in f:
        lines += 1
        m = re.findall(r'-?\d+\.*\d*', l)
        # print(m)
        x = []
        x.append(-1.0)
        for i in range(0, dim):
            x.append(float(m[i]))
            xmin = min(float(m[i]), xmin)
            xmax = max(float(m[i]), xmax)
        d = int(m[dim])
        x.append(d)
        xs.append(x)
        xxx = float(m[0])
        y = float(m[1])
        d = int(m[2])
        if d == 1:
            alltestcases_plot.plot(xxx, y, 'x', color='red')
        else:
            alltestcases_plot.plot(xxx, y, 'o', color='blue')
    alltestcases_canvas.draw()
    alltestcases_label.configure(text='All test cases')
    # print(lines)
    random.shuffle(xs)

    if (explorer_comboboxText.get() == 'perceptron1') | (explorer_comboboxText.get() == 'perceptron2'):
        traincase = xs
        testcase = xs
    else:
        traincasesize = int(lines * 2 / 3)
        traincase = xs[0:traincasesize]
        testcase = xs[traincasesize + 1:]

    bestw = w
    bestrecrate = 0
    for n in range(0, N):
        wrong = 0
        i = -1
        random.shuffle(traincase)
        for x in traincase:
            res = 0.0
            i += 1
            for j in range(0, dim + 1):
                res += x[j] * w[j]

            d = x[dim + 1]
            if (res > 0) & (d == 1):
                wrong += 1
                for j in range(0, dim + 1):
                    w[j] -= learnRate * x[j]
                # print('n = {:d}, i = {:d}, wrong_time = {:d}'.format(
                #     n, i, wrong))
            elif (res <= 0) & (d != 1):
                wrong += 1
                for j in range(0, dim + 1):
                    w[j] += learnRate * x[j]
                # print('n = {:d}, i = {:d}, wrong_time = {:d}'.format(
                #     n, i, wrong))
        passed = 0
        random.shuffle(traincase)
        for x in traincase:
            res = 0.0
            for j in range(0, dim + 1):
                res += x[j] * w[j]
            d = x[dim + 1]
            if (res <= 0) & (d == 1):
                passed += 1
            elif (res > 0) & (d != 1):
                passed += 1
        if (explorer_comboboxText.get() == 'perceptron1') | (explorer_comboboxText.get() == 'perceptron2'):
            recrate = float(passed / lines)
        else:
            recrate = float(passed / traincasesize)
        if recrate - bestrecrate > 0.001:
            bestrecrate = recrate
            bestw = w
        if recrate >= stoprate:
            break
    if bestrecrate < stoprate:
        w = bestw
    # print(w)
    xmin = 100
    xmax = -100
    passed = 0
    for x in traincase:
        xx = float(x[1])
        yy = float(x[2])
        d = int(x[3])
        xmin = min(xx, xmin)
        xmax = max(xx, xmax)
        if d == 1:
            traincase_plot.plot(xx, yy, 'x', color='red')
            if (explorer_comboboxText.get() == 'perceptron1') | (explorer_comboboxText.get() == 'perceptron2'):
                testcase_plot.plot(xx, yy, 'x', color='red')
        else:
            traincase_plot.plot(xx, yy, 'o', color='blue')
            if (explorer_comboboxText.get() == 'perceptron1') | (explorer_comboboxText.get() == 'perceptron2'):
                testcase_plot.plot(xx, yy, 'o', color='blue')
        res = 0.0
        for j in range(0, dim + 1):
            res += w[j] * x[j]
        if (res <= 0) & (d == 1):
            passed += 1
        elif (res > 0) & (d != 1):
            passed += 1
    if (explorer_comboboxText.get() == 'perceptron1') | (explorer_comboboxText.get() == 'perceptron2'):
        recrate = float(passed / lines)
    else:
        recrate = float(passed / traincasesize)
    if abs(w[2]) <= 0.001:
        yy = [0, 1]
        if abs(w[1]) <= 0.001:
            xx = [0, 0]
        else:
            xx = [w[0] / w[1]] * 2
    else:
        xx = np.linspace(xmin - 1, xmax + 1, 10)
        if abs(w[1]) <= 0.001:
            yy = [w[0] / w[2]] * 10
        else:
            yy = (w[0] - w[1] * xx) / w[2]
    traincase_plot.plot(xx, yy)
    traincase_canvas.draw()
    traincase_label.configure(
        text='Train case :\nRecognition Rate = %.2f' % recrate)
    if (explorer_comboboxText.get() == 'perceptron1') | (explorer_comboboxText.get() == 'perceptron2'):
        testcase_plot.plot(xx, yy)
        testcase_canvas.draw()
        testcase_label.configure(
            text='Test case:\nRecognition Rate = %.2f' % recrate)

        weights_label.configure(text='Weights:[%.2f, %.2f, %.2f]' %
                                (w[0], w[1], w[2]))
    else:
        random.shuffle(testcase)
        xmin = 100
        xmax = -100
        passed = 0
        for x in testcase:
            xx = float(x[1])
            yy = float(x[2])
            d = int(x[3])
            xmin = min(xx, xmin)
            xmax = max(xx, xmax)
            if d == 1:
                testcase_plot.plot(xx, yy, 'x', color='red')
            else:
                testcase_plot.plot(xx, yy, 'o', color='blue')
            res = 0.0
            for j in range(0, dim + 1):
                res += w[j] * x[j]
            if (res <= 0) & (d == 1):
                passed += 1
            elif (res > 0) & (d != 1):
                passed += 1
        if (explorer_comboboxText.get() == 'perceptron1') | (explorer_comboboxText.get() == 'perceptron2'):
            recrate = float(passed / lines)
        else:
            recrate = float(passed / (lines - traincasesize))
        if abs(w[2]) <= 0.001:
            if abs(w[1]) <= 0.001:
                xx = [0, 0]
            else:
                xx = [w[0] / w[1]] * 2
        else:
            xx = np.linspace(xmin - 1, xmax + 1, 10)
            if abs(w[1]) <= 0.001:
                yy = [w[0] / w[2]] * 10
            else:
                yy = (w[0] - w[1] * xx) / w[2]
        testcase_plot.plot(xx, yy)
        testcase_canvas.draw()
        testcase_label.configure(
            text='Test case:\nRecognition Rate = %.2f' % recrate)

        weights_label.configure(text='Weights:[%.2f, %.2f, %.2f]' %
                                (w[0], w[1], w[2]))


window = tk.Tk()
window.title('123')
window.geometry('800x800')
window.configure(background='white')

header_label = tk.Label(window, text='Perceptron')
header_label.pack()

# 以下為 controlls_frame 群組
controlls_frame = tk.Frame(window)
controlls_frame.pack(side=tk.LEFT)

# 以下為 learnrate_frame 群組
learnrate_frame = tk.Frame(controlls_frame)
learnrate_frame.pack(side=tk.TOP)
learnrate_label = tk.Label(learnrate_frame, text='Learn Rate')
learnrate_label.pack(side=tk.LEFT)
learnrate_entry = tk.Entry(learnrate_frame)
learnrate_entry.pack(side=tk.LEFT)

# 以下為 cycle_frame 群組
cycle_frame = tk.Frame(controlls_frame)
cycle_frame.pack(side=tk.TOP)
cycle_label = tk.Label(cycle_frame, text='Cycles')
cycle_label.pack(side=tk.LEFT)
cycle_entry = tk.Entry(cycle_frame)
cycle_entry.pack(side=tk.LEFT)

# 以下為 condition_frame 群組
condition_frame = tk.Frame(controlls_frame)
condition_frame.pack(side=tk.TOP)
condition_label = tk.Label(condition_frame, text='Stop after rate')
condition_label.pack(side=tk.LEFT)
condition_entry = tk.Entry(condition_frame)
condition_entry.pack(side=tk.LEFT)


# 以下為 explorer_frame 群組
explorer_frame = tk.Frame(controlls_frame)
explorer_frame.pack(side=tk.TOP)
explorer_label = tk.Label(explorer_frame, text="TestCase")
explorer_label.pack(side=tk.LEFT)
explorer_comboboxText = tk.StringVar()
explorer_comboboxText.set('Select a file...')
explorer_combobox = ttk.Combobox(
    explorer_frame, textvariable=explorer_comboboxText, state='readonly')
explorer_combobox['values'] = ['perceptron1',
                               'perceptron2',
                               '2Ccircle1',
                               '2Circle1',
                               '2Circle2',
                               '2CloseS',
                               '2CloseS2',
                               '2CloseS3',
                               '2cring',
                               '2CS',
                               '2Hcircle1',
                               '2ring']
explorer_combobox.pack(side=tk.RIGHT)

calculate_btn = tk.Button(controlls_frame, text='馬上計算', command=main)
calculate_btn.pack(side=tk.TOP)

results_frame = tk.Frame(window)
results_frame.pack(side=tk.LEFT)

alltestcases_frame = tk.Frame(results_frame)
alltestcases_frame.pack(side=tk.TOP, anchor=tk.W)
alltestcases_figure = Figure(figsize=(3, 2))
alltestcases_plot = alltestcases_figure.add_subplot(111)
alltestcases_canvas = FigureCanvasTkAgg(
    alltestcases_figure, master=alltestcases_frame)
alltestcases_canvas.get_tk_widget().pack(side=tk.LEFT, fill='both', expand=1)
alltestcases_label = tk.Label(alltestcases_frame)
alltestcases_label.pack(side=tk.LEFT)

traincase_frame = tk.Frame(results_frame)
traincase_frame.pack(side=tk.TOP, anchor=tk.W)
traincase_figure = Figure(figsize=(3, 2))
traincase_plot = traincase_figure.add_subplot(111)
traincase_canvas = FigureCanvasTkAgg(
    traincase_figure, master=traincase_frame)
traincase_canvas.get_tk_widget().pack(side=tk.LEFT, fill='both', expand=1)
traincase_label = tk.Label(traincase_frame)
traincase_label.pack(side=tk.LEFT)

testcase_frame = tk.Frame(results_frame)
testcase_frame.pack(side=tk.TOP, anchor=tk.W)
testcase_figure = Figure(figsize=(3, 2))
testcase_plot = testcase_figure.add_subplot(111)
testcase_canvas = FigureCanvasTkAgg(
    testcase_figure, master=testcase_frame)
testcase_canvas.get_tk_widget().pack(side=tk.LEFT, fill='both', expand=1)
testcase_label = tk.Label(testcase_frame)
testcase_label.pack(side=tk.LEFT)

weights_label = tk.Label(results_frame)
weights_label.pack(side=tk.RIGHT)

window.mainloop()
