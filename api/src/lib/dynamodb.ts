import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient } from '@aws-sdk/lib-dynamodb';

// Configure the DynamoDB client with your region and credentials (if needed)
const client = new DynamoDBClient({
  region: process.env.AWS_REGION, // Replace with your region, e.g., "us-east-1"
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID as string,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY as string,
  },
});

// DynamoDB Document Client, which provides a higher-level API
const dynamoDb = DynamoDBDocumentClient.from(client);

export default dynamoDb;