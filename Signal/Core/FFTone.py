import time
import scipy.fft
import numpy as np
from scipy.fft import fft, fftfreq, fftshift, ifft
import scipy.io as sio

import matplotlib.pyplot as plt

class FFTone:
    def __init__(self):
        self._dFFT=[]
        print("__ FFT __")
        self._tWalsh = None

    def One(self, d):
        return np.abs(scipy.fft.fft(d))
        # return np.abs(scipy.fft.fft(d))/d.__len__()

    def OneAll(self, d, nFFt, step):
        self._dFFT.clear()
        _countD = d.__len__()
        _countRep = _countD//step
        for i in range(0, _countRep):
            i0 = i * step
            i1= i0+nFFt
            if i >= _countRep:
                i1 = _countD
                i0 = i1-nFFt
            z = d[i0:i1]
            self._dFFT.append(np.abs(scipy.fft.fft(z))[0:nFFt//2])
        return self._dFFT


    def FFT_to_IFFT(self, d):
        yf = scipy.fft.fft(d)
        new_sig = scipy.fft.ifft(yf)
        plt.plot(new_sig)
        plt.show()



    def Test(self ):
        a = scipy.fft.fft(np.exp(2j * np.pi * np.arange(8) / 8))
        a1 = np.abs(a)
        plt.plot(a1)
        plt.show()
        k=1

    def Test1(self ):

        t = np.arange(256)

        sp = fftshift(fft(np.sin(t)))

        freq = fftshift(fftfreq(t.shape[-1]))

        plt.plot(freq, sp.real, freq, sp.imag)
        plt.show()
        k=1

    def WalshAll(self, d, nFFt, step):
        # _pathMat = "F:\\Python\\AnalisSigRTI\\Data\\matlab.mat"
        "/home/alanin/Python/Data/"
        _pathMat = "/home/alanin/Python/Data/matlab.mat"
        walshTabl = sio.loadmat(_pathMat)
        self._tWalsh = None

        _pathMat = "/home/alanin/Python/Data/matlab.mat"
        walshTabl = sio.loadmat(_pathMat)
        self._tWalsh = None
        match nFFt:
            case 128:
                self._tWalsh = walshTabl["walsh128"]
            case  256:
                self._tWalsh = walshTabl["walsh256"]
            case 512:
                self._tWalsh = walshTabl["walsh512"]
            case 1024:
                self._tWalsh = walshTabl["walsh1024"]
            case 2048:
                self._tWalsh = walshTabl["walsh2048"]
            case 4096:
                self._tWalsh = walshTabl["walsh4096"]
            case  _:
                self._tWalsh = None


        if self._tWalsh is None:
            return

        self._dFFT.clear()
        _countD = d.__len__()
        _countRep = (_countD-nFFt)//step

        start_time = time.time()
        # print(f" count d = {_countD}, step={step}   countRep = {_countRep} ")
        for i in range(0, _countRep):
            i0 = i * step
            i1= i0+nFFt
            if i >= _countRep:
                i1 = _countD
                i0 = _countD - nFFt
            self._dFFT.append(self._fWalsh(d[i0:i1]))

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f" Время расчета {elapsed_time:.2f} seconds to complete.")
        return self._dFFT

    def _fWalsh(self, z):
        harmonics =[]
        _harmonics = []
        count = len(z)
        _ = [_harmonics.append(np.dot(z, itWalsh)) for itWalsh in self._tWalsh]

        harmonics.append(np.pow(_harmonics[0], 2))
        _ = [harmonics.append(np.pow(_harmonics[i], 2)+np.pow(_harmonics[i+1], 2)) for   i in range(1, count-1, 2)]
        harmonics.append(np.pow(_harmonics[count-1], 2))

        return harmonics
    '''
    Сворачивает спектр в число 
    '''
    def SignalNoise(self, vFFT, endHarmonics, startHarmonicsNoise, countHarmonics):
        signal=[]
        noise = 0.0
        # vSignal = vFFT[:,:endHarmonics]
        yy1 = len(vFFT)
        countLs = len(vFFT[0])
        mNoise = np.zeros((len(vFFT),   countHarmonics))
        # signalCount = len(vFFT)  #* len(vFFT[0])

        for i in range(len(vFFT)):
            signal.append(np.sum( vFFT[i][:endHarmonics+1]))
            # noise = noise + np.sum(vFFT[i][startHarmonicsNoise: min(startHarmonicsNoise+countHarmonics, countLs)])
            mNoise[i,:] = vFFT[i][startHarmonicsNoise: min(startHarmonicsNoise+countHarmonics, countLs)]
        noise = np.std(mNoise)
        # return signal, noise/ signalCount
        return signal, noise*5