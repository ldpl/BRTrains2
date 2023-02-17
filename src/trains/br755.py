from datetime import date

import grf

from ..common import g, railtypes, train_props, templates
from ..lib import Unit, Train, MUTrain


br755_png = grf.ImageFile('gfx/BR755.png')
br755_sprite = lambda *args, **kw: grf.FileSprite(br755_png, *args, **kw, bpp=8)
br755a = Unit(
    sprites=templates.apply('train28px', 0, 0, br755_sprite),
    length=7,
    electric=True,
)
br755b = Unit(
    sprites=templates.apply('train28px', 0, 23, br755_sprite),
    length=7,
    electric=True,
)
br755c = Unit(
    sprites=templates.apply('train24px', 0, 46, br755_sprite),
    length=6,
    electric=True,
)
br755d = Unit(
    sprites=templates.apply('train24px', 0, 67, br755_sprite),
    length=6,
    electric=True,
)
br755pp = Unit(
    sprites=templates.apply('train20px', 0, 88, br755_sprite),
    length=5,
    electric=False,
)
br755_purchase = templates.apply('purchase', 160, 0, br755_sprite)


br755_common_props = dict(
    **train_props,
    introduction_date=date(2019, 7, 29),
    model_life=grf.VEHICLE_NEVER_EXPIRES,
    vehicle_life=30,
    reliability_decay=0,
    refittable_cargo_classes=grf.CargoClass.PASSENGERS,
    loading_speed=15,
    cargo_allow_refit=b'',

    max_speed=Train.mph(100),
    track_type=railtypes['RAIL'],
    ai_special_flag=Train.AIFlags.PASSENGER,
    running_cost_base=Train.RunningCost.ELECTRIC,
    engine_class=Train.EngineClass.DIESEL,
    tractive_effort_coefficient=grf.nml_te(0.3),
    air_drag_coefficient=grf.nml_drag(0.06),

    additional_text=g.strings['DSC_BR_755'],
)

# Class 755/3 (3.5car)
br755_3 = MUTrain(
    **br755_common_props,
    id=453,
    name=g.strings['BR_755_3CAR'],
    units=[br755a, br755pp, br755d, br755b],
    cost_factor=62,
    running_cost_factor=21,
    weight=Train.ton(94.8),

    total_capacity=167,
    electric_power=Train.hp(3500),
    diesel_power=Train.hp(1290),
    purchase_sprites=br755_purchase,
)

# Class 755/4 (4.5car)
br755_4 = MUTrain(
    **br755_common_props,
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
