import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY


def get_client() -> Client:
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"  [DB ERROR] Could not connect to Supabase: {e}")
        raise