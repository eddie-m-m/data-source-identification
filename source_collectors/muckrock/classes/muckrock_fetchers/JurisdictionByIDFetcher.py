from source_collectors.muckrock.classes.fetch_requests.FetchRequestBase import FetchRequest
from source_collectors.muckrock.classes.muckrock_fetchers.MuckrockFetcher import MuckrockFetcher
from source_collectors.muckrock.constants import BASE_MUCKROCK_URL


class JurisdictionByIDFetchRequest(FetchRequest):
    jurisdiction_id: int

class JurisdictionByIDFetcher(MuckrockFetcher):

    def build_url(self, request: JurisdictionByIDFetchRequest) -> str:
        return f"{BASE_MUCKROCK_URL}/jurisdiction/{request.jurisdiction_id}/"

    def get_jurisdiction(self, jurisdiction_id: int) -> dict:
        return self.fetch(request=JurisdictionByIDFetchRequest(jurisdiction_id=jurisdiction_id))
