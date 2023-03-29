
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

        # example list of members
        self._members = [
            {
                "id": self._generateId(),
                "first_name": "John",
                "last_name": last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": self._generateId(),
                "first_name": "Jane",
                "last_name": last_name,
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": self._generateId(),
                "first_name": "Jimmy",
                "last_name": last_name,
                "age": 5,
                "lucky_numbers": [1]
            }
        ]

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        # check if an ID is provided, otherwise generate a new one
        if "id" not in member:
            member["id"] = self._generateId()
        else:
            member_id = member["id"]
            # check if the provided ID already exists
            for m in self._members:
                if m["id"] == member_id:
                    raise APIException("Member with ID {} already exists".format(member_id), status_code=400)

        # add the member to the list of members
        self._members.append(member)

        # return the new member's ID
        return member["id"]


    def delete_member(self, id):
        # loop through the list of members and delete the one with the given ID
        for member in self._members:
            if member["id"] == id:
                self._members.remove(member)
                return True

        # if no member with the given ID is found, return False
        return False

    def update_member(self, id, member):
        # loop through the list of members and replace the one with the given ID
        for i, m in enumerate(self._members):
            if m["id"] == id:
                member["id"] = id
                self._members[i] = member
                return True

        # if no member with the given ID is found, return False
        return False

    def get_member(self, id):
        # loop through the list of members and return the one with the given ID
        for member in self._members:
            if member["id"] == id:
                return member

        # if no member with the given ID is found, return None
        return None

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members

    def test_get_single_member_implemented(client):
        response = client.get('/member/3443')
        print(response.status_code)
        print(response.json())
        assert response.status_code == 200
