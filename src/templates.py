import grf
import tomli


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
