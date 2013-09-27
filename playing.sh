#!/bin/sh
while [ true ]; do
  ncmpcpp --now-playing "%a - %t" > ~/ftp/site/playing.html
  echo "<br /><audio controls><source src="http://nantes.folschette.name:8000/mpd.ogg"></audio>" >> ~/ftp/site/playing.html
  sleep 5
done
