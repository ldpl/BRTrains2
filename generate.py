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

from src.trains.dmu.br158 import br158, br158_3
from src.trains.bmu.br755 import br755_3, br755_4
from src.trains.bmu.br800 import br800_5, br800_9
from src.trains.emu.br801 import br801_5, br801_9
from src.trains.bmu.br802 import br802_5, br802_9
from src.trains.emu.br803 import br803_5

# TODO sortpurchase.pnml
purchase_order = [
 # item_LNWRWebb,
 # item_GreatBear,
 # item_GWRHall,
 # item_GNRA1,
 # item_LNERA3,
 # item_BR08,
 # item_BR13,
 # item_BR31,
 # item_BR33_0,
 # item_BR33_1,
 # item_BR37,
 # item_BR252,  //Actually Class 41, which is why it's here
 # item_BR253,  //Actually Class 43, which is why it's here
 # item_BR47,
 # item_BR52,
 # item_Kestrel,
 # item_BR55,
 # item_BR57,
 # item_BR60,
 # item_BR66,
 # item_BR67,
 # item_BR68,
 # item_br_68_5a,
 # item_BR70OG,
 # item_BR70,
 # item_BR71,
 # item_BR73GatEx,
 # item_18100,
 # item_BR80,
 # item_BR81,
 # item_BR82,
 # item_BR83,
 # item_BR84,
 # item_BR85,
 # item_BR86,
 # item_BR87,
 # item_BR89,
 # item_BR90,
 # item_BR91,
 # item_BluePullman_6Car, // Don't really belong anywhere but after the IC225 and before the DMUs seems to fit
 # item_BluePullman_8Car, // Don't really belong anywhere but after the IC225 and before the DMUs seems to fit
 # item_BR121,
 # item_BR139,
 # item_BR140,
 # item_BR141,
 # item_BR142,
 # item_BR143,
 # item_BR150,
 # item_BR150_1,
 # item_BR150_2,
 # item_BR151,
 # item_BR153,
 # item_BR155,
 # item_BR156,
    br158, br158_3,
 # item_BR159,
 # item_BR165_0_2,
 # item_BR165_0_3,
 # item_BR165_1_2,
 # item_BR165_1_3,
 # item_BR166,
 # item_BR168,
 # item_BR168_3,
 # item_BR168_4,
 # item_BR170,
 # item_BR170_3,
 # item_BR171,
 # item_BR171_4,
 # item_BR1750,
 # item_BR1751,
 # item_BR180,
 # item_BR185,
 # item_br_195_0,
 # item_br_195_1,
 # item_br_196_0,
 # item_br_196_1,
 # item_br_197_0,
 # item_br_197_1,
 # item_BR220,
 # item_BR221,
 # item_BR221_4,
 # item_BR222,
 # item_BR222_5,
 # item_BR222_1,
 # item_BR230_2CAR,
 # item_BR230_3CAR,
 # item_IE2800,
 # item_BR302,
 # item_BR305_1,
 # item_BR305_2,
 # item_BR310_0,
 # item_BR310_1,
 # item_BR315,
 # item_BR319,
 # item_BR323,
 # item_br_331_0,
 # item_br_331_1,
 # item_BR333,
 # item_BR334,
 # item_br_345,
 # item_BR350,
 # item_BR357,
 # item_APTE,
 # item_BR370,
 # item_BR373,
 # item_BR373_25kv,
 # item_BR373_2,
 # item_BR374,
 # item_BR375_3,
 # item_BR375_4,
 # item_BR376,
 # item_BR377_3,
 # item_BR377_4,
 # item_BR377_4_dv,
 # item_BR377_5,
 # item_BR377_5dv,
 # item_BR378_3dv,
 # item_BR378_4,
 # item_BR378_4dv,
 # item_BR378_5,
 # item_BR378_5dv,
 # item_BR379,
 # item_BR387,
 # item_BR390,
 # item_BR390_11,
 # item_BR395,
 # item_br_397,
 # item_BR411,
 # item_BR411_9,
 # item_BR412,
 # item_BR413,
 # item_BR414_1,
 # item_BR414_2,
 # item_BR415_1,
 # item_BR415_2,
 # item_BR416_1,
 # item_BR416_2,
 # item_BR418_1,
 # item_BR421,
 # item_BR421_5,
 # item_BR421_7,
 # item_BR422,
 # item_BR423,
 # item_BR423_9,
 # item_BR432,
 # item_BR442,
 # item_BR444,
 # item_BR450,
 # item_BR4557,
 # item_BR4558,
 # item_BR4559,
 # item_BR456,
 # item_BR4580,
 # item_BR460,
 # item_BR465,
 # item_BR466,
 # item_BR480,
 # item_BR483,
 # item_BR484,
 # item_BR507,
 # item_BR508_1,
 # item_BR508_2,
 # item_BR700,
 # item_BR700_2,
 # item_br_701_0,
 # item_br_701_5,
 # item_BR707,
 # item_br_710_1,
 # item_br_710_2_4car,
 # item_br_710_2_5car,
 # item_BR717,
 # item_br_720_1,
 # item_br_720_5,
 # item_br_745,
 # item_br_777,
    br755_3, br755_4,
 # item_br_769,
 # item_br_769_9,
    br800_5, br800_9,
    br801_5, br801_9,
    br802_5, br802_9,
    br803_5,
 # item_DR98_9,
 # item_LU1938,
 # item_LUAStock,
 # item_LU1967,
 # item_LUCStock,
 # item_LUDStock,
 # item_LU1986,
 # item_LU1992_4,
 # item_LU1992,
 # item_LU1995,
 # item_LU1996,
 # item_LU2009,
 # item_LULS7,
 # item_LULS8,
 # item_BR325,
 # item_RS_SWB_Hopper,
 # item_BRHHA,
 # item_BRTTA,
 # item_BRContainer,
 # item_RMTPO,
 # item_LNERTK,
 # item_LNERBCK,
 # item_LNERPV,
 # item_LNERBG,
 # item_BRMK1FO,
 # item_BRMK1SO,
 # item_BRMK1TSO,
 # item_BRMK1FK,
 # item_BRMK1CK,
 # item_BRMK1SK,
 # item_BRMK1BSO,
 # item_BRMK1BSOT,
 # item_BRMK1BFK,
 # item_BRMK1BCK,
 # item_BRMK1BSK,
 # item_BRMK1BG,
 # item_BRMK1RK,
 # item_BRMK1RMB,
 # item_BRMK2ATSO,
 # item_BRMK2AFO,
 # item_BRMK2ABSO,
 # item_BRMK2DTSO,
 # item_BRMK2DFO,
 # item_BRMK2DBSO,
 # item_BRMK2DDBSO,
 # item_253_BRMK3TF,
 # item_253_BRMK3TS,
 # item_253_BRMK3TGS,
 # item_253_BRMK3TRSB,
 # item_253_BRMK3TRUB,
 # item_253_BRMK3TRUK,
 # item_BRMk3Sleeper,
]

# TODO fix sorting
prev = None
for v  in purchase_order:
    if prev is not None:
        prev._props['sort_purchase_list'] = v.id
    prev = v

g.add(*purchase_order)

g.write('brtrains2.grf')
