from unittest import TestCase
from app import app, db
from models import Cupcake

# Set up the test database URI and configure Flask for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

# Define CUPCAKE_DATA
CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

# Define CUPCAKE_DATA_2
CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeViewsTestCase(TestCase):
    """Tests for views of the API."""

    def setUp(self):
        """Make demo data and set up application context."""
        self.app = app.test_client()  # Create a test client
        self.ctx = app.app_context()
        self.ctx.push()  # Push an application context
        db.create_all()  # Create the database tables

        # Create a cupcake
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()
        self.cupcake = cupcake

    def tearDown(self):
        """Clean up and pop application context."""
        db.session.remove()  # Remove the session
        db.drop_all()  # Drop the database tables
        self.ctx.pop()  # Pop the application context

    def test_list_cupcakes(self):
        with self.app:
            resp = self.app.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with self.app:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = self.app.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with self.app:
            url = "/api/cupcakes"
            resp = self.app.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # Don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        with self.app:
            # Prepare data for updating the cupcake
            updated_data = {
                "flavor": "UpdatedFlavor",
                "size": "UpdatedSize",
                "rating": 8,
                "image": "http://updated.com/cupcake.jpg"
            }

            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = self.app.patch(url, json=updated_data)

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "UpdatedFlavor",
                    "size": "UpdatedSize",
                    "rating": 8,
                    "image": "http://updated.com/cupcake.jpg"
                }
            })

            # Verify that the cupcake was updated in the database
            updated_cupcake = Cupcake.query.get(self.cupcake.id)
            self.assertEqual(updated_cupcake.flavor, "UpdatedFlavor")
            self.assertEqual(updated_cupcake.size, "UpdatedSize")
            self.assertEqual(updated_cupcake.rating, 8)
            self.assertEqual(updated_cupcake.image, "http://updated.com/cupcake.jpg")

    def test_delete_cupcake(self):
        with self.app:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = self.app.delete(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {"message": "Deleted"})

           
            deleted_cupcake = Cupcake.query.get(self.cupcake.id)
            self.assertIsNone(deleted_cupcake)

    def test_edit_cupcake_with_no_image(self):
        with self.app:
            # Prepare data for editing the cupcake with no new image URL
            updated_data = {
                "flavor": "EditedFlavor",
                "size": "EditedSize",
                "rating": 9,
                "image": ""
            }

            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = self.app.patch(url, json=updated_data)

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "EditedFlavor",
                    "size": "EditedSize",
                    "rating": 9,
                    "image": "http://test.com/cupcake.jpg" 
                }
            })

            # Verify that the cupcake was updated in the database
            edited_cupcake = Cupcake.query.get(self.cupcake.id)
            self.assertEqual(edited_cupcake.flavor, "EditedFlavor")
            self.assertEqual(edited_cupcake.size, "EditedSize")
            self.assertEqual(edited_cupcake.rating, 9)
            self.assertEqual(edited_cupcake.image, "http://test.com/cupcake.jpg")  # Original image URL

    def test_edit_cupcake_without_changes(self):
        with self.app:
            # Prepare data for editing the cupcake without making any changes
            updated_data = {
                "flavor": "TestFlavor",
                "size": "TestSize",
                "rating": 5,
                "image": "http://test.com/cupcake.jpg"
            }

            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = self.app.patch(url, json=updated_data)

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

            # Check if db changes
            unchanged_cupcake = Cupcake.query.get(self.cupcake.id)
            self.assertEqual(unchanged_cupcake.flavor, "TestFlavor")
            self.assertEqual(unchanged_cupcake.size, "TestSize")
            self.assertEqual(unchanged_cupcake.rating, 5)
            self.assertEqual(unchanged_cupcake.image, "http://test.com/cupcake.jpg")
