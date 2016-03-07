setTimeout(function() {
    // replace the current background with a larger image
    var bg = "/static/img/bar.jpg",
        img = new Image();

    img.onload = function() {
        document.body.style.backgroundImage = 'url("' + bg + '")';
    };
    img.src = bg;
}, 1);
