import numpy as np 
from channels.OFDMAChannel import OFDMAChannel

class GradientDescent(object):
    def __init__(self,
                 no_subcarriers,
                 no_receivers,
                 bandwidth_sub,
                 Pmax,
                 P_PScir,
                 P_APcir,
                 P_UserCir,
                 noise,
                 eff_path,
                 threshold):
        self.no_subcarriers = no_subcarriers
        self.no_receivers = no_receivers
        self.BW = bandwidth_sub
        self.P0 = Pmax
        self.P_PScir = P_PScir
        self.P_APcir = P_APcir
        self.P_UserCir = P_UserCir
        self.pc = P_APcir + no_receivers*P_UserCir
        self.noise = noise 
        self.eff_path = eff_path
        self.threshold = threshold

    def BackTrackingLineSearch(self, PS_AP, AP_users, lamda, power, div_lamda, div_p, q, mode):
        step = 1
        beta = 0.5 # tau belongs to (0, 1)
        while (1):
            step = beta*step
            if mode == 'lamda':
                f = self.function(PS_AP, AP_users, lamda, power, q)
                f_delta = self.function(PS_AP, AP_users, lamda - step*div_lamda, power, q)
                if (f_delta > f - step/2*(np.abs(div_lamda))**2).all():
                    break
            else:
                # import ipdb; ipdb.set_trace()
                f = self.function(PS_AP, AP_users, lamda, power, q)
                f_delta = self.function(PS_AP, AP_users, lamda, power + step*div_p, q)
                if (f_delta > f - step/2*(np.abs(div_p))**2).all():
                    break  
        return step

    def function(self, PS_AP, AP_users, lamda, power, q):
        t = self.eff_path*np.sum((PS_AP**2), axis=2)
        return self.BW*self.P0*t*(1 + lamda)*np.log2(1 + power*AP_users) - \
               (q*(self.P0 + self.P_PScir) + lamda*self.threshold)*power - \
               q*(self.P_APcir*(self.P0*(1 - t) + self.P_PScir) + self.P0*t*self.pc) - \
               (self.P0*t + self.P_APcir)*lamda*self.threshold

    def optimizer(self, PS_AP, AP_users, q):
        t = self.eff_path*np.sum((PS_AP**2), axis=2)
        epsilon_1 = 0.0001
        epsilon_2 = 0.0001
        lamda = np.zeros((AP_users.shape[1], 1))
        
        while (1):
            # import ipdb; ipdb.set_trace()
            power = np.ones((AP_users.shape[1], AP_users.shape[2])) # 60000*
            div_lamda = self.BW*self.P0*t*np.log2(1 + power*AP_users) - \
                        lamda*(power + self.P0*t + self.P_APcir)
            while (1):
                div_p = self.BW*self.P0*t*AP_users/((1 + power*AP_users)*np.log(2)) - \
                        q*(self.P0 + self.P_PScir) - lamda*self.threshold
                step_1 = self.BackTrackingLineSearch(PS_AP, 
                                                     AP_users, 
                                                     lamda, 
                                                     power, 
                                                     div_lamda, 
                                                     div_p,
                                                     q, 
                                                     mode='power')
    
                power = power + step_1*div_p
                power = power.clip(min=0)
                
                print(np.abs(div_p))
                if (np.abs(div_p) <= epsilon_1).all():
                    break
                # div_p = self.BW*self.P0*t*AP_users/((1 + power*AP_users)*np.log(2)) - \
                #         q*(self.P0 + self.P_PScir) - lamda*self.threshold
                
                opt_primal = self.function(PS_AP, AP_users, lamda, power, q)
                print('opt_primal: ', opt_primal)

            step_2 = self.BackTrackingLineSearch(PS_AP, 
                                                 AP_users, 
                                                 lamda, 
                                                 power, 
                                                 div_lamda, 
                                                 div_p,
                                                 q, 
                                                 mode='lamda')
            lamda = lamda - step_2*div_lamda
            lamda = lamda.clip(min=0)
            if (np.abs(div_lamda) <= epsilon_2).all():
                break
            # div_lamda = self.BW*self.P0*t*np.log2(1 + power*AP_users) - \
            #             lamda*(power + self.P0*t + self.P_APcir)
            opt_dual = self.function(PS_AP, AP_users, lamda, power, q)
            print('opt_dual: ', opt_dual)
            
        opt = self.function(PS_AP, AP_users, lamda, power, q)
        return power, lamda, opt 


def main():
    channel = OFDMAChannel(noise=10**(-110/10)*0.001, 
                           BW=180e3,
                           eff_path=2.4,
                           no_subcarriers=1, 
                           no_TransmitterAntens=5,
                           no_ReceiverAntens=6,
                           no_transmitters=1,
                           pos_transmitters = np.array([0+1j*00]), 
                           no_receivers=1,
                           pos_receivers=np.array([0+1j*10]),
                           pos_receivers_area=np.array([-50, 50, -50 , 50]),
                           pos_receiver_mode=None)
    channels, channel_mrcs = channel.channel(1)
    PS_AP = channel_mrcs

    channel = OFDMAChannel(noise=10**(-110/10)*0.001, 
                           BW=180e3,
                           eff_path=2.4,
                           no_subcarriers=1, 
                           no_TransmitterAntens=5,
                           no_ReceiverAntens=6,
                           no_transmitters=1,
                           pos_transmitters = np.array([0+1j*10]), 
                           no_receivers=1,
                           pos_receivers=np.array([0+1j*10]),
                           pos_receivers_area=np.array([-50, 50, -50 , 50]),
                           pos_receiver_mode='random')
    channels, channel_mrcs = channel.channel(1)
    AP_users = channel_mrcs

    GD = GradientDescent(no_subcarriers=1,
                         no_receivers=1,
                         bandwidth_sub=78*10**3,
                         Pmax=10**(np.arange(10,15,5)/10)*0.001,
                         P_PScir=10**((5/10)-3),
                         P_APcir=10**((5/10)-3),
                         P_UserCir=10**(-3),
                         noise=10**((-174/10)-3),
                         eff_path=0.8,
                         threshold=120*10**3)

    power, lamda, opt = GD.optimizer(PS_AP, AP_users, q=1)

if __name__ == '__main__':
    main()
            

