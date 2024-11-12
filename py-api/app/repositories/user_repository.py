import boto3
from botocore.exceptions import ClientError
from app.schemas.user_schema import UserCreate, UserResponse
from app.config import settings  # Configuration for DynamoDB setup (e.g., table name)

class UserRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.DYNAMODB_REGION)
        self.table = self.dynamodb.Table(settings.USERS_TABLE)

    def create_user(self, username: str, email: str, password_hash: str) -> UserResponse:
        user_data = {
            "id": str(uuid.uuid4()),  # Generate unique ID
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "is_active": True
        }

        try:
            self.table.put_item(Item=user_data)
            return UserResponse(**user_data)
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None

    def get_user_by_id(self, user_id: str) -> UserResponse:
        try:
            response = self.table.get_item(Key={"id": user_id})
            if "Item" in response:
                return UserResponse(**response["Item"])
            return None
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None

    def get_user_by_email(self, email: str) -> UserResponse:
        try:
            response = self.table.query(
                IndexName="email-index",  # Ensure an index on "email" exists
                KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(email)
            )
            items = response.get("Items")
            if items:
                return UserResponse(**items[0])
            return None
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None

    def update_user(self, user_id: str, username: str, email: str, password_hash: str) -> UserResponse:
        try:
            response = self.table.update_item(
                Key={"id": user_id},
                UpdateExpression="SET username = :username, email = :email, password_hash = :password_hash",
                ExpressionAttributeValues={
                    ":username": username,
                    ":email": email,
                    ":password_hash": password_hash
                },
                ReturnValues="ALL_NEW"
            )
            return UserResponse(**response["Attributes"])
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None
