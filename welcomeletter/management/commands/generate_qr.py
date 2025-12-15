from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Generate an SVG QR code for the given URL and save it to static/images/'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, default='https://ramseshilton.com', help='URL to encode')
        parser.add_argument('--output', type=str, default=None, help='Output file path (optional)')
        parser.add_argument('--scale', type=int, default=10, help='Scale for the SVG')

    def handle(self, *args, **options):
        url = options['url']
        scale = options['scale'] or 10
        out = options['output']

        # Resolve default output to project's static/images
        base_static = Path(settings.BASE_DIR) / 'static' / 'images'
        base_static.mkdir(parents=True, exist_ok=True)

        if out:
            output_path = Path(out)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            output_path = base_static / 'ramseshilton_qr.svg'

        try:
            import segno
        except Exception as e:
            self.stderr.write('segno is not installed. Please install with `pip install segno`')
            raise

        qr = segno.make(url, error='H')
        qr.save(str(output_path), scale=scale)

        self.stdout.write(self.style.SUCCESS(f'QR for {url} saved to {output_path}'))
