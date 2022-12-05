from marshmallow import Schema, fields, validates, ValidationError, INCLUDE
from marshmallow.validate import Length, Range
import json



def is_json(dictionary : dict) -> bool:
    try:
        json.dumps(dictionary)
        return True
    except (TypeError, OverflowError):
        return False

class MessageSchema(Schema):

    class Meta:
        unknown = INCLUDE
    
    type = fields.String(required = True)

class UserRequestSchema(MessageSchema):

    user_id = fields.Int(required = True)
    model_name = fields.Str(required = True)

    @validates('user_id')
    def is_user(self, value):
        # make sure user exists
        pass

    @validates("model_name")
    def is_model(self, value):
        # make sure model exists
        pass

class UserResponseSchema(MessageSchema):

    seq = fields.Int(required = True)
    prediction = fields.Str(required = True)
    optional = fields.Dict(required = False)

    @validates('prediction')
    def is_valid_prediction(self, value):
        # make sure that the prediction is valid
        pass

    @validates('optional')
    def is_json(self, value):
        if not is_json(value):
            raise ValidationError()

class PredictionRequestSchema(MessageSchema):

    seq = fields.Int(required = True)
    data = fields.Dict(required = True)
    client = fields.Int(required = True)

    @validates('data')
    def is_json(self, value):
        if not is_json(value):
            raise ValidationError()

class PredictionResponseSchema(MessageSchema):

    seq = fields.Int(required = True)
    prediction = fields.Str(required = True)
    client = fields.Int(required = True)

    @validates('prediction')
    def is_valid_prediction(self, value):
        # make sure that the prediction is valid
        pass

user_response = UserResponseSchema()
user_request = UserRequestSchema()
prediction_request = PredictionRequestSchema()
prediction_response = PredictionResponseSchema()
message_schema = MessageSchema()