from test.conversation_fixture import ConversationFixture


class TestConversationAPI(ConversationFixture):
    def test_success_create_conversation(self, client, user_1):
        # Arrange
        payload = {
            'title': 'test',
            'user_id': user_1.id,
        }
        # Act
        response = client.post('/api/conversation', json=payload)
        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['title'] == 'test'
        assert data['id'] is not None
        assert data['user_id'] == user_1.id

    def test_fail_create_conversation_user_not_found(self, client):
        # Arrange
        payload = {
            'title': 'test',
            'user_id': 99999999,
        }
        # Act
        response = client.post('/api/conversation', json=payload)
        # Assert
        assert response.status_code == 404, response.text
        assert response.json() == {'detail': 'User with id 99999999 not found'}

    def test_success_get_conversation_by_id(self, client, conversation_1):
        # Arrange
        # Act
        response = client.get(f'/api/conversation/{conversation_1.id}')
        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['title'] == conversation_1.title
        assert data['id'] == conversation_1.id

    def test_success_search_conversation_for_user_1(
        self, client, user_1, conversation_1, conversation_2, conversation_3
    ):
        # Arrange
        # Act
        response = client.get(
            '/api/conversation',
            params={'user_id': user_1.id, 'page': 1, 'page_size': 10},
        )
        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data['data']) == 2
        assert data['total'] == 2
        assert {conversation['id'] for conversation in data['data']} == {
            conversation_1.id,
            conversation_3.id,
        }
