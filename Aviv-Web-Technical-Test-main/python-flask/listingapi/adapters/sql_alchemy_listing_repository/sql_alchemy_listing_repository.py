from sqlalchemy.orm import scoped_session

from listingapi.adapters.sql_alchemy_listing_repository import mappers, models
from listingapi.domain import entities, ports
from listingapi.domain.entities import exceptions


class SqlAlchemyListingRepository(ports.ListingRepository):
    def __init__(self, db_session: scoped_session):
        self.db_session = db_session

    def init(self) -> None:
        models.Base.metadata.create_all(self.db_session.get_bind())

    # def create(self, listing: entities.ListingEntity) -> dict:
    #     listing_model = mappers.ListingMapper.from_entity_to_model(listing)
    #     self.db_session.add(listing_model)
    #     self.db_session.commit()
    #     data = mappers.ListingMapper.from_model_to_dict(listing_model)
    #     return data
    
    def create(self, listing: entities.ListingEntity) -> dict:
        listing_model = mappers.ListingMapper.from_entity_to_model(listing)
        
        self.db_session.add(listing_model)
        
        self.db_session.commit()
        self.db_session.refresh(listing_model)
        
        price_history_model = models.PriceHistoryModel(
            price=listing_model.price,
            listing=listing_model.id
        )
        self.db_session.add(price_history_model)
        self.db_session.commit()
        
        data = mappers.ListingMapper.from_model_to_dict(listing_model)
        return data

    def get_all(self) -> list[dict]:
        listing_models = self.db_session.query(models.ListingModel).all()
        listings = [
            mappers.ListingMapper.from_model_to_dict(listing)
            for listing in listing_models
        ]
        print('from sql alchemy listings',listings)
        return listings

    # def update(self, listing_id: int, listing: entities.ListingEntity) -> dict:
    #     existing_listing = self.db_session.get(models.ListingModel, listing_id)
    #     if existing_listing is None:
    #         raise exceptions.ListingNotFound
    #     self.db_session.delete(existing_listing)

    #     listing_model = mappers.ListingMapper.from_entity_to_model(listing)
    #     listing_model.id = listing_id
    #     self.db_session.add(listing_model)
    #     self.db_session.commit()

    #     listing_dict = mappers.ListingMapper.from_model_to_dict(listing_model)
    #     return listing_dict
    
    def update(self, listing_id: int, listing: entities.ListingEntity) -> dict:
        existing_listing = self.db_session.get(models.ListingModel, listing_id)
        if existing_listing is None:
            raise exceptions.ListingNotFound
        
        self.db_session.delete(existing_listing)
        
        listing_model = mappers.ListingMapper.from_entity_to_model(listing)
        listing_model.id = listing_id
        
        self.db_session.add(listing_model)
        self.db_session.commit()
        
        price_history_model = models.PriceHistoryModel(
            price=listing_model.price,
            listing_id=listing_id
        )
        self.db_session.add(price_history_model)
        self.db_session.commit()
        
        listing_dict = mappers.ListingMapper.from_model_to_dict(listing_model)
        return listing_dict
    
    def get_prices(self, listing_id: int) -> dict:
        existing_listing = self.db_session.query(models.ListingModel).filter(models.ListingModel.id==listing_id).first()
        if existing_listing is None:
            raise exceptions.ListingNotFound

        existing_prices = self.db_session.query(models.PriceHistoryModel).filter(models.PriceHistoryModel.listing_id==listing_id).all()
        
        listings = [
            mappers.ListingMapper.from_model_to_dict_prices(listing)
            for listing in existing_prices
        ]

        return listings
