import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from marshmallow import Schema, fields, validate, ValidationError

from .models import Robot


class RobotSchema(Schema):
    model = fields.Str(required=True, validate=validate.Length(max=2))
    version = fields.Str(required=True, validate=validate.Length(max=2))
    created = fields.DateTime(required=True)


@csrf_exempt
@require_POST
def add_robot(request):
    try:
        json_data = json.loads(request.body)
        robot_schema = RobotSchema()
        robot_data = robot_schema.load(json_data)
        serial = f'{robot_data["model"]}-{robot_data["version"]}'
        Robot.objects.create(**robot_data, serial=serial)
    except ValidationError as e:
        return JsonResponse({"errors": e.messages}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"errors": "json body required"}, status=400)

    return JsonResponse({'message': 'robot created'})
