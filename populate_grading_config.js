// Insert problem config.json in the config variable, and run this script on
// the browser console while the browser is showing the Judgels Problem Grading
// Config page.

config = {};

_DEFAULT_JUDGELS_SUBTASK = 10;

function getSampleInputName(sample, subtask) {
  return 'sampleTestCaseSubtaskIds[' + sample + '][' + subtask + ']';
}

function getTestGroupInputName(test_group, subtask) {
  return 'testGroupSubtaskIds[' + test_group + '][' + subtask + ']';
}

function getSubtaskPointsInputName(subtask) {
  return 'subtaskPoints[' + subtask + ']';
}

function fillTimeAndMemoryLimitValues() {
  $('input[name="timeLimit"]').val(config.time_limit_ms);
  $('input[name="memoryLimit"]').val(config.memory_limit_mb * 1024);
}

function fillSampleCasesSubtasksAllocation() {
  for (var sample = 0; sample < config.sample_cases.length; ++sample) {
    for (var subtask = 0;
         subtask < config.sample_cases[sample].length;
         ++subtask) {
      $('input[name="' + getSampleInputName(sample, subtask) + '"]').prop(
          "checked", config.sample_cases[sample][subtask]);
    }
    for (var subtask = config.sample_cases[sample].length;
         subtask < _DEFAULT_JUDGELS_SUBTASK;
         ++subtask) {
      $('input[name="' + getSampleInputName(sample, subtask) + '"]').prop(
          "checked", false);
    }
  }
}

function fillTestGroupsSubtasksAllocation() {
  for (var test_group = 0;
       test_group < config.test_groups.length;
       ++test_group) {
    if ($('input[name="'
          + getTestGroupInputName(test_group, 0)
          + '"]').length == 0) {
      $("#test-group-add").click();
    }
    for (var subtask = 0;
         subtask < config.test_groups[test_group].length;
         ++subtask) {
      $('input[name="'
        + getTestGroupInputName(test_group, subtask)
        + '"]').prop("checked", config.test_groups[test_group][subtask]);
    }
    for (var subtask = config.test_groups[test_group].length;
         subtask < _DEFAULT_JUDGELS_SUBTASK;
         ++subtask) {
      $('input[name="'
        + getTestGroupInputName(test_group, subtask)
        + '"]').prop("checked", false);
    }
  }
}

function fillSubtasksPoints() {
  for (var subtask = 0; subtask < config.points.length; ++subtask) {
    $('input[name="' + getSubtaskPointsInputName(subtask) + '"]').val(
        config.points[subtask]);
  }
  for (var subtask = config.points.length;
       subtask < _DEFAULT_JUDGELS_SUBTASK;
       ++subtask) {
    $('input[name="' + getSubtaskPointsInputName(subtask) + '"]').val("");
  }
}

function fillCommunicator () {
  $('select[name="communicator"]').val("communicator.cpp");
}

function fillCustomScorer() {
  $('select[name="customScorer"]').val("scorer.cpp");
}

fillTimeAndMemoryLimitValues();
fillSampleCasesSubtasksAllocation();
fillTestGroupsSubtasksAllocation();
fillSubtasksPoints();

if (config.interactive) {
  fillCommunicator();
} else {
  fillCustomScorer();
}
