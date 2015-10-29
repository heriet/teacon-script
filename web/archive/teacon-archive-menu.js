"use strict";

$(function() {
  var PERIOD_DATA = {
    'period1': {
      results:[
        {key: '001', label: '第1週目'},
        {key: '001_1', label: '第1週目（再）'},
        {key: '002', label: '第2週目'},
        {key: '002_1', label: '第2週目（再）'},
        {key: '003', label: '第3週目'},
      ]
    },
    'period2': {
      results:[
        {key: '001', label: '第1週目'}
      ]
    }
  };

  $('#period-selector').on('change', handlePeriodSelectorChange);
  refreshWeekSelector();

  $('#show-eno').on('click', handleShowEnoClick);
  $('#show-report').on('click', handleShowReportClick);

  function handlePeriodSelectorChange(event) {
  	refreshWeekSelector();
  }

  function refreshWeekSelector() {
  	var period = $('#period-selector').val();
  	var periodData = PERIOD_DATA[period];

  	var $weekSelector = $('#week-selector');
  	$weekSelector.children().remove();

  	periodData.results.forEach(function (result) {
      $weekSelector.append($('<option>').val(result.key).text(result.label))
    });

    $weekSelector.children('option:last-child').prop('selected', 'selected');
  }

  function handleShowEnoClick(event) {
  	
    var eno = parseInt($('#eno').val(), 10);
    var period = $('#period-selector').val();
    var week = $('#week-selector').val();

    if (!eno || !period || !week) {
      return;
    }

    var path = './' + period + '/' + week + '/RESULT/c' + padZero(eno, 4) + '.html';

    if ($('#eno-another-window').is(':checked')) {
      window.open(path);

    } else {
      var targetWindow = parent ? parent.main : window;
      targetWindow.location = path;
    }
  }

  function handleShowReportClick(event) {
    
    var period = $('#period-selector').val();
    var week = $('#week-selector').val();

    if (!period || !week) {
      return;
    }

    var path = '../report/' + period + '/' + week + '.html';

    if ($('#report-another-window').is(':checked')) {
      window.open(path);

    } else {
      var targetWindow = parent ? parent.main : window;
      targetWindow.location = path;
    }
  }

  function padZero(number, length) {
    return (Array(length).join('0') + number).slice(-length);
  }

});