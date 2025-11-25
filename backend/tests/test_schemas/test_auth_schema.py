"""
Tests for authentication schema definitions and validation.
These tests define the requirements for authentication schemas.
"""

from backend.schemas.auth import Token, TokenData


class TestTokenSchema:
    """Tests for Token schema validation."""

    def test_token_has_required_fields(self):
        """Test that Token has the expected required fields."""
        # Test that required fields exist
        assert "access_token" in Token.model_fields
        assert "token_type" in Token.model_fields

        assert Token.model_fields["access_token"].is_required()
        assert Token.model_fields["token_type"].is_required()


class TestTokenDataSchema:
    """Tests for TokenData schema validation."""

    def test_token_data_has_required_fields(self):
        """Test that TokenData has the expected required fields."""
        # Test that required fields exist
        assert "user_id" in TokenData.model_fields
        assert "email" in TokenData.model_fields

        assert not TokenData.model_fields["user_id"].is_required()
        assert not TokenData.model_fields["email"].is_required()
