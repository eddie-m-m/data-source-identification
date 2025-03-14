from source_collectors.muckrock.classes.exceptions.RequestFailureException import RequestFailureException
from source_collectors.muckrock.classes.muckrock_fetchers.MuckrockIterFetcherBase import MuckrockIterFetcherBase


class MuckrockGeneratorFetcher(MuckrockIterFetcherBase):
    """
    Similar to the Muckrock Loop fetcher, but behaves
    as a generator instead of a loop
    """

    def generator_fetch(self) -> str:
        """
        Fetches data and yields status messages between requests
        """
        url = self.build_url(self.initial_request)
        final_message = "No more records found. Exiting..."
        while url is not None:
            try:
                data = self.get_response(url)
            except RequestFailureException:
                final_message = "Request unexpectedly failed. Exiting..."
                break

            yield self.process_results(data["results"])
            url = data["next"]

        yield final_message



