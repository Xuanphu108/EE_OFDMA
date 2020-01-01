import numpy as np
from numpy import linalg as LA
from numpy.random import randn
import matplotlib.pyplot as plt
import pickle

class OFDMAChannel(object):
    def __init__(self, 
                 noise=10**(-110/10)*0.001, 
                 BW=180e3,
                 eff_path=2.4,
                 no_subcarriers=12, 
                 no_TransmitterAntens=5,
                 no_ReceiverAntens=5,
                 no_transmitters=1,
                 pos_transmitters=np.array([0+1j*00]),
                 no_receivers=1,
                 pos_receivers=np.array([0+1j*00]),
                 pos_receivers_area=np.array([-50, 50, -50 , 50]),
                 pos_receiver_mode='random'):
        self.noise = noise
        self.BW = BW
        self.no_subcarriers = no_subcarriers
        self.no_TransmitterAntens = no_TransmitterAntens
        self.no_ReceiverAntens = no_ReceiverAntens
        self.no_transmitters = no_transmitters
        if (no_transmitters == len(pos_transmitters)):
            self.pos_transmitters = pos_transmitters
        else:
            raise ValueError('Length of pos_transmitters must be same no_transmitters')
        self.no_receivers = no_receivers
        self.pos_receivers = pos_receivers
        if (len(pos_receivers_area) == 4):
            self.pos_receivers_area = pos_receivers_area
        else:
            raise ValueError('The length of pos_receivers_area must be 4')
        self.pos_receiver_mode = pos_receiver_mode
        self.PathLoss = self.PathLoss(no_transmitters, no_receivers, pos_transmitters, 
                                      pos_receivers_area, no_subcarriers, eff_path)

    def PathLoss(self, no_transmitters, no_receivers, 
                 pos_transmitters, pos_receivers_area,  
                 no_subcarriers, eff_path):
        if (self.pos_receiver_mode == 'random'):
            receiver_temp = []
            for i in range(1000):
                receiver_real = np.random.uniform(pos_receivers_area[0], pos_receivers_area[1])
                receiver_img = 1j*np.random.uniform(pos_receivers_area[2], pos_receivers_area[3])
                dist = LA.norm(receiver_real + receiver_img)
                if dist > 2 and dist < 10:
                    receiver = receiver_real + receiver_img
                    receiver_temp = np.append(receiver_temp, receiver)
            pos_receivers = receiver_temp[:no_receivers]
        else:
            if (no_receivers == len(self.pos_receivers)):
                pos_receivers = self.pos_receivers
            else:
                raise ValueError('Length of pos_receivers must be same no_receiver')
        """
        distance_col: distance between transmitter_i and receivers 
        """
        distance_row = []
        for i in range(no_transmitters):
            distance_col = []
            for j in range(no_receivers):
                distance_sub = []
                for k in range(no_subcarriers):
                    d = abs(pos_transmitters[i] - pos_receivers[j])
                    distance_sub.append(d)
                distance_col.append(distance_sub)
            distance_row.append(distance_col)
        distance_row = np.array(distance_row)
        PathLoss = np.power(distance_row, -eff_path)*(10**(-3))
        return PathLoss
    def channel(self, no_samples):
        channel_size = (self.no_transmitters,
                        self.no_receivers,
                        self.no_subcarriers,
                        self.no_TransmitterAntens, 
                        self.no_ReceiverAntens)
        # import ipdb; ipdb.set_trace()
        channels = []
        channel_mrcs = []
        for i in range(no_samples):
            PathLoss = np.sqrt(self.PathLoss/2)
            rand = randn(*channel_size)+randn(*channel_size)*1j
            channel = rand*PathLoss.reshape(self.no_transmitters, self.no_receivers, 
                                            self.no_subcarriers, 1, 1)
            channel_mrc = LA.norm(channel, axis = 3)
            channel_mrc = LA.norm(channel_mrc, axis = 3)
            channels.append(channel)
            channel_mrcs.append(channel_mrc)
        channels = np.array(channels)
        channel_mrcs = np.array(channel_mrcs)
        return channels, channel_mrcs

def main():
    channel = OFDMAChannel(noise=10**(-110/10)*0.001, 
                          BW=180e3,
                          eff_path=2.4,
                          no_subcarriers=12, 
                          no_TransmitterAntens=5,
                          no_ReceiverAntens=6,
                          no_transmitters=2,
                          pos_transmitters = np.array([0+1j*00, 0+1j*5]), 
                          no_receivers=3,
                          pos_receivers=np.array([0+1j*10, 0+1j*15, 0+1j*20]),
                          pos_receivers_area=np.array([-50, 50, -50 , 50]),
                          pos_receiver_mode='random')
    channels, channel_mrcs = channel.channel(2)
    print(channels.shape) 
    # print(channels)
    print(channel_mrcs.shape)
    # print(channel_mrcs)

if __name__ == '__main__':
    main()



