import React, { useState, useEffect } from 'react';
import Layout from './components/Layout';
import FileUploader from './components/FileUploader';
import StatsCards from './components/StatsCards';
import { api } from './services/api';

function App() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    try {
      const response = await api.getDashboardData();
      // Handle the case where backend returns 204 (No Content)
      if (response.status === 204) {
        setDashboardData(null);
      } else {
        setDashboardData(response.data);
      }
    } catch (error) {
      console.error("Error fetching dashboard:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        {/* Header Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Equipment Dashboard</h2>
          <p className="text-gray-500">Upload CSV logs to analyze performance metrics.</p>
        </div>

        {/* Upload Section */}
        <FileUploader onUploadSuccess={fetchDashboardData} />

        {/* Stats Section */}
        {loading ? (
           <div className="text-center py-10 text-gray-500">Loading data...</div>
        ) : dashboardData ? (
          <>
            <StatsCards data={dashboardData.summary} />
            
            {/* Placeholder for Charts & Tables  */}
            <div className="bg-white p-6 rounded-xl border border-gray-100 text-center text-gray-400">
              Charts and Data Tables will appear here in the next step.
            </div>
          </>
        ) : (
          <div className="text-center py-10 bg-white rounded-xl border border-gray-100">
             <p className="text-gray-500">No data found. Upload a file to get started.</p>
          </div>
        )}
      </div>
    </Layout>
  );
}

export default App;