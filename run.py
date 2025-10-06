from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    debug_env = os.environ.get("DEBUG", "False").lower()
    debug_mode = debug_env in ["1", "true", "yes"]
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
