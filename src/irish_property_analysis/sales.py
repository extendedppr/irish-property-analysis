from irish_property_analysis.listings import ListingDB, ListingObject


class SaleObject(ListingObject):
    __repr__ = ListingObject._listing_repr


class SaleDB(ListingDB):
    model_class = SaleObject


sale_db = SaleDB()
