from website import create_app
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)