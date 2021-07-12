CREATE_HOLO_MEMBER_QUERY = """
    INSERT INTO holo_member (type, name, description, twitter, age)
    VALUES (:type, :name, :description, :twitter, :age)
    RETURNING id, type, name, description, twitter, age;
"""

GET_HOLO_MEMBER_BY_ID_QUERY = """
    SELECT type, id, name, description, twitter, age
    FROM holo_member
    WHERE id = :id;
"""

GET_ALL_HOLO_MEMBER_QUERY = """
    SELECT id, type, name, description, twitter, age
    FROM holo_member;
"""

UPDATE_HOLO_MEMBER_BY_ID_QUERY = """
    UPDATE holo_member
    SET type          = :type,
        name          = :name,
        description   = :description,
        age           = :age,
        twitter       = :twitter
    WHERE id = :id
    RETURNING id, type, name, description, age, twitter;
"""

DELETE_HOLO_MEMBER_BY_ID_QUERY = '''
    DELETE FROM holo_member
    WHERE id = :id
    RETURNING id;
'''