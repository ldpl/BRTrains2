import json

import grf

from .common import elecrified_railtypes, templates, railtypes, train_props


ELECTRIC_EFFECT = grf.Train.visual_effect_and_powered(grf.Train.VisualEffect.ELECTRIC, position=2, wagon_power=False)
DIESEL_EFFECT = grf.Train.visual_effect_and_powered(grf.Train.VisualEffect.DIESEL, position=2, wagon_power=False)


def make_liveries(png, liveries, *, xofs=0, yofs=0):
    if isinstance(png, str):
        png = grf.ImageFile(png)
    func = lambda *args, **kw: grf.FileSprite(png, *args, **kw, bpp=8)
    res = {}
    for name, slot in liveries.items():
        res[name] = templates.apply('train32px', xofs, yofs + 25 * slot, func)
    return res


class Train(grf.Train):

    next_articulated_id = 4000

    def __init__(self, *args, length, **kw):
        super().__init__(
            *args,
            **train_props,
            shorten_by=8-length,
            **kw,
        )

    def add_articulated_part(self, length, **kw):
        super().add_articulated_part(
            **kw,
            shorten_by=8-length,
            id=Train.next_articulated_id
        )
        Train.next_articulated_id += 1


class Unit:
    ELECTRIC, DIESEL = 1, 2

    def __init__(self, *, length, power_type=0, sprites=None, liveries=None, colour_mapping=None):
        if liveries is None:
            assert sprites is not None
            liveries = {None: sprites}
        self.liveries = liveries
        self.length = length
        self.power_type = power_type
        self.colour_mapping = colour_mapping

    def make_props(self, use_liveries):
        if self.power_type & self.ELECTRIC > 0:
            electric_effect = ELECTRIC_EFFECT
        else:
            electric_effect = Train.VisualEffect.DISABLE
        if self.power_type & self.DIESEL > 0:
            default_effect = DIESEL_EFFECT
        else:
            default_effect = Train.VisualEffect.DISABLE
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
    def __init__(self, *, id, units, total_capacity, design_speed=None, use_liveries=None, purchase_sprites=None, **kw):
        # TODO GetAdjustedCost for cost_factor and runnig_cost_factor
        # TODO multiply capacity by param_pax
        assert units

        self.units = units
        self.can_attach = None
        self.purchase_sprites = purchase_sprites
        self.design_speed = design_speed
        self._capacity_switch_cache = {}

        def calc_capacity(total_capacity):
            # Split total capacity between units, as equially as possible
            assert total_capacity <= 255 * len(self.units), total_capacity
            capacity = [total_capacity // len(self.units)] * len(self.units)
            for i in range(total_capacity - sum(capacity)):
                capacity[i] += 1
            return capacity

        # Find common liveries
        self.common_liveries = set.intersection(*(set(u.liveries.keys()) for u in units))
        if use_liveries:
            assert all(l in self.common_liveries for l in use_liveries)
            self.common_liveries = set(use_liveries)

        if isinstance(total_capacity, int):
            self.capacity = {None: calc_capacity(total_capacity)}
        else:
            assert len(total_capacity) > 1
            self.capacity = {k: calc_capacity(v) for k, v in total_capacity.items()}
            assert len(self.common_liveries) == len(self.capacity), (self.common_liveries, self.capacity.keys())
        default_capacity = next(iter(self.capacity.values()))

        common_props = {
            'misc_flags': Train.Flags.MULTIPLE_UNIT,
        }
        head = units[0]
        super().__init__(
            id=id,
            **head.make_props(self.common_liveries),
            **common_props,
            cargo_capacity=default_capacity[0],
            **kw,
        )
        for i, u in enumerate(units[1:]):
            self.add_articulated_part(
                **u.make_props(self.common_liveries),
                **common_props,
                cargo_capacity=default_capacity[i + 1],
            )

    def _make_capacity_switch(self, position):
        if position in self._capacity_switch_cache:
            return self._capacity_switch_cache[position]
        liveries = self.units[position].liveries
        res = self._capacity_switch_cache[position] = grf.Switch(
            'cargo_subtype',
            ranges={
                i: self.capacity[l][position]
                for i, l in enumerate(liveries.keys())
                if l in self.common_liveries
            },
            default=0,  # TODO no default(fail)
        )
        return res

    def _set_articulated_part_callbacks(self, g, position, callbacks):
        if len(self.capacity) > 1:
            callbacks.properties.cargo_capacity = self._make_capacity_switch(position)

    def _set_callbacks(self, g):
        super()._set_callbacks(g)

        if self.can_attach is not None:
            self.callbacks.can_attach_wagon = grf.Switch(
                f'(grfid == {g.grfid_value}) * vehicle_type_id',
                {
                    t.id: 0x401  # allow
                    for t in self.can_attach
                },
                default=g.strings['CANNOT_ATTACH'].get_global_id()
            )

        if len(self.capacity) > 1:
            self.callbacks.properties.cargo_capacity = self._make_capacity_switch(0)

        # TODO switch between service and design speed based on parameter

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



class EMUTrain(MUTrain):
    def __init__(self, **kw):
        super().__init__(
            track_type=railtypes['ELRL'],
            running_cost_base=Train.RunningCost.ELECTRIC,
            engine_class=Train.EngineClass.ELECTRIC,
            visual_effect_and_powered=ELECTRIC_EFFECT,
            **kw
        )


DMUTrain = MUTrain


class BMUTrain(MUTrain):
    def __init__(self, *, electric_power=None, diesel_power=None, **kw):
        self.electric_power = electric_power
        self.diesel_power = diesel_power

        power = electric_power
        if power is None or (diesel_power is not None and diesel_power > power):
            power = diesel_power

        super().__init__(
            power=power,
            track_type=railtypes['RAIL'],
            running_cost_base=Train.RunningCost.ELECTRIC,
            engine_class=Train.EngineClass.DIESEL,  # even if its 3rd rail, ELECTRIC would give overhead wire effects
            visual_effect_and_powered=ELECTRIC_EFFECT,
            **kw,
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
