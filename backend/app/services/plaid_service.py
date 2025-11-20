
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from app.core.config import settings

class PlaidService:
    def __init__(self):
        configuration = plaid.Configuration(
            host=plaid.Environment.Sandbox,
            api_key={
                'clientId': settings.PLAID_CLIENT_ID,
                'secret': settings.PLAID_SECRET,
            }
        )
        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    def create_link_token(self, user_id: str):
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id=user_id),
            client_name="Personal Finance Tracker",
            products=[Products('investments')],
            country_codes=[CountryCode('US')],
            language='en'
        )
        response = self.client.link_token_create(request)
        return response.to_dict()

    def exchange_public_token(self, public_token: str):
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = self.client.item_public_token_exchange(request)
        return response.to_dict()

    def get_investment_holdings(self, access_token: str):
        request = InvestmentsHoldingsGetRequest(access_token=access_token)
        response = self.client.investments_holdings_get(request)
        return response.to_dict()
