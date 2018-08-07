var featureArray = [];
var bugArray = [];

feature_data.forEach(function(item) {
  featureArray.push({x: Date.parse(item.dt_raised), y: item.ticket_count});
});
bug_data.forEach(function(item) {
  bugArray.push({x: Date.parse(item.dt_raised), y: item.ticket_count});
});

var chart = new Chartist.Line('.ct-chart', {
  series: [
    {
      name: 'Features',
      data: featureArray
    },
    {
      name: 'Bugs',
      data: bugArray
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
