import React, { useState } from 'react';
import { UploadCloud, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

const FileUploader = ({ onUploadSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      await api.uploadFile(file);
      setSuccess(true);
      onUploadSuccess(); // Refresh the parent dashboard
      
      // Reset success message after 3 seconds
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      console.error(err);
      setError("Failed to upload file. Please check format.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-8">
      <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-500 hover:bg-blue-50 transition-colors relative group">
        <input 
          type="file" 
          accept=".csv"
          onChange={handleFileChange}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          disabled={loading}
        />
        
        <div className="flex flex-col items-center justify-center gap-3">
          {loading ? (
            <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
          ) : success ? (
            <CheckCircle className="w-10 h-10 text-green-500" />
          ) : error ? (
            <AlertCircle className="w-10 h-10 text-red-500" />
          ) : (
            <UploadCloud className="w-10 h-10 text-gray-400 group-hover:text-blue-500 transition-colors" />
          )}

          <div className="space-y-1">
            <p className="font-medium text-gray-700">
              {loading ? "Processing Data..." : success ? "Upload Successful!" : "Click to upload or drag and drop"}
            </p>
            <p className="text-sm text-gray-500">
              {error ? <span className="text-red-500">{error}</span> : "CSV files only (max 10MB)"}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileUploader;