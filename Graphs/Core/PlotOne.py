import matplotlib.pyplot as plt
import numpy as np
from sympy.strategies.core import switch

from Core.Enum.TypePlot import TypePlot


def ShowMy():
    plt.show()

class PlotInfoOne:
    def __init__(self, **kwargs):
        self.x = None
        self.y = None
        self.fs = None
        self.nameX = None
        self.nameY = None
        self.nameTitle = None
        if kwargs.__len__()>0:
            self.ParserArg(**kwargs)

    def ParserArg(self, **kwargs):
        self.x = kwargs.get("x", self.x)
        self.y = kwargs.get("y", self.y)
        self.fs = kwargs.get("fs", self.fs)
        self.nameX = kwargs.get("nameX", self.nameX)
        self.nameY = kwargs.get("nameY", self.nameY)
        self.nameTitle = kwargs.get("Title", self.nameTitle)

    def Set(self, **kwargs):
        self.ParserArg(**kwargs)

    def PlotRun(self, axx):
        axx.plot(self.x)
        if not(self.nameX is None):
            axx.set_xlabel(self.nameX)  # Подпись для оси х
        if not(self.nameY is None):
            axx.set_ylabel(self.nameY)  # Подпись для оси y
        if not(self.nameTitle is None):
            axx.set_title(self.nameTitle)  # Подпись для оси y
        k=1


class PlotOne:
    def __init__(self):
        self._data = None
        self._fs = None
        self._show = None
        self._nameX = None
        self._nameY = None
        self._nameTitle = None
        self._typePlot = TypePlot.One
        print("__ Plot __")

    def OneFFT(self, **kwargs):
        self.ParserArg(**kwargs)
        if self._data is None:
            return None

        _nFFT_2 = self._data.shape[0]//2
        t = np.arange(start=0, stop=_nFFT_2+1, step=1)*self._fs
        tCount = t.__len__()
        y=self._data[0:tCount]
        plt.plot(t, y)
        self.__GraphName()

        if self._show is None:
            ShowMy()

    def OnePlotx(self, d, show=None):
        plt.figure()
        plt.plot(d)
        plt.grid()
        if show is None:
            return
        ShowMy()

    def OnePlotxLine(self, d, line):
        t=[x for x in range(len(d))]
        yLime = [line for x in range(len(d))]
        plt.figure()
        plt.plot(t, d, t, yLime)
        plt.grid()


    def ParserArg(self, **kwargs):
        self._data = kwargs.get("d", self._data)
        self._fs = kwargs.get("fs", self._fs)
        self._show = kwargs.get("show", self._show)
        self._nameX = kwargs.get("nameX", self._nameX)
        self._nameY = kwargs.get("nameY", self._nameY)
        self._nameTitle = kwargs.get("Title", self._nameTitle)
        self._typePlot =  kwargs.get("TypePlot", self._typePlot)


    def __GraphName(self):
        if not(self._nameX is None):
            plt.xlabel(self._nameX)  # Подпись для оси х
        if not(self._nameY is None):
            plt.ylabel(self._nameY)  # Подпись для оси y
        if not(self._nameTitle is None):
            plt.title(self._nameTitle)  # Подпись для оси y

    def SubPlots(self, **kwargs):
        self.ParserArg(**kwargs)
        if self._data is None:
            raise "!!! error not Data "

        count = len(self._data)
        if (count == 1) and (self._typePlot != TypePlot.D2):
            plt.plot(self._data[0][0].x)
            # plt.plot(self._data[0][0])
            if "show" == self._show:
                plt.show()
            return

        match self._typePlot:
            case TypePlot.D1Vert:
                fig, axs = plt.subplots(count, 1, figsize=(12, 7)) # , figsize=(12, 7)
                for i in range(count):
                   self._data[i][0].PlotRun(axs[i])
                # plt.show()


            case  TypePlot.D1Hor:
                fig, axs = plt.subplots(1, count)

                for i in range(count):
                    self._data[i][0].PlotRun(axs[i])
                    # axs[i].plot(self._data[i][0].x)
                # plt.show()

            case TypePlot.D2:
                fig, axs = plt.subplots(count, 2)
                _size = axs.shape
                k0=0
                try:
                    k0 = _size[1]
                except:
                    pass

                if k0==0:
                    self._data[0][0].PlotRun(axs[0])
                    self._data[0][1].PlotRun(axs[1])
                else:
                    for i in range(count):
                        self._data[i][0].PlotRun(axs[i, 0])
                        self._data[i][1].PlotRun(axs[i, 1])
                # plt.show()
            case TypePlot.One:
                pass
            case  _:
                pass

        if not(self._show is None):
            plt.show()

