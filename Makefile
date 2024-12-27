all: setup images songs videos upload

songs:
	cd src && ./songs.py

videos:
	cd src && ./videos.sh

upload:
	cd src && ./upload.py

images:
	cd src && ./images.py

setup:
	[ -d .venv ] || python3 -m venv .venv
	.venv/bin/pip3 install -r requirements.txt
