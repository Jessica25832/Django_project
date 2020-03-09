var gulp = require("gulp");
var cssnano = require("gulp-cssnano");
var rename = require("gulp-rename")
var uglify = require("gulp-uglify")
var concat = require("gulp-concat")
var imagemin = require("gulp-imagemin")
var cache = require("gulp-cache")
var watch = require("gulp-watch")
//cnpm install browser-sync --save-dev 
var bs = require("browser-sync").create()
var sass = require("gulp-sass")
var util = require("gulp-util") //js错误消息写到日志中 不打印
gulp.task("greet",async()=>{
    await console.log("hello world")
})


var path = {
    'html':'./templates/**/',
    'css':'./src/css/**/',
    'js':'./src/js/',
    'images':'/src/images/',
    'css_dist':'./dist/css/',
    'js_dist':'./dist/js/',
    'images_dist':'./dist/images/',
}

gulp.task("html",function(){
    gulp.src(path.html+'*.html')
        .pipe(bs.stream())
})


//压缩并且改名字 css
gulp.task("css",async()=>{
    await gulp.src(path.css+'*.scss') //找到css 源文件
    .pipe(sass().on("error",sass.logError))
    .pipe(cssnano())  //调用插件压缩 
    .pipe(rename({'suffix':'.min'}))
    .pipe(gulp.dest(path.css_dist)) //压缩后的文件放到指定的目录 
    .pipe(bs.stream()) //如果自动刷新浏览器 这一行要加上   
    //获取结果
});

//合并压缩及重命名  
gulp.task("js",async()=>{
    await gulp.src(path.js + "*.js")
    .pipe(uglify().on("error",util.log))
    .pipe(rename({'suffix':'.min'}))
    .pipe(gulp.dest(path.js_dist))
    .pipe(bs.stream())
})

//压缩图片
gulp.task("img",async()=>{
     await gulp.src(path.images+"*.*")
    // .pipe(imagemin())  #无损压缩
    .pipe(cache(imagemin()))  //为了避免重复压缩 压缩以后放缓存中
    .pipe(rename({'suffix':'.min'}))
    .pipe(gulp.dest(path.images_dist))
    .pipe(bs.stream())
})



// //监控文件修改 
gulp.task("watch",function(){
    watch(path.html+".html",gulp.series('html'));
    watch(path.css+"*.scss",gulp.series('css'));
    watch(path.js+"*.js",gulp.series('js'));
    watch(path.images+"*.*",gulp.series('img'));
}) 


gulp.task("bs",function(){
    bs.init({
        'server':{
            'baseDir':'./'
        }
    })
})


gulp.task("default",gulp.parallel('bs','watch'));

//gulp default   或者 直接 gulp  





