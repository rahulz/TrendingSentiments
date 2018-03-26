app = angular.module('ts', []);

app.controller('HomeController', function ($scope, $http, $timeout) {
    $http.post('/').then(function (data) {
        $scope.trends = data.data.data;
        $scope.render_finished()
    });
    var labels = [];
    var d1 = [];
    var d2 = [];
    $scope.render_finished = function () {
        $timeout(function () {
            $scope.trends.forEach(function (trend) {
                labels.push(trend.name);
                d1.push(trend.positive);
                d2.push(trend.negative);
                console.log('canvas-' + trend.name);

            });
            var ctx = document.getElementById('canvas').getContext('2d');

            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Positive',
                            data: d1,
                            backgroundColor: 'green'
                        },
                        {
                            label: 'Negative',
                            data: d2,
                            backgroundColor: 'red'
                        }

                    ]
                },
                options: {
                    scales: {
                        xAxes: [{stacked: true}]
                    }
                }
            })
        }, 100);

    }
});

// app.config(function ($routeProvider) {
//     $routeProvider
//         .when("/", {
//             templateUrl: "dashboard",
//             controller: "DashBoardController"
//         })
//         .when("/user/:id", {
//             templateUrl: "user",
//             controller: "UserController"
//         })
// });
