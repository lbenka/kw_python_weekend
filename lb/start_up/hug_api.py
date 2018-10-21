"""For local debugging."""
import hug 

from lb.journey_finder_hug import api as hug_api

hug.API(__name__).extend(api=hug_api)
hug.API(__name__).http.serve()
