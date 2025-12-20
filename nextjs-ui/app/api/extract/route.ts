import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';

const PYTHON_API = process.env.PYTHON_API || process.env.NEXT_PUBLIC_PYTHON_API || 'http://127.0.0.1:5000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Increase timeout significantly - enrichment can take 2-4 minutes
    const baseTimeoutMs = Math.max((body.timeout || 10) * 10000, 120000);
    const timeout = body.enable_enrich
      ? Math.max(baseTimeoutMs * 2, 240000) // 4 minutes floor when enrichment is enabled
      : baseTimeoutMs;
    
    console.log('[Next.js API] Sending extraction request to', PYTHON_API);
    console.log('[Next.js API] Body:', JSON.stringify(body).substring(0, 200));
    console.log('[Next.js API] Timeout:', timeout, 'ms');
    
    // Call Python backend API
    const response = await axios.post(`${PYTHON_API}/api/extract`, body, {
      timeout,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    console.log('[Next.js API] Success:', response.status);
    return NextResponse.json(response.data);
  } catch (error: any) {
    console.error('[Next.js API] Full error:', error);
    console.error('[Next.js API] Error code:', error.code);
    console.error('[Next.js API] Error message:', error.message);
    console.error('[Next.js API] Response status:', error.response?.status);
    console.error('[Next.js API] Response data:', error.response?.data);
    
    const errorMessage = error.response?.data?.error || 
                        error.message || 
                        'Extraction failed. Check that Flask API on localhost:5000 is running.';
    
    return NextResponse.json(
      { 
        error: errorMessage,
        details: error.response?.data?.details || error.message || ''
      },
      { status: error.response?.status || 500 }
    );
  }
}
