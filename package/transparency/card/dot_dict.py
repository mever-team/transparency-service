class DotDict(dict):
    def __init__(self, **kwargs):
        super().__init__({k: v for k,v in kwargs.items()})

    def __getattr__(self, attr):
        try: return self[attr]
        except KeyError: raise AttributeError

    def __setattr__(self, attr, value):
        assert attr in self, f"Can only set an existing attribute among: {', '.join(self.keys())}"
        self[attr] = value

    def __delattr__(self, attr):
        try: del self[attr]
        except KeyError: raise AttributeError

    def validate_assign(self, other: dict):
        assert isinstance(other, dict), f"Can only assign dictionaries to field, not {type(other)}"
        for k in other:
            if k not in self: raise AssertionError(f"Cannot assign field {k}. Candidates: "+",".join(self.keys()))
            if isinstance(self[k], DotDict): self[k].validate_assign(other[k])

    def _assign(self, other: dict):
        for k in self:
            if k in other:
                if isinstance(self[k], DotDict): self[k]._assign(other[k])
                else: self[k] = other[k]

    def assign(self, other: dict):
        self.validate_assign(other)
        self._assign(other)
        return self
