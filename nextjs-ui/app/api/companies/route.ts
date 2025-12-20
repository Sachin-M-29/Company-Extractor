import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';

const PYTHON_API = process.env.PYTHON_API || process.env.NEXT_PUBLIC_PYTHON_API || 'http://127.0.0.1:5000';

export async function GET(request: NextRequest) {
  try {
    console.log('[Next.js API] Fetching all companies from database');
    
    // Call Python backend API to get all companies
    const response = await axios.get(`${PYTHON_API}/api/companies`, {
      timeout: 10000,
    });

    console.log('[Next.js API] Success:', response.status);
    return NextResponse.json(response.data);
  } catch (error: any) {
    console.error('[Next.js API] Fetch error:', error.message);
    
    const errorMessage = error.response?.data?.error || 
                        error.message || 
                        'Failed to fetch companies';
    
    return NextResponse.json(
      { 
        error: errorMessage,
        companies: []
      },
      { status: error.response?.status || 500 }
    );
  }
}
