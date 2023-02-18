import grf

from .templates import TemplateManager


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

g.strings.import_lang_dir('lang', 'english.lng')
templates = TemplateManager.from_toml('templates.toml')

# railtype table
railtypes = {
    'RAIL': g.add_railtype('RAIL'),
    'ELRL': g.add_railtype('ELRL'),
    'BR_3RDR': g.add_railtype('SAA3', '3RDR', 'ELRL'), # 3rd Rail
    'BR_3RDC': g.add_railtype('SAAZ', 'SAA3', '3RDC', '3RDR', 'ELRL'),  # 3rd Rail or Catenary
    'BR_4RDR': g.add_railtype('SAA4', 'SAA3', 'ELRL'),  # 3rd or 4th rail
}
rt_elrl = railtypes['ELRL']
elecrified_railtypes = (railtypes['ELRL'], railtypes['BR_3RDC'])

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

# Set commmon properties to make sure they're not overriden by accident
train_props = dict(
    climates_available=grf.ALL_CLIMATES,
    cargo_age_period=185,
    bitmask_vehicle_info=0,
    extra_weight_per_wagon=0,
    extra_power_per_wagon=0,
    dual_headed=0, # TODO only BRMPV is
    non_refittable_cargo_classes=0,
    refit_cost=0,
    cargo_disallow_refit=b'',
)
