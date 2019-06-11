import os
import shutil
import sys

import gen_description
import gen_test_case
import run_solution
import verify_input


def PrepareGeneratedDirectory(problem_dir):
  generated_dir = os.path.join(problem_dir, "generated")
  if os.path.isdir(generated_dir):
    shutil.rmtree(generated_dir)
  os.makedirs(generated_dir)
  return generated_dir


def GenerateDescription(problem_dir):
  gen_description.GenerateDescription(problem_dir)

def GenerateTestCase(problem_dir):
  gen_test_case.GenerateTestCase(problem_dir)

def VerifyInput(problem_dir):
  verify_input.VerifyInput(problem_dir)

def RunSolutions(problem_dir):
  run_solution.RunSolutions(problem_dir)

def CleanUp(problem_dir):
  runner_exec = os.path.join(problem_dir, "runner")

  os.remove("scorer")
  os.remove("solution")
  os.remove(runner_exec)
  shutil.rmtree("tc")


def main():
  if len(sys.argv) != 2:
    raise RuntimeError("Usage: python gen_problem.py problem_dir")
  problem_dir = sys.argv[1]
  PrepareGeneratedDirectory(problem_dir)
  GenerateDescription(problem_dir)
  GenerateTestCase(problem_dir)
  VerifyInput(problem_dir)
  RunSolutions(problem_dir)
  CleanUp(problem_dir)


if __name__ == "__main__":
  main()
