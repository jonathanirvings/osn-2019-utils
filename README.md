# OSN 2019 Problem Preparation Utilities

## About

Currently `gen_problem.py` generates `generated/` directory containing:

- Ready to upload problem description HTML, together with sample cases, open
subtasks, and subtask headers.
- A ZIP file of all testcases.

Additionally, `gen_problem.py` also checks the following:

- `{slug}_sample_X.in` matches `samples/sample_X.in`.
- `{slug}_X_1.in` matches `opens/open_X.in`.
- All testcases passes input verifier for all subtasks it belongs to.
- All solutions have the expected verdict.

More generated contents (for easier upload process to
[Judgels](https://github.com/ia-toki/judgels)) and validations in
`gen_problem.py` is currently WIP.

## Requirements

- Python 2
- Unix-based operating system
- tcframe >= v1.0 in local machine and $TCFRAME_HOME setup accordingly

## Usage

1. Install all requirements (`pip install -r requirements.txt`)

2. Run `python gen_problem.py problem_dir`, where `problem_dir` is a problem
   directory root. `problem_dir` must be an absolute path and must not contain a
   whitespace.
