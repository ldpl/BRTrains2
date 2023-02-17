import json

import grf

from .common import elecrified_railtypes


class Train(grf.Train):

    next_articulated_id = 4000

    def __init__(self, *args, length, **kw):
        super().__init__(
            *args,
            shorten_by=8-length,
            **kw,
        )

    def add_articulated_part(self, length, **kw):
        super().add_articulated_part(
            **kw,
            shorten_by=8-length,
            id=self.__class__.next_articulated_id
        )
        self.__class__.next_articulated_id += 1


class Unit:
    def __init__(self, *, length, electric, sprites=None, liveries=None, colour_mapping=None):
        if liveries is None:
            assert sprites is not None
            liveries = {None: sprites}
        self.liveries = liveries
        self.length = length
        self.electric = electric
        self.colour_mapping = colour_mapping

    def make_props(self, use_liveries):
        if self.electric:
            electric_effect = Train.visual_effect_and_powered(Train.VisualEffect.ELECTRIC, position=2, wagon_power=False)
            default_effect = Train.VisualEffect.DISABLE
        else:
            electric_effect = Train.VisualEffect.DISABLE
            default_effect = Train.visual_effect_and_powered(Train.VisualEffect.DIESEL, position=2, wagon_power=False)
        liveries = [
            {
                'name': name,
                'sprites': sprites,
            }
            for name, sprites in self.liveries.items() if name in use_liveries
        ]
        callbacks = {
            'visual_effect_and_powered': grf.Switch(
                'current_railtype',
                {
                    rt: electric_effect
                    for rt in elecrified_railtypes
                },
                default_effect,
            )
        }

        if self.colour_mapping is not None:
            callbacks['colour_mapping'] = self.colour_mapping

        return dict(
            liveries=liveries,
            length=self.length,
            callbacks=callbacks,
        )


class MUTrain(Train):
    def __init__(self, *, id, units, total_capacity, purchase_sprites=None, electric_power=None, diesel_power=None, **kw):
        # TODO GetAdjustedCost for cost_factor and runnig_cost_factor
        # TODO multiply capacity by param_pax
        assert units
        self.electric_power = electric_power
        self.diesel_power = diesel_power
        self.units = units
        self.can_attach = None
        self.purchase_sprites = purchase_sprites

        power = electric_power
        if power is None or (diesel_power is not None and diesel_power > power):
            power = diesel_power

        common_props = {
            'misc_flags': Train.Flags.MULTIPLE_UNIT,
        }

        # Split total capacity between units, as equially as possible
        assert total_capacity <= 255 * len(self.units), total_capacity
        capacity = [total_capacity // len(self.units)] * len(self.units)
        for i in range(total_capacity - sum(capacity)):
            capacity[i] += 1

        # Find common liveries
        self.common_liveries = set.intersection(*(set(u.liveries.keys()) for u in units))

        head = units[0]
        super().__init__(
            id=id,
            **head.make_props(self.common_liveries),
            power=power,
            **common_props,
            cargo_capacity=capacity[0],
            **kw,
        )
        for i, u in enumerate(units[1:]):
            self.add_articulated_part(
                **u.make_props(self.common_liveries),
                **common_props,
                cargo_capacity=capacity[i + 1],
            )

    def _set_callbacks(self, g):
        super()._set_callbacks(g)
        if self.electric_power is not None and self.diesel_power is not None:
            self.callbacks.properties.power = grf.Switch(
                'current_railtype',
                {
                    rt: self.electric_power
                    for rt in elecrified_railtypes
                },
                default=self.diesel_power
            )

        if self.can_attach is not None:
            self.callbacks.can_attach_wagon = grf.Switch(
                f'(grfid == {g.grfid_value}) * vehicle_type_id',
                {
                    t.id: 0x401  # allow
                    for t in self.can_attach
                },
                default=g.strings['CANNOT_ATTACH'].get_global_id()
            )

    # TODO find a better way of defining purchase sprites (possibly group by class)
    def get_sprites(self, g):
        res = []
        if self.purchase_sprites:
            assert len(self.purchase_sprites) in (1, 4, 8), len(self.purchase_sprites)
            res.append(grf.Action1(
                feature=grf.TRAIN,
                set_count=1,
                sprite_count=len(self.purchase_sprites),
            ))
            res.extend(self.purchase_sprites)
            res.append(layout := grf.GenericSpriteLayout(
                ent1=(0,),
                ent2=(0,),
            ))

            self.callbacks.purchase_graphics = layout

        res.extend(super().get_sprites(g))
        return res

