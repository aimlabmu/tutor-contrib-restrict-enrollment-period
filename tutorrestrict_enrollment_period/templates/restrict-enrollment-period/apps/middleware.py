from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from django.utils.deprecation import MiddlewareMixin
from opaque_keys.edx.keys import CourseKey
from common.djangoapps.student.models import CourseEnrollment
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from .models import CourseEnrollmentRule


class EnrollmentPeriodMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Only check for course-related views
        course_id = view_kwargs.get('course_id')
        if not course_id:
            return None

        try:
            course_key = CourseKey.from_string(course_id)
            course = CourseOverview.get_from_id(course_key)
            enrollment_rule = CourseEnrollmentRule.objects.filter(course=course).first()

            if not enrollment_rule:
                return None

            # Check if user is enrolled
            if not request.user.is_authenticated:
                return None

            enrollment = CourseEnrollment.get_enrollment(request.user, course_key)
            
            if not enrollment_rule.can_access(enrollment):
                message = enrollment_rule.get_access_message(enrollment)
                context = {
                    'message': message,
                    'course_name': course.display_name
                }
                return HttpResponseForbidden(
                    render_to_string('restrict_enrollment_period/access_denied.html', context)
                )

        except Exception:
            # Log the error but don't block access in case of errors
            return None

        return None
