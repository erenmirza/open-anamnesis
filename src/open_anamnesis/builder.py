"""
Builder module - generates web interface for the project
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Any

from .project import Project
from .deck import Deck
from .compiler import Compiler


class Builder:
    """Builds web interface from Anamnesis project"""
    
    def __init__(self, project_dir: str = "."):
        self.project = Project(project_dir)
        self.build_dir = self.project.root_path / "build"
        self.compiler = Compiler(project_dir)
    
    def build(self) -> None:
        """Build the web interface"""
        self.build_dir.mkdir(exist_ok=True)
        
        # Generate project manifest
        manifest = self._generate_manifest()
        
        # Write manifest
        with open(self.build_dir / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        
        # Generate HTML
        self._generate_html()
        
        # Copy static assets
        self._copy_assets()
    
    def _generate_manifest(self) -> Dict[str, Any]:
        """Generate project manifest with all decks and cards"""
        deck_names = self.project.list_decks()
        deck_order = self.compiler.get_deck_order()
        
        decks_data = []
        for deck_name in deck_names:
            deck_path = self.project.decks_dir / deck_name
            deck = Deck(str(deck_path))
            
            decks_data.append({
                "id": deck_name,
                "metadata": deck.get_metadata(),
                "cards": deck.get_cards(),
            })
        
        return {
            "project": self.project.get_project_metadata(),
            "decks": decks_data,
            "deck_order": deck_order,
            "dependency_graph": self.compiler.get_dependency_graph(),
        }
    
    def _generate_html(self) -> None:
        """Generate main HTML file from template"""
        template_path = Path(__file__).parent / "templates" / "index.html"
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        with open(self.build_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def _copy_assets(self) -> None:
        """Copy static assets (CSS, JS) from src/static to build/static"""
        static_dir = self.build_dir / "static"
        static_dir.mkdir(exist_ok=True)

        # Copy CSS and JS files from src/static
        src_static = Path(__file__).parent / "static"
        shutil.copy2(src_static / "style.css", static_dir / "style.css")
        shutil.copy2(src_static / "app.js", static_dir / "app.js")

    def serve(self, host: str = "127.0.0.1", port: int = 5000) -> None:
        """Serve the built web interface using SimpleHTTPServer"""
        import http.server
        import socketserver
        
        # Change to build directory
        original_dir = os.getcwd()
        os.chdir(self.build_dir)
        
        try:
            class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
                """HTTP handler that serves index.html for root and supports caching headers"""
                
                def log_message(self, format, *args):
                    """Suppress default logging"""
                    pass
                
                def end_headers(self):
                    """Add cache control headers"""
                    self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
                    super().end_headers()
                
                def do_GET(self):
                    """Handle GET requests"""
                    if self.path == '/':
                        self.path = '/index.html'
                    elif self.path.endswith('/'):
                        self.path = self.path + 'index.html'
                    return super().do_GET()
            
            # Suppress default server logging
            socketserver.TCPServer.allow_reuse_address = True
            
            with socketserver.TCPServer((host, port), QuietHTTPRequestHandler) as httpd:
                click = __import__('click')
                click.echo(f"SUCCESS: Build successful!")
                click.echo(f"  Web interface generated in 'build/' directory")
                click.echo(f"  Starting server at http://{host}:{port}")
                click.echo("  Press Ctrl+C to exit")
                click.echo()
                
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    click.echo("\nSTOPPED: Server stopped")
        finally:
            os.chdir(original_dir)
