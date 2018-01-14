from django.test import TestCase
from team_members.models import TeamMember
from django.core.exceptions import ValidationError
from django.test import Client
import json


class TeamMemberTestCase(TestCase):

    def test_accept_valid_phone_and_email_string(self):
        team_member = TeamMember(
            first_name="first_name1",
            last_name="last_name1",
            role="admin",
            phone_number="1234567890",
            email="test1@gmail.com"
        )
        team_member.full_clean()
        self.assertTrue(True)

    def test_phonenumber_rejects_digit_string(self):
        team_member = TeamMember(
            first_name="first_name1",
            last_name="last_name1",
            role="admin",
            phone_number="123456789",
            email="test1@gmail.com"
        )
        with self.assertRaises(ValidationError) as ve:
            team_member.full_clean()
        self.assertTrue(
          "phone_number" in str(ve.exception),
          "invalid phone number accepted"
        )

    def test_phonenumber_rejects_non_digit_string(self):
        team_member = TeamMember(
            first_name="first_name1",
            last_name="last_name1",
            role="admin",
            phone_number="123456789w",
            email="test1@gmail.com"
        )
        with self.assertRaises(ValidationError) as ve:
            team_member.full_clean()
        self.assertTrue(
          "phone_number" in str(ve.exception),
          "invalid phone number accepted"
        )

    def test_role_accepts_admin_and_regular(self):
        for role in ["admin", "regular"]:
            team_member = TeamMember(
                first_name="first_name1",
                last_name="last_name1",
                role=role,
                phone_number="1234567890",
                email="test1@gmail.com"
            )
            team_member.full_clean()

    def test_role_rejects_invalids(self):
        team_member = TeamMember(
            first_name="first_name1",
            last_name="last_name1",
            role="user",
            phone_number="1234567890",
            email="test1@gmail.com"
        )
        with self.assertRaises(ValidationError) as ve:
            team_member.full_clean()
        self.assertTrue("role" in str(ve.exception), "invalid role accepted")


class TemaMemberListViewTestCase(TestCase):

    def setUp(self):
        TeamMember.objects.create(
            first_name="first_name1",
            last_name="last_name1",
            role="admin",
            phone_number="1234567890",
            email="test1@gmail.com"
        )
        TeamMember.objects.create(
            first_name="first_name2",
            last_name="last_name2",
            role="regular",
            phone_number="1234567891",
            email="test2@gmail.com"
        )

    def test_get_lists_team_members(self):
        c = Client()
        response = c.get("/team_members/")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["first_name"], "first_name1")

    def test_post_fails_new_team_member_with_invalid_phone_email(self):
        c = Client()
        data = {
            "first_name": "first_name3",
            "last_name": "last_name1",
            "role": "admin",
            "email": "testgmail.com"
        }
        response = c.post("/team_members/", data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('phone_number' in response.data.keys())
        self.assertTrue('email' in response.data.keys())
        team_members = list(TeamMember.objects.filter())
        self.assertEqual(len(team_members), 2)

    def test_post_create_new_team_member(self):
        c = Client()
        data = {
            "first_name": "first_name3",
            "last_name": "last_name1",
            "role": "admin",
            "phone_number": "1234567890",
            "email": "test1@gmail.com"
        }
        response = c.post("/team_members/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["first_name"], "first_name3")
        self.assertEqual(response.data["last_name"], "last_name1")
        self.assertEqual(response.data["role"], "admin")
        self.assertEqual(response.data["phone_number"], "1234567890")
        self.assertEqual(response.data["email"], "test1@gmail.com")

        team_members = list(TeamMember.objects.filter())
        self.assertEqual(len(team_members), 3)
        self.assertEqual(team_members[2].first_name, "first_name3")


class TeamMemberDetailViewTestCase(TestCase):

    def setUp(self):
        self.TeamMember1 = TeamMember.objects.create(
            first_name="first_name1",
            last_name="last_name1",
            role="admin",
            phone_number="1234567890",
            email="test1@gmail.com"
        )

    def test_update_updates_team_member(self):
        c = Client()
        data = {
            "first_name": "first_name3",
            "last_name": "last_name",
            "role": "regular",
            "phone_number": "1111111111",
            "email": "test3@gmail.com"
        }
        response = c.put(
          "/team_members/{}/".format(self.TeamMember1.id),
          json.dumps(data),
          content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], "first_name3")
        self.assertEqual(response.data['last_name'], "last_name")
        self.assertEqual(response.data['role'], "regular")
        self.assertEqual(response.data['phone_number'], "1111111111")
        self.assertEqual(response.data['email'], "test3@gmail.com")

    def test_patch_updates_team_member_partial_data(self):
        c = Client()
        data = {
            "first_name": "abcd",
            "phone_number": "1111111111"
        }
        response = c.patch(
          "/team_members/{}/".format(self.TeamMember1.id),
          json.dumps(data),
          content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], "abcd")
        self.assertEqual(response.data['phone_number'], "1111111111")
        # rest of the properties should not change
        self.assertEqual(response.data['last_name'], "last_name1")
        self.assertEqual(response.data['role'], "admin")
        self.assertEqual(response.data['email'], "test1@gmail.com")

    def test_update_invalid_team_member_id_api_returns_404(self):
        c = Client()
        data = {
            "first_name": "first_name3",
            "last_name": "last_name",
            "role": "regular",
            "phone_number": "1111111111",
            "email": "test3@gmail.com"
        }
        response = c.put("/team_members/2/", data)
        self.assertEqual(response.status_code, 404)

    def test_delete_team_member(self):
        c = Client()
        response = c.delete("/team_members/{}/".format(self.TeamMember1.id))
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(TeamMember.DoesNotExist):
            TeamMember.objects.get(id=self.TeamMember1.id)
