import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class PLTExporter:
    def __init__(self):
        pass

    @staticmethod
    def extract_history(history):
        plt.plot(history)
        plt.show()
