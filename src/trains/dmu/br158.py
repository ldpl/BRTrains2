from datetime import date

import grf

from ...common import g, railtypes, templates
from ...lib import Unit, Train, DMUTrain, make_liveries


br158a_png = grf.ImageFile('gfx/BR158a.png')
br158_purchase = templates.apply('purchase', 0, 0, lambda *args, **kw: grf.FileSprite(br158a_png, *args, **kw, bpp=8))

# TODO livery order

br158ab_liveries = {
    'RegionalExpress': 10,
    'WalesWest': 12,
    'AlphaWales': 3,
    'AlphaWessex': 8,
    'WessexGinster': 11,
    'ArrivaSilver': 1,
    'ArrivaTPNS': 16,
    'ATW': 0,
    'ATWMail': 5,
    'FNW': 2,
    'FirstScotRail': 13,
    'FirstTPE': 17,
    'FGW': 20,
    'NatExScotRail': 9,
    'WYPTEMetro': 15,
    'NorthernRail': 6,
    'NorthernRailMetro': 4,
    'ScotrailSaltire': 14,
    'Central': 7,
    'EMT': 18,
    'NSE': 19,
    'SWT': 18,  # TODO same as EMT?
    'Northern': 21,
    'EMRMaroonWhite': 22,
    'EMRTransition': 23,
    'SWR': 24,
    'TfW': 25,
    'NorthernToY': 26,
}

br158a = Unit(
    liveries=make_liveries(br158a_png, br158ab_liveries, yofs=13),
    length=8,
    power_type=Unit.DIESEL,
    colour_mapping=grf.Palette.CC_FIRST,
)

br158b = Unit(
    liveries=make_liveries(grf.ImageFile('gfx/BR158b.png'), br158ab_liveries, yofs=13),
    length=8,
    power_type=Unit.DIESEL,
    colour_mapping=grf.Palette.CC_FIRST,
)

br158c_liveries = {
    'RegionalExpress': 10,
    'ArrivaTPNS': 16,
    'FirstTPE': 17,
    'FGW': 20,
    'WYPTEMetro': 15,
    'NorthernRail': 6,
    'EMT': 18,
    'NSE': 19,
    'SWT': 18,
    'Northern': 21,
    # TOOD 'SWR': 24,  has spriteset but not in subtype switch ?
}

br158c_png = grf.ImageFile('gfx/BR158c.png')
br158_3_purchase = templates.apply('purchase', 0, 0, lambda *args, **kw: grf.FileSprite(br158c_png, *args, **kw, bpp=8))

br158c = Unit(
    liveries=make_liveries(br158c_png, br158c_liveries, yofs=13),
    length=8,
    power_type=Unit.DIESEL,
    colour_mapping=grf.Palette.CC_FIRST,
)

br158_common_props = dict(
    introduction_date=date(1989, 4, 21),
    model_life=8,
    retire_early=1,
    vehicle_life=50,
    reliability_decay=7,
    refittable_cargo_classes=grf.CargoClass.PASSENGERS,
    loading_speed=20,
    cargo_allow_refit=b'',  # TODO PASS, TOUR

    max_speed=Train.mph(90),
    track_type=railtypes['RAIL'],
    ai_special_flag=Train.AIFlags.CARGO,
    running_cost_base=Train.RunningCost.DIESEL,
    engine_class=Train.EngineClass.DIESEL,
    # effect_spawn_model_and_powered: EFFECT_SPAWN_MODEL_DIESEL;
    tractive_effort_coefficient=grf.nml_te(0.3),
    air_drag_coefficient=grf.nml_drag(0.1),
)

br158 = DMUTrain(
    **br158_common_props,
    id=36,
    name=g.strings['NAME_BR158'],
    units=[br158a, br158b],
    cost_factor=38,
    running_cost_factor=20,
    weight=Train.ton(76),

    total_capacity=69 * 2,
    power=Train.hp(700),
    purchase_sprites=br158_purchase,
    # TODO additional_text=g.strings['DSC_BR_755'],
    # TODO create_effect:                      diesel_create_visual_effect;
    # TODO sound_effect:                       sw_dmu_sound;
)

br158_3 = DMUTrain(
    **br158_common_props,
    id=39,
    name=g.strings['NAME_BR158_3'],
    units=[br158a, br158b, br158c],
    cost_factor=50,
    running_cost_factor=28,
    weight=Train.ton(113),

    total_capacity=69 * 3,
    power=Train.hp(1050),
    purchase_sprites=br158_3_purchase,
    # TODO additional_text=g.strings['DSC_BR_755'],
    # TODO create_effect:                      diesel_create_visual_effect;
    # TODO sound_effect:                       sw_dmu_sound;
)
