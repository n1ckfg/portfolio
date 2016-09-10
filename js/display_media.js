
function setup() {
    var el = document.getElementById('media_thumbs');
    if (num_media > 1) {
        for (var m=0; m<num_media; m++) {
            console.log(m);
            var sq = document.createElement('a');
            sq.innerHTML = "&nbsp;&#9675;&nbsp;";
            sq.setAttribute('onClick', 'javascript:displayMedia(' + m + '); return false;'); 
            el.appendChild(sq);
        }
    } else {
        el.parentNode.removeChild(el);
    }
    displayMedia(0);
}

function displayMedia(index) {
    index = parseInt(index);    
    if (isNaN(index)) index = 0;
    for (var m=0; m<num_media; m++) {
        el = document.getElementById('media_' + m);
        if (m == index) {
            el.style.display = "block";
        } else {
            el.style.display = "none";
        }
    }
    if (num_media > 1) {
        var el = document.getElementById('media_thumbs');
        for (c in el.childNodes) {
            if (c == index + 1) {
                el.childNodes[c].innerHTML = "<span class='on'>&nbsp;&#9679;&nbsp;</span>";
            } else {
                el.childNodes[c].innerHTML = "&nbsp;&#9675;&nbsp;";
            }
        }
    }
}

window.onload = setup;
