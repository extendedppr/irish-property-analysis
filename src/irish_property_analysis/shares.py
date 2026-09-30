from irish_property_analysis.listings import ListingDB, ListingObject


class ShareObject(ListingObject):
    __repr__ = ListingObject._listing_repr


class ShareDB(ListingDB):
    model_class = ShareObject


share_db = ShareDB()
