from flask import Blueprint, jsonify, request
from ..services.Models import get_reason
api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/reason', methods=['POST'])
def reason():
    if request.is_json:
        print(request)
        data = request.get_json()
        query = data["input_data"]

        reason = get_reason(query)
        return jsonify({"reason": reason}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400
    
if __name__ == "__main__":
    reason()

