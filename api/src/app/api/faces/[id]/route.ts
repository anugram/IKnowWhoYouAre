import { NextResponse } from 'next/server';
import dynamoDb from '@/lib/dynamodb';
import { UpdateCommand, UpdateCommandInput, DeleteCommand } from '@aws-sdk/lib-dynamodb';

export async function PUT(req: Request, { params }: { params: { id: string } }) {
    const { id } = params;
    const { name } = await req.json();

    const updateParams: UpdateCommandInput = {
      TableName: process.env.DYNAMODB_TABLE as string,
      Key: { id: id },  // Assuming 'id' is a string, adjust if it's of a different type
      UpdateExpression: 'SET #name = :name',
      ExpressionAttributeNames: { '#name': 'name' },
      ExpressionAttributeValues: { ':name': name },
      ReturnValues: 'UPDATED_NEW',
    };

    try {
      const command = new UpdateCommand(updateParams);
      const data = await dynamoDb.send(command);
      return NextResponse.json({ updatedAttributes: data.Attributes }, { status: 200 });
    } catch (error) {
      return NextResponse.json({ error: 'Failed to update item' }, { status: 500 });
    }
  }

export async function DELETE(req: Request, { params }: { params: { id: string } }) {
  const { id } = params;
  const deleteParams = {
    TableName: process.env.DYNAMODB_TABLE as string,
    Key: { id },
  };

  try {
    const command = new DeleteCommand(deleteParams);
    await dynamoDb.send(command);
    return NextResponse.json({ message: 'Item deleted' }, { status: 200 });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to delete item' }, { status: 500 });
  }
}