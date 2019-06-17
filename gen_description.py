from colorama import Fore, Style
import os
import shutil
import zipfile

import problem_config

_SAMPLES_DIRNAME = "samples"
_OPEN_SUBTASKS_DIRNAME = "opens"
_LANGUAGES = {"en", "id"}

_DESCRIPTION_FILENAME = {
    "en": "description-en.html", "id": "description-id.html"
}
_SAMPLE_INPUT_FORMAT = {
    "en": "Sample Input {}", "id": "Contoh Masukan {}"
}
_SAMPLE_OUTPUT_FORMAT = {
    "en": "Sample Output {}", "id": "Contoh Keluaran {}"
}
_OPEN_SUBTASK_PREFIX = {
    "en": "Consists of only the following test case:",
    "id": "Hanya berisi kasus uji berikut:"
}
_SUBTASK_FORMAT = {
    "en": "Subtask {} ({} points)",
    "id": "Subsoal {} ({} poin)"
}

_SAMPLE_CASES_TAG_FORMAT = "<samplecase{}/>"
_OPEN_SUBTASK_TAG_FORMAT = "<open{}/>"
_SUBTASK_TAG_FORMAT = "<subtask{}/>"


def GenerateDescription(problem_dir):
  config = problem_config.get_problem_config(problem_dir)
  print("Generating problem description")

  for language in _LANGUAGES:
    problem_description_location = os.path.join(problem_dir,
                                                _DESCRIPTION_FILENAME[language])
    
    if os.path.isfile(problem_description_location):
      problem_description = open(problem_description_location, "r").read()

      if not config.interactive:
        # Sample cases
        for index in range(1, len(config.sample_cases) + 1):
          sample_case_html = ""

          sample_case_html += "<h3>{}</h3>\n".format(
              _SAMPLE_INPUT_FORMAT[language].format(index))
          sample_case_html += "<pre>\n"
          with open(os.path.join(problem_dir,
                                 _SAMPLES_DIRNAME,
                                 "sample_%d.in" % index)) as f:
            contents = [x.strip() for x in f.readlines()]
            for content in contents:
              sample_case_html += content + "\n"
          sample_case_html += "</pre>\n"

          sample_case_html += "<h3>{}</h3>\n".format(
              _SAMPLE_OUTPUT_FORMAT[language].format(index))
          sample_case_html += "<pre>\n"
          with open(os.path.join(problem_dir,
                                 _SAMPLES_DIRNAME,
                                 "sample_%d.out" % index)) as f:
            contents = [x.strip() for x in f.readlines()]
            for content in contents:
              sample_case_html += content + "\n"
          sample_case_html += "</pre>"

          problem_description = problem_description.replace(
              _SAMPLE_CASES_TAG_FORMAT.format(index), sample_case_html)

        # Open subtasks
        open_subtasks_location = os.path.join(problem_dir,
                                              _OPEN_SUBTASKS_DIRNAME)
        if os.path.isdir(open_subtasks_location):
          open_subtasks = os.listdir(open_subtasks_location)
          for index in range(1, len(open_subtasks) + 1):
            open_subtask_html = ""

            open_subtask_html += "<p>{}</p>\n".format(
                _OPEN_SUBTASK_PREFIX[language])
            open_subtask_html += "<pre>\n"
            with open(os.path.join(problem_dir,
                                   _OPEN_SUBTASKS_DIRNAME,
                                   "open_%d.in" % index)) as f:
              contents = [x.strip() for x in f.readlines()]
              for content in contents:
                open_subtask_html += content + "\n"
            open_subtask_html += "</pre>"

            problem_description = problem_description.replace(
                _OPEN_SUBTASK_TAG_FORMAT.format(index), open_subtask_html)

      # Subtasks
      for index in range(1, len(config.points) + 1):
        subtask_html = "<h4>{}</h4>".format(
            _SUBTASK_FORMAT[language].format(index, config.points[index - 1]))

        problem_description = problem_description.replace(
            _SUBTASK_TAG_FORMAT.format(index), subtask_html)

      generated_dir = os.path.join(problem_dir, "generated")
      with open(os.path.join(generated_dir,
                             _DESCRIPTION_FILENAME[language]), "w") as f:
        f.write(problem_description)

      print("  lang {}: {}{}{}".format(
          language, 
          Fore.GREEN,
          "OK", 
          Style.RESET_ALL))
    else:
      print("  lang {}: {}{}{}".format(
          language, 
          Fore.RED, 
          "FAIL: {} is not found".format(problem_description_location), 
          Style.RESET_ALL))

  if os.path.isdir(os.path.join(problem_dir, "render")):
    shutil.copytree(os.path.join(problem_dir, "render"),
                    os.path.join(generated_dir, "render"))
    zip = zipfile.ZipFile(os.path.join(generated_dir, "render.zip"), "w")
    for root, _, files in os.walk(os.path.join(generated_dir, "render")):
      for file in files:
        zip.write(os.path.join(root, file), file)
    zip.close()
