

import pyvisa
import numpy as np
import time


# load device
rm = pyvisa.ResourceManager()
rm.list_resources()
fgen2=rm.open_resource('ASRL4::INSTR') # may change 

# check device
fgen2.query('*IDN?')

# generate function in certain mode
def genfun(fgen,freq,amp,waveform="SIN",dco=0): # waveform: SIN, SQU, RAMP, NOIS, USER
    """ freq: 0.1-25M Hz
        amp: -5-5 Vpp
        waveform: SIN, SQU, RAMP, NOIS, USER
    """
    fgen.write("SOUR1:FUNC " + str(waveform))
    fgen.write("SOUR1:FREQ "+ str(freq))
    fgen.write("SOUR1:AMPL "+ str(amp))
    fgen.write("SOUR1:DCO "+ str(dco))
    #fgen.write("OUTPut ON")

#genfun(fgen2,1732,1.618,"SIN",0)

# reset and initiate device
def resett(fgen):
    fgen.write("OUTPut OFF")
    fgen.write("*RST")
    fgen.write("*CLS")

def funinit(fgen):
    resett(fgen)
    fgen.write("SOUR1:FUNC SIN")
    fgen.write("SOUR1:FREQ 0.1")
    fgen.write("SOUR1:AMPL 0")
    fgen.write("SOUR1:DCO 0")
    funReport(fgen)
    print("init")


# report function status on screen
def funReport(fgen):
    fgen.query("SOUR1:APPL?")
    print(
    fgen.query("SOUR1:FUNC?")[0:3] + "\t" +
    str(round(float(fgen.query(f"SOUR1:FREQ?")),2)) + " \t\t" +
    str(round(float(fgen.query(f"SOUR1:AMPL?")),2)),
    end="\r"
    )


#funReport(fgen2)

# report function status on screen with time remains
def funReportT(fgen,t):
    fgen.query("SOUR1:APPL?")
    print(
    fgen.query("SOUR1:FUNC?")[0:3] + "\t" +
    str(round(float(fgen.query(f"SOUR1:FREQ?")),2)) + " \t\t" +
    str(round(float(fgen.query(f"SOUR1:AMPL?")),2)) + "\t\t",
    secToclock(t),
    end="\r"
    )

#funReportT(fgen2,123)

# format time
def secToclock(tf): # secs
    tf=int(tf)
    mins, secs = divmod(tf, 60)
    hrs, mins = divmod(mins, 60)
    return '{:02d}:{:02d}:{:02d}'.format(hrs, mins, secs)

# tf=t*60
# secToclock(120)

# generate function with time countdown
def genfunTime(fgen, duration, freqI, freqF, ampI, ampF, waveform="SIN"):
    """duration: sec"""
    tsteps=duration #*60
    freqs=np.linspace(freqI, freqF, tsteps)
    amps=np.linspace(ampI, ampF, tsteps)
    
    print("FUN\tFREQ(Hz)\tAMPL(Vpp)")
    funinit(fgen)
    fgen.write("OUTPut ON")
    print("start \t"+str(freqI)+" \t\t"+str(ampI))
    for f, a in zip(freqs,amps):
        genfun(fgen,f,a)
        funReport(fgen)
        time.sleep(1)
    print("\n")


#genfunTime(fgen2,10,1234,1434,1.3,2.5)

#genfunTime(fgen2,10,10,10,0.05,2.5)

# time in minute
def genfunTimeM(fgen, duration, freqI, freqF, ampI, ampF, waveform="SIN"):
    """duration: min"""
    tsteps=duration*60
    freqs=np.linspace(freqI, freqF, tsteps)
    amps=np.linspace(ampI, ampF, tsteps)
    
    print("FUN\tFREQ(Hz)\tAMPL(Vpp)")
    funinit(fgen)
    fgen.write("OUTPut ON")
    print("start \t"+str(freqI)+" \t\t"+str(ampI))
    for f, a in zip(freqs,amps):
        fgen.write("SOUR1:FREQ " + str(f))
        fgen.write("SOUR1:AMPL " + str(a))
        funReport(fgen)
        time.sleep(1)
    print("\n")

#genfunTimeM(fgen2,1,1234,1434,1.3,2.5)


# test function
def genfunTimeMT(fgen, duration, freqI, freqF, ampI, ampF, waveform="SIN", init=False):
    """duration: min"""
    tsteps=duration*60
    tf=np.linspace(tsteps, 1, tsteps)
    freqs=np.linspace(freqI, freqF, tsteps)
    amps=np.linspace(ampI, ampF, tsteps)
    
    print("FUN\tFREQ(Hz)\tAMPL(Vpp)\t")
    if init:
        funinit(fgen)
        fgen.write("OUTPut ON")
    
    print("start \t"+str(freqI)+" \t\t"+str(ampI), "\t\t",secToclock(tsteps))
    for f, a, t in zip(freqs,amps, tf):
        fgen.write("SOUR1:FREQ " + str(f))
        fgen.write("SOUR1:AMPL " + str(a))
        funReportT(fgen,t)
        time.sleep(1)
    print("\n")


# genfunTimeMT(fgen2,2,1000,1000,0.5,1)

def timeReport(fgen,mins):
    """duration: min"""
    endt=mins*60
    duration=range(1,endt)
    
    print("FUN\tFREQ(Hz)\tAMPL(Vpp)")
    for i in duration:
        funReport(fgen)
        print(i,end="\r")
        time.sleep(1)
    print("\n")

#timeReport(fgen2,2)

def timeReportT(fgen,mins):
    """duration: min"""
    tsteps=mins*60
    duration=np.linspace(tsteps, 1, tsteps)
    
    print("FUN\tFREQ(Hz)\tAMPL(Vpp)\t",secToclock(tsteps))
    for i in duration:
        funReportT(fgen,i)
        time.sleep(1)
    print("\n")

#timeReportT(fgen2,2)







# execution instance

# electroformation0823 one-sided 5 mg/mL, 2.5 uL 1kHz 2.5 Vpp
start_time = time.time()
print(time.strftime("%H:%M:%S", time.localtime()))

genfunTimeMT(fgen2,1,1000,1000,0.5,2.5,init=True)
genfunTimeMT(fgen2,180,1000,1000,2.5,2.5)
genfunTimeMT(fgen2,1,1000,2,2.5,2.5)
genfunTimeMT(fgen2,30,2,2,2.5,2.5)
fgen2.write("OUTPut OFF")

print(time.strftime("%H:%M:%S", time.localtime()))
print("total %s mins..." % ((time.time() - start_time)/60))


# test instance
start_time = time.time()
print(time.strftime("%H:%M:%S", time.localtime()))

genfunTimeMT(fgen2,1,300,300,0.5,2.5,init=True)
genfunTimeMT(fgen2,1,300,300,2.5,2.5)
genfunTimeMT(fgen2,1,300,2,2.5,2.5)
genfunTimeMT(fgen2,1,2,2,2.5,2.5)
print(time.strftime("%H:%M:%S", time.localtime()))
print("total %s mins..." % ((time.time() - start_time)/60))



# execution record
################
>>> # electroformation0819 one-sided 5 mg/mL, 2.5 uL 1kHz 2.5 Vpp
>>> start_time = time.time()
>>> print(time.strftime("%H:%M:%S", time.localtime()))
10:55:41
>>>
>>> genfunTimeMT(fgen2,1,1000,1000,0.5,2.5,init=True)
FUN     FREQ(Hz)        AMPL(Vpp)
init    0.1             0.0
start   1000            0.5              00:01:00
SIN     1000.0          2.5              00:00:01

>>> genfunTimeMT(fgen2,180,1000,1000,2.5,2.5)
FUN     FREQ(Hz)        AMPL(Vpp)
start   1000            2.5              03:00:00
SIN     1000.0          2.5              00:00:01

>>> genfunTimeMT(fgen2,1,1000,2,2.5,2.5)
FUN     FREQ(Hz)        AMPL(Vpp)
start   1000            2.5              00:01:00
SIN     2.0             2.5              00:00:01

>>> genfunTimeMT(fgen2,30,2,2,2.5,2.5)
FUN     FREQ(Hz)        AMPL(Vpp)
start   2               2.5              00:30:00
SIN     2.0             2.5              00:00:01

>>> fgen2.write("OUTPut OFF")
12
>>>
>>> print(time.strftime("%H:%M:%S", time.localtime()))
14:29:28


