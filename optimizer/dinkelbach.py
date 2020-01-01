import numpy as np 

class dinkelbach(object):
    def __init__(self,
                 no_subcarriers,
                 no_receivers,
                 bandwidth_sub,
                 Pmax,
                 P_PScir,
                 P_APcir,
                 noise,
                 eff_path):
    self.no_subcarriers = no_subcarriers
    self.no_receivers = no_receivers
    self.bandwidth_sub = bandwidth_sub
    self.Pmax = Pmax
    self.P_PScir = P_PScir
    self.P_APcir = P_APcir
    self.noise = noise 
    self.eff_path = eff_path
    self.q = 0.001
    self.epsilon = 0.001
    self.flag = False 

    def optimizer(self, channel):
        div_p
     