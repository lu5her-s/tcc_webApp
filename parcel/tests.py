from django.test import TestCase, Client
from django.urls import reverse

from parcel.models import RequestBill, RequestBillDetail
from asset.models import Category, StockItem
from account.models import Profile
from django.contrib.auth.models import User

class ParcelViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.department = Profile.objects.create(user=self.user, department='IT')
        self.profile = Profile.objects.create(user=self.user, department__name='IT')
        self.stock = Profile.objects.create(user=User.objects.create_user(username='stockuser', password='12345'), department='Stock')
        self.category = Category.objects.create(name='Computer')
        self.item = StockItem.objects.create(name='Computer', category=self.category, serial='1234567890')
        self.stock_item = StockItem.objects.create(item=self.item, quantity=10, profile=self.stock)
        self.bill = RequestBill.objects.create(user=self.user, stock=self.stock, status='DRAFT')
        self.bill_detail = RequestBillDetail.objects.create(bill=self.bill, request_case='Normal', item_type='Normal', item_control='Normal', money_type='Normal', job_no='1234567890')

    def test_parcel_detail_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('parcel:detail', kwargs={'pk': self.bill.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'แจ้งซ่อมเลขที่')
        self.assertContains(response, 'รายละเอียด')
        self.assertContains(response, 'รายละเอียดเพิ่มเติม')

    def test_parcel_detail_view_for_stock(self):
        self.client.login(username='stockuser', password='12345')
        response = self.client.get(reverse('parcel:detail', kwargs={'pk': self.bill.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'แจ้งซ่อมเลขที่')
        self.assertContains(response, 'รายละเอียด')
        self.assertContains(response, 'รายละเอียดเพิ่มเติม')

    def test_parcel_detail_view_for_other_user(self):
        user = User.objects.create_user(username='otheruser', password='12345')
        profile = Profile.objects.create(user=user, department='Other')
        self.client.login(username='otheruser', password='12345')
        response = self.client.get(reverse('parcel:detail', kwargs={'pk': self.bill.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'แจ้งซ่อมเลขที่')
        self.assertContains(response, 'รายละเอียด')
        self.assertContains(response, 'รายละเอียดเพิ่มเติม')

    def test_parcel_detail_view_for_anonymous_user(self):
        response = self.client.get(reverse('parcel:detail', kwargs={'pk': self.bill.pk}))
        self.assertEqual(response.status_code, 302)

    def test_parcel_save_draft_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('parcel:save_draft', kwargs={'pk': self.bill.pk}), {'receiver': self.profile.pk, 'request_case': 'Normal', 'item_type': 'Normal', 'item_control': 'Normal', 'money_type': 'Normal', 'job_no': '1234567890'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('parcel:detail', kwargs={'pk': self.bill.pk}))

    def test_parcel_save_draft_view_for_stock(self):
        self.client.login(username='stockuser', password='12345')
        response = self.client.post(reverse('parcel:save_draft', kwargs={'pk': self.bill.pk}), {'receiver': self.profile.pk, 'request_case': 'Normal', 'item_type': 'Normal', 'item_control': 'Normal', 'money_type': 'Normal', 'job_no': '1234567890'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('parcel:detail', kwargs={'pk': self.bill.pk}))

    def test_parcel_save_draft_view_for_other_user(self):
        user = User.objects.create_user(username='otheruser', password='12345')
        profile = Profile.objects.create(user=user, department='Other')
        self.client.login(username='otheruser', password='12345')
        response = self.client.post(reverse('parcel:save_draft', kwargs={'pk': self.bill.pk}), {'receiver': self.profile.pk, 'request_case': 'Normal', 'item_type': 'Normal', 'item_control': 'Normal', 'money_type': 'Normal', 'job_no': '1234567890'})
        self.assertEqual(response.status_code, 403)

    def test_parcel_save_draft_view_for_anonymous_user(self):
        response = self.client.post(reverse('parcel:save_draft', kwargs={'pk': self.bill.pk}), {'receiver': self.profile.pk, 'request_case': 'Normal', 'item_type': 'Normal', 'item_control': 'Normal', 'money_type': 'Normal', 'job_no': '1234567890'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:login') + '?next=' + reverse('parcel:save_draft', kwargs={'pk': self.bill.pk}))

    def test_parcel_request_bill_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('parcel:request_bill', kwargs={'pk': self.bill.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('parcel:detail', kwargs={'pk': self.bill.pk}))

    def test_parcel_request_bill_view_for_stock(self):
        self.client.login(username='stockuser', password='12345')
        response = self.client.post(reverse('parcel:request_bill', kwargs={'pk': self.bill.pk}))
        self.assertEqual(response.status_code, 403)

    def test_parcel_request_bill_view_for_other_user(self):
        user = User.objects.create_user(username='otheruser', password='12345')
        profile = Profile.objects.create(user=user, department='Other')
        self.client.login(username='otheruser', password='12345')
        response = self.client.post(reverse('parcel:request_bill', kwargs={'pk': self.bill.pk}))
        self.assertEqual(response.status_code, 403)

    def test_parcel_request_bill_view_for_anonymous_user(self):
        response = self.client.post(reverse('parcel:request_bill', kwargs={'pk': self.bill.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:login') + '?next=' + reverse('parcel:request_bill', kwargs={'pk': self.bill.pk}))

    def test_parcel_reject_bill_view(self):
        self.client.login(username='stockuser', password='12345')
        response = self.client.post(reverse('parcel:reject_bill', kwargs={'pk': self.bill.pk}), {'note': 'This is a test note'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('parcel:detail', kwargs={'pk': self.bill.pk}))
