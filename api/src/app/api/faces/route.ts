import { NextResponse } from 'next/server';
import dynamoDb from '@/lib/dynamodb';
import { ScanCommand, PutCommand } from '@aws-sdk/lib-dynamodb';

export async function GET() {
  const params = { TableName: process.env.DYNAMODB_TABLE as string };

  try {
    const command = new ScanCommand(params);
    const data = await dynamoDb.send(command);
    return NextResponse.json(data.Items, { status: 200 });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to retrieve items' }, { status: 500 });
  }
}

export async function POST(req: Request) {
  const { id, name } = await req.json();
  const params = {
    TableName: process.env.DYNAMODB_TABLE as string,
    Item: { id, name },
  };

  try {
    const command = new PutCommand(params);
    await dynamoDb.send(command);
    return NextResponse.json({ message: 'Item created successfully' }, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to create item' }, { status: 500 });
  }
}