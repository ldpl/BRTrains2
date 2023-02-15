import json

import tomli

import grf


class TemplateManager:
    def __init__(self):
        self._templates = {}
        self._template_idx = {}

    @classmethod
    def from_toml(cls, filename):
        res = cls()
        res.load_toml(filename)
        return res

    @classmethod
    def from_json(cls, filename):
        res = cls()
        res.load_json(filename)
        return res

    def __len__(self):
        return len(self._templates)

    def load_dict(self, data):
        self._templates = {}
        self._templates_idx = {}
        for name, tlist in data.items():
            t = tuple(map(tuple, tlist))

            self._templates[name] = t
            self._template_idx[t] = name

    def load_json(self, filename):
        self.load_dict(json.load(open(filename)))

    def load_toml(self, filename):
        self.load_dict(tomli.load(open(filename, 'rb')))

    def save_json(self, filename):
        with open(filename, 'w') as f:
            print('{', end='', file=f)
            joiner = ''
            for k, t in self._templates.items():
                print(joiner, file=f)
                print(f'    "{k}": [', end='', file=f)
                ljoiner = ''
                for l in t:
                    print(ljoiner, file=f)
                    print(f'        {list(l)!r}', end='', file=f)
                    ljoiner = ','
                print('', file=f)
                print(f'    ]', end='', file=f)
                joiner = ','
            print('}', file=f)

    def find(self, t):
        return self._template_idx.get(t)

    def __getitem__(self, name):
        return self._templates[name]

    def get(self, name):
        return self._templates.get(name)

    def __setitem__(self, name, value):
        assert isinstance(value, tuple)
        assert all(isinstance(v, tuple) for v in value)

        self._templates[name] = value
        self._template_idx[value] = name

    def apply(self, name, x, y, func):
        tpl = self.get(name)
        return [func(x + xx, y + yy, w, h, xofs=xofs, yofs=yofs) for xx, yy, w, h, xofs, yofs in tpl]


class SpriteSetManager:
    def __init__(self, templates):
        assert isinstance(templates, TemplateManager)
        self._sets = {}
        self.templates = templates

    def __len__(self):
        return len(self._sets)

    def load(self, filename):
        self._sets = json.load(open(filename))

    def save(self, filename):
        with open(filename, 'w') as f:
            print('{', end='', file=f)
            joiner = ''
            for k, data in self._sets.items():
                file, tmpl, args = data['file'], data['template'], list(data['args'])
                print(joiner, file=f)
                print(f'    "{k}": {{', file=f)
                print(f'        "file": "{file}",', file=f)
                print(f'        "template": "{tmpl}",', file=f)
                if 'tags' in data:
                    print(f'        "args": {args},', file=f)
                    tags = list(data['tags'])
                    print(f'        "tags": {json.dumps(tags)}', file=f)
                else:
                    print(f'        "args": {args}', file=f)
                print(f'    }}', end='', file=f)
                joiner = ','
            print('}', file=f)

    def __getitem__(self, name):
        return self._sets[name]

    def get(self, name):
        return self._sets.get(name)

    def __setitem__(self, name, value):
        self._sets[name] = value

    def get_sets_on_sheet(resource_dir, filename):
        img = grf.ImageFile(path)
        res = []
        for k, s in sets._sets.items():
            if s['file'] != filename:
                continue

            tmpl = self.templates[s['template']]
            ox, oy = s['args']

            res.append((k, [
                grf.FileSprite(img, x + ox, y + oy, w, h, xofs=xofs, yofs=yofs)
                for x, y, w, h, xofs, yofs in tmpl
            ]))
        return res


class Train(grf.Train):

    next_articulated_id = 4000

    def __init__(self, *args, length, sprites, **kw):
        super().__init__(
            *args,
            liveries=[{'name': 'Default', 'sprites': sprites}],
            shorten_by=8-length,
            **kw,
        )

    def add_articulated_part(self, length, sprites, **kw):
        super().add_articulated_part(
            **kw,
            shorten_by=8-length,
            liveries=[{'name': 'Default', 'sprites': sprites}],
            id=self.__class__.next_articulated_id
        )
        self.__class__.next_articulated_id += 1


class Unit:
    def __init__(self, sprites, length, electric):
        self.sprites = sprites
        self.length = length
        self.electric = electric

    def make_props(self):
        effect = Train.VisualEffect.ELECTRIC if self.electric else Train.VisualEffect.DIESEL
        return dict(
            sprites=self.sprites,
            length=self.length,
            visual_effect_and_powered=Train.visual_effect_and_powered(effect, position=2, wagon_power=False),
        )


class MUTrain(Train):
    def __init__(self, *, id, units, total_capacity, purchase_sprites=None, electric_power=None, diesel_power=None, **kw):
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

        head = units[0]
        super().__init__(
            id=id,
            **head.make_props(),
            power=power,
            **common_props,
            cargo_capacity=capacity[0],
            **kw,
        )
        for i, u in enumerate(units[1:]):
            self.add_articulated_part(
                **u.make_props(),
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
                    for rt in g.elecrified_railtypes
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

        # TODO switch visual effect by railtype

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

