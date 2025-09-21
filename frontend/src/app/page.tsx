'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

//const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'
const API_URL = 'http://localhost:8000'

export default function Home() {
    const [apiStatus, setApiStatus] = useState<string>('checking...')
    const [postgresStatus, setPostgresStatus] = useState<string>('checking...')
    const [sqlserverStatus, setSqlserverStatus] = useState<string>('checking...')
    const [sampleResponse, setSampleResponse] = useState<any>(null)

    useEffect(() => {
        checkHealthStatus()
        testSampleAPI()
    }, [])

    const checkHealthStatus = async () => {
        try {
            // Check API health
            await axios.get(`${API_URL}/health`)
            setApiStatus('✅ Healthy')
        } catch (error) {
            setApiStatus('❌ Unhealthy')
        }

        try {
            // Check PostgreSQL health
            await axios.get(`${API_URL}/health/postgres`)
            setPostgresStatus('✅ Healthy')
        } catch (error) {
            setPostgresStatus('❌ Unhealthy')
        }

        try {
            // Check SQL Server health
            await axios.get(`${API_URL}/health/sqlserver`)
            setSqlserverStatus('✅ Healthy')
        } catch (error) {
            setSqlserverStatus('❌ Unhealthy')
        }
    }

    const testSampleAPI = async () => {
        try {
            const response = await axios.get(`${API_URL}/sample`)
            setSampleResponse(response.data)
        } catch (error) {
            console.error('Error calling sample API:', error)
            setSampleResponse({ error: 'Failed to call sample API' })
        }
    }

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', maxWidth: '1200px', margin: '0 auto' }}>
            <h1>Docker Swarm Stack Demo</h1>

            {/* Health Status */}
            <div style={{ marginBottom: '30px', padding: '20px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
                <h2>Service Health Status</h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px' }}>
                    <div>API Backend: {apiStatus}</div>
                    <div>PostgreSQL: {postgresStatus}</div>
                    <div>SQL Server: {sqlserverStatus}</div>
                </div>
                <button
                    onClick={checkHealthStatus}
                    style={{ marginTop: '10px', padding: '8px 16px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                >
                    Refresh Status
                </button>
            </div>

            {/* Sample API Test */}
            <div style={{ marginBottom: '30px', padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
                <h2>Sample API Test</h2>
                <button
                    onClick={testSampleAPI}
                    style={{ padding: '8px 16px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', marginBottom: '15px' }}
                >
                    Test Sample API
                </button>

                {sampleResponse && (
                    <div style={{ backgroundColor: '#ffffff', padding: '15px', borderRadius: '4px', border: '1px solid #ddd' }}>
                        <h3>API Response:</h3>
                        <pre style={{ backgroundColor: '#f8f9fa', padding: '10px', borderRadius: '4px', overflow: 'auto' }}>
                            {JSON.stringify(sampleResponse, null, 2)}
                        </pre>
                    </div>
                )}
            </div>

            {/* API Information */}
            <div style={{ padding: '20px', backgroundColor: '#e9ecef', borderRadius: '8px' }}>
                <h2>Available Endpoints</h2>
                <ul style={{ listStyle: 'none', padding: 0 }}>
                    <li style={{ padding: '5px 0', borderBottom: '1px solid #ddd' }}>
                        <strong>GET /</strong> - Root endpoint with API information
                    </li>
                    <li style={{ padding: '5px 0', borderBottom: '1px solid #ddd' }}>
                        <strong>GET /health</strong> - General health check
                    </li>
                    <li style={{ padding: '5px 0', borderBottom: '1px solid #ddd' }}>
                        <strong>GET /health/postgres</strong> - PostgreSQL health check
                    </li>
                    <li style={{ padding: '5px 0', borderBottom: '1px solid #ddd' }}>
                        <strong>GET /health/sqlserver</strong> - SQL Server health check
                    </li>
                    <li style={{ padding: '5px 0' }}>
                        <strong>GET /sample</strong> - Sample API that returns success message
                    </li>
                </ul>

                <div style={{ marginTop: '15px', padding: '10px', backgroundColor: '#d4edda', borderRadius: '4px', border: '1px solid #c3e6cb' }}>
                    <strong>API Documentation:</strong>
                    <a href={`${API_URL}/docs`} target="_blank" rel="noopener noreferrer" style={{ marginLeft: '10px', color: '#007bff' }}>
                        {API_URL}/docs
                    </a>
                </div>
            </div>
        </div>
    )
}