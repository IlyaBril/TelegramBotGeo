from marshmallow import Schema, fields, validate, ValidationError, post_dump
from pprint import pprint
from .test_response import t3
from .models import URLFilter

bot_response = URLFilter()


class RequestSchema(Schema):
    lat = fields.Float()
    lon = fields.Float()
    radius = fields.Int(validate=validate.Range(min=1, max=5000))
    limit = fields.Int(validate=validate.Range(min=1, max=10))
    categories = fields.Str()
    filter = fields.Method("filter_circle_field")
    bias = fields.Method("bias_proximity_field")
    apiKey = fields.Str()
    conditions = fields.Str()

    def filter_circle_field(self, obj):
        return "circle:" + str(obj.lon) + "," + str(obj.lat) + "," + str(obj.radius)

    def bias_proximity_field(self, obj):
        return "proximity:" + str(obj.lon) + "," + str(obj.lat)


#Markers
class MarkerCoordinatesSchema(Schema):
    lon = fields.Float()
    lat = fields.Float()
    color = fields.Str(dump_default="#ff0000")
    size = fields.Str(dump_default ="42")
    text = fields.Str()
    contentsize = fields.Str(dump_default = "22")
    #distance = fields.Int()


class MapSchema(Schema):
    properties = fields.Nested(MarkerCoordinatesSchema)


class FeaturesSchema(Schema):
    features = fields.Pluck(MapSchema, field_name="properties",
                            many=True, data_key="markers")
    style = fields.Str(dump_default="osm-bright")
    scaleFactor = fields.Int(dump_default=2)
    width = fields.Int(dump_default=600)
    height = fields.Int(dump_default=400)
    zoom = fields.Int(dump_default=14)


    @post_dump
    def add_marker_id(self, data, **kwargs):
        #add center coordinates to map
        data["center"] = {
                        "lat": bot_response.lat,
                        "lon": bot_response.lon
                    }

        #add sequence text to each marker
        if "markers" in data:
            for sequence, marker in enumerate(data["markers"]):
                marker["text"] = str(sequence + 1)

            #add customer position marker
            position_marker = {
                "lat": bot_response.lat,
                "lon": bot_response.lon,
                "type": "circle",
                "color": "#000099",
                "size": "22",
            }
            data["markers"].append(position_marker)
        return data


#Tourists Places Serializer
class PlacesProperties(Schema):
    formatted = fields.Str()
    distance = fields.Int()
    name = fields.Str()
    text_full = fields.Method("text_cont")

    def text_cont(self, obj):
        #Concatinate data fields into one as response message

        return ('.Наименование: {} \nАдрес: {}\n Расстояние: {} м.'.
        format(
            obj.get("name", "-"),
            obj.get("formatted", "-"),
            str(obj.get("distance", "-"))
        ))


class PlacesFeature(Schema):
    properties = fields.Nested(PlacesProperties)


class FinalSchema(Schema):
    features = fields.Pluck(PlacesFeature, field_name="properties", many=True, data_key="places")

    @post_dump
    def add_places_id(self, data, **kwargs):
        #Create final answer
        answer = ""
        if "places" in data:
            for numb, place in enumerate(data["places"]):
                answer = answer + str(numb+1) + str(place["text_full"]) + "\n"
            return str(answer)


#Test
schema2 = FeaturesSchema()
result = schema2.dump(t3)
#pprint(result)
