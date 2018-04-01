import matplotlib.pyplot as plt
import numpy as np
import random

class Neuron:
    """
    Models a single neuron to be used in a larger network

    Fields:
    numPoissonNeurons = number of input neurons to receive signals from
    threshold = voltage potential (mV) minimum that must be reached in order to
    generate spikes
    """

    def __init__(self, numPoissonNeurons, threshold):
        self.numPoissonNeurons = 10
        self.threshold = threshold

    def getPSP(self, tau, alpha, Q, t):
        """
        Generates post-synaptic potential from a dendrite entering the neuron

        Inputs:
        alpha - typically in the range of [1,2]
        tau - typically 20msec
        Q - typically in the range of [30,60]
        t - an array of time values
        """
        return (Q/(alpha * np.sqrt(t))) * (np.exp(-1 * np.power(alpha, 2) / t)) * (np.exp(-1 * t / tau))

    def getOutputSpikeTimes(self, inputSpikeTrain):
        outputSpikeTimes = []
        record = True

        for j in range(len(inputSpikeTrain[0])):
            sum = 0

            for i in range(len(inputSpikeTrain)):
                sum += inputSpikeTrain[i][j]
            if sum >= self.threshold and record:
                record = False
                print("hit")
                outputSpikeTimes.append(j)
            if sum < self.threshold:
                record = True

        return outputSpikeTimes



if __name__ == '__main__':

    # Set number of Poisson neurons and threshold
    numPoissonNeurons = 10

    # Instantiate Neuron object
    neuron = Neuron(numPoissonNeurons, 60)

    # Set lambda as maximum for spike generation
    lam = 0.00005 # should be 0.0001

    # Set time interval in milliseconds
    interval = 0.01

    # Create time array
    t = (np.arange(0.01, 500, 0.01))

    # Create list to record spikes and initialize current PSP
    spikeTimes = []

    # Set Q, tau, and alpha
    Q = 10
    tau = 20
    alpha = 0.30

    # Calculate spike once for usage later
    spike = list(neuron.getPSP(tau, alpha, Q, t))

    # spikeTrain holds all Poisson neuron PSP's
    spikeTrains = []

    # Initialize count used to go through the Poisson neurons
    count = 0

    # Loop through all Poisson neuron inputs
    while count < numPoissonNeurons:

        spikeTimes = []

        # Generate spike randomly with low success rate
        for i in range(len(t)):
            if random.random() < lam:
                spikeTimes.append(i)

        PSP = [0] * len(t)

        for i in range(len(spikeTimes)):
            PSP = PSP[0:spikeTimes[i]] + spike
            PSP = PSP[0:49999]

        spikeTrains.append(PSP)

        count += 1

    # Generate Neuron spike trains
    outputSpikeTimes = neuron.getOutputSpikeTimes(spikeTrains)
    outputSpikeTrain = [0] * len(t)

    for i in range(len(outputSpikeTimes)):
        outputSpikeTrain = outputSpikeTrain[0:outputSpikeTimes[i]] + spike
        outputSpikeTrain = outputSpikeTrain[0:49999]

    # Plot input Poisson neurons spike trains that trigger spikes at the current neuron
    fig, axes = plt.subplots(nrows=numPoissonNeurons + 1, ncols=1, sharex=True, sharey=True)
    fig.text(0.5, 0.04, 'Time (ms)', ha='center')
    fig.text(0.04, 0.5, 'Potential (mV)', va='center', rotation='vertical')
    plt.suptitle('Poisson Neuron Spike Train')

    for i in range(numPoissonNeurons):
        axes[i].plot(t, spikeTrains[i], 'r')

    axes[numPoissonNeurons].plot(t, outputSpikeTrain, 'b')

    plt.show()
