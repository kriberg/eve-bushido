var gulp = require('gulp'),
    connect = require('gulp-connect'),
    proxy = require('http-proxy-middleware');

gulp.task('webserver', function() {
    connect.server({
        port: 5000,
        livereload: true,
        root: 'app',
        debug: true,
        middleware: function (connect, opt) {
            return [
                proxy('/dojo', {
                    target: 'http://localhost:8000'
                })
            ];
        }
    })
});


gulp.task('default', ['webserver']);