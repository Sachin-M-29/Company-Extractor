import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';

const PYTHON_API = process.env.PYTHON_API || process.env.NEXT_PUBLIC_PYTHON_API || 'http://127.0.0.1:5000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Call Python backend API for batch extraction
    const response = await axios.post(`${PYTHON_API}/api/batch-extract`, body, {
      timeout: Math.max((body.timeout || 10) * 3000, 60000), // Longer timeout for batch
    });

    return NextResponse.json(response.data);
  } catch (error: any) {
    console.error('Batch extraction error:', error);
    return NextResponse.json(
      { 
        error: error.response?.data?.error || error.message || 'Batch extraction failed',
        details: error.response?.data?.details || ''
      },
      { status: error.response?.status || 500 }
    );
  }
}
