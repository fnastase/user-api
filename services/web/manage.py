from flask.cli import FlaskGroup
import unittest


from app import app, db

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("test")
def test():
    """Run the unit tests."""

    # app = create_app('testing')

    tests = unittest.TestLoader().discover('tests')
    print(tests)

    unittest.TextTestRunner(verbosity=2).run(tests) 


if __name__ == "__main__":
    cli()
