#!/bin/bash

cd $HOME/pycoa/daily_plots
DISPLAY=:
DATE=`date +'%Y%m%d%H%M'`
LOGDIR=www/log
for w in mpox owid spf
do
	./daily_$w.py > $LOGDIR/$w.$DATE.out 2> $LOGDIR/$w.$DATE.err
done
