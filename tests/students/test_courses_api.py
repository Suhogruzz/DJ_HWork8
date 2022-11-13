import pytest



@pytest.mark.django_db
def test_retrieve_logic(api_client,course_factory):
    courses = course_factory(_quantity=10)

    response = api_client.get('/api/v1/courses/1/')

    data = response.json()
    
    assert response.status_code == 200 
    assert data['name'] == courses[0].name

@pytest.mark.django_db
def test_list_logic(api_client, course_factory):
    courses = course_factory(_quantity=10)

    response = api_client.get('/api/v1/courses/')

    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)

@pytest.mark.django_db
def test_filtering_id(api_client,course_factory):
    courses = course_factory(_quantity=10)

    response = api_client.get(f'/api/v1/courses/', {'id': f'{courses[2].id}'})

    data = response.json()

    assert response.status_code == 200
    assert courses[2].id == data[0]['id']


@pytest.mark.django_db
def test_filtering_name(api_client, course_factory):
    courses = course_factory(_quantity=10)

    response = api_client.get('/api/v1/courses/',{'name': f'{courses[2].name}'})

    data = response.json()

    assert response.status_code == 200
    assert courses[2].name == data[0]['name']

@pytest.mark.django_db
def test_create_course(api_client):
    expected_courses = {
        'name': 'test',
        'students':[],
    }

    response = api_client.post(
        '/api/v1/courses/',
        data=expected_courses,
        format="json"
    )

    assert response.status_code == 201
    assert response.data['name'] == 'test'

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    courses = course_factory(_quantity=23)

    response = api_client.patch(f'/api/v1/courses/{courses[22].id}/',
                                data={'name': 'test', 'students':[]})

    assert response.status_code == 200
    assert response.data['name'] == 'test'

@pytest.mark.django_db
def test_remove_course(api_client, course_factory):
    courses = course_factory(_quantity=10)
    
    response = api_client.delete(f'/api/v1/courses/{courses[2].id}/')
    count_courses = api_client.get('/api/v1/courses/').json()

    assert response.status_code == 204
    assert len(count_courses) == len(courses) - 1

