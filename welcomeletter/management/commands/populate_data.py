from django.core.management.base import BaseCommand
from welcomeletter.models import ExternalLink, Restaurant, TransferOption, SiteSettings


class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Creating initial data...')
        
        # Create Site Settings
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        if created:
            self.stdout.write(self.style.SUCCESS('Created Site Settings'))
        
        # Create External Links
        links_data = [
            {
                'name': 'Villa Verona Menu',
                'slug': 'villa-verona-menu',
                'category': 'restaurant',
                'url': 'https://www.jbr-restaurants.com/_files/ugd/4b96f7_c8b52d9fc6564f7498a2aa7a11ddbb0d.pdf',
            },
            {
                'name': 'Trader Vic\'s Menu',
                'slug': 'trader-vics-menu',
                'category': 'restaurant',
                'url': 'https://www.jbr-restaurants.com/_files/ugd/4b96f7_cc71ee6753c9498db7e3ccbe610df6d2.pdf',
            },
            {
                'name': 'Hartisan Menu',
                'slug': 'hartisan-menu',
                'category': 'restaurant',
                'url': 'https://drive.google.com/file/d/1LNOivCAVSLugg8zQGvJCWeqcfNa0HVLy/view?usp=drive_link',
            },
            {
                'name': 'In-Room Dining Menu',
                'slug': 'room-dining-menu',
                'category': 'room_dining',
                'url': 'https://drive.google.com/file/d/1uB6EanehPuN--i62bb61oybIVDMDvjXB/view?usp=drive_link',
            },
            {
                'name': 'Spa Menu',
                'slug': 'spa-menu',
                'category': 'spa',
                'url': 'https://assets.hiltonstatic.com/hilton-asset-cache/image/upload/v1737566860/dx/wp/dxbjbhi-hilton-dubai-jumeirah/pdf/Dec%202024%20Spa_Booklet%2020x20CM%202024%201%201%20FINAL-ua_qgvsxn.pdf',
            },
        ]
        
        for link_data in links_data:
            link, created = ExternalLink.objects.get_or_create(
                slug=link_data['slug'],
                defaults=link_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created link: {link.name}'))
        
        # Create Restaurants
        restaurants_data = [
            {
                'name': 'Villa Verona',
                'slug': 'villa-verona',
                'description': 'Offers authentic Italian cuisine, featuring fresh ingredients, traditional flavors, and stunning sea views.',
                'image_url': 'https://static.wixstatic.com/media/4b96f7_0fde266a26a940748f2e6032b4a87a79~mv2.webp/v1/fill/w_560,h_324,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/Villa%20Verona%203.webp',
                'menu_slug': 'villa-verona-menu',
                'facebook_url': 'https://www.facebook.com/RamsesHilton',
                'instagram_url': 'https://www.instagram.com/ramseshilton',
                'tiktok_url': 'https://www.tiktok.com/@ramseshilton',
                'email': 'villaverona@ramseshilton.com',
                'opening_hours': '6:00 PM - 11:00 PM',
                'location': 'Ground Floor - Marina Area',
                'order': 1,
            },
            {
                'name': 'Trader Vic\'s JBR',
                'slug': 'trader-vics-jbr',
                'description': 'A vibrant Polynesian bar and restaurant with tropical cocktails, fusion cuisine, and an island-inspired vibe.',
                'image_url': 'https://static.wixstatic.com/media/4b96f7_1eb9e02890b14f3db8f76e00e8eb663b~mv2.webp/v1/fill/w_560,h_324,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/TV%20JBR-.webp',
                'menu_slug': 'trader-vics-menu',
                'facebook_url': 'https://www.facebook.com/RamsesHilton',
                'instagram_url': 'https://www.instagram.com/ramseshilton',
                'tiktok_url': 'https://www.tiktok.com/@ramseshilton',
                'email': 'tradervics@ramseshilton.com',
                'opening_hours': '5:00 PM - 12:00 AM',
                'location': '2nd Floor - Atrium Bar',
                'order': 2,
            },
            {
                'name': 'Hartisan',
                'slug': 'hartisan',
                'description': 'The stylish all-day dining restaurant offers a hearty breakfast to kick-start your day.',
                'image_url': 'https://static.wixstatic.com/media/4b96f7_82d5ebf0f31241e4ab15a8d6c1aa8af7~mv2.webp/v1/fill/w_560,h_324,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/Hartisan_2358226867.webp',
                'menu_slug': 'hartisan-menu',
                'facebook_url': 'https://www.facebook.com/RamsesHilton',
                'instagram_url': 'https://www.instagram.com/ramseshilton',
                'tiktok_url': 'https://www.tiktok.com/@ramseshilton',
                'email': 'hartisan@ramseshilton.com',
                'opening_hours': '6:30 AM - 11:00 PM',
                'location': '3rd Floor - Main Dining',
                'order': 3,
            },
            {
                'name': 'Taliah\'s Café',
                'slug': 'taliahs-cafe',
                'description': 'Located in the lobby, offering the perfect selection of coffee and pâtisserie delights.',
                'image_url': '',
                'menu_slug': None,
                'facebook_url': 'https://www.facebook.com/RamsesHilton',
                'instagram_url': 'https://www.instagram.com/ramseshilton',
                'tiktok_url': '',
                'email': 'cafe@ramseshilton.com',
                'opening_hours': '7:00 AM - 10:00 PM',
                'location': 'Lobby Ground Floor',
                'order': 4,
            },
            {
                'name': 'Marbar',
                'slug': 'marbar',
                'description': 'Our new rooftop tapas bar on the 10th floor, featuring Spanish-inspired small plates and cocktails with panoramic views of the sea, Ain Dubai, and Palm Jumeirah.',
                'image_url': '',
                'menu_slug': None,
                'facebook_url': 'https://www.facebook.com/RamsesHilton',
                'instagram_url': 'https://www.instagram.com/ramseshilton',
                'tiktok_url': 'https://www.tiktok.com/@ramseshilton',
                'email': 'marbar@ramseshilton.com',
                'opening_hours': '5:00 PM - 1:00 AM',
                'location': '10th Floor - Rooftop',
                'order': 5,
            },
            {
                'name': 'Wavebreaker Beach Restaurant & Grill',
                'slug': 'wavebreaker',
                'description': 'Beachfront dining at its finest with refreshed menus crafted to bring you new flavors and experiences.',
                'image_url': '',
                'menu_slug': None,
                'facebook_url': 'https://www.facebook.com/RamsesHilton',
                'instagram_url': 'https://www.instagram.com/ramseshilton',
                'tiktok_url': '',
                'email': 'wavebreaker@ramseshilton.com',
                'opening_hours': '12:00 PM - 11:00 PM',
                'location': 'Beach Level',
                'order': 6,
            },
        ]
        
        for rest_data in restaurants_data:
            menu_link = None
            if rest_data.get('menu_slug'):
                menu_link = ExternalLink.objects.filter(slug=rest_data['menu_slug']).first()
            
            restaurant, created = Restaurant.objects.get_or_create(
                slug=rest_data['slug'],
                defaults={
                    'name': rest_data['name'],
                    'description': rest_data['description'],
                    'image_url': rest_data['image_url'],
                    'menu_link': menu_link,
                    'facebook_url': rest_data.get('facebook_url', ''),
                    'instagram_url': rest_data.get('instagram_url', ''),
                    'tiktok_url': rest_data.get('tiktok_url', ''),
                    'email': rest_data.get('email', ''),
                    'opening_hours': rest_data.get('opening_hours', ''),
                    'location': rest_data.get('location', ''),
                    'order': rest_data['order'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created restaurant: {restaurant.name}'))
        
        # Create Transfer Options
        transfers_data = [
            {
                'name': 'Sedan',
                'vehicle_type': 'Lexus ES / Hybrid / BMW 5 or similar',
                'max_capacity': '2 adults including luggage',
                'price_to_hotel': 235,
                'price_from_hotel': 200,
                'icon': '🚗',
                'order': 1,
            },
            {
                'name': 'Tesla Model 3',
                'vehicle_type': 'Go Green & Go Electric!',
                'max_capacity': '2 adults, including 2 pieces of luggage',
                'price_to_hotel': 390,
                'price_from_hotel': 325,
                'icon': '🔋',
                'order': 2,
            },
            {
                'name': 'Mid-size SUV',
                'vehicle_type': 'Comfortable and spacious',
                'max_capacity': '5 adults including luggage',
                'price_to_hotel': 255,
                'price_from_hotel': 220,
                'icon': '🚙',
                'order': 3,
            },
            {
                'name': 'GMC Yukon / Mercedes Viano',
                'vehicle_type': 'Perfect for groups',
                'max_capacity': 'up to 6 adults including luggage',
                'price_to_hotel': 390,
                'price_from_hotel': 325,
                'icon': '🚐',
                'order': 4,
            },
        ]
        
        for transfer_data in transfers_data:
            transfer, created = TransferOption.objects.get_or_create(
                name=transfer_data['name'],
                defaults=transfer_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created transfer: {transfer.name}'))
        
        self.stdout.write(self.style.SUCCESS('Initial data population complete!'))
