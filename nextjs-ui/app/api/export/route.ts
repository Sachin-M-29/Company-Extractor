import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { format, data } = body;

    if (!data) {
      return NextResponse.json({ error: 'No data to export' }, { status: 400 });
    }

    const items = Array.isArray(data) ? data : [data];

    if (format === 'json') {
      const json = JSON.stringify(data, null, 2);
      return new NextResponse(json, {
        headers: {
          'Content-Type': 'application/json',
          'Content-Disposition': `attachment; filename="companies_${new Date().toISOString().slice(0, 10)}.json"`,
        },
      });
    } else if (format === 'csv') {
      const headers = ['Company Name', 'Website', 'Industry', 'Confidence'];
      const rows = items.map((item: any) => [
        item.company_name || '',
        item.website || '',
        item.industry || '',
        item.confidence || '',
      ]);

      const csv = [
        headers.join(','),
        ...rows.map((row: string[]) => row.map(cell => `"${cell}"`).join(',')),
      ].join('\n');

      return new NextResponse(csv, {
        headers: {
          'Content-Type': 'text/csv',
          'Content-Disposition': `attachment; filename="companies_${new Date().toISOString().slice(0, 10)}.csv"`,
        },
      });
    }

    return NextResponse.json({ error: 'Invalid format' }, { status: 400 });
  } catch (error) {
    return NextResponse.json({ error: 'Export failed' }, { status: 500 });
  }
}
