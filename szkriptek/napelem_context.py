#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import datetime as dt
import dateutil.relativedelta

BASEDIR=os.path.dirname(__file__) + "/.."

def daily():
    ctx = NapelemContext()
    ctx.daily()
    return ctx
    
def monthly():
    ctx = NapelemContext()
    ctx.monthly()
    return ctx

def yearly():
    ctx = NapelemContext()
    ctx.yearly()
    return ctx


class NapelemContext:
    def __init__(self):
        self.df = pd.read_csv(BASEDIR +"/adatok/inverter.csv", parse_dates=['Time'])
        pass
    
    def daily(self):
        if len(os.sys.argv) == 2:
            argdate = os.sys.argv[1]
            self.mindate = pd.to_datetime(argdate)
            self.filesuffix = "-" + str(self.mindate.date())
        else:
            self.mindate = pd.to_datetime(dt.date.today())
            self.filesuffix = ""
        self.maxdate = self.mindate + pd.DateOffset(days = 1)
        self.df = self.filter(self.df)
        self.datetext = str(self.mindate.date())

    def monthly(self):
        if len(os.sys.argv) == 2:
            argdate = os.sys.argv[1]
            self.mindate = pd.to_datetime(argdate)
            self.maxdate = self.mindate + dateutil.relativedelta.relativedelta(months=1)
            self.filesuffix = "-" + self.mindate.strftime('%Y-%m')
            self.datetext = self.mindate.strftime('%Y-%m')
        else:
            self.maxdate = pd.to_datetime(dt.date.today() + dateutil.relativedelta.relativedelta(days=1))
            self.mindate = pd.to_datetime(self.maxdate - dateutil.relativedelta.relativedelta(months=1))
            self.filesuffix = ""
            self.datetext = "[" + str(self.mindate.date()) + " - " + str(dt.date.today()) + "]"
        self.df = self.filter(self.df)

    def yearly(self):
        if len(os.sys.argv) == 2:
            argdate = os.sys.argv[1]
            self.mindate = pd.to_datetime(argdate)
            self.maxdate = self.mindate + dateutil.relativedelta.relativedelta(years=1)
            self.filesuffix = "-" + self.mindate.strftime('%Y')
            self.datetext = self.mindate.strftime('%Y')
        else:
            self.maxdate = pd.to_datetime(dt.date.today() + dateutil.relativedelta.relativedelta(days=1))
            self.mindate = pd.to_datetime(self.maxdate - dateutil.relativedelta.relativedelta(years=1))
            self.filesuffix = ""
            self.datetext = "[" + str(self.mindate.date()) + " - " + str(dt.date.today()) + "]"
        self.df = self.filter(self.df)

    def filter(self, df):
        df = df[df['Time'] >= self.mindate]
        df = df[df['Time'] < self.maxdate]
        return df
    
    def getDataframe(self):
        return self.df
    
    def date(self):
        return self.datetext

    def fileName(self, name):
        return name.replace("%s", self.filesuffix)

    def roundUp(self, limit, *dfs):
        maxa = None
        for df in dfs:
            maxv = df.max()
            if maxa is None:
                maxa = maxv
            else:
                maxa = max(maxa, maxv)

        limdelta = limit - limit / 100
        
        return int((maxa + limdelta) / limit) * limit
