var timestamps = [];
var people = [];

d3.csv("static/sampleData.csv").then(makeChart).then(()=>{
    new Chart(document.getElementById("myChart"), {
        type: 'bar',
        data: {
          labels: timestamp,
          datasets: [
            {
              label: 'People',
              backgroundColor: [
                // "#91ACBF",
                "#FF6600",
                // "#4A6035",
                // "#626C72",
                // "#777B51",
              ],
              data: people,
            },
            {
              label: 'Dogs',
              backgroundColor: [
                "#91ACDF",
                // "#FF6600",
                // "#4A6035",
                // "#626C72",
                // "#777B51",
              ],
              data: dogs,
            },
          ],
        },
        options: {
          legend: { display: true },
          title: {
            display: true,
            text: "Activity Today",
          },
          scales: {
            y: {
              ticks: {color: 'white'},
            },
            x: {
              ticks: {color: 'white'},
            },
          }
        },
      });
});
function makeChart(data) {
  timestamp = data.map(function (d) {
    date = new Date(parseInt(d.timestamp))
    year = date.getFullYear();
    // return year;
    return `${date.getMonth()}\/${date.getDate()} @ ${date.getHours()}:${date.getMinutes()}`;
  });
  people = data.map((d) => d.people);
  dogs = data.map((d) => d.dogs);
}