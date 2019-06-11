from colorama import Fore, Style
import os
import shutil
import subprocess

import problem_config

def tcframe_string_to_verdict(s):
  if s == "AC" or s == "OK":
    return problem_config.Verdict.ACCEPTED
  if s == "WA":
    return problem_config.Verdict.WRONG_ANSWER
  if s == "TLE":
    return problem_config.Verdict.TIME_LIMIT_EXCEEDED
  if s == "RTE":
    return problem_config.Verdict.RUNTIME_ERROR
  raise RuntimeError("Verdict not valid.")

def _get_grading_verdicts(runner_exec, executable, config):
  grading_log = subprocess.check_output([
    runner_exec, 
    "grade",
    "--solution=%s" % (executable),
    "--time-limit=%d" % (config.time_limit_ms // 1000),
    "--memory-limit=%d" % (config.memory_limit_mb),
    "--brief"
  ]).decode('utf-8')

  grading_verdicts = grading_log.split('\n')[:-1]
  
  # tcframe is weird, if there is only 1 subtask --brief will only
  # print 1 line, the verdict for that subtask. if there are n > 1
  # subtask, --brief will print n+1 line, first line being the summary
  if len(grading_verdicts) > 1:
    grading_verdicts = grading_verdicts[1:]
  grading_verdicts = list(map(lambda x: tcframe_string_to_verdict(x.split()[0]),
                              grading_verdicts))

  return grading_verdicts


def _check_verdicts(expected_verdicts, verdicts):
  if len(verdicts) != len(expected_verdicts):
    return False
  
  for i in range(len(expected_verdicts)):
    expected = expected_verdicts[i]
    verdict = verdicts[i]

    if expected == problem_config.Verdict.DO_NOT_RUN:
      continue
    elif expected == problem_config.Verdict.INCORRECT_SOLUTION:
      if verdict == problem_config.Verdict.ACCEPTED:
        return False
    elif expected != verdict:
      return False
  
  return True


def RunSolutions(problem_dir):
  config = problem_config.get_problem_config(problem_dir)
  
  assert os.path.exists("tc"), "TC not generated yet"
  
  runner_exec = os.path.join(problem_dir, "runner")

  print("Running solutions")
  for solution in config.solutions:
    file = os.path.join(problem_dir, "solutions", solution.filename)
    executable = os.path.join(problem_dir, "solutions", "run-solution")

    fnull = open(os.devnull, 'w')
    subprocess.call([
        "g++", "-std=c++11", "-O2", "-o", executable, file
    ], stderr=fnull)

    verdicts = _get_grading_verdicts(runner_exec, executable, config)
    os.remove(executable)

    is_valid_verdicts = _check_verdicts(solution.verdicts, verdicts)
    result = "OK"
    if not is_valid_verdicts:
      result = "expected %s, got %s" % (solution.verdicts, verdicts)

    print("  sol {}: {}{}{}".format(
      solution.filename, 
      Fore.GREEN if result == "OK" else Fore.RED, 
      result, 
      Style.RESET_ALL))
