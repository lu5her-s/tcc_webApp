from django.test import TestCase
from django.urls import reverse_lazy
from operation.models import Operation, Team
from operation.forms import OperationForm, TeamForm
from django.contrib.auth.models import User
from unittest.mock import patch


class OperationCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_login(self.user)

    @patch("operation.views.OperationForm")
    @patch("operation.views.TeamForm")
    def test_get(self, mock_team_form, mock_operation_form):
        mock_operation_form.return_value = OperationForm()
        mock_team_form.return_value = TeamForm()
        response = self.client.get(reverse_lazy("operation:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "operation/operation_form.html")
        self.assertTrue("operation_form" in response.context)
        self.assertTrue("team_form" in response.context)

    # @patch("operation.views.OperationForm")
    # @patch("operation.views.TeamForm")
    # def test_post_valid(self, mock_team_form, mock_operation_form):
    #     mock_operation_form.return_value = OperationForm()
    #     mock_operation_form.is_valid.return_value = True
    #     mock_team_form.return_value = TeamForm()
    #     mock_team_form.is_valid.return_value = True
    #     mock_operation_form.cleaned_data = {
    #         "type_of_work": "OT",
    #         "other_type": "Other",
    #     }
    #     response = self.client.post(reverse_lazy("operation:create"), data={})
    #     self.assertRedirects(
    #         response,
    #         reverse_lazy(
    #             "operation:detail", kwargs={"pk": mock_operation_form.instance.pk}
    #         ),
    #         fetch_redirect_response=True,
    #     )

    @patch("operation.views.OperationForm")
    @patch("operation.views.TeamForm")
    def test_post_invalid(self, mock_team_form, mock_operation_form):
        mock_operation_form.return_value = OperationForm()
        mock_operation_form.is_valid.return_value = False
        mock_team_form.return_value = TeamForm()
        mock_team_form.is_valid.return_value = True
        response = self.client.post(reverse_lazy("operation:create"), data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "operation/operation_form.html")
        self.assertTrue("operation_form" in response.context)
