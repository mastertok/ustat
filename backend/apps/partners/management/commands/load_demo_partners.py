from django.core.management.base import BaseCommand
from apps.partners.models import Partner

class Command(BaseCommand):
    help = 'Loads demo partners data'

    def handle(self, *args, **kwargs):
        partners_data = [
            {
                'name': 'IT Academy',
                'logo': 'partners/logos/it-academy.png',
                'website': 'https://itacademy.kg',
            },
            {
                'name': 'Makers',
                'logo': 'partners/logos/makers.png',
                'website': 'https://makers.kg',
            },
            {
                'name': 'Codify',
                'logo': 'partners/logos/codify.png',
                'website': 'https://codify.kg',
            },
            {
                'name': 'Neobis',
                'logo': 'partners/logos/neobis.png',
                'website': 'https://neobis.kg',
            },
        ]

        for partner_data in partners_data:
            Partner.objects.get_or_create(
                name=partner_data['name'],
                defaults={
                    'logo': partner_data['logo'],
                    'website': partner_data['website'],
                }
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created partner {partner_data["name"]}')
            )
