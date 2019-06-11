import filecmp
import os
import shutil
import subprocess
import zipfile

import problem_config


def _check_samples(problem_dir):
  config = problem_config.get_problem_config(problem_dir)
  slug = None
  for root, _, files in os.walk("tc"):
    for file in files:
      slug = file.split('_')[0]
  for i in range(len(config.sample_cases)):
    assert filecmp.cmp(os.path.join(problem_dir,
                                    "samples",
                                    "sample_%d.in" % (i + 1)),
                       os.path.join("tc",
                                    "%s_sample_%d.in" % (slug, i + 1))
                      ), "Sample input %d is different." % (i + 1)
    assert filecmp.cmp(os.path.join(problem_dir,
                                    "samples",
                                    "sample_%d.out" % (i + 1)),
                       os.path.join("tc",
                                    "%s_sample_%d.out" % (slug, i + 1))
                      ), "Sample output %d is different." % (i + 1)

def _check_open_subtasks(problem_dir):
  config = problem_config.get_problem_config(problem_dir)
  slug = None
  for root, _, files in os.walk("tc"):
    for file in files:
      slug = file.split('_')[0]
  open_subtasks = os.listdir(os.path.join(problem_dir, "opens"))
  for i in range(len(open_subtasks)):
    assert filecmp.cmp(os.path.join(problem_dir,
                                    "opens",
                                    "open_%d.in" % (i + 1)),
                       os.path.join("tc",
                                    "%s_%d_1.in" % (slug, i + 1))
                      ), "Open subtask %d is different." % (i + 1)


def GenerateTestCase(problem_dir):
  config = problem_config.get_problem_config(problem_dir)

  def compile(file, executable):
    subprocess.call(["g++", "-std=c++11", "-O2", "-o", executable, file])

  compile(os.path.join(problem_dir, "scorer.cpp"), "scorer")
  compile(os.path.join(problem_dir, "solution.cpp"), "solution")

  spec_file = os.path.join(problem_dir, "spec.cpp")
  runner_exec = os.path.join(problem_dir, "runner")

  os.system(' '.join([
      "g++",
      "-std=c++11",
      "\'-D__TCFRAME_SPEC_FILE__=\"%s\"\'" % spec_file,
      "-I",
      "%s/include" % os.environ['TCFRAME_HOME'],
      "-o",
      "%s" % runner_exec,
      "%s/src/tcframe/runner.cpp" % os.environ['TCFRAME_HOME']
  ]))

  subprocess.call([runner_exec])

  _check_samples(problem_dir)
  print("Sample cases match")

  _check_open_subtasks(problem_dir)
  print("Open subtasks match")

  generated_dir = os.path.join(problem_dir, "generated")

  zip = zipfile.ZipFile(os.path.join(generated_dir, "testcases.zip"), "w")
  for root, _, files in os.walk("tc"):
    for file in files:
      zip.write(os.path.join("tc", file), file)

  zip.close()
