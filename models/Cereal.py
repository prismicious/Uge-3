class Cereal:
    def __init__(self,
                 name: str,
                 mfr: str,
                 type_: str,
                 calories: int,
                 protein: int,
                 fat: int,
                 sodium: int,
                 fiber: float,
                 carbo: float,
                 sugars: int,
                 potass: int,
                 vitamins: int,
                 shelf: int,
                 weight: float,
                 cups: float,
                 rating: float):

        # Type assignments
        self.name = name
        self.mfr = mfr
        self.type_ = type_
        self.calories = int(calories)
        self.protein = int(protein)
        self.fat = int(fat)
        self.sodium = int(sodium)
        self.fiber = float(fiber)
        self.carbo = float(carbo)
        self.sugars = int(sugars)
        self.potass = int(potass)
        self.vitamins = int(vitamins)
        self.shelf = int(shelf)
        self.weight = float(weight)
        self.cups = float(cups)
        self.rating = float(rating.replace('.', '')) if isinstance(
            rating, str) else float(rating)

    def count_attributes(self) -> int:
        # Returns the number of attributes in the Cereal object.
        return len(self.__dict__)

    def __repr__(self) -> str:
        return f"Cereal({self.name}, {self.mfr}, {self.type_}, {self.calories} cal)"

    @classmethod
    def from_dict(cls, data):
        # Automatically converts data (e.g., dictionary) into class instance.
        return cls(
            name=data['name'],
            mfr=data['mfr'],
            type_=data['type'],
            calories=data['calories'],
            protein=data['protein'],
            fat=data['fat'],
            sodium=data['sodium'],
            fiber=data['fiber'],
            carbo=data['carbo'],
            sugars=data['sugars'],
            potass=data['potass'],
            vitamins=data['vitamins'],
            shelf=data['shelf'],
            weight=data['weight'],
            cups=data['cups'],
            rating=data['rating']
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "mfr": self.mfr,
            "type": self.type_,
            "calories": self.calories,
            "protein": self.protein,
            "fat": self.fat,
            "sodium": self.sodium,
            "fiber": self.fiber,
            "carbo": self.carbo,
            "sugars": self.sugars,
            "potass": self.potass,
            "vitamins": self.vitamins,
            "shelf": self.shelf,
            "weight": self.weight,
            "cups": self.cups,
            "rating": self.rating
        }
