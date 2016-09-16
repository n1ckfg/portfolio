# Portfolio

Static site generator / personal portfolio site

    ./generate.py
    cd www
    python3 -m http.server &
    open http://localhost:8000

...might want to do this first (it helps opengraph too):

    cd images
    for i in *.jpg; do echo "Processing $i"; exiftool -all= "$i"; done

### Copyright/License

Copyright (c) 2016 Brian House
