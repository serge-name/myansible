#!/bin/bash

type="$1"
path="$2"

case $type in
rsa)
  opts='-b 4096'
  ;;
ed25519)
  opts=''
  ;;
*)
  echo "$type: wrong key type" >&2
  exit 1
  ;;
esac

set -e

rm -f $path.new $path.new.pub
ssh-keygen -q -f $path.new -N '' -t $type $opts
mv -f $path.new $path
mv -f $path.new.pub $path.pub
