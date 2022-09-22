import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


def extract_history(history):
    plt.plot(history)
    plt.show()
