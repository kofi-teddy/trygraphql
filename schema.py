import uuid
import graphene
import json
from datetime import datetime
import uuid



class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()


class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    created_at = graphene.DateTime()
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return f"http://cloudinary.com/{self.username}/{self.id}"


class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return "world!"

    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info, limit=None):
        return [
            User(
                id="1",
                username="Kofi",
                created_at=datetime.now(),
            ),
            User(
                id="2",
                username="Teddy",
                created_at=datetime.now(),
            ),
            User(
                id="3",
                username="Mawuli",
                created_at=datetime.now(),
            ),
            User(
                id="4",
                username="Agudogo",
                created_at=datetime.now(),
            ),
        ][:limit]


class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title, content):
        if info.context.get("is_anonymous"):
            raise Exception("Not Authenticated!")
        post = Post(title=title, content=content)
        return CreatePost(post=post)


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()
        id = graphene.ID(default_value=str(uuid.uuid4()))

    def mutate(self, info, username, id):
        user = User(
            id=id,
            username=username,
            created_at=datetime.now())
        return CreateUser(user=user)


# Add ability add/update
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()


# schema = graphene.Schema(query=Query)
schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)

# result = schema.execute(
#     """
#     {
#         isAdmin
#     }
#     """
# )

# result = schema.execute(
#     """
#     {
#         is_admin
#     }
#     """
# )

# result = schema.execute(
#     """
#         {
#             users(limit: 1){
#                 id
#                 username
#                 created_at
#             }
#         }
#     """
# )

# Mutation
# result = schema.execute(
#     """
#         mutation{
#             create_user(username: "Morephones"){
#                 user{
#                     id
#                     username
#                     created_at
#                 }
#             }
#         }
#     """
# )

# Passing dynamic values to a mutation
# result = schema.execute(
#     """
#         mutation($username: String){
#             create_user(username: $username){
#                 user{
#                     id
#                     username
#                     created_at
#                 }
#             }
#         }
#     """,
#     variable_values = {
#         "username": "Teddy"
#     }
# )

# Passing limit as a dynamic value
# result = schema.execute(
#     """
#         query getUsersQuery($limit: Int){
#             users(limit: $limit){
#                 id
#                 username
#                 created_at
#             }
#         }
#     """,
#     variable_values = {
#         "limit": 1
#     }
# )

# Create post
# result = schema.execute(
#     """
#         mutation {
#             create_post(title: "Hello", content: "World!"){
#                 post {
#                     title
#                     content
#                 }
#             }
#         }
#     """,
#     context = {
#         "is_anonymous": True 
#     }
#     # variable_values = {
#     #     "limit": 1
#     # }
# )

# Using self and info context
result = schema.execute(
    """
        {
            users {
                id 
                username
                avatar_url
                created_at  
            }
        }  
    """
    # context = {
    #     "is_anonymous": True 
    # }
    # variable_values = {
    #     "limit": 1
    # }
)

# print(result.data.items())
dicResult = dict(result.data.items())
print(json.dumps(dicResult, indent=2))