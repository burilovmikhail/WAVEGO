#!/bin/bash
for dev in $(ls /dev/video* 2>/dev/null | sort -V); do
    if v4l2-ctl --device "$dev" --info 2>/dev/null | grep -q 'Video Capture'; then
        echo "$dev"
        exit 0
    fi
done
echo "No capture device found" >&2
exit 1
