from django.utils import timezone
from django.db.models import Sum
from .models import Goal

def evaluate_progress(goal):
    """
    目標に対する進捗状況を評価する。
    """
    # 合計学習時間を計算 (分)
    total_minutes = goal.records.aggregate(total_duration=Sum('duration'))['total_duration'] or 0
    total_hours_studied = total_minutes / 60

    remaining_hours = goal.target_hours - total_hours_studied

    today = timezone.now().date()
    # 今日が開始日より前なら開始日から、そうでなければ今日から計算
    start_calculation_date = max(today, goal.start_date)
    # 当日を含めるために +1 する
    remaining_days = (goal.end_date - start_calculation_date).days + 1

    if remaining_hours <= 0:
        return {
            "status": "completed",
            "message": "おめでとうございます！目標学習時間をクリアしました。",
            "remaining_hours": 0,
            "remaining_days": remaining_days,
            "daily_hours_needed": 0
        }

    if remaining_days <= 0:
        return {
            "status": "failed",
            "message": "学習期間が終了していますが、目標時間に達していません。",
            "remaining_hours": round(remaining_hours, 1),
            "remaining_days": 0,
            "daily_hours_needed": 0
        }

    daily_hours_needed = remaining_hours / remaining_days

    if daily_hours_needed <= 2:
        status = "good"
        message = "順調です。この調子で続けましょう。"
    elif daily_hours_needed <= 4:
        status = "warning"
        message = "少しペースを上げる必要があります。"
    else:
        status = "critical"
        message = "目標達成にはかなり厳しいペースです。計画の見直しを検討してください。"

    return {
        "status": status,
        "message": message,
        "remaining_hours": round(remaining_hours, 1),
        "remaining_days": remaining_days,
        "daily_hours_needed": round(daily_hours_needed, 1)
    }
