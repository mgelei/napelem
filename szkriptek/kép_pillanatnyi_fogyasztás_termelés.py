#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.ticker as mtick

BASEDIR=os.path.dirname(__file__) + "/.."

if len(os.sys.argv) == 2:
    argdate = os.sys.argv[1]
    maxdate = pd.to_datetime(argdate).date()
    napneve = "-" + str(maxdate)
else:
    maxdate = dt.date.today()
    napneve = ""


df = pd.read_csv(BASEDIR +"/adatok/egyesített.csv", parse_dates=['Idő', 'Nap'])

mindate = (maxdate + pd.DateOffset(days = -3)).date()

df = df[df['Idő'] >= pd.to_datetime(mindate)]
df = df[df['Idő'] < pd.to_datetime(maxdate)]

df['Fogyasztás'] = -df['Fogyasztás']
df['Fogyasztás'] = df['Fogyasztás'] * 4000
df['Napelem fogyasztás'] = df['Napelem fogyasztás'] * 4000
df['Termelés'] = df['Termelés'] * 4000

plot = df.plot.area(x='Idő', y=['Fogyasztás', 'Napelem fogyasztás', 'Termelés'], linewidth = 0,
          label=['Pillanatnyi fogyasztás', 'Napelemből fogyasztás', 'Pillanatnyi termelés'],
          title='Pillanatnyi fogyasztás és termelés  -  [' + str(mindate) + " - " + str(maxdate) + "]", color=['green', 'royalblue', 'cornflowerblue'])

yticks = mtick.FormatStrFormatter('%.0fW')
plot.yaxis.set_major_formatter(yticks)

fig = plot.get_figure()
fig.set_size_inches(15, 5)
fig.savefig(BASEDIR + "/képek/eon/PillanatnyiFogyasztásÉsTermelés"+ napneve +".png", bbox_inches = "tight")
