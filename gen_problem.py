import os
import shutil
import sys

import gen_description


def PrepareGeneratedDirectory(problem_dir):
  generated_dir = os.path.join(problem_dir, "generated")
  if os.path.isdir(generated_dir):
    shutil.rmtree(generated_dir)
  os.makedirs(generated_dir)
  return generated_dir


def GenerateDescription(problem_dir):
  gen_description.GenerateDescription(problem_dir)


def main():
  if len(sys.argv) != 2:
    raise RuntimeError("Usage: python gen_problem.py problem_dir")
  problem_dir = sys.argv[1]
  PrepareGeneratedDirectory(problem_dir)
  GenerateDescription(problem_dir)


if __name__ == "__main__":
  main()
