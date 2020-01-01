import argparse
import logging
import os
import numpy as np 
from runpy import run_path

from channels.OFDMAChannel import OFDMAChannel 

def parse_args():
    parser = argparse.ArgumentParser(description='Optimize')
    config_args = parser.add_argument('config', help='Config file path')
    parser.add_argument('--work_dir', help='the dir to save logs and results')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    cfg = run_path(args.config)
    if (cfg['channel_PS_AP']['data_root'] == None):
        print('Warning: Channel between PS and AP will be generated automatically!')
        AP_users_chanel = OFDMAChannel(noise=cfg['phy_params']['noise'],
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
        _, PS_AP_chanel_samples = AP_users_chanel.channel(cfg['channel_PS_AP']['no_samples'])
    else:
        print('Read dataset')

    if (cfg['channel_AP_users']['data_root'] == None):
        print('Warning: Channels between AP and users will be generated automatically!')
        AP_users_chanel = OFDMAChannel(noise=cfg['phy_params']['noise'],
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
        _, AP_users_chanel_samples = AP_users_chanel.channel(cfg['channel_AP_users']['no_samples'])
    else:
        print('Read dataset')

if __name__ == '__main__':
    main()


