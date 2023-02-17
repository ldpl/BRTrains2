# So there are two types of definition: old and new (old and new here being within the context of the work on this specific set)

# Old would be something like this Class 158 (the old ones are usually named BRXXX)

# https://github.com/BRTrains/BRTrains2/blob/master/src/trains/dmu/BR158_3.pnml

# Spritesets are defined lines 0-47, switches are lines 49-106 (some for sprites, others for other things like articulation and livery list), and then the unit definitions are line 108 onward, noting that there are 3 separate definitions for the 3 cars (front, rear, and middle), articulated together by one of the switches

# Then there's a very similar file for the 2-car class 158

# https://github.com/BRTrains/BRTrains2/blob/master/src/trains/dmu/BR158.pnml

# Noting that some of the switches and spriteset definitions are shared between units sometimes (but, and this is that inconsistency I mentioned, not always)
# And then there's the newer style from MUTS which usually has the spritesets separated into a different file, but starts off with the switches, and then item definitions. Eg this Class 755

# https://github.com/BRTrains/BRTrains2/blob/master/src/trains/bmu/755-3.pnml

# One obvious difference here is that there is only one vehicle definition, and that things like the length and spriteset to use are defined by switches, based on the position in the overall articulated unit
# Ideally we'd be generating something more like the latter, the old style is much more verbose for no real reason in most cases

# That wouldn't be very relational, to do it that way. The idea would be that there would be minimal copy-paste of duplicated data

# I've not exactly fleshed the idea out yet so this wouldn't be a final form, but my plan would be to have something like:

# Type (Electrostar, Aventra, Sprinter etc)
#     Class (eg 168) which contains things that are shared like name, refitable cargo classes, engine class etc
#     Subclass (eg 168/1 3-car) which contains things that may not be shared like capacity, number of cars, top speed (overriding the class, if set here), power type (3rd rail etc)

# Liveries
#     SubType-Livery, linking liveries and SubTypes

# The result is much like inheritance, but the data being stored outside of python and the livery linking would be much nicer IMO

import struct
import glob
import importlib

import grf

from src.common import g

# debugmode_switch.pnml
# if (param[1] == 0) {
#   disable_item(FEAT_TRAINS, 469); // BR121 - Uses livery test strings
#   disable_item(FEAT_TRAINS, 476); // BR70OG (Southern region Class 70) (Unfinished)
#   disable_item(FEAT_TRAINS, 477); // BR71
#   disable_item(FEAT_TRAINS, 483); // RM_TPO
#   disable_item(FEAT_TRAINS, 484); // GWR Great Bear (Unfinished)
#   disable_item(FEAT_TRAINS, 512); // GWR Castle
 # }

# simplemode_switch.pnml
#   if (param[3] == 1) {
#   disable_item(FEAT_TRAINS, 270); // 455
#   disable_item(FEAT_TRAINS, 268); // 455
#   disable_item(FEAT_TRAINS, 256); // 700
#   disable_item(FEAT_TRAINS, 234); // 378
#   disable_item(FEAT_TRAINS, 231, 232);  //378
#   disable_item(FEAT_TRAINS, 225); // 378
#   disable_item(FEAT_TRAINS, 218, 224); // 377
#   disable_item(FEAT_TRAINS, 203, 213); // 375/376/377
#   disable_item(FEAT_TRAINS, 197); // 375 (3-car)
#   disable_item(FEAT_TRAINS, 192); // 221
#   disable_item(FEAT_TRAINS, 181); // 222
#   disable_item(FEAT_TRAINS, 176); // 222
#   disable_item(FEAT_TRAINS, 124); // 390 (11-car)
#   disable_item(FEAT_TRAINS, 97); // 373
#   disable_item(FEAT_TRAINS, 62); // 170
#   disable_item(FEAT_TRAINS, 39); // 158 (3-car)
#   disable_item(FEAT_TRAINS, 51); // 150
#   disable_item(FEAT_TRAINS, 44); // 150
#   disable_item(FEAT_TRAINS, 402); // 165
#   disable_item(FEAT_TRAINS, 399); // 165
#   disable_item(FEAT_TRAINS, 9, 11); // LNER coaches apart from "Tourist Corridor"
#   disable_item(FEAT_TRAINS, 139, 150); // Mk 1 coaches apart from FO/SO (Fist Open/Standard Open)
#   disable_item(FEAT_TRAINS, 322, 323); // Mk2 coaches apart from FO/SO
#   disable_item(FEAT_TRAINS, 15, 18); // Mk3 coaches apart from TF/TS (Trailer First/Trailer Standard)

#  }

# templates.pnml
# switch(FEAT_TRAINS, SELF, GetAdjustedCost, base, param_cost_factor) {
#   1: return base / 4;
#   2: return base / 2;
#   3: return base;
#   4: return base * 2;
#   5: return base * 4;
# }

# TODO sortpurchase.pnml

from src.trains.br755 import br755_3, br755_4
g.add(br755_3, br755_4)
from src.trains.br158 import br158, br158_3
g.add(br158, br158_3)

g.write('brtrains2.grf')
