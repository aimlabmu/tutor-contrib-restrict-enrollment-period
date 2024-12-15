from django.db import models
from django.utils import timezone
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview


class CourseEnrollmentRule(models.Model):
    course = models.OneToOneField(
        CourseOverview,
        on_delete=models.CASCADE,
        related_name='enrollment_rule'
    )
    min_days_before_access = models.PositiveIntegerField(
        default=0,
        help_text="Minimum number of days a user must be enrolled before accessing the course"
    )
    max_days_until_expiry = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum number of days after enrollment before access expires (leave blank for no expiry)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course Enrollment Rule"
        verbose_name_plural = "Course Enrollment Rules"

    def __str__(self):
        return f"Enrollment Rule for {self.course.display_name}"

    def can_access(self, enrollment):
        if not enrollment:
            return False

        days_enrolled = (timezone.now() - enrollment.created).days

        # Check minimum days requirement
        if days_enrolled < self.min_days_before_access:
            return False

        # Check expiry if set
        if self.max_days_until_expiry and days_enrolled > self.max_days_until_expiry:
            return False

        return True

    def get_access_message(self, enrollment):
        if not enrollment:
            return "You are not enrolled in this course."

        days_enrolled = (timezone.now() - enrollment.created).days

        if days_enrolled < self.min_days_before_access:
            days_remaining = self.min_days_before_access - days_enrolled
            return f"You must be enrolled for {self.min_days_before_access} days before accessing this course. {days_remaining} days remaining."

        if self.max_days_until_expiry and days_enrolled > self.max_days_until_expiry:
            return f"Your enrollment has expired. The course was accessible for {self.max_days_until_expiry} days after enrollment."

        return None
