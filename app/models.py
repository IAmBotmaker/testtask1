from app import db


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(10), unique=True)
    title = db.Column(db.String(500), nullable=False)
    reviews = db.relationship('Reviews', backref='products', lazy='dynamic')

    def __repr__(self):
        return "<Products('%s', '%s', '%s')>" % (self.asin, self.title, self.reviews)

    #def as_dict(self):
    #    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def as_dict(self):
        data = {
            'id': self.id,
            'asin': self.asin,
            'title': self.title,
            'reviews': self.reviews
        }
        return data

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(10), unique=False)
    title = db.Column(db.String(500), nullable=False)
    review = db.Column(db.Text, nullable=False)
    product_ids = db.Column(db.Integer, db.ForeignKey('products.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "<Reviews('%s', '%s', '%s', '%s')>" % (self.asin, self.title, self.review, self.product_ids)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
