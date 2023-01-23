#!/bin/bash

#arm-man v0.4

MANPAGES='./arm-man-pages/'
DESTINATION='/usr/local/share/man/man7/'

# It must be a better way, oh well
CHK=`2>/dev/null ls ${DESTINATION}arm* |wc -l`
if (( $CHK > 0 )); then
  if ! [ "$1" = "-f" ]; then
    echo "!) You may overwrite some man pages in $DESTINATION by running this script."
    echo ")) Use -f to overwrite man pages beginning with 'arm', if any."
    exit 3
  fi
fi

cp ${MANPAGES}arm.7   ${DESTINATION}
cp ${MANPAGES}arm32.7 ${DESTINATION}
cp ${MANPAGES}arm64.7 ${DESTINATION}
cp ${MANPAGES}*/*/*.7 ${DESTINATION}
