import { NextRequest, NextResponse } from "next/server";

interface RequestBody {
  file_base64: string;
  filename: string;
  fileUrl?: string;
  thread_id: string;
  user_id: string;
}

interface ExternalApiResponse {
  dataset_id?: string;
  id?: string;
  rows?: number;
  row_count?: number;
  columns?: number;
  column_count?: number;
  sheets?: number;
  description?: string;
  data?: unknown[];
  processed_data?: unknown[];
  [key: string]: unknown;
}

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:5002";
const EXTERNAL_API_ENDPOINT = "/api/v1/chats/import-data";
const QUERY_PARAMS = new URLSearchParams({
  distributions_format: "list",
  save_profile_json: "false",
  profile_field_name: "ProfileJson",
});

export async function POST(request: NextRequest) {
  try {
    const requestBody: RequestBody = await request.json();
    const { file_base64, filename, fileUrl, thread_id, user_id } = requestBody;

    if (!file_base64 || !filename || !user_id) {
      return NextResponse.json(
        {
          success: false,
          message: "Missing required fields: file_base64, filename, user_id",
        },
        { status: 400 }
      );
    }

    const payload = {
      file_base64,
      filename,
      fileUrl: fileUrl || "",
      thread_id,
      user_id,
    };

    const response = await fetch(
      `${BASE_URL}${EXTERNAL_API_ENDPOINT}?${QUERY_PARAMS}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`External API error [${response.status}]:`, errorText);

      return NextResponse.json(
        {
          success: false,
          message: `External API failed with status ${response.status}`,
        },
        { status: response.status }
      );
    }

    const result: ExternalApiResponse = await response.json();

    return NextResponse.json({
      success: true,
      data: {
        dataset_id: result.dataset_id || result.id || `imported-${Date.now()}`,
        rows: result.rows || result.row_count || 0,
        columns: result.columns || result.column_count || 0,
        sheets: result.sheets || 1,
        description: result.description || `Imported dataset from ${filename}`,
        processedData: result.data || result.processed_data || [],
        ...result,
      },
    });
  } catch (error) {
    console.error("API Route error:", error);

    return NextResponse.json(
      {
        success: false,
        message:
          error instanceof Error
            ? error.message
            : "An unexpected error occurred",
      },
      { status: 500 }
    );
  }
}
