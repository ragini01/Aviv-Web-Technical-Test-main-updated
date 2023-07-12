from listingapi.domain import ports


class RetrieveListingPrice:
    def __init__(self, listing_repository: ports.ListingRepository):
        self.listing_repository = listing_repository

    def perform(self, listing_id: int) -> dict:
        listing_dict = self.listing_repository.get_prices(listing_id)
        return listing_dict