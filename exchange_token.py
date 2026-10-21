import sys
import os

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR_PATH)

from auth_youtube import exchange_code

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python exchange_token.py <code_or_url>")
        sys.exit(1)
    exchange_code(sys.argv[1])
