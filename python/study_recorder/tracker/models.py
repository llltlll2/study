from django.db import models
from django.core.validators import MinValueValidator

class Goal(models.Model):
    title = models.CharField(max_length=200, verbose_name="資格名")
    target_hours = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="目標学習時間(時間)",
        help_text="合格に必要な総学習時間"
    )
    start_date = models.DateField(verbose_name="開始日")
    end_date = models.DateField(verbose_name="終了日")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class StudyRecord(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='records')
    studied_at = models.DateTimeField(verbose_name="学習日時")
    duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="学習時間(分)",
        help_text="1回の学習時間"
    )
    comment = models.TextField(blank=True, verbose_name="コメント")

    def __str__(self):
        return f"{self.goal.title} - {self.studied_at}"
