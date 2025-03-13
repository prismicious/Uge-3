class Cereal:
    def __init__(self,
                 name: str,
                 mfr: str,
                 type_: str,
                 calories: int = 0,
                 protein: int = 0,
                 fat: int = 0,
                 sodium: int = 0,
                 fiber: float = 0.0,
                 carbo: float = 0.0,
                 sugars: int = 0,
                 potass: int = 0,
                 vitamins: int = 0,
                 shelf: int = 0,
                 weight: float = 0.0,
                 cups: float = 0.0,
                 rating: float = 0.0,
                 id: int = None):  # Optional id field

        self.id = id
        self.name = name
        self.mfr = mfr
        self.type_ = type_
        self.calories = calories
        self.protein = protein
        self.fat = fat
        self.sodium = sodium
        self.fiber = fiber
        self.carbo = carbo
        self.sugars = sugars
        self.potass = potass
        self.vitamins = vitamins
        self.shelf = shelf
        self.weight = weight
        self.cups = cups
        self.rating = rating

    @classmethod
    def from_dict(cls, data):
        if 'name' not in data or 'mfr' not in data or 'type' not in data:
            raise ValueError(
                "Missing required fields: 'name', 'mfr', and 'type' are mandatory.")

        return cls(
            id=data.get('id'),  # Optional id field
            name=data.get('name'),
            mfr=data.get('mfr'),
            type_=data.get('type'),
            calories=data.get('calories', 0),
            protein=data.get('protein', 0),
            fat=data.get('fat', 0),
            sodium=data.get('sodium', 0),
            fiber=data.get('fiber', 0.0),
            carbo=data.get('carbo', 0.0),
            sugars=data.get('sugars', 0),
            potass=data.get('potass', 0),
            vitamins=data.get('vitamins', 0),
            shelf=data.get('shelf', 0),
            weight=data.get('weight', 0.0),
            cups=data.get('cups', 0.0),
            rating=data.get('rating', 0.0)
        )

    def to_dict(self):
        # Convert the object's attributes to a dictionary, excluding 'id'
        return {key: value for key, value in self.__dict__.items() if key != 'id'}