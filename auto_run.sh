#!/usr/bin/sh
cd /mnt/qa1/shared/heptax-qa
git pull
hash=`git log --pretty=format:'%h' -n 1`
DATE=`date +%Y%m%d`
mkdir -p /mnt/qa1/shared/regression/$DATE
cp -r ./cases  /mnt/qa1/shared/regression/$DATE
cp -r ./scripts  /mnt/qa1/shared/regression/$DATE

cd /mnt/qa1/shared/regression/$DATE
echo `date` >> ver.txt
echo "$hash" >> ver.txt

python ./scripts/run.py
python ./scripts/diff.py
