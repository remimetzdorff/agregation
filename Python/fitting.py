# add self.params_key for each function

import numpy as np
from scipy.optimize import curve_fit
import pandas

def find_exponent(value):
    return np.floor(np.log10(abs(value)))

def display_readable(param, uparam):
    exponent = find_exponent(param)
    uexponent = find_exponent(uparam)
    poweroften = int(exponent - uexponent)
    new_uparam = np.round(uparam * 10 ** (-uexponent)) * 10 ** -poweroften
    new_param = np.round(param * 10 ** (-uexponent)) * 10 ** -poweroften
    return (str("(%." + str(poweroften) + "f +/- %." + str(poweroften) + "f) * 1e%.0f") % (new_param, new_uparam, exponent))

class Fit():

    def __init__(self, func, x=None, y=None, uy=None, verbosemode=True):
        self.x = x
        self.y = y
        self.data = pandas.Series(y, index=x)
        self.func_name = func
        self.func = (getattr(self, self.func_name))
        self.uy = uy
        self.verbosemode = verbosemode


    def linear(self, x, slope, y0):
        """
        slope   : slope
        y0      : y0 at x=0
        """
        self.params_key = ["slope", "y0"]
        return slope*x + y0
    def _guesslinear(self):
        max = self.data.max()
        min = self.data.min()
        slope = (max-min)/(self.x.max() - self.x.min())
        y0 = self.data.mean() - self.x.mean()*slope
        fit_params = [slope, y0]
        return fit_params

    def exponential(self, x, scale, alpha):
        """
        scale   : scale
        alpha   : alpha
        offset  : offset (background)
        """
        self.params_key = ["scale", "alpha"]
        return scale*np.exp(alpha*x)
    def _guessexponential(self):
        data = np.log(self.data.values)
        max = data.max()
        min = data.min()
        slope = (max - min) / (self.x.max() - self.x.min())
        y0 = data.mean() - self.x.mean() * slope
        firstguess = [slope, y0]
        guess_params = [np.exp(firstguess[1]), firstguess[0]]
        return guess_params

    def exponential_offset(self, x, scale, alpha, y0):
        """
        scale   : scale
        alpha   : alpha
        offset  : offset (background)
        """
        self.params_key = ["scale", "alpha", "offset"]
        return scale*np.exp(alpha*x) + y0
    def _guessexponential_offset(self):
        data = np.log(self.data.values)-self.y.mean()
        max = data.max()
        min = data.min()
        slope = (max - min) / (self.x.max() - self.x.min())
        y0 = data.mean() - self.x.mean() * slope
        firstguess = [slope, y0]
        guess_params = [np.exp(firstguess[1]), firstguess[0], self.y.mean()]
        return guess_params

    def sin(self, x, freq, scale, phi, offset):
        """
        freq   : frequency in 1/x unit
        scale  : amplitude (half peak to peak)
        phi    : phase at x=0
        offset : offset (mean value)
        """
        self.params_key = ["freq", "scale", "phi", "offset"]
        return scale*np.sin(2*np.pi*freq*x + phi) + offset
    def _guesssin(self):
        length = len(self.data)
        fft = np.fft.fft(self.data)/length
        d=np.abs(self.data.index[-1]-self.data.index[0])/length
        freq = np.fft.fftfreq(length,d=d)
        y0 = fft[0]
        fft[0]=0
        maxpos = (abs(fft)).argmax()
        maxfreq = freq[maxpos]
        #if maxpos%2==1:
        phase = np.angle(fft[maxpos])+np.pi/2
        fit_params = [abs(maxfreq), 2*abs(fft[maxpos]), phase, abs(y0)]
        return fit_params

    def sinc(self, x, center, freq, scale, offset):
        """
        center : center
        freq   : frequency in 1/x unit
        scale  : amplitude (half peak to peak)
        offset : offset (mean value)
        """
        self.params_key = ["center", "freq", "scale", "offset"]
        X = 2*np.pi*freq*(x-center)
        return offset + scale*np.sin(X)/X

    def sinc_squarred(self, x, center, freq, scale, offset):
        """
        center : center
        freq   : frequency in 1/x unit
        scale  : amplitude (half peak to peak)
        offset : offset (mean value)
        """
        self.params_key = ["center", "freq", "scale", "offset"]
        return offset + scale * (self.sinc(x, center, freq, 1, 0)) ** 2
    def _guess_sinc_squarred(self):
        x = list(self.x)
        y = list(self.y)
        data = pandas.Series(y, index=x)
        center = data.idxmax()
        offset = data.min()
        scale = data.max()-offset
        for xx, yy in zip(x,y):
            if yy > scale/2:
                x1 = xx
                break
        x.reverse, y.reverse()
        for xx, yy in zip(x, y):
            if yy > scale/2:
                x2 = xx
                break
        freq = 1/(2*np.pi*(x2-x1))
        guess_params = [center, freq, scale, offset]
        return guess_params

    def gaussian(self, x, center, bandwidth, scale):
        self.params_key = ["center", "bandwidth", "scale"]
        return scale * np.exp(-1 * ((x - center) / abs(bandwidth)) ** 2)




    def guess_params(self):
        guess_params=self._guessfunction(self)
        return guess_params

    def fit(self, manualguess_params=None, verbosemode=None):
        if manualguess_params is not None:
            guess_params = manualguess_params
        else:
            try:
                function_name = str(self.func.__name__)
                guess_function = "_guess"+function_name
                self._guessfunction = (getattr(Fit, guess_function))
                autoguess_params = self.guess_params()
                guess_params = autoguess_params
            except:
                guess_params = None
        fit_params, pcov = curve_fit(self.func, self.x, self.y, sigma=self.uy, p0=guess_params)
        self.fit_params = fit_params
        self.fit_uparams = np.sqrt(np.abs(np.diagonal(pcov)))
        if verbosemode is None:
            if self.verbosemode:
                self.report()
        elif verbosemode:
            self.report()
        return fit_params

    def chi2(self):
        """computed after fit"""
        if self.uy is not None:
            uy = self.uy
        else:
            uy = np.ones(len(self.x))
        return np.sum(((self.y - self.func(self.x, *self.fit_params))/uy)**2)

    def chi2r(self):
        return self.chi2()/(len(self.x)-len(self.fit_params))

    def report(self):
        print("##### Fit results #####")
        print("RAW")
        print("        optimised params :", self.fit_params)
        print("        uncertainties    :", self.fit_uparams)
        print("        chi2r            :", self.chi2r())
        print("READABLE")
        for param, uparam, key in zip(self.fit_params, self.fit_uparams, self.params_key):
            new_key = key
            while (len(new_key) < 10):
                new_key += " "
            print(str("        "+new_key+" = "+display_readable(param, uparam)))
        print("#######################")
