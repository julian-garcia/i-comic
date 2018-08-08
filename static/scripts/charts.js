var featureArray = [];
var featureArrayWeek = [];
var featureArrayWeekGrouped = [];
var featureArrayMonth = [];
var featureArrayMonthGrouped = [];
var bugArray = [];
var bugArrayWeek = [];
var bugArrayWeekGrouped = [];
var bugArrayMonth = [];
var bugArrayMonthGrouped = [];

function populate_arrays(inArray, outArray, type) {
  inArray.forEach(function(item, index) {
    var dt_raised = new Date(item.dt_raised);

    if (type == "daily") {
      outArray.push({x: Date.parse(item.dt_raised), y: item.ticket_count});
    }

    if (type == "weekly") {
      var week_date = new Date(dt_raised.getFullYear(),
                               dt_raised.getMonth(),
                               dt_raised.getDate() - dt_raised.getDay());
      outArray.push({x: Date.parse(week_date), y: item.ticket_count});
    }

    if (type == "monthly") {
      var month_date = new Date(dt_raised.getFullYear(),
                                dt_raised.getMonth(), 1);

      outArray.push({x: Date.parse(month_date), y: item.ticket_count});
    }
  });
}

function group_array(inarray, outarray) {
  inarray.reduce(function (res, value) {
      if (!res[value.x]) {
          res[value.x] = {
              x: value.x,
              y: 0
          };
          outarray.push(res[value.x])
      }
      res[value.x].y += value.y
      return res;
  }, {});
}

function render_chart(chartBugArray, chartFeatureArray, chartClass) {
  var chart = new Chartist.Line(chartClass, {
    series: [
      {
        name: 'Features',
        data: chartFeatureArray
      },
      {
        name: 'Bugs',
        data: chartBugArray
      }
    ]
  }, {
    axisX: {
      type: Chartist.FixedScaleAxis,

      labelInterpolationFnc: function(value) {
        return moment(value).format('MMM D');
      }
    },
    axisY: {
      onlyInteger: true
    },
    plugins: [
      Chartist.plugins.ctAxisTitle({
        axisX: {
          axisTitle: 'Date Raised',
          axisClass: 'ct-axis-title',
          offset: {
            x: 0,
            y: 30
          },
          textAnchor: 'middle'
        },
        axisY: {
          axisTitle: 'Tickets',
          axisClass: 'ct-axis-title',
          offset: {
            x: 0,
            y: 20
          },
          textAnchor: 'middle',
          flipTitle: true
        }
      })
    ]
  });
}

populate_arrays(feature_data, featureArray, 'daily');
populate_arrays(bug_data, bugArray, 'daily');
populate_arrays(feature_data_weekly, featureArrayWeek, 'weekly');
populate_arrays(bug_data_weekly, bugArrayWeek, 'weekly');
populate_arrays(feature_data_monthly, featureArrayMonth, 'monthly');
populate_arrays(bug_data_monthly, bugArrayMonth, 'monthly');

group_array(featureArrayWeek, featureArrayWeekGrouped);
group_array(featureArrayMonth, featureArrayMonthGrouped);
group_array(bugArrayWeek, bugArrayWeekGrouped);
group_array(bugArrayMonth, bugArrayMonthGrouped);

render_chart(bugArray, featureArray, '.ct-chart');
render_chart(bugArrayWeekGrouped, featureArrayWeekGrouped, '.ct-chart-week');
render_chart(bugArrayMonthGrouped, featureArrayMonthGrouped, '.ct-chart-month');
