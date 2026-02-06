import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import FileUploader from './components/FileUploader';
import StatsCards from './components/StatsCards';
import ChartsSection from './components/ChartsSection';
import DataTable from './components/DataTable';
import AnalyticsCharts from './components/AnalyticsCharts';
import { api } from './services/api';
import { FileDown } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  // --- Data Fetching ---
  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const response = await api.getDashboardData();
      if (response.status !== 204) {
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

  // --- PDF Download Logic ---
  const handleDownloadPDF = async () => {
    try {
      const response = await api.downloadPDF();
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'equipment_report.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (e) {
      console.error("Download failed", e);
      alert("Failed to download PDF.");
    }
  };

  // --- Render Content ---
  const renderContent = () => {
    if (loading) {
      return (
        <div className="flex h-96 items-center justify-center text-slate-400">
          <div className="flex flex-col items-center gap-2">
            <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            <p>Loading Data...</p>
          </div>
        </div>
      );
    }

    if (!dashboardData) {
      return (
        <div className="text-center py-20 bg-white rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-lg font-medium text-slate-900">No Data Available</h3>
          <p className="text-slate-500 mb-6">Upload a CSV file to begin analysis.</p>
          <div className="max-w-md mx-auto">
            <FileUploader onUploadSuccess={fetchDashboardData} />
          </div>
        </div>
      );
    }

    switch (activeTab) {
      case 'overview':
        return (
          <div className="space-y-8 animate-in fade-in duration-500">
            
            {/* 1. Stats Row (Top) */}
            <div>
              <h3 className="text-lg font-semibold text-slate-800 mb-4">Key Performance Indicators</h3>
              <StatsCards data={dashboardData.summary} />
            </div>

            {/* 2. Charts Row (Middle) - Full Width Fix */}
            <div>
              <h3 className="text-lg font-semibold text-slate-800 mb-4">Visual Trends</h3>
              {/* Removed the extra grid wrapper here. ChartsSection now takes full width. */}
              <ChartsSection distribution={dashboardData.distribution} equipmentList={dashboardData.equipment_list} />
            </div>

            {/* 3. Upload Row (Bottom) */}
            <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
                  <h3 className="font-semibold text-slate-800 mb-4">Upload New Data</h3>
                  <FileUploader onUploadSuccess={fetchDashboardData} compact={false} />
            </div>
          </div>
        );

      case 'analytics':
        return (
            <div className="space-y-6 animate-in slide-in-from-right duration-300">
                <div className="flex justify-between items-center border-b border-slate-200 pb-4">
                     <h2 className="text-xl font-bold text-slate-800">Analytics & Reports</h2>
                     <button 
                        onClick={handleDownloadPDF}
                        className="flex items-center gap-2 bg-slate-900 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-slate-800 transition-colors"
                     >
                        <FileDown size={16} />
                        Download PDF Report
                     </button>
                </div>

                {/* Advanced Charts */}
                <AnalyticsCharts equipmentList={dashboardData.equipment_list} />
                
                <h3 className="text-lg font-semibold text-slate-800 mt-8">Type Distribution</h3>
                <ChartsSection distribution={dashboardData.distribution} equipmentList={dashboardData.equipment_list} />
            </div>
        );

      case 'data':
        return (
            <div className="space-y-6 animate-in slide-in-from-bottom duration-300">
                <div className="flex justify-between items-center bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                    <h2 className="text-xl font-bold text-slate-800">Raw Data Logs</h2>
                </div>
                <DataTable data={dashboardData.equipment_list} />
            </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="bg-slate-50 min-h-screen font-sans text-slate-900 flex">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      <div className="flex-1 ml-64 transition-all duration-300">
        <header className="bg-white h-16 border-b border-slate-200 sticky top-0 z-40 px-8 flex items-center shadow-sm">
            <h1 className="text-xl font-bold text-slate-800 capitalize tracking-tight">{activeTab}</h1>
        </header>

        <main className="p-8 max-w-7xl mx-auto">
            {renderContent()}
        </main>
      </div>
    </div>
  );
}

export default App;