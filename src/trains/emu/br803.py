from datetime import date

import grf

from ...common import g, templates
from ...lib import Unit, Train, BMUTrain, EMUTrain, make_liveries
from ..bmu.br800 import br80x_front, br80x_middle, br80x_rear, br803_purchase


br803_common_props = dict(
    model_life=grf.VEHICLE_NEVER_EXPIRES,
    introduction_date=date(2019, 9, 16),
    vehicle_life=28,  # (27.5) years after vehicle is deemed "old" and should be replaced
    reliability_decay=0,  # dont reduce reliabilty, (will grow from 75% upwards over the years)
    refittable_cargo_classes=grf.CargoClass.PASSENGERS,
    cargo_allow_refit=b'',

    max_speed=201,
    design_speed=225,
    ai_special_flag=Train.AIFlags.PASSENGER,
    tractive_effort_coefficient=grf.nml_te(0.3),
    air_drag_coefficient=grf.nml_drag(0.06),

    additional_text=g.strings['DSC_BR803'],
)

# Class 803/1 (5 car)
br803_5 = EMUTrain(
    **br803_common_props,
    id=547,
    name=g.strings['BR803_5CAR'],
    units=[br80x_front, br80x_middle, br80x_middle, br80x_middle, br80x_rear],
    use_liveries=('Lumo',),
    cost_factor=84,
    running_cost_factor=60,
    weight=Train.ton(205),
    power=Train.hp(3200),

    total_capacity=302,
    loading_speed=12,
    purchase_sprites=br803_purchase,
)

br803_5.can_attach = (br803_5,)
