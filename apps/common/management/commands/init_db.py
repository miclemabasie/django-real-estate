from django.core.management.base import BaseCommand, CommandParser
import requests
import faker, random
from django.contrib.auth import get_user_model
from apps.properties.models import Property
from apps.enquiries.models import Enquiry
from apps.profiles.models import Profile
from apps.ratings.models import Rating

User = get_user_model()
faker = faker.Faker()


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "amount_of_fake_data",
            type=int,
            help="Provide the amount of fake data for each model you want to generate",
        )

        return super().add_arguments(parser)

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(f"We are generating a test database for you project")
        )
        self.amout = options["amount_of_fake_data"]
        self.generate_users(self.amout)
        self.generate_properties(self.amout)
        self.generate_enquiries(self.amout)
        # self.generrate_ratings(self.amout)

    def generate_properties(self, number_of_properties: int):
        """This method is used to generate fake data for properties in the database"""

        # Define fields needed for property creation
        # Randomly get a user based on id
        random_id = random.randint(1, 11)
        user = User.objects.get(pkid=random_id)
        for _ in range(number_of_properties):
            property = Property.objects.create(
                user=user,
                title=faker.name(),
                description=faker.text(max_nb_chars=100),
                # country=faker.country(),
                city=faker.city(),
                postal_code=faker.postcode(),
                street_address=faker.street_address(),
            )
            property.save()

    def generate_enquiries(self, number_of_enquries):
        """This method is used to generate fake data for enquiries in the database"""
        for _ in range(number_of_enquries):
            enquiry = Enquiry.objects.create(
                name=faker.name(),
                phone_number=faker.phone_number(),
                email=faker.email(),
                subject=faker.text(max_nb_chars=10),
                message=faker.text(max_nb_chars=100),
            )
            enquiry.save()

    def generate_users(self, number_of_users):
        """This method is used to generate fake data for users in the database"""
        for _ in range(number_of_users):
            user = User.objects.create(
                email=faker.email(),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
            )
            password = faker.password()
            user.set_password(password)
            user.save()

    def generrate_ratings(self, number_of_ratings):
        """This method is used to generate fake data for ratings in the database"""
        for _ in range(number_of_ratings):
            rating = Rating.objects.create(
                rater=User.objects.get(pkid=random.randint(1, 11)),
                agent=Profile.objects.get(pkid=random.randint(1, 11)),
                rating=random.randint(1, 5),
                comment=faker.text(),
            )
            rating.save()
