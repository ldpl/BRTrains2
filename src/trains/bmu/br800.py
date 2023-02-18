from datetime import date

import grf

from ...common import g, templates
from ...lib import Unit, Train, BMUTrain, EMUTrain, make_liveries


png = grf.ImageFile('gfx/BR80X.png')
liveries = {
    'LNER': 0,
    'GWR': 3,
    'Lumo': 6,
    # 'EMR': 9, TODO unused?
    'TPE': 12,
    'HullTrains': 15,
    'VTEC': 18,
}

livery_name_func = lambda name: g.strings['LIVERY_BR800_' + name]
br80x_front = Unit(
    liveries=make_liveries(png, livery_name_func, liveries),
    length=8,
    power_type=Unit.ELECTRIC | Unit.DIESEL,
)

liveries_middle = make_liveries(png, livery_name_func, {k: v + 1 for k, v in liveries.items()})
br80x_middle = Unit(
    liveries=liveries_middle,
    length=8,
)
br80x_middle_special = Unit(
    # replace HullTrains livery with a special variant
    liveries={**liveries_middle, **make_liveries(png, livery_name_func, {'HullTrains': 16}, xofs=172)},
    length=8,
)

br80x_rear = Unit(
    liveries=make_liveries(png, livery_name_func, {k: v + 2 for k, v in liveries.items()}),
    length=8,
    power_type=Unit.ELECTRIC | Unit.DIESEL,
)

br800_purchase = templates.apply('purchase', 200, 39, lambda *args, **kw: grf.FileSprite(png, *args, **kw, bpp=8))
br801_purchase = templates.apply('purchase', 200, 0, lambda *args, **kw: grf.FileSprite(png, *args, **kw, bpp=8))
br802_purchase = templates.apply('purchase', 200, 13, lambda *args, **kw: grf.FileSprite(png, *args, **kw, bpp=8))
br803_purchase = templates.apply('purchase', 200, 26, lambda *args, **kw: grf.FileSprite(png, *args, **kw, bpp=8))


br800_common_props = dict(
    introduction_date=date(2017, 10, 6),
    model_life=grf.VEHICLE_NEVER_EXPIRES,
    vehicle_life=28,  # (27.5) years after vehicle is deemed "old" and should be replaced
    reliability_decay=0,  # dont reduce reliabilty, (will grow from 75% upwards over the years)
    refittable_cargo_classes=grf.CargoClass.PASSENGERS,
    cargo_allow_refit=b'',

    max_speed=201,
    design_speed=225,
    ai_special_flag=Train.AIFlags.PASSENGER,
    tractive_effort_coefficient=grf.nml_te(0.3),
    air_drag_coefficient=grf.nml_drag(0.06),

    additional_text=g.strings['DSC_BR800'],
)

# Class 800/0/2 (5 car)
br800_5 = BMUTrain(
    **br800_common_props,
    id=459,
    name=g.strings['BR800_5CAR'],
    units=[br80x_front, br80x_middle, br80x_middle, br80x_middle, br80x_rear],
    use_liveries=('LNER', 'GWR', 'VTEC'),
    cost_factor=84,
    running_cost_factor=60,
    weight=Train.ton(205),
    electric_power=Train.hp(3200),
    diesel_power=Train.hp(2250),

    total_capacity={
        'LNER': 302,
        'GWR': 326,
        'VTEC': 302,
    },
    loading_speed=12,
    purchase_sprites=br800_purchase,
)

# Class 800/1/3 (9car)
br800_9 = BMUTrain(
    **br800_common_props,
    id=460,
    name=g.strings['BR800_9CAR'],
    units=[br80x_front, br80x_middle, br80x_middle, br80x_middle, br80x_middle, br80x_middle, br80x_middle, br80x_middle, br80x_rear],
    use_liveries=('LNER', 'GWR', 'VTEC'),
    cost_factor=147,
    running_cost_factor=90,
    weight=Train.ton(438),
    electric_power=Train.hp(5760),
    diesel_power=Train.hp(3750),

    total_capacity={
        'LNER': 611,
        'GWR': 650,
        'VTEC': 611,
    },
    loading_speed=10,
    purchase_sprites=br800_purchase,
)


br800_5.can_attach = br800_9.can_attach = (br800_5, br800_9)  # TODO br802
