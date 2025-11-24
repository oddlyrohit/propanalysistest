"""
Suburbs API Blueprint
Handles all suburb-related endpoints
"""
from flask import Blueprint, jsonify, request
from middleware import handle_errors, ApiError, validate_suburb_id, validate_search_query

suburbs_bp = Blueprint('suburbs', __name__)


def get_suburb_data(suburb_id: str, service_method, error_message: str):
    """Common pattern for fetching suburb-related data"""
    validate_suburb_id(suburb_id)
    data = service_method(suburb_id)

    if not data:
        raise ApiError(error_message, status_code=404)

    return jsonify(data), 200


def init_routes(data_service):
    """Initialize routes with data service dependency"""

    @suburbs_bp.route('/suburbs/search', methods=['GET'])
    @handle_errors('search_suburbs')
    @validate_search_query(min_length=1, max_length=100)
    def search_suburbs():
        """Search suburbs by name"""
        query = request.args.get('q', '')
        results = data_service.search_suburbs(query)
        return jsonify(results), 200

    @suburbs_bp.route('/suburb/<suburb_id>', methods=['GET'])
    @handle_errors('get_suburb')
    def get_suburb(suburb_id):
        """Get suburb details by ID"""
        validate_suburb_id(suburb_id)
        suburb = data_service.get_suburb_details(suburb_id)

        if not suburb:
            raise ApiError("Suburb not found", status_code=404)

        return jsonify(suburb), 200

    @suburbs_bp.route('/suburb/<suburb_id>/demographics', methods=['GET'])
    @handle_errors('get_demographics')
    def get_demographics(suburb_id):
        """Get demographics data for a suburb"""
        return get_suburb_data(suburb_id, data_service.get_demographics, "Demographics not found")

    @suburbs_bp.route('/suburb/<suburb_id>/amenities', methods=['GET'])
    @handle_errors('get_amenities')
    def get_amenities(suburb_id):
        """Get amenities data for a suburb"""
        return get_suburb_data(suburb_id, data_service.get_amenities, "Amenities not found")

    @suburbs_bp.route('/suburb/<suburb_id>/market-trends', methods=['GET'])
    @handle_errors('get_market_trends')
    def get_market_trends(suburb_id):
        """Get market trends data for a suburb"""
        return get_suburb_data(suburb_id, data_service.get_market_trends, "Market trends not found")

    @suburbs_bp.route('/suburb/<suburb_id>/schools', methods=['GET'])
    @handle_errors('get_schools')
    def get_schools(suburb_id):
        """Get schools data for a suburb"""
        return get_suburb_data(suburb_id, data_service.get_schools, "Schools not found")

    @suburbs_bp.route('/suburb/<suburb_id>/developments', methods=['GET'])
    @handle_errors('get_developments')
    def get_developments(suburb_id):
        """Get development applications for a suburb"""
        return get_suburb_data(suburb_id, data_service.get_developments, "Developments not found")

    @suburbs_bp.route('/suburb/<suburb_id>/market-insights', methods=['GET'])
    @handle_errors('get_market_insights')
    def get_market_insights(suburb_id):
        """Get market insights for a suburb"""
        validate_suburb_id(suburb_id)
        metric = request.args.get('metric')
        property_type = request.args.get('property_type')
        data = data_service.get_market_insights(suburb_id, metric, property_type)

        if not data:
            raise ApiError("Market insights not found", status_code=404)

        return jsonify(data), 200

    @suburbs_bp.route('/suburb/<suburb_id>/pocket-insights', methods=['GET'])
    @handle_errors('get_pocket_insights')
    def get_pocket_insights(suburb_id):
        """Get pocket-level market insights for a suburb"""
        validate_suburb_id(suburb_id)
        geojson = request.args.get('geojson', 'true').lower() == 'true'
        property_type = request.args.get('property_type')
        data = data_service.get_pocket_insights(suburb_id, geojson, property_type)

        if not data:
            raise ApiError("Pocket insights not found", status_code=404)

        return jsonify(data), 200

    @suburbs_bp.route('/suburb/<suburb_id>/street-insights', methods=['GET'])
    @handle_errors('get_street_insights')
    def get_street_insights(suburb_id):
        """Get street-level market insights for a suburb"""
        validate_suburb_id(suburb_id)
        geojson = request.args.get('geojson', 'true').lower() == 'true'
        property_type = request.args.get('property_type')
        data = data_service.get_street_insights(suburb_id, geojson, property_type)

        if not data:
            raise ApiError("Street insights not found", status_code=404)

        return jsonify(data), 200

    @suburbs_bp.route('/suburb/<suburb_id>/risk', methods=['GET'])
    @handle_errors('get_risk_factors')
    def get_risk_factors(suburb_id):
        """Get risk factors for a suburb"""
        validate_suburb_id(suburb_id)
        geojson = request.args.get('geojson', 'true').lower() == 'true'
        data = data_service.get_risk_factors(suburb_id, geojson)

        if not data:
            raise ApiError("Risk factors not found", status_code=404)

        return jsonify(data), 200

    @suburbs_bp.route('/suburb/<suburb_id>/info', methods=['GET'])
    @handle_errors('get_suburb_info')
    def get_suburb_info(suburb_id):
        """Get suburb basic geographical information"""
        validate_suburb_id(suburb_id)
        geojson = request.args.get('geojson', 'true').lower() == 'true'
        data = data_service.get_suburb_info(suburb_id, geojson)

        if not data:
            raise ApiError("Suburb info not found", status_code=404)

        return jsonify(data), 200

    @suburbs_bp.route('/suburb/<suburb_id>/summary', methods=['GET'])
    @handle_errors('get_suburb_summary')
    def get_suburb_summary(suburb_id):
        """Get AI-generated suburb summary and scores"""
        return get_suburb_data(suburb_id, data_service.get_suburb_summary, "Suburb summary not found")

    @suburbs_bp.route('/suburb/<suburb_id>/catchments', methods=['GET'])
    @handle_errors('get_school_catchments')
    def get_school_catchments(suburb_id):
        """Get school catchment areas for a suburb"""
        validate_suburb_id(suburb_id)
        geojson = request.args.get('geojson', 'true').lower() == 'true'
        data = data_service.get_school_catchments(suburb_id, geojson)

        if not data:
            raise ApiError("School catchments not found", status_code=404)

        return jsonify(data), 200

    @suburbs_bp.route('/suburb/<suburb_id>/zoning', methods=['GET'])
    @handle_errors('get_zoning')
    def get_zoning(suburb_id):
        """Get zoning information for a suburb"""
        validate_suburb_id(suburb_id)
        geojson = request.args.get('geojson', 'true').lower() == 'true'
        data = data_service.get_zoning(suburb_id, geojson)

        if not data:
            raise ApiError("Zoning info not found", status_code=404)

        return jsonify(data), 200

    @suburbs_bp.route('/suburb/<suburb_id>/similar', methods=['GET'])
    @handle_errors('get_similar_suburbs')
    def get_similar_suburbs(suburb_id):
        """Get similar suburbs"""
        validate_suburb_id(suburb_id)
        geojson = request.args.get('geojson', 'true').lower() == 'true'
        data = data_service.get_similar_suburbs(suburb_id, geojson)

        if not data:
            raise ApiError("Similar suburbs not found", status_code=404)

        return jsonify(data), 200

    @suburbs_bp.route('/suburbs/<suburb_id>/street-rankings', methods=['GET'])
    @handle_errors('get_street_rankings')
    def get_street_rankings(suburb_id):
        """Get street rankings for a suburb"""
        validate_suburb_id(suburb_id)
        property_type = request.args.get('property_type')
        data = data_service.get_street_rankings(suburb_id, property_type)

        if not data:
            raise ApiError("Street rankings not found", status_code=404)

        return jsonify(data), 200
