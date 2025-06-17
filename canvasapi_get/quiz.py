from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.quiz_group import QuizGroup
from canvasapi.submission import Submission
from canvasapi.user import User
from canvasapi.util import combine_kwargs, obj_or_id


class Quiz(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    def get_all_quiz_reports(self, **kwargs):
        """
        Get a list of all quiz reports for this quiz

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/reports \
        <https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.quiz.QuizReport`
        """
        return PaginatedList(
            QuizReport,
            self._requester,
            "GET",
            "courses/{}/quizzes/{}/reports".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_question(self, question, **kwargs):
        """
        Get as single quiz question by ID.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id \
        <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.show>`_

        :param question: The object or ID of the quiz question to retrieve.
        :type question: int, str or :class:`canvasapi_get.quiz.QuizQuestion`

        :rtype: :class:`canvasapi.quiz.QuizQuestion`
        """
        question_id = obj_or_id(question, "question", (QuizQuestion,))

        response = self._requester.request(
            "GET",
            "courses/{}/quizzes/{}/questions/{}".format(
                self.course_id, self.id, question_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return QuizQuestion(self._requester, response_json)

    def get_questions(self, **kwargs):
        """
        List all questions for a quiz.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/questions \
        <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.quiz.QuizQuestion`
        """
        return PaginatedList(
            QuizQuestion,
            self._requester,
            "GET",
            "courses/{}/quizzes/{}/questions".format(self.course_id, self.id),
            {"course_id": self.course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_quiz_group(self, id, **kwargs):
        """
        Get details of the quiz group with the given id

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id \
        <https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.show>`_

        :param id: The ID of the question group.
        :type id: int

        :returns: `QuizGroup` object
        :rtype: :class:`canvasapi.quiz_group.QuizGroup`
        """
        response = self._requester.request(
            "GET",
            "courses/{}/quizzes/{}/groups/{}".format(self.course_id, self.id, id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return QuizGroup(self._requester, response_json)

    def get_quiz_report(self, id, **kwargs):
        """
        Returns the data for a single quiz report.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/reports/:id \
        <https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.show>`_

        :param id: The ID of the quiz report you want to retrieve, or the report object
        :type id: int or :class:`canvasapi.quiz.QuizReport`

        :returns: `QuizReport` object
        :rtype: :class:`canvasapi.quiz.QuizReport`
        """
        id = obj_or_id(id, "id", (QuizReport,))

        response = self._requester.request(
            "GET",
            "courses/{}/quizzes/{}/reports/{}".format(self.course_id, self.id, id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return QuizReport(self._requester, response_json)

    def get_quiz_submission(self, quiz_submission, **kwargs):
        """
        Get a single quiz submission.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.show>`_

        :param quiz_submission: The object or ID of the quiz submission to retrieve.
        :type quiz_submission: int, string, :class:`canvasapi_get.quiz.QuizSubmission`

        :rtype: :class:`canvasapi.quiz.QuizSubmission`
        """
        quiz_submission_id = obj_or_id(
            quiz_submission, "quiz_submission", (QuizSubmission,)
        )

        response = self._requester.request(
            "GET",
            "courses/{}/quizzes/{}/submissions/{}".format(
                self.course_id, self.id, quiz_submission_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()["quiz_submissions"][0]
        response_json.update({"course_id": self.course_id})
        if len(response.json().get("quizzes", [])) > 0:
            response_json.update(
                {"quiz": Quiz(self._requester, response.json()["quizzes"][0])}
            )
        if len(response.json().get("submissions", [])) > 0:
            response_json.update(
                {
                    "submission": Submission(
                        self._requester, response.json()["submissions"][0]
                    )
                }
            )
        if len(response.json().get("users", [])) > 0:
            response_json.update(
                {"user": User(self._requester, response.json()["users"][0])}
            )

        return QuizSubmission(self._requester, response_json)

    def get_statistics(self, **kwargs):
        """
        Get statistics for for all quiz versions, or the latest quiz version.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/statistics \
        <https://canvas.instructure.com/doc/api/quiz_statistics.html#method.quizzes/quiz_statistics.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.quiz.QuizStatistic`
        """
        return PaginatedList(
            QuizStatistic,
            self._requester,
            "GET",
            "courses/{}/quizzes/{}/statistics".format(self.course_id, self.id),
            {"course_id": self.course_id},
            _root="quiz_statistics",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_submissions(self, **kwargs):
        """
        Get a list of all submissions for this quiz.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.quiz.QuizSubmission`
        """
        return PaginatedList(
            QuizSubmission,
            self._requester,
            "GET",
            "courses/{}/quizzes/{}/submissions".format(self.course_id, self.id),
            {"course_id": self.course_id},
            _root="quiz_submissions",
            _kwargs=combine_kwargs(**kwargs),
        )


class QuizStatistic(CanvasObject):
    def __str__(self):
        return "Quiz Statistic {}".format(self.id)


class QuizSubmission(CanvasObject):
    def __str__(self):
        return "Quiz {} - User {} ({})".format(self.quiz_id, self.user_id, self.id)

    def get_submission_events(self, **kwargs):
        """
        Retrieve the set of events captured during a specific submission attempt.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/events \
        <https://canvas.instructure.com/doc/api/quiz_submission_events.html#method.quizzes/quiz_submission_events_api.index>`_

        :returns: PaginatedList of QuizSubmissionEvents.
        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
          :class:`canvasapi_get.quiz.QuizSubmissionEvent`
        """
        return PaginatedList(
            QuizSubmissionEvent,
            self._requester,
            "GET",
            "courses/{}/quizzes/{}/submissions/{}/events".format(
                self.course_id, self.quiz_id, self.id
            ),
            _root="quiz_submission_events",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_submission_questions(self, **kwargs):
        """
        Get a list of all the question records for this quiz submission.

        :calls: `GET /api/v1/quiz_submissions/:quiz_submission_id/questions \
        <https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.index>`_

        :returns: A list of quiz submission questions.
        :rtype: list of :class:`canvasapi.quiz.QuizSubmissionQuestion`
        """
        response = self._requester.request(
            "GET",
            "quiz_submissions/{}/questions".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        questions = list()
        for question in response.json().get("quiz_submission_questions", []):
            question.update({"quiz_submission_id": self.id, "attempt": self.attempt})
            questions.append(QuizSubmissionQuestion(self._requester, question))

        return questions

    def get_times(self, **kwargs):
        """
        Get the current timing data for the quiz attempt, both the end_at timestamp and the
        time_left parameter.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/time \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.time>`_

        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            "courses/{}/quizzes/{}/submissions/{}/time".format(
                self.course_id, self.quiz_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()


class QuizExtension(CanvasObject):
    def __str__(self):
        return "{}-{}".format(self.quiz_id, self.user_id)


class QuizQuestion(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.question_name, self.id)


class QuizReport(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.report_type, self.id)


class QuizSubmissionEvent(CanvasObject):
    def __str__(self):
        return "{}".format(self.event_type)


class QuizSubmissionQuestion(CanvasObject):
    def __str__(self):
        return "QuizSubmissionQuestion #{}".format(self.id)


class QuizAssignmentOverrideSet(CanvasObject):
    def __str__(self):
        return "Overrides for quiz_id {}".format(self.quiz_id)
