from colorama import Fore, Style
import os
import subprocess

import problem_config

def VerifyInput(problem_dir):
  config = problem_config.get_problem_config(problem_dir)

  assert os.path.exists("tc"), "TC not generated yet"

  verifier = os.path.join(problem_dir, "verifier.py")

  def verify(file, subtask):
    with open(os.path.join("tc", file), "r") as stream:
      try:
        subprocess.check_output(["python", verifier, str(subtask)],
                                 stdin=stream, stderr=subprocess.STDOUT)
      except subprocess.CalledProcessError as e:
        print("%s input failed on subtask %d" % (file, subtask))
        print(e.output.decode('utf-8'))

        return False

    return True

  slug = None
  for file in os.listdir("tc"):
    slug = file.split('_')[0]

  print("Verifying input cases")
  for subtask in range(len(config.points)):
    has_verify_failed = False

    for i, sample_case in enumerate(config.sample_cases):
      if sample_case[subtask]:
        file = "%s_sample_%d.in" % (slug, i + 1)
        if not verify(file, subtask + 1):
          has_verify_failed = True
          break

    for i, test_group in enumerate(config.test_groups):
      if has_verify_failed:
        break
      if test_group[subtask]:
        for file in os.listdir("tc"):
          file_test_group = file.split('_')[1]

          if ".in" not in file or file_test_group == "sample":
            continue

          if int(file_test_group) == i + 1:
            if not verify(file, subtask + 1):
              has_verify_failed = True
              break

    if has_verify_failed:
      print("  subtask {}: {}FAILED{}".format(
            subtask + 1,
            Fore.RED,
            Style.RESET_ALL))
    else:
      print("  subtask {}: {}PASSED{}".format(
            subtask + 1,
            Fore.GREEN,
            Style.RESET_ALL))
