import attr
from enum import Enum
import json
import os

_CONFIG_FILENAME = "config.json"

class Verdict(Enum):
  ACCEPTED = 0
  WRONG_ANSWER = 1
  TIME_LIMIT_EXCEEDED = 2
  RUNTIME_ERROR = 3
  INCORRECT_SOLUTION = 4
  DO_NOT_RUN = 5


def string_to_verdict(s):
  if s == "ACCEPTED":
    return Verdict.ACCEPTED
  if s == "WRONG_ANSWER":
    return Verdict.WRONG_ANSWER
  if s == "TIME_LIMIT_EXCEEDED":
    return Verdict.TIME_LIMIT_EXCEEDED
  if s == "RUNTIME_ERROR":
    return Verdict.RUNTIME_ERROR
  if s == "INCORRECT_SOLUTION":
    return Verdict.INCORRECT_SOLUTION
  if s == "DO_NOT_RUN":
    return Verdict.DO_NOT_RUN
  raise RuntimeError("Verdict not valid.")


@attr.s
class Solution(object):
  filename = attr.ib()  # type: str
  verdicts = attr.ib()  # type: List[Verdict]


@attr.s
class ProblemConfig(object):
  title_en = attr.ib()  # type: str
  title_id = attr.ib()  # type: str
  memory_limit_mb = attr.ib()  # type: int
  time_limit_ms = attr.ib()  # type: int
  points = attr.ib()  # type: List[int]
  sample_cases = attr.ib()  # type: List[List[bool]]
  test_groups = attr.ib()  # type: List[List[bool]]
  solutions = attr.ib()  # type: List[Solution]

  def check_sample_cases(self):
    for i in range(len(self.sample_cases)):
      if len(self.sample_cases[i]) != len(self.points):
        raise RuntimeError("All elements in sample_cases must have |`points`| "
                           "elements.")

  def check_test_groups(self):
    for i in range(len(self.test_groups)):
      if len(self.test_groups[i]) != len(self.points):
        raise RuntimeError("All elements in test_groups must have |`points`| "
                           "elements.")

  def check_solutions(self):
    for solution in self.solutions:
      if len(solution.verdicts) != len(self.points):
        raise RuntimeError("All elements in solution.verdicts must have "
                           "|`points`| elements.")

  def check_parameters(self):
    self.check_sample_cases()
    self.check_solutions()


def parse_json_to_problem_config(object):
  object_json = json.loads(object)
  solutions = []
  for solution in object_json["solutions"]:
    solutions.append(
        Solution(solution["filename"],
                 list(map(string_to_verdict, solution["verdicts"]))))
  problem_config = ProblemConfig(
    object_json["title_en"],
    object_json["title_id"],
    object_json["memory_limit_mb"],
    object_json["time_limit_ms"],
    object_json["points"],
    object_json["sample_cases"],
    object_json["test_groups"],
    solutions)
  problem_config.check_parameters()
  return problem_config


def parse_json_file_to_problem_config(path):
  with open(path) as f:
    return parse_json_to_problem_config(f.read())


def get_problem_config(problem_dir):
  return parse_json_file_to_problem_config(os.path.join(problem_dir,
                                                        _CONFIG_FILENAME))
