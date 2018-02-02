import time


class StatsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.start_time = time.time()

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        duration = time.time() - request.start_time
        response["X-Page-Generation-Duration-ms"] = int(duration * 1000)

        return response
