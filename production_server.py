"""Production server using Waitress (Windows-compatible)."""

from waitress import serve
from app import app
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    host = '0.0.0.0'
    
    print("="*70)
    print(" PRODUCTION SERVER - Household Goods Calculator")
    print("="*70)
    print(f"\n[OK] Server starting on: http://localhost:{port}")
    print(f"[OK] Network access: http://10.97.112.102:{port}")
    print(f"\n[APP] Single Calculator: http://localhost:{port}/")
    print(f"[APP] Bulk Upload: http://localhost:{port}/bulk")
    print(f"[APP] Health Check: http://localhost:{port}/health")
    print(f"\n[INFO] Using Waitress (production-ready WSGI server)")
    print(f"[INFO] Workers: 4 threads")
    print(f"\n[WARN] Press CTRL+C to stop the server")
    print("="*70)
    print()
    
    # Serve with waitress (production-ready, Windows-compatible)
    serve(app, host=host, port=port, threads=4)
