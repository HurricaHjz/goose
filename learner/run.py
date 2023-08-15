import argparse
import os
from representation import REPRESENTATIONS
from util.search import search_cmd

parser = argparse.ArgumentParser()
parser.add_argument("domain_pddl", type=str,
                    help="path to domain pddl file")
parser.add_argument("task_pddl", type=str,
                    help="path to task pddl file")
parser.add_argument("--representation", "-r", required=True, type=str, choices=REPRESENTATIONS,
                    help="graph representation")
parser.add_argument("--model_path", "-m", required=True, type=str,
                    help="path to saved model weights")
parser.add_argument("--search", "-s", type=str, default="gbbfs", choices=["gbbfs", "gbfs"],
                    help="search algorithm")
parser.add_argument("--timeout", "-t", type=int, default=600,
                    help="timeout in seconds")
args = parser.parse_args()

cmd, intermediate_file = search_cmd(
  rep=args.representation,
  df=args.domain_pddl,
  pf=args.task_pddl,
  m=args.model_path,
  search=args.search,
  timeout=args.timeout,
  seed=0,
) 

os.system(cmd)
