"""
# Copyright (c) 2021-2022 RAM-LAB
# Authors: kinzhang (qzhangcb@connect.ust.hk)
# Usage: Collect Data or Eval Agent
# Message: All references pls check the readme
"""
from leaderboard.leaderboard_evaluator import LeaderboardEvaluator
from leaderboard.utils.statistics_manager import StatisticsManager
from utils import bcolors as bc
from utils import CarlaServerManager
import hydra
import sys, os
import datetime, time
import gc
from pathlib import Path
import logging
import subprocess
log = logging.getLogger(__name__)

@hydra.main(config_path="config", config_name="collect")
def main(args):
    # config init =============> make all path with absolute
    args.scenarios = os.path.join(args.absolute_path,args.scenarios)
    args.routes    = os.path.join(args.absolute_path,args.routes)
    args.agent     = os.path.join(args.absolute_path, args.agent)
    if 'data_save' in args.agent_config:
        args.agent_config.data_save = os.path.join(args.absolute_path, args.agent_config.data_save)
    # for multi carla
    args.traffic_manager_port = args.port + 6000
    # =============> 

    # start CARLA
    server_manager = CarlaServerManager(args.carla_sh_path, port=args.port)
    server_manager.start()

    print('-'*20 + "TEST Agent: " + bc.OKGREEN + args.agent.split('/')[-1] + bc.ENDC + '-'*20)

    # run official leaderboard ====>
    leaderboard_evaluator = LeaderboardEvaluator(args, StatisticsManager(args.checkpoint, args.debug_checkpoint))
    leaderboard_evaluator.run(args)
    # run official leaderboard ====>
    
    # kill CARLA
    # server_manager.stop()

if __name__ == '__main__':
    
    start_time = time.time()
    main()
    print('clean memory on no.', gc.collect(), "Uncollectable garbage:", gc.garbage)
    print(f"{bc.OKGREEN}TOTAL RUNNING TIME{bc.ENDC}: --- %s hours ---" % round((time.time() - start_time)/3600,2))