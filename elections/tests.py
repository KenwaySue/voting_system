from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import Election, Candidate, Vote

class ModelCreationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='candidate1',
            password='testpass'
        )

        self.candidate = Candidate.objects.create(
            user=self.user,
            full_name='Ivan Ivanov',
            bio='Bio',
            program='Program'
        )

        self.election = Election.objects.create(
            title='Test Election',
            description='Description',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            is_active=True
        )

    def test_models_created(self):
        self.assertEqual(Candidate.objects.count(), 1)
        self.assertEqual(Election.objects.count(), 1)
class VoteModelTest(TestCase):

    def setUp(self):
        self.voter = User.objects.create_user(
            username='voter',
            password='testpass'
        )

        self.candidate_user = User.objects.create_user(
            username='candidate',
            password='testpass'
        )

        self.candidate = Candidate.objects.create(
            user=self.candidate_user,
            full_name='Candidate',
            bio='Bio',
            program='Program'
        )

        self.election = Election.objects.create(
            title='Election',
            description='Desc',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            is_active=True
        )

    def test_unique_vote_constraint(self):
        Vote.objects.create(
            voter=self.voter,
            candidate=self.candidate,
            election=self.election
        )

        with self.assertRaises(Exception):
            Vote.objects.create(
                voter=self.voter,
                candidate=self.candidate,
                election=self.election
            )
class VoteViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.voter = User.objects.create_user(
            username='voter',
            password='testpass'
        )

        self.candidate_user = User.objects.create_user(
            username='candidate',
            password='testpass'
        )

        self.candidate = Candidate.objects.create(
            user=self.candidate_user,
            full_name='Candidate',
            bio='Bio',
            program='Program'
        )

        self.election = Election.objects.create(
            title='Election',
            description='Desc',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            is_active=True
        )

        self.vote_url = reverse(
            'elections:vote',
            args=[self.election.id, self.candidate.id]
        )

    def test_vote_requires_login(self):
        response = self.client.post(self.vote_url)
        self.assertEqual(response.status_code, 302)

    def test_user_can_vote_once(self):
        self.client.login(username='voter', password='testpass')

        response = self.client.post(self.vote_url)
        self.assertEqual(Vote.objects.count(), 1)

        response = self.client.post(self.vote_url)
        self.assertEqual(Vote.objects.count(), 1)
