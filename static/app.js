var app = angular.module('myApp', [
    'btford.socket-io',
    'ngCookies'
]);

app.factory('socket', function (socketFactory) {
    var myIoSocket = io.connect('http://' + document.domain + ':' + location.port + '/broadcast');
    socket = socketFactory({
        ioSocket: myIoSocket
    });
    return socket;
});

app.controller('ChatController', ['$scope', '$http', 'socket', '$cookies', function ($scope, $http, socket, $cookies) {
    $scope.messages = [];
    $scope.user = {name: ""};
    $scope.username = $cookies.get('rechat_username');
    socket.on('connect', function() {
        $http({
            method: 'GET',
            url: '/_get_messages'
        }).then(function success(response) {
            $scope.messages = response.data.messages;
        }, function error(response) {

        });
        socket.emit('my event', {data: 'I\'m connected!'});
    });
    $scope.message = {text: ""};

    $scope.newMessage = function () {
        socket.emit('new message', {text: $scope.message.text, username: $scope.username});
        var messageObj = {text: $scope.message.text};
        $scope.message.text = "";
    };

    $scope.setUsername = function () {
        $scope.username = $scope.user.name;
        $cookies.put('rechat_username', $scope.username);
    };

    socket.on('broadcast event', function(msg) {
        msg = {text: msg.text, username: msg.username};
        if ($scope.messages.length >= 25) {
            $scope.messages.shift();
        }
        $scope.messages.push(msg);
    });
}]);

