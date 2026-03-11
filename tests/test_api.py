import pytest
from utils.api_client import APIClient


@pytest.fixture
def client():
    return APIClient()


# ─────────────────────────────────────────────
# POSTS TESTS
# ─────────────────────────────────────────────

class TestPostsAPI:
    """Tests for /posts endpoint."""

    @pytest.mark.smoke
    def test_get_all_posts_status_200(self, client):
        """GET /posts returns 200."""
        response = client.get("/posts")
        assert response.status_code == 200

    @pytest.mark.smoke
    def test_get_all_posts_returns_100_items(self, client):
        """GET /posts returns 100 posts."""
        response = client.get("/posts")
        data = response.json()
        assert len(data) == 100

    @pytest.mark.regression
    def test_get_single_post(self, client):
        """GET /posts/1 returns correct post."""
        response = client.get("/posts/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "title" in data
        assert "body" in data
        assert "userId" in data

    @pytest.mark.regression
    def test_post_has_required_fields(self, client):
        """Each post contains id, userId, title, body."""
        response = client.get("/posts")
        posts = response.json()
        for post in posts[:5]:  # check first 5
            assert "id" in post
            assert "userId" in post
            assert "title" in post
            assert "body" in post

    @pytest.mark.regression
    def test_get_nonexistent_post_returns_404(self, client):
        """GET /posts/9999 returns 404."""
        response = client.get("/posts/9999")
        assert response.status_code == 404

    @pytest.mark.smoke
    def test_create_post_returns_201(self, client):
        """POST /posts returns 201 Created."""
        payload = {
            "title": "Test Post",
            "body": "This is a test post body.",
            "userId": 1
        }
        response = client.post("/posts", payload)
        assert response.status_code == 201

    @pytest.mark.regression
    def test_create_post_returns_correct_data(self, client):
        """POST /posts echoes back the sent data."""
        payload = {
            "title": "My New Post",
            "body": "Post body content here.",
            "userId": 5
        }
        response = client.post("/posts", payload)
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["body"] == payload["body"]
        assert data["userId"] == payload["userId"]
        assert "id" in data

    @pytest.mark.regression
    def test_update_post_returns_200(self, client):
        """PUT /posts/1 returns 200."""
        payload = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated body.",
            "userId": 1
        }
        response = client.put("/posts/1", payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"

    @pytest.mark.regression
    def test_delete_post_returns_200(self, client):
        """DELETE /posts/1 returns 200."""
        response = client.delete("/posts/1")
        assert response.status_code == 200

    @pytest.mark.regression
    def test_filter_posts_by_user(self, client):
        """GET /posts?userId=1 returns only posts for user 1."""
        response = client.get("/posts", params={"userId": 1})
        assert response.status_code == 200
        posts = response.json()
        assert len(posts) > 0
        for post in posts:
            assert post["userId"] == 1


# ─────────────────────────────────────────────
# USERS TESTS
# ─────────────────────────────────────────────

class TestUsersAPI:
    """Tests for /users endpoint."""

    @pytest.mark.smoke
    def test_get_all_users_status_200(self, client):
        """GET /users returns 200."""
        response = client.get("/users")
        assert response.status_code == 200

    @pytest.mark.regression
    def test_get_all_users_returns_10_items(self, client):
        """GET /users returns 10 users."""
        response = client.get("/users")
        data = response.json()
        assert len(data) == 10

    @pytest.mark.regression
    def test_user_has_required_fields(self, client):
        """Each user contains id, name, email, username."""
        response = client.get("/users")
        users = response.json()
        for user in users:
            assert "id" in user
            assert "name" in user
            assert "email" in user
            assert "username" in user

    @pytest.mark.regression
    def test_get_single_user(self, client):
        """GET /users/1 returns correct user."""
        response = client.get("/users/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "name" in data
        assert "email" in data

    @pytest.mark.regression
    def test_user_email_contains_at_symbol(self, client):
        """All user emails are valid format."""
        response = client.get("/users")
        users = response.json()
        for user in users:
            assert "@" in user["email"], f"Invalid email: {user['email']}"


# ─────────────────────────────────────────────
# COMMENTS TESTS
# ─────────────────────────────────────────────

class TestCommentsAPI:
    """Tests for /comments endpoint."""

    @pytest.mark.smoke
    def test_get_all_comments_status_200(self, client):
        """GET /comments returns 200."""
        response = client.get("/comments")
        assert response.status_code == 200

    @pytest.mark.regression
    def test_get_all_comments_returns_500_items(self, client):
        """GET /comments returns 500 comments."""
        response = client.get("/comments")
        data = response.json()
        assert len(data) == 500

    @pytest.mark.regression
    def test_filter_comments_by_post(self, client):
        """GET /comments?postId=1 returns only comments for post 1."""
        response = client.get("/comments", params={"postId": 1})
        assert response.status_code == 200
        comments = response.json()
        assert len(comments) > 0
        for comment in comments:
            assert comment["postId"] == 1

    @pytest.mark.regression
    def test_comment_has_required_fields(self, client):
        """Each comment contains postId, id, name, email, body."""
        response = client.get("/comments/1")
        comment = response.json()
        assert "postId" in comment
        assert "id" in comment
        assert "name" in comment
        assert "email" in comment
        assert "body" in comment


# ─────────────────────────────────────────────
# RESPONSE HEADER / CONTENT TYPE TESTS
# ─────────────────────────────────────────────

class TestAPIHeaders:
    """Tests for response headers and content types."""

    @pytest.mark.regression
    def test_response_content_type_is_json(self, client):
        """Response Content-Type is application/json."""
        response = client.get("/posts/1")
        assert "application/json" in response.headers["Content-Type"]

    @pytest.mark.regression
    def test_response_time_under_2_seconds(self, client):
        """GET /posts responds within 2 seconds."""
        response = client.get("/posts")
        assert response.elapsed.total_seconds() < 2.0, \
            f"Response too slow: {response.elapsed.total_seconds()}s"
