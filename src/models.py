class Tour:
    def __init__(self, name, country, price, rating, description, attributes, duration, included, image_url, hotel_stars, season, visa):
        self.name = name
        self.country = country
        try:
            self.price = float(str(price).replace('$', '').replace(' ', '').replace(',', '.'))
        except:
            self.price = 0.0
        
        try:
            self.rating = float(str(rating).replace(',', '.'))
        except:
            self.rating = 0.0
            
        self.description = description
        self.attributes = attributes
        self.duration = duration
        self.included = included
        self.image_url = image_url
        self.hotel_stars = hotel_stars
        self.season = str(season)
        self.visa = str(visa)

    def __repr__(self):
        return f"<Tour: {self.name}>"