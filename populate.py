#!/usr/bin/python
from elixir import *
from model import *
from datetime import datetime

metadata.bind = "sqlite:///custom.hike" # connect

setup_all()

bl = Location(e=0,n=0)
br = Location(e=10,n=0)
tr = Location(e=10,n=10)
tl = Location(e=0,n=10)

noon = datetime(2009,06,22,12,00)
noon_15 = datetime(2009,06,22,12,15)
noon_30 = datetime(2009,06,22,12,30)
noon_45 = datetime(2009,06,22,12,45)

br_noon = Event(time=noon,loc=br)
tr_noon = Event(time=noon,loc=tr)
tl_noon = Event(time=noon,loc=tl)
bl_noon = Event(time=noon,loc=bl)

br_noon_15 = Event(time=noon_15,loc=br)
tr_noon_15 = Event(time=noon_15,loc=tr)
tl_noon_15 = Event(time=noon_15,loc=tl)
bl_noon_15 = Event(time=noon_15,loc=bl)

br_noon_30 = Event(time=noon_30,loc=br)
tr_noon_30 = Event(time=noon_30,loc=tr)
tl_noon_30 = Event(time=noon_30,loc=tl)
bl_noon_30 = Event(time=noon_30,loc=bl)

br_noon_45 = Event(time=noon_45,loc=br)
tr_noon_45 = Event(time=noon_45,loc=tr)
tl_noon_45 = Event(time=noon_45,loc=tl)
bl_noon_45 = Event(time=noon_45,loc=bl)

team_1 = Team(number=101)
team_2 = Team(number=102)
team_3 = Team(number=103)
team_4 = Team(number=104)

team_1.seen.append(bl_noon)
team_1.seen.append(br_noon_15)
team_1.seen.append(tl_noon_45)

team_2.seen.append(bl_noon)
team_2.seen.append(tl_noon_15)
team_2.seen.append(tr_noon_30)
team_2.seen.append(br_noon_45)

team_3.seen.append(bl_noon)
team_3.seen.append(tr_noon_15)
team_3.seen.append(tl_noon_30)
team_3.seen.append(br_noon_45)

team_4.seen.append(bl_noon)
team_4.seen.append(tr_noon_15)
team_4.seen.append(tr_noon_30)
team_4.seen.append(br_noon_45)

session.commit()
