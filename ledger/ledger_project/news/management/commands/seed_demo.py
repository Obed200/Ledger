from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import Profile
from news.models import Article

User = get_user_model()

ARTICLES = [
    ("Central Banks Signal a Slower Path on Rates",
     "Policymakers in three major economies hint at patience, favoring data over drama as inflation cools unevenly.",
     "Markets",
     "Officials speaking this week converged on a common theme: no rush. After eighteen months of aggressive tightening, the tone from monetary authorities has shifted from urgency to observation.\n\nMarket pricing had assumed a faster pivot, but futures adjusted quickly once the latest commentary landed.",
     True),
    ("The Founders Who Walked Away From Their Own Unicorns",
     "A growing number of company builders are choosing to step back at the peak, trading control for a different kind of freedom.",
     "Leadership",
     "Succession has always been the hardest chapter for a founder to write. Increasingly, some are choosing to write it early.\n\nThe move runs against instinct, but those who have done it describe a common thread: clarity about what they are actually good at.",
     False),
    ("Inside the Quiet Race to Rebuild the Power Grid",
     "Utilities are spending at levels unseen in a generation, betting that electrification will outpace every forecast.",
     "Technology",
     "The grid was built for a world of predictable, one-directional power flow. That world is gone.\n\nUtilities that spent decades optimizing for stability are now being asked to optimize for growth.",
     False),
    ("Why Family Offices Are Buying Farmland Again",
     "With public markets volatile, a quiet allocation shift toward hard, productive assets is picking up pace.",
     "Money",
     "Farmland has none of the glamour of venture capital or private equity, and that, several allocators say, is precisely the appeal right now.",
     False),
]


class Command(BaseCommand):
    help = "Seeds a demo administrator, a demo author and a handful of sample stories."

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username="admin", defaults={"first_name": "Site Administrator", "is_staff": True, "is_superuser": True}
        )
        if created:
            admin.set_password("admin12345")
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created administrator "admin" / password "admin12345"'))

        author, created = User.objects.get_or_create(
            username="jkim", defaults={"first_name": "Jordan Kim"}
        )
        if created:
            author.set_password("author12345")
            author.save()
            Profile.objects.filter(user=author).update(role="author", bio="Covers markets and monetary policy.")
            self.stdout.write(self.style.SUCCESS('Created author "jkim" / password "author12345"'))

        for title, dek, category, body, featured in ARTICLES:
            Article.objects.get_or_create(
                title=title,
                defaults={"dek": dek, "category": category, "body": body, "author": admin, "featured": featured},
            )
        self.stdout.write(self.style.SUCCESS("Demo content seeded."))
