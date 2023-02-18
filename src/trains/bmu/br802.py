from datetime import date

import grf

from ...common import g, templates
from ...lib import Unit, Train, BMUTrain, EMUTrain, make_liveries
from .br800 import br80x_front, br80x_middle, br80x_middle_special, br80x_rear, br802_purchase, br800_5, br800_9


br802_common_props = dict(
    introduction_date=date(2018, 8, 18),
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
)

# Class 800/0/2 (5 car)
br802_5 = BMUTrain(
    **br802_common_props,
    id=461,
    name=g.strings['BR802_5CAR'],
    units=[br80x_front, br80x_middle, br80x_middle_special, br80x_middle, br80x_rear],
    use_liveries=('GWR', 'TPE', 'HullTrains'),
    cost_factor=92,
    running_cost_factor=60,
    weight=Train.ton(261),
    electric_power=Train.hp(3200),
    diesel_power=Train.hp(2820),

    total_capacity={
        'GWR': 342,
        'TPE': 326,
        'HullTrains': 342,
    },
    loading_speed=12,
    purchase_sprites=br802_purchase,
    additional_text=g.strings['DSC_BR802_5CAR'],
)

# Class 800/1/3 (9car)
br802_9 = BMUTrain(
    **br802_common_props,
    id=460,
    name=g.strings['BR802_9CAR'],
    units=[br80x_front, br80x_middle, br80x_middle, br80x_middle, br80x_middle, br80x_middle, br80x_middle, br80x_middle, br80x_rear],
    use_liveries=('GWR',),
    cost_factor=147,
    running_cost_factor=90,
    weight=Train.ton(457),
    electric_power=Train.hp(5760),
    diesel_power=Train.hp(4700),

    total_capacity=647,
    loading_speed=10,
    purchase_sprites=br802_purchase,
    additional_text=g.strings['DSC_BR802_9CAR'],
)

br800_5.can_attach = br800_9.can_attach = br802_5.can_attach = br802_9.can_attach = (br800_5, br800_9, br802_5, br802_9)
