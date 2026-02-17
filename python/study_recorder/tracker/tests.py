from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Goal, StudyRecord
from .services import evaluate_progress

class GoalModelTests(TestCase):
    def test_create_goal(self):
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        goal = Goal.objects.create(
            title="Test Goal",
            target_hours=100,
            start_date=start_date,
            end_date=end_date
        )
        self.assertEqual(goal.title, "Test Goal")
        self.assertEqual(goal.target_hours, 100)

class StudyRecordModelTests(TestCase):
    def setUp(self):
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        self.goal = Goal.objects.create(
            title="Test Goal",
            target_hours=100,
            start_date=start_date,
            end_date=end_date
        )

    def test_create_record(self):
        record = StudyRecord.objects.create(
            goal=self.goal,
            studied_at=timezone.now(),
            duration=60,
            comment="Test study"
        )
        self.assertEqual(record.duration, 60)
        self.assertEqual(record.goal, self.goal)

class ServiceTests(TestCase):
    def setUp(self):
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        self.goal = Goal.objects.create(
            title="Test Goal",
            target_hours=100,
            start_date=start_date,
            end_date=end_date
        )

    def test_evaluate_progress_start(self):
        # 学習記録なし
        result = evaluate_progress(self.goal)
        self.assertEqual(result['status'], 'warning') # 100時間/30日 = 3.33時間/日 -> warning

    def test_evaluate_progress_good(self):
        # 30日後に100時間必要。今は0日経過。
        # 目標を減らしてgoodになるかテスト
        self.goal.target_hours = 30
        self.goal.save()
        result = evaluate_progress(self.goal)
        self.assertEqual(result['status'], 'good') # 30時間/30日 = 1時間/日 -> good

    def test_evaluate_progress_failed(self):
        # 期限切れ
        self.goal.end_date = timezone.now().date() - timedelta(days=1)
        self.goal.save()
        result = evaluate_progress(self.goal)
        self.assertEqual(result['status'], 'failed')

    def test_evaluate_progress_last_day(self):
        # 期限当日
        self.goal.end_date = timezone.now().date()
        self.goal.save()
        result = evaluate_progress(self.goal)
        # remaining_days = 1
        self.assertEqual(result['remaining_days'], 1)
        # 100 / 1 = 100 -> critical
        self.assertEqual(result['status'], 'critical')

    def test_evaluate_progress_future_start(self):
        # 開始日が未来
        future_start = timezone.now().date() + timedelta(days=10)
        self.goal.start_date = future_start
        self.goal.end_date = future_start + timedelta(days=29) # 30日間
        self.goal.save()
        result = evaluate_progress(self.goal)
        # remaining_days = 30
        self.assertEqual(result['remaining_days'], 30)
        # 100 / 30 = 3.33 -> warning
        self.assertEqual(result['status'], 'warning')

    def test_evaluate_progress_completed(self):
        # 目標達成
        StudyRecord.objects.create(
            goal=self.goal,
            studied_at=timezone.now(),
            duration=6000, # 100 hours
            comment="Completed"
        )
        result = evaluate_progress(self.goal)
        self.assertEqual(result['status'], 'completed')

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        self.goal = Goal.objects.create(
            title="Test Goal",
            target_hours=100,
            start_date=start_date,
            end_date=end_date
        )

    def test_goal_list_view(self):
        response = self.client.get(reverse('tracker:goal_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/goal_form.html')

    def test_goal_detail_view(self):
        response = self.client.get(reverse('tracker:goal_detail', args=[self.goal.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/goal_detail.html')
        self.assertContains(response, "Test Goal")

    def test_create_goal_view(self):
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        response = self.client.post(reverse('tracker:goal_create'), {
            'title': 'New Goal',
            'target_hours': 50,
            'start_date': start_date,
            'end_date': end_date
        })
        self.assertEqual(response.status_code, 302) # Redirect
        self.assertEqual(Goal.objects.count(), 2)

    def test_create_record_view(self):
        studied_at = timezone.now()
        response = self.client.post(reverse('tracker:record_create', args=[self.goal.pk]), {
            'studied_at': studied_at,
            'duration': 60,
            'comment': 'Good study'
        })
        self.assertEqual(response.status_code, 302) # Redirect
        self.assertEqual(StudyRecord.objects.count(), 1)
