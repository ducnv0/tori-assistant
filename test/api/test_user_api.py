from test.user_fixture import UserFixture


class TestUserAPI(UserFixture):
    def test_success_create_user(self, client):
        # Arrange
        payload = {
            'username': 'test',
        }
        # Act
        response = client.post('/api/user', json=payload)
        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['username'] == 'test'
        assert data['id'] is not None

    def test_success_get_user_by_id(self, client, user_1):
        # Arrange
        # Act
        response = client.get(f'/api/user/{user_1.id}')
        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['username'] == user_1.username
        assert data['id'] == user_1.id

    def test_success_search_user(self, client, user_1, user_2):
        # Arrange
        # Act
        response = client.get('/api/user', params={'page': 1, 'page_size': 10})
        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data['data']) == 2
