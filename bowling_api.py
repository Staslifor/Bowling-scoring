# -*- coding: utf-8 -*-

import argparse
from bowling.bowling import game_score, International, Native

parser = argparse.ArgumentParser()
parser.add_argument('--result')
parser.add_argument('--score_rules')
args = parser.parse_args()

if args.score_rules == 'International':
    print(game_score(score_rules=International, game_result=args.result))
elif args.score_rules == 'Native':
    print(game_score(score_rules=Native, game_result=args.result))
