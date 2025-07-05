from flask import Blueprint, request, jsonify
from flaskProject.mapper.PreferenceMapper import PreferenceAnalysisMapper
import logging

preference_bp = Blueprint('preference', __name__)
preference_mapper = PreferenceAnalysisMapper()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@preference_bp.route('/preference', methods=['GET'])
def audience_preference():
    try:
        type_name = request.args.get('type', type=str).strip()
        start_month = request.args.get('start_month', type=str).strip()
        end_month = request.args.get('end_month', type=str).strip()

        ret = preference_mapper.get_audience_preference(type_name, start_month, end_month)
        return jsonify(ret)

    except Exception as e:
        logger.error(f"观众偏好获取失败: {str(e)}")
        return jsonify({
            "times": [],
            "attendees": []
        })


@preference_bp.route('/industry', methods=['GET'])
def yearly_production():
    try:
        start_month = request.args.get('start_month', type=str).strip()
        end_month = request.args.get('end_month', type=str).strip()
        ret = preference_mapper.get_industry_data(start_month, end_month)
        return jsonify(ret)

    except Exception as e:
        logger.error(f"市场总票房统计错误: {str(e)}")
        return jsonify({
            "times": [],
            "box_offices": []
        })
