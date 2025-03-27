from test.message_fixture import MessageFixture


class TestMessageAPI(MessageFixture):
    def test_success_create_message(self, client, message_1_user_text):
        assert message_1_user_text.id is not None

    def test_success_get_message_by_id(self, client, message_1_user_text):
        # Arrange
        # Act
        response = client.get(f'/api/message/{message_1_user_text.id}')
        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['id'] == message_1_user_text.id
        assert data['content'] == message_1_user_text.content
        assert data['role'] == message_1_user_text.role
        assert data['message_type'] == message_1_user_text.message_type
        assert 'file_path' in data

    def test_success_search_message_for_conversation_1(self, client, conversation_1, message_1_user_text, message_2_bot_text, message_3_user_audio, message_4_user_image,):
        # Arrange
        # Act
        response = client.get('/api/message', params={'conversation_id': conversation_1.id, 'page': 1, 'page_size': 10,})
        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data['data']) == 3
        assert data['total'] == 3
        assert {message['id'] for message in data['data']} == {message_1_user_text.id, message_2_bot_text.id, message_3_user_audio.id}
