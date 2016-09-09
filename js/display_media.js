
function setup() {
    var el = document.getElementById('media_thumbs');
    if (media.length > 1) {
        for (m in media) {
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
    el = document.getElementById('media_object');
    el.innerHTML = media[index];
    if (media.length > 1) {
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
