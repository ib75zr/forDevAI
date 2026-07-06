"""Test suite for GET /users/<id> endpoint."""

import json
import unittest

from app import app, USERS


class TestGetUserEndpoint(unittest.TestCase):
    """Tests for the GET /users/<int:id> endpoint."""

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    # ── Happy path: existing user ──────────────────────────────────────

    def test_existing_user_returns_200(self):
        """GET /users/1 should return 200 for an existing user."""
        resp = self.client.get("/users/1")
        self.assertEqual(resp.status_code, 200)

    def test_existing_user_returns_json(self):
        """Response Content-Type should be application/json."""
        resp = self.client.get("/users/1")
        self.assertEqual(resp.content_type, "application/json")

    def test_existing_user_returns_correct_fields(self):
        """Response body should contain 'name' and 'email' keys."""
        resp = self.client.get("/users/1")
        data = resp.get_json()
        self.assertIn("name", data)
        self.assertIn("email", data)

    def test_existing_user_returns_correct_values(self):
        """Response body values should match the in-memory USERS dict."""
        resp = self.client.get("/users/1")
        data = resp.get_json()
        self.assertEqual(data["name"], USERS[1]["name"])
        self.assertEqual(data["email"], USERS[1]["email"])

    def test_each_user_in_store(self):
        """Every user in the USERS dict should be retrievable with 200."""
        for uid, user_data in USERS.items():
            with self.subTest(user_id=uid):
                resp = self.client.get(f"/users/{uid}")
                self.assertEqual(resp.status_code, 200)
                data = resp.get_json()
                self.assertEqual(data["name"], user_data["name"])
                self.assertEqual(data["email"], user_data["email"])

    # ── Bug fix: non-existent user returns 404 JSON ────────────────────

    def test_nonexistent_user_returns_404(self):
        """GET /users/999 should return 404 for a user that doesn't exist."""
        resp = self.client.get("/users/999")
        self.assertEqual(resp.status_code, 404)

    def test_nonexistent_user_returns_json(self):
        """404 response should still be application/json."""
        resp = self.client.get("/users/999")
        self.assertEqual(resp.content_type, "application/json")

    def test_nonexistent_user_returns_error_key(self):
        """404 response body should contain an 'error' key."""
        resp = self.client.get("/users/999")
        data = resp.get_json()
        self.assertIn("error", data)

    def test_nonexistent_user_error_message(self):
        """The 'error' value should be 'User not found'."""
        resp = self.client.get("/users/999")
        data = resp.get_json()
        self.assertEqual(data["error"], "User not found")

    def test_nonexistent_user_no_extra_keys(self):
        """404 response should only contain the 'error' key (no leak)."""
        resp = self.client.get("/users/999")
        data = resp.get_json()
        self.assertEqual(list(data.keys()), ["error"])

    # ── Invalid id type (non-integer path segment) ─────────────────────

    def test_invalid_id_type_returns_404(self):
        """GET /users/abc should return 404 (Flask int converter rejects it)."""
        resp = self.client.get("/users/abc")
        self.assertEqual(resp.status_code, 404)

    def test_invalid_id_type_returns_json(self):
        """GET /users/abc should return JSON 404 (global error handler)."""
        resp = self.client.get("/users/abc")
        self.assertEqual(resp.content_type, "application/json")

    def test_negative_id_returns_404(self):
        """GET /users/-1 should return 404 (not in USERS dict)."""
        resp = self.client.get("/users/-1")
        self.assertEqual(resp.status_code, 404)

    def test_negative_id_returns_json(self):
        """GET /users/-1 should return JSON 404 (global error handler)."""
        resp = self.client.get("/users/-1")
        self.assertEqual(resp.content_type, "application/json")

    def test_zero_id_returns_404(self):
        """GET /users/0 should return 404 (not in USERS dict)."""
        resp = self.client.get("/users/0")
        self.assertEqual(resp.status_code, 404)

    # ── Global 404 handler consistency ─────────────────────────────────

    def test_nonexistent_route_returns_json_404(self):
        """GET /nonexistent should return JSON 404 (global error handler)."""
        resp = self.client.get("/nonexistent")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.content_type, "application/json")

    def test_nonexistent_route_has_error_key(self):
        """Global 404 response should contain an 'error' key."""
        resp = self.client.get("/nonexistent")
        data = resp.get_json()
        self.assertIn("error", data)

    # ── HTTP method guard ──────────────────────────────────────────────

    def test_post_method_not_allowed(self):
        """POST /users/1 should return 405 Method Not Allowed."""
        resp = self.client.post("/users/1")
        self.assertEqual(resp.status_code, 405)

    def test_put_method_not_allowed(self):
        """PUT /users/1 should return 405 Method Not Allowed."""
        resp = self.client.put("/users/1")
        self.assertEqual(resp.status_code, 405)

    def test_delete_method_not_allowed(self):
        """DELETE /users/1 should return 405 Method Not Allowed."""
        resp = self.client.delete("/users/1")
        self.assertEqual(resp.status_code, 405)


if __name__ == "__main__":
    unittest.main()
