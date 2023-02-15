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
from datetime import date

import grf

import lib


g = grf.NewGRF(
    grfid=b'brv3',  # BRTrains v2, based on BRTrains, BROS, and the Modern UK Trains set (addon to BRTrains)
    name='[grf-py] British Rail Set (BRTrains v2)',
    description=( # TODO translated
        'A development of the BRTrains set (based on BROS) and Modern UK Train'
        ' Set (MUTS).{}{}{WHITE}The British Rail Set (BRTrains v2){COPYRIGHT}2020'
        ' {LTBLUE}Audigex{WHITE}{}MUTS {COPYRIGHT}2020 {LTBLUE}KubaP {WHITE}&'
        ' {GREEN}AlmostCthulhu{WHITE}{}UKTrains (v1) {COPYRIGHT}2015 {LTBLUE}Leander'
        ' {WHITE}& {GREEN}BROS Artists{}{}{WHITE}License: {LTBLUE}GPL v2'
    ),
    version=5,
    min_compatible_version=5,  # bump up this number to version when breaking compatibility
)

Train, MUTrain = map(g.bind, (lib.Train, lib.MUTrain))

g.strings.import_lang_dir('lang', 'english.lng')
templates = lib.TemplateManager.from_toml('templates.toml')

#   param 0 {
#       param_max_speed {
#           type: int;
#           name: string(STR_PARAM_MAX_SPEED);
#           desc: string(STR_PARAM_MAX_SPEED_DESC);
#           min_value: 0;
#           max_value: 1;
#           def_value: 0;
#           names: {
#               0: string(STR_PARAM_MAX_SPEED_SERVICE);
#               1: string(STR_PARAM_MAX_SPEED_DESIGN);
#           };
#       }
#   }
#   param 1 {
#       param_dev_mode{
#           name: string(STR_PARAM_NAME_DEV);
#           desc: string(STR_PARAM_DESC_DEV);
#           min_value: 0;
#           max_value: 1;
#           def_value: 0;
#           names: {
#               0: string(STR_PARAM_DEV_OFF);
#               1: string(STR_PARAM_DEV_ON);
#           };
#       }
#   }
#   param 2 {
#       param_sounds{
#           name: string(STR_PARAM_NAME_SOUNDS);
#           desc: string(STR_PARAM_DESC_SOUNDS);
#           min_value: 0;
#           max_value: 1;
#           def_value: 1;
#           names: {
#               0: string(STR_PARAM_SOUNDS_OFF);
#               1: string(STR_PARAM_SOUNDS_ON);
#           };
#       }
#   }
#   param 3 {
#       param_simple_mode{
#           name: string(STR_PARAM_NAME_SIMPLE);
#           desc: string(STR_PARAM_DESC_SIMPLE);
#           min_value: 0;
#           max_value: 1;
#           def_value: 0;
#           names: {
#               0: string(STR_PARAM_COMPLEX);
#               1: string(STR_PARAM_SIMPLE);
#           };
#       }
#   }
#   param 4 {
#       param_pax{
#           name: string(STR_PARAM_NAME_PAX_MULTIPLIER);
#           desc: string(STR_PARAM_DESC_PAX_MULTIPLIER);
#           min_value: 1;
#           max_value: 4;
#           def_value: 1;
#           names: {
#               1: string(STR_PARAM_1X);
#               2: string(STR_PARAM_2X);
#               3: string(STR_PARAM_3X);
#               4: string(STR_PARAM_4X);
#           };
#       }
#   }
#   param 5 {
#           param_cost_factor{
#               name: string(STR_PARAM_NAME_COST_MULTIPLIER);
#               desc: string(STR_PARAM_DESC_COST_MULTIPLIER);
#               min_value: 1;
#               max_value: 5;
#               def_value: 3;
#               names: {
#                   1: string(STR_PARAM_QUARTER);
#                   2: string(STR_PARAM_HALF);
#                   3: string(STR_PARAM_1X);
#                   4: string(STR_PARAM_2X);
#                   5: string(STR_PARAM_4X);
#               };
#           }
#       }
#   param 6 {
#           param_2cc{
#               name: string(STR_PARAM_NAME_2CC);
#               desc: string(STR_PARAM_DESC_2CC);
#               min_value: 0;
#               max_value: 2;
#               def_value: 1;
#               names: {
#                   0: string(STR_NO_2CC);
#                   1: string(STR_USE_2CC);
#                   2: string(STR_ONLY_2CC);
#               };
#           }
#   }
# }


# RT g.add(lib.set_global_train_y_offset(2))

# RT g.add(lib.set_global_train_depot_width_32())

# disable_item(FEAT_TRAINS);

# if(param["BRT\16", 1] != 0)
# {
#   error(ERROR,string(STR_Error_MUTSBRTrains));
#   deactivate("BRT\16");
# }

# if(param["MUKT", 1] != 0)
# {
#   error(ERROR,string(STR_Error_MUTSBRTrains));
#   deactivate("MUKT");
# }

# if(param["RUKT", 1] != 0)
# {
#   error(ERROR,string(STR_Error_RUKTS));
# }

# railtype table
railtypes = {
    'RAIL': g.add_railtype('RAIL'),
    'ELRL': g.add_railtype('ELRL'),
    'BR_3RDR': g.add_railtype('SAA3', '3RDR', 'ELRL'), # 3rd Rail
    'BR_3RDC': g.add_railtype('SAAZ', 'SAA3', '3RDC', '3RDR', 'ELRL'),  # 3rd Rail or Catenary
    'BR_4RDR': g.add_railtype('SAA4', 'SAA3', 'ELRL'),  # 3rd or 4th rail
}
g.elecrified_railtypes = (railtypes['ELRL'], railtypes['BR_3RDC'])

g.set_cargo_table([
    # Default cargos
    'PASS', 'MAIL', 'COAL', 'FOOD', 'GOLD', 'GOOD', 'GRAI', 'IORE', 'LVST', 'OIL_', 'PAPR', 'STEL', 'VALU', 'WHEA', 'WOOD',

    # Tropical cargos
    'CORE', 'DIAM', 'FRUT', 'MAIZ', 'RUBR', 'WATR',

    # ECS
    'AORE', 'BDMT', 'BRCK', 'CERA', 'CERE', 'CMNT', 'DYES', 'FERT', 'FICR', 'FISH', 'GLAS', 'LIME', 'OLSD', 'PETR', 'PLAS', 'POTA', 'RFPR', 'SAND', 'SULP', 'TOUR', 'VEHI', 'WDPR', 'WOOL',

    # FIRS
    'BEER', 'CLAY', 'ENSP', 'FMSP', 'FRVG', 'GRVL', 'MILK', 'MNSP', 'PHOS', 'PORE', 'RCYC', 'SCMT', 'SGBT', 'SGCN', 'JAVA', 'COPR', 'SUGR',

    # BRIndustry
    'ALCO', 'MEOX', 'BMAT', 'CHEM', 'MACH', 'PROD', 'MEOR', 'ELEC', 'METL', 'COTT', 'WSTE', 'NUCF', 'NUCW', 'AGGR', 'TIMB',
])

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


br755_png = grf.ImageFile('gfx/BR755.png')
br755_sprite = lambda *args, **kw: grf.FileSprite(br755_png, *args, **kw, bpp=8)
br755a = lib.Unit(
    sprites=templates.apply('train28px', 0, 0, br755_sprite),
    length=7,
    electric=True,
)
br755b = lib.Unit(
    sprites=templates.apply('train28px', 0, 23, br755_sprite),
    length=7,
    electric=True,
)
br755c = lib.Unit(
    sprites=templates.apply('train24px', 0, 46, br755_sprite),
    length=6,
    electric=True,
)
br755d = lib.Unit(
    sprites=templates.apply('train24px', 0, 67, br755_sprite),
    length=6,
    electric=True,
)
br755pp = lib.Unit(
    sprites=templates.apply('train20px', 0, 88, br755_sprite),
    length=5,
    electric=False,
)
br755_purchase = templates.apply('purchase', 160, 0, br755_sprite)


br755_common = dict(
    climates_available=grf.ALL_CLIMATES,
    introduction_date=date(2019, 7, 29),
    model_life=grf.VEHICLE_NEVER_EXPIRES,
    vehicle_life=30,
    reliability_decay=0,
    refittable_cargo_classes=grf.CargoClass.PASSENGERS,
    non_refittable_cargo_classes=0,
    loading_speed=15,
    cargo_allow_refit=b'',
    cargo_disallow_refit=b'',

    max_speed=Train.mph(100),
    refit_cost=0,
    track_type=railtypes['RAIL'],
    ai_special_flag=Train.AIFlags.PASSENGER,
    running_cost_base=Train.RunningCost.ELECTRIC,
    dual_headed=0,
    engine_class=Train.EngineClass.DIESEL,
    extra_power_per_wagon=0,
    tractive_effort_coefficient=grf.nml_te(0.3),
    air_drag_coefficient=grf.nml_drag(0.06),
    bitmask_vehicle_info=0,

    additional_text=g.strings['DSC_BR_755'],
)

# Class 755/3 (3.5car)
br755_3 = MUTrain(
    **br755_common,
    id=453,
    name=g.strings['BR_755_3CAR'],
    units=[br755a, br755pp, br755d, br755b],
    cost_factor=62,  # TODO GetAdjustedCost
    running_cost_factor=21,  # TODO GetAdjustedCost
    weight=Train.ton(94.8),

    total_capacity=167,  # TODO * param_pax
    electric_power=Train.hp(3500),
    diesel_power=Train.hp(1290),
    purchase_sprites=br755_purchase,
)

# Class 755/4 (4.5car)
br755_4 = MUTrain(
    **br755_common,
    id=454,
    name=g.strings['BR_755_4CAR'],
    units=[br755a, br755c, br755pp, br755d, br755b],
    cost_factor=76,
    running_cost_factor=25,
    weight=Train.ton(114.3),

    total_capacity=229,
    electric_power=Train.hp(3500),
    diesel_power=Train.hp(2570),
    purchase_sprites=br755_purchase,
)

br755_3.can_attach = br755_4.can_attach = (br755_3, br755_4)

g.write('brtrains2.grf')
