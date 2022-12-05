var regions;
var values;
var dates;

d3.csv("static/classifications.csv").then(makeChart).then(()=>{
    new Chart(document.getElementById("myChart"), {
        type: 'line',
        data: {
          labels: regions,
          datasets: [
            {
              label: dates,
              backgroundColor: [
                "#3e95cd",
                "#8e5ea2",
                "#3cba9f",
                "#e8c3b9",
                "#c45850",
              ],
              data: values,
            },
            {
              label: 'AB',
              backgroundColor: '#000000',
              data: values,
            },
          ],
        },
        options: {
          legend: { display: false },
          title: {
            display: true,
            text: "Activity",
          },
        },
      });
});
function makeChart(data) {
  regions = data.map((d)=>{
    return d.region;
  });
  values = data.map((d)=>{
    return d.value;
  });
  dates = data.map((d)=>{
    return d.dates;
  });
}
