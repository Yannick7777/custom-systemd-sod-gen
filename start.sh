#!/bin/bash

call_bsod() {
	sudo journalctl --user --flush --rotate --vacuum-time=1s
	sudo systemd-cat -p emerg echo "$(printf %b '\e[H\e[J')$1"
	sudo /usr/lib/systemd/systemd-bsod &
}

framefile=${1:-'frames.txt'}
echo "Using file $framefile for SOD"
echo "Initializing sequence."

IFS='=' read -ra frames <<< "$(cat "$framefile")"
for frame in "${frames[@]}"; do
	call_bsod "$frame"
	sleep 0.05
done
