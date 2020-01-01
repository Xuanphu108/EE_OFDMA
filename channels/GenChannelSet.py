import argparse
import logging
import os
import numpy as np 
from runpy import run_path

from OFDMAChannel import OFDMAChannel 

def parse_args():
    parser = argparse.ArgumentParser(description='Optimize')
    config_args = parser.add_argument('config', help='Config file path')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    cfg = run_path(args.config)

    chanel_PS_AP = OFDMAChannel(noise=cfg['phy_params']['noise'],
                                BW=cfg['phy_params']['bandwidth_sub'],
                                eff_path=cfg['phy_params']['eff_path'],
                                no_subcarriers=cfg['channel_PS_AP']['no_subcarriers'], 
                                no_TransmitterAntens=cfg['channel_PS_AP']['no_TransmitterAntens'],
                                no_ReceiverAntens=cfg['channel_PS_AP']['no_ReceiverAntens'],
                                no_transmitters=cfg['channel_PS_AP']['no_transmitters'],
                                pos_transmitters=cfg['channel_PS_AP']['pos_transmitters'], 
                                no_receivers=cfg['channel_PS_AP']['no_receivers'],
                                pos_receivers=cfg['channel_PS_AP']['pos_receivers'],
                                pos_receivers_area=cfg['channel_PS_AP']['pos_receivers_area'],
                                pos_receiver_mode=None)
    
    chanel_AP_users = OFDMAChannel(noise=cfg['phy_params']['noise'],
                                   BW=cfg['phy_params']['bandwidth_sub'],
                                   eff_path=cfg['phy_params']['eff_path'],
                                   no_subcarriers=cfg['channel_AP_users']['no_subcarriers'], 
                                   no_TransmitterAntens=cfg['channel_AP_users']['no_TransmitterAntens'],
                                   no_ReceiverAntens=cfg['channel_AP_users']['no_ReceiverAntens'],
                                   no_transmitters=cfg['channel_AP_users']['no_transmitters'],
                                   pos_transmitters=cfg['channel_AP_users']['pos_transmitters'], 
                                   no_receivers=cfg['channel_AP_users']['no_receivers'],
                                   pos_receivers=cfg['channel_AP_users']['pos_receivers'],
                                   pos_receivers_area=cfg['channel_AP_users']['pos_receivers_area'],
                                   pos_receiver_mode='random')
    
    _, chanel_PS_AP_samples = chanel_PS_AP.channel(cfg['channel_PS_AP']['no_samples'])
    _, chanel_AP_users_samples = chanel_AP_users.channel(cfg['channel_AP_users']['no_samples'])
    print(chanel_PS_AP_samples.shape)
    print(chanel_AP_users_samples.shape)
    path_PS_AP = cfg['channel_PS_AP']['gen_data_root']
    os.makedirs(path_PS_AP, exist_ok=True)
    path_AP_users = cfg['channel_AP_users']['gen_data_root']
    os.makedirs(path_AP_users, exist_ok=True) 
    
    for i in range(chanel_AP_users_samples.shape[0]):
        PS_AP = chanel_PS_AP_samples[i][0]
        np.savetxt(path_PS_AP + "frame_%d.csv" %(i+1), PS_AP, delimiter=",")
        AP_users = chanel_AP_users_samples[i][0]
        np.savetxt(path_AP_users + "frame_%d.csv" %(i+1), AP_users, delimiter=",")

if __name__ == '__main__':
    main()