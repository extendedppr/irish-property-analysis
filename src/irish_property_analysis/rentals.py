from irish_property_analysis.listings import ListingDB, ListingObject


class RentalObject(ListingObject):
    __repr__ = ListingObject._listing_repr


class RentalDB(ListingDB):
    model_class = RentalObject


rental_db = RentalDB()
