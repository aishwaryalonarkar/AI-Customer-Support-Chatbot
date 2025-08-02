import { NextRequest, NextResponse } from 'next/server';

// The URL of the Python backend
const BACKEND_URL = process.env.BACKEND_URL || 'http://127.0.0.1:8000';

export async function POST(req: NextRequest) {
  try {
    // 1. Get the user's question from the frontend request
    const body = await req.json();
    const { question } = body;

    if (!question) {
      return NextResponse.json({ error: 'Question is required' }, { status: 400 });
    }

    // 2. Forward the question to the Python/FastAPI backend
    const backendResponse = await fetch(`${BACKEND_URL}/api/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ question }),
    });

    // 3. Check if the backend request was successful
    if (!backendResponse.ok) {
      const errorBody = await backendResponse.text();
      console.error('Backend error:', errorBody);
      return NextResponse.json(
        { error: 'Failed to get response from backend', details: errorBody },
        { status: backendResponse.status }
      );
    }

    // 4. Return the backend's response to the frontend
    const data = await backendResponse.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('Error in API route:', error);
    return NextResponse.json({ error: 'An internal server error occurred' }, { status: 500 });
  }
}
