from config import create_app

from db import db

app = create_app()


@app.after_request
def close_request(response):
    db.session.commit()
    return response


if __name__ == '__main__':
    app.run(debug=True)
